#!/bin/bash

PAXDIR=`kpsewhich -var-value TEXMFDIST`/scripts/pax

perl $PAXDIR/pdfannotextractor.pl LNI-Startseiten
cd papers/
for d in */ ; do
	cd "$d"
	echo "Processing $d.." 
	perl $PAXDIR/pdfannotextractor.pl paper
	echo "Finished with $d"
	cd ..
done
echo "Finished everything" 
