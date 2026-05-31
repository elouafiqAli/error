# TMLR paper build
PAPER = main

all: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex $(PAPER).bib tmlr.sty tmlr.bst
	pdflatex -interaction=nonstopmode $(PAPER).tex
	bibtex $(PAPER)
	pdflatex -interaction=nonstopmode $(PAPER).tex
	pdflatex -interaction=nonstopmode $(PAPER).tex

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.fls *.fdb_latexmk

distclean: clean
	rm -f $(PAPER).pdf

.PHONY: all clean distclean
