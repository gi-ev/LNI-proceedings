#!/bin/bash
perl `kpsewhich -var-value TEXMFDIST`/scripts/pax/pdfannotextractor.pl proceedings.pdf
pdflatex proceedings-cropped.pdf
pdflatex proceedings-cropped.pdf
