# Errata and Audit Log for `gnn.md`

This file is the active worklog, audit checklist, and postmortem ledger for the full theorem-by-theorem review of the book.

## Audit protocol
- Work chapter by chapter.
- Within each chapter, audit definitions, theorem statements, proofs, narrative claims, and exercises.
- Log issues here **before** patching `gnn.md`.
- Commit only after a full chapter has been audited and repaired.

---

## Global migration note
- Previous high-level pedagogical checklist reviewed from `gnn_review.md`.
- Going forward, this file (`errata.md`) is the only audit ledger.

---

# Chapter 1 Audit — Partitions and 1-WL

## Chapter 1 checklist
- [x] Read chapter introduction and roadmap
- [x] Audit all definitions
- [x] Audit all theorem statements
- [x] Audit all theorem proofs
- [x] Audit all narrative claims
- [x] Audit all exercises one by one
- [x] Apply chapter fixes to `gnn.md`
- [x] Write chapter postmortem
- [ ] Commit chapter

## Pre-fix findings

### Structural / notation
1. **Global notation bug inherited into front matter:** the refinement-order bullet in the conventions section is broken across lines (`$` followed by a newline before `\Pi_1 \preceq \Pi_2`).
2. **Chapter 1 theorem labeling / scope mismatch:** Theorem 1.2 claims that `Part(V)` is a **complete lattice**, but the statement only discusses binary meets and joins, and the proof only proves the meet.

### Theorem-level issues
3. **Theorem 1.2 incompleteness:** join is not proved in the main theorem, despite later exercises depending on it.
4. **Theorem 1.2 overstatement risk:** if the chapter only needs binary meet and join at this stage, it is cleaner either to prove both or to weaken the theorem to a lattice statement and mention finiteness separately.

### Narrative claims
5. **Section 1.5 overstatement:** “no parameter training can ever solve the task” is too strong without explicitly fixing the observable inputs and the architecture class. It should be qualified as “within the given message-passing observables / initialization regime.”
6. **Section 1.5 architecture comparison claim:** the GCN-vs-GIN statement is pedagogically useful but currently phrased a bit too categorically; it should be framed as an initialization-dependent explanation inside the current partition formalism.

### Exercise-level issues
7. **Exercise 1.9 does not satisfy its own task statement:** the task says “List all partitions strictly finer than `\Pi^{(0)}`,” but the solution only counts them.
8. **Exercise 1.10 final sentence is too strong / too specific:** the claim about requiring “at least the `k=3` Folklore-WL test” is not needed for the exercise and is better replaced with a safer statement about global connectivity being invisible to 1-WL under constant initialization on these graphs.
9. **Exercise 1.3 wording:** the solution verifies the Bell number and recursion but does not literally enumerate all 15 partitions explicitly; this is acceptable for brevity, but the wording should be softened from “Enumerate all partitions” to “Count the partitions by block-size signature,” or else the partitions should be listed.

## Planned fixes
- Repair the broken refinement-order notation in the front matter.
- Rewrite Theorem 1.2 so it proves both meet and join cleanly, while clarifying why finiteness gives completeness.
- Qualify the strongest architectural-ceiling narrative sentence in Section 1.5.
- Expand Exercise 1.9 to explicitly list the 9 strictly finer partitions.
- Soften the last sentence of Exercise 1.10.
- Optionally soften Exercise 1.3 task wording to match the solution style.

## Postmortem
### Chapter 1 postmortem
Chapter 1 was conceptually strong from the start, but the audit found one major mathematical incompleteness and several smaller textbook-quality mismatches.

#### What was repaired
- The broken refinement-order notation in the front matter was fixed.
- Theorem 1.2 was rewritten so that it now actually proves both meet and join, and its completeness claim is framed through finiteness.
- The strongest “expressivity ceiling” sentence was qualified so that it is accurate relative to a fixed observable/message-passing setup.
- The architecture-comparison remark was softened into a setup-dependent interpretation.
- Exercise 1.3 now matches what its solution actually does.
- Exercise 1.9 now genuinely lists the partitions it asked for.
- Exercise 1.10 no longer makes an unnecessary higher-order-WL claim.

#### Net result
Chapter 1 now reads more like a reliable textbook chapter than a research-note chapter: the central lattice theorem is complete, the narrative claims are scoped correctly, and the exercise section now matches its own prompts.
