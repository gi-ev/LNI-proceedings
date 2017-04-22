@echo off
pdflatex -synctex=1 proceedings
pdflatex -synctex=1 proceedings
rem TOC should be correct now
sed -i "s/\\\\IeC //g" proceedings.bib
biber proceedings
pdflatex -synctex=1 proceedings
texindy proceedings.idx
pdflatex -synctex=1 proceedings
pdflatex -synctex=1 proceedings
sed -i "s/\\\\IeC //g" proceedings.bib
sed -i "s/\\\\IeC //g" proceedings.csv
sed -i "s/ ;/;/g" proceedings.csv
