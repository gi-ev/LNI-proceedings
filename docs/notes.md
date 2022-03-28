---
nav_order: 7
---
# Random notes

## Advanced usage

It is possible to update the pages information in each paper's `paper.tex`.
Although this is uncessary, because of `cut-proceedings.sh`.
In case `cut-proceedings.sh` does not work on your side, this alternative way can be used.

1. Execute `generate-updatepages.sh-from-pages-txt.sh`.
   This generates `update-pages.sh`.
2. Execute `sh update-pages.sh`.
3. Recompile all pdfs.

## Current minimal example

The current minimal example is built using GitHub actions.
One can browse to the latest build and then to "Artifacts" to see the generated files.
These generated proceedings **do not** follow the guide lines:
The headings of each papers are too long, because the authors and titles are too long.
Manual adjustements using the `\addpaper` commands are required.
The minimal example should only show that the commands of the toolchain work.

## Implementation documentation

This section discusses some design decisions done when implementing this way to generate proceedings.

`slicing`: `cut-proceedings.sh` is an alternative script to `slicing.py`.
It was developed before `slicing.py`, but puts each paper to a separate sub directory.
Currently, it is not used, but left there, because it could get useful sometime.
