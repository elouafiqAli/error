#!/usr/bin/env python3
"""End-to-end RunPod orchestrator for the D-Full GNN-bracket experiment.

Plan:
  1. Create a single-GPU RunPod pod (RTX 4090 by default) running a
     PyTorch image with our SSH public key injected via PUBLIC_KEY.
  2. Poll until the pod is RUNNING and SSH is reachable.
  3. rsync the partition-sandwich-preprint/experiments/ tree to the
     pod and a small remote runner script.
  4. SSH-exec: pip install missing deps -> run e3d_arch_full.run_all on
     CUDA -> write JSON to /workspace/results/e3d_arch_full.json.
  5. SCP the JSON back to partition-sandwich-preprint/experiments/results/.
  6. Terminate the pod.

Logs are streamed to stdout. The pod is always terminated in `finally`,
even if anything in between fails, so we never leak GPU hours.

Run:
    RUNPOD_API_KEY=... python3 runpod_dfull.py \
        [--gpu "NVIDIA GeForce RTX 4090"] [--epochs 200] [--seeds 5] \
        [--datasets cora citeseer pubmed twitch_en ogbn_arxiv] \
        [--keep] [--name dfull-1]
"""
import argparse
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

import runpod


REPO_ROOT = Path(__file__).resolve().parent
LOCAL_EXP = REPO_ROOT / "partition-sandwich-preprint" / "experiments"
LOCAL_RES = LOCAL_EXP / "results"
SSH_KEY = Path.home() / ".ssh" / "id_ed25519_main"
PUB_KEY = SSH_KEY.with_suffix(".pub")
DEFAULT_IMAGE = (
    "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
)


def log(msg: str) -> None:
    print(f"[runpod] {msg}", flush=True)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", default="NVIDIA GeForce RTX 4090")
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument("--cloud", default="COMMUNITY",
                    choices=["COMMUNITY", "SECURE", "ALL"])
    ap.add_argument("--disk", type=int, default=30, help="container disk GB")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--epochs", type=int, default=200)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--datasets", nargs="+", default=[
        "cora", "citeseer", "pubmed", "twitch_en", "ogbn_arxiv"])
    ap.add_argument("--name", default="dfull")
    ap.add_argument("--keep", action="store_true",
                    help="don't terminate pod on exit (for debugging)")
    ap.add_argument("--remote-out",
                    default="/workspace/results/e3d_arch_full.json")
    return ap.parse_args()


def get_ssh(pod: dict) -> tuple[str, int] | None:
    rt = pod.get("runtime") or {}
    ports = rt.get("ports") or []
    for p in ports:
        if p.get("privatePort") == 22 and p.get("isIpPublic"):
            return p["ip"], int(p["publicPort"])
    return None


def wait_ssh(pod_id: str, timeout_s: int = 600) -> tuple[str, int]:
    log(f"waiting for SSH on pod {pod_id} ...")
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        pod = runpod.get_pod(pod_id)
        ssh = get_ssh(pod)
        status = (pod.get("desiredStatus")
                  or pod.get("lastStatusChange") or "?")
        if ssh:
            ip, port = ssh
            log(f"  SSH ready: {ip}:{port}  (status={status})")
            return ip, port
        log(f"  status={status}  elapsed={int(time.time()-t0)}s")
        time.sleep(10)
    raise TimeoutError("pod never became SSH-reachable")


def ssh_run(ip: str, port: int, cmd: str, *, check: bool = True,
            stream: bool = True) -> subprocess.CompletedProcess:
    full = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "ServerAliveInterval=30",
        "-i", str(SSH_KEY),
        "-p", str(port), f"root@{ip}", cmd,
    ]
    log(f"ssh: {cmd[:120]}{'...' if len(cmd) > 120 else ''}")
    if stream:
        return subprocess.run(full, check=check)
    return subprocess.run(full, check=check, capture_output=True, text=True)


def scp_to(ip: str, port: int, local: Path, remote: str) -> None:
    """Tar local dir/file -> stream over ssh -> untar remotely.

    Avoids depending on rsync being installed in the container image.
    """
    log(f"upload -> {local} :: {remote}")
    if local.is_dir():
        ssh_run(ip, port, f"mkdir -p {shlex.quote(remote)}", stream=False)
        tar = subprocess.Popen(
            ["tar", "--exclude=__pycache__",
             "--exclude=.DS_Store", "-czf", "-", "-C",
             str(local.parent), local.name],
            stdout=subprocess.PIPE)
        ssh = subprocess.Popen([
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-i", str(SSH_KEY), "-p", str(port), f"root@{ip}",
            f"tar -xzf - -C {shlex.quote(remote)} --strip-components=1",
        ], stdin=tar.stdout)
        tar.stdout.close()
        rc = ssh.wait(timeout=600)
        tar.wait(timeout=10)
        if rc != 0:
            raise RuntimeError(f"tar-over-ssh upload failed rc={rc}")
    else:
        subprocess.run([
            "scp", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-i", str(SSH_KEY), "-P", str(port),
            str(local), f"root@{ip}:{remote}",
        ], check=True, timeout=300)


def scp_from(ip: str, port: int, remote: str, local: Path) -> None:
    log(f"scp <- {remote} :: {local}")
    local.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "scp", "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-i", str(SSH_KEY), "-P", str(port),
        f"root@{ip}:{remote}", str(local),
    ], check=True)


REMOTE_RUNNER = r"""#!/usr/bin/env bash
set -euo pipefail
cd /workspace/experiments
echo "=== nvidia-smi ==="
nvidia-smi || true
echo "=== python ==="
python3 --version
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"
echo "=== install deps (hard-pinned, no network loops) ==="
pip install --quiet --no-input --disable-pip-version-check \
    "torch_geometric>=2.5,<2.8" \
    "ogb==1.3.6" \
    "scikit-learn>=1.3" \
    "scipy>=1.10" \
    "pandas>=2.0" \
    "matplotlib>=3.7"
echo "=== run experiment ==="
mkdir -p /workspace/results
timeout 7200 python3 -u e3d_arch_full.py \
    --datasets %DATASETS% \
    --seeds %SEEDS% \
    --epochs %EPOCHS% \
    --hidden %HIDDEN% \
    --out /workspace/results/e3d_arch_full.json
echo "=== done ==="
ls -la /workspace/results/
"""


def write_remote_runner(local_path: Path, args) -> Path:
    seeds = " ".join(str(i) for i in range(args.seeds))
    script = (REMOTE_RUNNER
              .replace("%DATASETS%", " ".join(args.datasets))
              .replace("%SEEDS%", seeds)
              .replace("%EPOCHS%", str(args.epochs))
              .replace("%HIDDEN%", str(args.hidden)))
    local_path.write_text(script)
    local_path.chmod(0o755)
    return local_path


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("RUNPOD_API_KEY")
    if not api_key:
        log("ERROR: RUNPOD_API_KEY env var is empty"); return 2
    runpod.api_key = api_key

    if not PUB_KEY.exists() or not SSH_KEY.exists():
        log(f"ERROR: missing SSH key at {SSH_KEY}"); return 2
    pubkey = PUB_KEY.read_text().strip()

    log(f"creating pod  gpu={args.gpu!r}  image={args.image}")
    pod = runpod.create_pod(
        name=args.name,
        image_name=args.image,
        gpu_type_id=args.gpu,
        cloud_type=args.cloud,
        support_public_ip=True,
        start_ssh=True,
        container_disk_in_gb=args.disk,
        volume_in_gb=0,
        ports="22/tcp,8888/http",
        env={"PUBLIC_KEY": pubkey},
    )
    pod_id = pod["id"]
    log(f"pod created: id={pod_id}")
    try:
        ip, port = wait_ssh(pod_id)
        # finite retry budget; ssh-then-handshake should be quick
        ok = False
        for attempt in range(6):
            try:
                r = subprocess.run([
                    "ssh", "-o", "StrictHostKeyChecking=no",
                    "-o", "UserKnownHostsFile=/dev/null",
                    "-o", "ConnectTimeout=15",
                    "-i", str(SSH_KEY), "-p", str(port),
                    f"root@{ip}", "echo OK"],
                    capture_output=True, text=True, timeout=30)
                if r.returncode == 0:
                    ok = True
                    log(f"  ssh OK on attempt {attempt+1}")
                    break
                log(f"  ssh handshake retry {attempt+1}: rc={r.returncode}")
            except subprocess.TimeoutExpired:
                log(f"  ssh handshake timeout {attempt+1}")
            time.sleep(5)
        if not ok:
            raise RuntimeError("ssh never accepted connection")

        # explicit, hand-rolled deps (no relying on image extras)
        log("installing rsync/git/curl on remote ...")
        ssh_run(ip, port,
                "apt-get update -qq && "
                "apt-get install -y -qq --no-install-recommends "
                "rsync git curl ca-certificates >/dev/null")

        # stage code
        ssh_run(ip, port, "mkdir -p /workspace/experiments /workspace/results")
        scp_to(ip, port, LOCAL_EXP, "/workspace/experiments")

        runner = REPO_ROOT / "_runpod_runner.sh"
        write_remote_runner(runner, args)
        try:
            scp_to(ip, port, runner, "/workspace/run.sh")
        finally:
            runner.unlink(missing_ok=True)
        ssh_run(ip, port, "chmod +x /workspace/run.sh")

        # execute (streamed)
        t0 = time.time()
        ssh_run(ip, port, "/workspace/run.sh 2>&1 | tee /workspace/run.log")
        log(f"experiment wall-time: {int(time.time()-t0)}s")

        # fetch result (may be partial if some datasets failed)
        out = LOCAL_RES / "e3d_arch_full.json"
        try:
            scp_from(ip, port, args.remote_out, out)
            log(f"saved -> {out}  size={out.stat().st_size}B")
        except subprocess.CalledProcessError as e:
            log(f"  WARN: result fetch failed: {e}")

        # fetch log too
        try:
            scp_from(ip, port, "/workspace/run.log",
                     LOCAL_RES / "e3d_arch_full.log")
        except Exception as e:
            log(f"  (log fetch skipped: {e})")
        return 0
    finally:
        if args.keep:
            log(f"--keep set; pod {pod_id} left running. "
                f"Terminate via runpod.terminate_pod('{pod_id}').")
        else:
            log(f"terminating pod {pod_id} ...")
            try:
                runpod.terminate_pod(pod_id)
                log("  terminated.")
            except Exception as e:
                log(f"  WARN: terminate failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
