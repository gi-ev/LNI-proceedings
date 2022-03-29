---
nav_order: 5
---
# Generating the proceedings

1. Request [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier) prefix from GI
1. Setup a new git repository based on the LNI-proceedings repoository by following <https://github.com/gi-ev/LNI-proceedings/generate>.
1. Get the cover page ready.
   The template is available at <https://gi.de/fileadmin/GI/Hauptseite/Service/Publikationen/LNI/LNI-Cover-Vorlage.ppt>.
   This preparation provides you the necessary information for the next step.
   You also need to submit the cover to the GI and to the printing service.
1. Adapt `config.tex` to your conference.
   Here, you also set the DOI prefix used for generating a unique DOI for each paper.
1. Check that `LNI-Startseiten.docx` is the latest version retrieved from <https://gi.de/fileadmin/GI/Hauptseite/Service/Publikationen/LNI/LNI-Startseiten.docx>.
1. Adapt `LNI-Startseiten.docx` to your conference.
1. Convert `LNI-Startseiten.docx` to `LNI-Startseiten.pdf` using Microsoft Word.
1. Create all paper folders using a naming scheme:
   `[Category][NumberOfSubcategory]-[NumberWithinSession]`.
   See also [Directory scheme](#directory-scheme).
1. Collect all papers.
   Place the source and the pdf within each paper's folder.
   For instance, the first paper goes into `papers/A1-1/`.
1. Rename all papers to `paper.{pdf,tex,docx}`.
   To do this, open a CMD, `cd papers` and run `papers_rename.cmd`.
   This should rename all `.tex`, `.pdf`, and `.docx` files to `paper.tex`, `paper.pdf`, and `paper.docx` respectively.
   The paper directories should only contain one file of this file extension.
1. To extract author and title information from Microsoft Word docx files, run `add_tex_via_docx.cmd` in the `papers` directory.
   On Linux, you can run `add_tex_via_docx.sh`.
   Make sure you installed python-docx as described in system setup.
   The `add_tex_via_docx.cmd` script will create minimal paper.tex files (title and author only) for each paper.docx, which can be processed by the following scripts.
1. Check for all `paper.tex` that all authors are the format `\author[Firstname Lastname \and ...]{...}`
1. Copy the author information from each `paper.tex` into `proceedings.tex`:
   * Open a [git bash](https://git-for-windows.github.io/)
   * cd into `papers`
   * During fixup phase, run (on linux, because of expansion) `python ../addAuthTi.py ../proceedings.template.tex ../proceedings.tex */paper.tex`.
     The `proceedings.tex` created by this script uses build ids as workshop titles which makes it easier to identify the specific papers causing issues.
   * To override the extraction of author and title for a specific paper, just put a the desired `\addpaper` statement into the `paper.tex` of that paper.
     Prefix it with `%` to ensure the normal latex run on that paper does not cause issues.
   * For final proceedings, fill the workshop table in `addAuthTiProduction.py` and run `python ../addAuthTiProduction.py ../proceedings.template.tex ../proceedings.tex */paper.tex`.
     This will create a `proceedings.tex` with the real workshop titles instead of build ids.
1. Fix spaces before `\and` in `proceedings.tex`: Replace `SPACE\and` by `\and`, where `SPACE` denotes the [white space character](https://en.wikipedia.org/wiki/Whitespace_character).
   Reason: `\unskip` does nothing at `\texorpdfstring` in combination with hyperref
1. Execute `lualatex -synctex=1 proceedings.tex` to see whether `lualatex` gets through.
1. `proceedings.tex`: Adapt `pages=x-y` (and possibly `\pdfbookmark`) at `\includepdf[pagecommand={\thispagestyle{empty}},pages=5-5]{LNI-Startseiten.pdf}` and subsequent `\includepdf` statements to match the page numbers of your foreword and sponsoring.
1. Check `proceedings.pdf` whether **all fonts are embedded**.
   In case some fonts are not embedded, follow folling steps:
    * go to the folder of the paper
    * locate the PDF containing the picture
    * embed the font using Acrobat Professional's preflight functionality
    * Recompile the paper (`lualatex paper`, ...)
    * Recompile the proceedings (`lualatex -synctex=1 proceedings`)
1. Do the usual `lualatex`, `biblatex`, `texindy` runs.
   All these steps are automatically done by `make-proceedings` or by `latexmk proceedings`.
    * Linux: Execute `latexmk proceedings` (or `make-proceeding.sh`) to execute all required steps
    * Windows: Execute `latexmk proceedings` (or `make-proceedings.bat`) to execute all required steps
1. Check proceedings and make necessary adaptions.
    During the fixup phase, you can run `lualatex -synctex=1 proceedings` to quickly build the proceedings.
    Nevertheless, run `latexmk proceedings` (or `make-proceedings.bat`) every now and then to ensure a correctly generated index.
1. Compile the final proceedings
    * Linux: Execute `latexmk proceedings` (or `make-proceeding.sh`) to execute all required steps
    * Windows: Execute `latexmk proceedings` (or `make-proceedings.bat`) to execute all required steps
1. Shrink the size of the final pdf:
   * Rename `proceedings.pdf` to `proceedings-large.pdf`
   * Execute `cpdfsqueeze` for a lossless pdf compression:
     * `docker run -it --rm -v c:\git-repositories\LNI-proceedings:/workdir koppor/cpdfsqueeze cpdfsqueeze proceedings-large.pdf proceedings.pdf`
   * Alternative: Lossy compression using ghostscript (based on Alfred Klomp's [shrink.sh](http://www.alfredklomp.com/programming/shrinkpdf/))
     * The current drawback is that the PDF bookmarks are not shown and the initial view is not the page view, but fit page width.
     * Execute `./shrinkpdf.sh proceedings-large.pdf proceedings.pdf`
     * When using git bash (and MiKTeX), modify `shrinkpdf.sh` to call `mgs` instead of `gs`.
     * In case you have trouble with rotating pages, try `//None` instead of `/None`.

`proceedings.pdf` is now ready to be sent to the printing service.
See below.

The automated steps of this workflow are stated at [.github/workflows/build.yml](https://github.com/gi-ev/LNI-proceedings/blob/main/.github/workflows/build.yml).

## Generated files

During the process, following files are generated:

* `proceedings.pdf`
  * It is not recommended to version this file during the process of proceedings generation, because it gets very large.
  * The page size of this file is already the final page size of both the printed and the electronic proceedings.
    Delivering this format is agreed with the publisher.
* `proceedings.bib` - BibTeX bibliography of the proceedings. Ensure that you run `makeproceedings.sh` so that `\textunderscore` is correctly replaced by `_`.
* `proceedings.csv` - CSV containing some information on the proceedings. Ensure that you run `makeproceedings.sh` so that there is no space before each `;` anymore.
* `papers.txt` - list of paper id and starting page.

## Directory scheme

Naming scheme: `[Category][NumberOfSubcategory]-[NumberWithinSession]`.

Paper name always: `paper.tex`

The following list may be generated out of an Excel file or something else.
Otherwise, just create the folders and adapt `proceedings.tex` accordingly.

```text
A = Eingeladene Vorträge
A1-1 = Erster eingeladener Vortrag

B = Scientific Program (nach Themen gegliedert, Kapitel)
B1 = Topic 1
B1-1 = Talk 1
```
