#!/bin/bash

perl /usr/share/texlive/texmf-dist/scripts/pax/pdfannotextractor.pl LNI-Startseiten
cd papers/
for d in */ ; do
	cd "$d"
	echo "Processing $d.." 
	perl /usr/share/texlive/texmf-dist/scripts/pax/pdfannotextractor.pl paper
	echo "Finished with $d"
	cd ..
done
echo "Finished everything" 
