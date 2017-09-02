#!/bin/bash

for d in */ ; do
	cd "$d"
	for f in *.docx ; do
		[ -f "$f" ] || continue
		cd ..
		python add_tex_via_docx.py "$d" "$f"
		cd "$d"
	done
	cd ..
done
