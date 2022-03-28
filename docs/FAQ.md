---
nav_order: 8
---
# FAQ

Q: Some papers do not contain the short author list (i.e., `\author{...authorlist...}` instead of `\author[...authorlist...]{...authorlist...}`.  
A: Use the online service <https://regex101.com/>.
  The regex is `(\\footnote{.*})|(\\footnotemark\[.\])|%.*|\\textsuperscript{.*}`.
  Paste the `\author` content to "Test String" and expand "Substituation" at the bottom.

Q: The number of pages changed. What should I do?  
A: `lualatex proceedings`, do it twice to be sure that the TOC is created correctly and that the TOC has more than one page.
   Continue at "Update the page numbers" above

Q: What can I do if the hyperlinks in the proceedings do not work?  
A: With `newpax` this should not be the case: The link information is extracted before included the PDF.
Thus, `paper.newpax` is generated right before the information of `paper.newpax` is read.

Q: What if a paper needs adjustments?  
A: Sometimes, the GI required adjustments.
For instance, if an author did not use the LNI style for the bibliography.
You can either ask the authors directly or do it for yourself.
In case you decide to adjust the paper for yourself, replace `\editor{...}` and `\booktitle{...}` by `\input{../../config.tex}` to ensure that all papers have the same conference configuration.

Q: I recompiled some papers. How can I check for errors?  
A: Use [ack](https://beyondgrep.com/) to globally check for errors.

* Run it from root directory to be sure everything compiled well. Insall it using [choco install ack](https://chocolatey.org/packages/ack).
* `ack "LaTeX Warning: Label(s) may have changed."`
* `ack "Package hyperref Warning: Token not allowed in a PDF string (PDFDocEncoding)"`

Q: How can I get the PDFs with the correct headers?  
A: Execute `cut-proceedings.sh proceedings.pdf`. [pdftk](https://www.pdflabs.com/tools/pdftk-server/) and ghostscript installed.

Q: Some papers are cut strangely and the PDF is broken. What can I do?  
A: The authors use an old version of the template.

Please ask them to update to the new version 1.1, available at <https://www.ctan.org/tex-archive/macros/latex/contrib/lni>.
You can also update the `paper.tex` file for yourself.
The differences are not too much.
Finally, you could try to adapt `\addpaperWRONGLAYOUT`.
That command is made for inclusion of papers of the old format.
However, it is currently not maintained and may produce wrong output.

Q: Some latex papers have two overlapping, slightly offset versions of the copyright icons on their first page in the proceedings.  
A: This seems to be a slight mismatch between the current LNI Latex template (v1.3) and the proceedings template. To fix this, you can surround the `\ccbynceu` on line 315 and 317 with `\phantom` like so: `\phantom{\ccbynceu}` and rebuild these papers.

Q: I get `AttributeError: 'NoneType' object has no attribute 'group'` at `part_a = match_a.group(1)` when running `addAuthTiProduction.py`  
A: You are not following the directory pattern `[Category][NumberOfSubcategory]-[NumberWithinSession]`.
   For instance, `A1-1` is valid, but `A-1` is invalid.

Q: I get `KeyError: 'A1'` when running `addAuthTiProduction.py`  
A: You did not update `addAuthTiProduction.py`.
   Please update `lookup_workshop` in there.

Q: I get `AttributeError: 'NoneType' object has no attribute 'splitlines'` when using `metaExract.py`.  
A: Not all columns are filled in `papers.csv`.

## Trouble shooting of compiled papers

If you are in need to recompile the submitted papers, there might be errors occurring.
This section provides hints on some of the most prominent errors.

* `\openbox already defined` -> `\let\openbox\relax` before `\usepackage{amsthm}`
* If you get something about `\spacing in math mode`, ensure that your bib file is correct and that you re-ran bibtex.
* `! Undefined control sequence.`  
  `l.27 \ulp@afterend`  
    You have used pdfcomments package, but you disabled it.
    Delete `paper.aux` and recompile.
* `! You can't use ``\spacefactor' in internal vertical mode.`: Currently unknown
