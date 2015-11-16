include ../Makefile.inc

PNG_PLOTS=$(PLOTS:%.pdf=%.png)

all: $(PNG_PLOTS)

%.png: %.pdf
	convert -flatten -density 300 -quality 100 -transparent white $< $(<:%.pdf=%.png)
