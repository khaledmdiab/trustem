include ../Makefile.inc

PNG_FIGURES=$(FIGURES:%.pdf=%.png)

all: $(FIGURES) $(PNG_FIGURES)

%.pdf: %.tex
	pdflatex $<

%.png: %.pdf
	convert -flatten -density 300 -quality 100 -transparent white $< $(<:%.pdf=%.png)

clean:
	rm -rf $(FIGURES:pdf=aux) $(FIGURES:pdf=log)
