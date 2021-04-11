#!/bin/bash
lualatex -synctex=1 proceedings
lualatex -synctex=1 proceedings
biber proceedings
lualatex -synctex=1 proceedings
texindy -C utf8 proceedings.idx
lualatex -synctex=1 proceedings
lualatex -synctex=1 proceedings
sed -i "s/\\\\textunderscore /_/g" proceedings.bib
sed -i "s/ ;/;/g" proceedings.csv
