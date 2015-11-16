.PHONY: plots figs clean
.SUFFIXES: .tex .dvi .ps .fig .eps .gnu .c

include Makefile.inc
FIGURE_DEPS=$(FIGURES:%.pdf=figs/%.pdf)
PNG_FIGURE_DEPS=$(FIGURES:%.pdf=figs/%.png)

PDF = ps2pdf -dUseCIEColor -dPDFSETTINGS=/printer -dMaxSubsetPct=100 -dCompatibilityLevel=1.4 -dSubsetFonts=true -dEmbedAllFonts=true
TARGET=report
DOBIB=yes
tikz_figs=$(wildcard tikz/*.tex)

all: figs $(FIGURE_DEPS) $(PNG_FIGURE_DEPS) clean_figs
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex
	bibtex $(TARGET)
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex

display: 
	evince $(TARGET).pdf &
	
$(TARGET): $(TARGET).tex
	latex $(TARGET)
	latex $(TARGET)
	latex $(TARGET)
ifeq ($(DOBIB),yes)
	bibtex $(TARGET)
	latex $(TARGET)
	latex $(TARGET)
	latex $(TARGET)
endif

figs:
	cd tikz; make
	mv tikz/*.pdf figs
	mv tikz/*.png figs/png

plots:
	cd plots; make
	mv plots/*.png plots/png

clean: clean_figs
	$(RM) $(TARGET).ps 
	$(RM) $(TARGET).log
	$(RM) $(TARGET).dvi 
	$(RM) $(TARGET).tex.flc 
	$(RM) $(TARGET).blg
	$(RM) *.synctex.gz
	$(RM) *.log *.dvi *.blg
	
clean_figs:
	cd tikz; make clean

