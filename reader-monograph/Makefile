# Makefile for the gnn.md monograph reader companion.
#
# Targets:
#   make plots   — regenerate all numerical illustrations
#   make pdf     — render gnn.md to gnn.pdf via Pandoc + xelatex
#   make clean   — remove generated artefacts

GNN_MD := ../gnn.md
GNN_PDF := ../gnn.pdf
NB_SCRIPT := notebooks/nb_master.py
PLOTS_DIR := plots

PANDOC := pandoc
PANDOC_OPTS := \
	--from=markdown+tex_math_dollars+yaml_metadata_block \
	--to=pdf \
	--pdf-engine=xelatex \
	--variable=geometry:margin=1in \
	--variable=fontsize:11pt \
	--variable=mainfont:"Times New Roman" \
	--variable=mathfont:"Latin Modern Math" \
	--toc --toc-depth=2 \
	--number-sections \
	--bibliography=references.bib \
	--citeproc

.PHONY: plots pdf clean

plots:
	python $(NB_SCRIPT)

pdf: $(GNN_PDF)

$(GNN_PDF): $(GNN_MD) references.bib
	$(PANDOC) $(PANDOC_OPTS) -o $(GNN_PDF) $(GNN_MD)

clean:
	rm -f $(GNN_PDF)
	rm -f $(PLOTS_DIR)/*.png
