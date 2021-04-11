# LNI Proceedings

This repository supports generating of proceedings based on the "Lecture Notes in Informatics" papers typeset using the [lni class](https://www.ctan.org/pkg/lni).
An example output is available at [proceedings-example.pdf](proceedings-example.pdf).

## Success stories

Following proceedings were typeset using this template:

* [BTW 2017](https://dl.gi.de/handle/20.500.12116/21090/)
* [BTW 2017 Workshopband](https://dl.gi.de/handle/20.500.12116/21091/)
* [SKILL 2018](https://dl.gi.de/handle/20.500.12116/28971/browse)
* [SKILL 2019](https://dl.gi.de/handle/20.500.12116/28988/browse)
* [Software Engineering and Software Management 2019](https://dx.doi.org/10.18420/se2019-58)

## Aims of this work

* Generate proceedings conforming with GI's requirements stated at the "[Herausgeberrichtlinien](https://www.gi.de/service/publikationen/lni/autorenrichtlinien.html)".
* Automatic generation of
  * running heads (including page numbers, authors, title of the paper)
  * table of contents
  * PDF bookmarks
  * index
  * `proceedings.bib` listing all papers including page numbers
* Working hyperlinks
  * from the TOC to the papers
  * within the papers
  * from the index to the papers

## Howto

### System setup

This section describes the setup of software required.
This howto is based on a Windows environment.
Linux users should have ready most of the tools required.

#### Using Docker

On both Windows and Linux, one can use [Docker](https://www.docker.com/) for a fully configured Linux environment being able to build the proceedings.
For inspection, the docker image can be found at <https://hub.docker.com/r/danteev/texlive/>.
Assuming, the proceedings reside in `c:\git-repositories\LNI-proceedings`, following command leads to a bash shell enabling running the required commands:

```terminal
docker run -v c:\git-repositories\LNI-proceedings:/var/texlive -it danteev/texlive:v1.6.0 bash
```

#### Manual Setup on Windows

##### Recommended setup of MiKTeX

MiKTeX should be installed in a single-user setup to avoid troubles when updating packages.
Furthermore, it should be installed at `C:\MiKTeX` to enable easy installation of the pax utility.
Otherwise, you have to follow the steps described at <http://tex.stackexchange.com/a/108490/9075> to keep your MiKTeX distribution updated.

* Download the basic installer from <http://miktex.org/download>
* Start it
* First screen: Read the license condiditions and be sure that you really agree.
* Second screen: "Shared Installation": Install MiKTeX for: "Only for: `username`"
* Third screen: "Installation Directory": Install MiKTeX to: `C:\MiKTeX`. This enabled browsing for documentation at `C:\MiKTeX29\doc\latex`
* Fourth screen: "Settings": Preferred paper: A4 and Install missing packages on the fly: `Yes`
* Fifth screen: Press "Start"
* After the installation:
  1. Open `cmd.exe`
  2. Execute `mpm --update-db`
  3. Execute `mpm --update`
  4. Execute `mpm --install=cm-super`
  5. Execute `initexmf --update-fndb`
  6. Execute `initexmf --mklinks --force`

##### pax

[pax](http://ctan.org/pkg/pax) is a utility, which enables hyperlinks still working when combining PDFs using pdflatex.
In the installation, we rely on [chocolatey](https://chocolatey.org/), because it eases installation much.

* Installl java runtime environment using `choco install jre8`. [chocolatey page](https://chocolatey.org/packages/jre8).
* Install unzip, wget, and curl using `choco install unzip wget curl`.
* Install perl using `choco install strawberryperl`. [chocolatey page](https://chocolatey.org/packages/StrawberryPerl).
* Install pax using the MiKTeX package manager
* Execute `perl C:\MiKTeX\scripts\pax\pdfannotextractor.pl --install` to enable downloading of a pdfbox version fitting for pax.
* Ignore the error regarding "MiKTeX Configuration Utility"
* Start "MiKTeX Settings"
* Click on "Refresh FNDB"
* Click on "Update Formats"
* Now, `pdfannotextractor.pl` is ready to go

Source for installing pax: <http://tex.stackexchange.com/a/44104/9075>

##### Python 2.7

This is required to automatically extract the authors and title from the papers source texs.

1. Install Python 2.7: `choco install python2`
2. Install pip
   * wget https://bootstrap.pypa.io/get-pip.py
   * `c:\Python27\python get-pip.py`
3. Install `pyparsing`
   * `c:\Python27\Scripts\pip install pyparsing`
4. Install `python-docx`
   * `c:\Python27\Scripts\pip install python-docx`

##### Linux commands available at cmd.exe

We need `sed` being available at a cmd.exe shell.
This should be available when you executed `choco install git`.

##### PDFtk

This is required for to cut the proceedings.pdf into separate PDF files, one per paper, to submit to "Digitale Bibliothek der GI".

* Install PDFtk using `choco install pdftk`

### Generating the proceedings

1. Request [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier) prefix from GI
1. Download [main.zip](https://github.com/gi-ev/LNI-proceedings/archive/main.zip) from the [LNI-proceedings repository](https://github.com/gi-ev/LNI-proceedings).
1. Extract `main.zip` into the directory you are going to work on the proceedings.
1. Get the cover page ready.
   The template is available at <https://www.gi.de/fileadmin/redaktion/Autorenrichtlinien/LNI-Cover-Vorlage.ppt>.
   This preparation provides you the necessary information for the next step.
   You also need to submit the cover to the GI and to the printing service.
1. Adapt `config.tex` to your conference.
   Here, you also set the DOI prefix used for generating a unique DOI for each paper.
1. Check that `LNI-Startseiten.docx` is the latest version retrieved from <https://www.gi.de/fileadmin/redaktion/Autorenrichtlinien/LNI-Startseiten.docx>.
1. Adapt `LNI-Startseiten.docx` to your conference.
1. Convert `LNI-Startseiten.docx` to `LNI-Startseiten.pdf` using Microsoft Word.
1. Adapt `pages=x-y` (and possibly `\pdfbookmark`) at `\includepdf[pagecommand={\thispagestyle{empty}},pages=5-5]{LNI-Startseiten.pdf}` and subsequent `\includepdf` statements to match the page numbers of your foreword and sponsoring.
1. Create all paper folders using a naming scheme:
   `[Category][NumberOfSubcategory]-[NumberWithinSession]`.
   See also [Directory scheme](#directory-scheme).
1. Collect all papers. Place the source and the pdf within each paper's folder.
   For instance, the first paper goes into `papers/A1-1/`.
1. Rename all papers to paper.pdf etc. To do this, open a CMD, `cd papers` and run `papers_rename.cmd`. This should rename all .tex .pdf and .docx files to paper.tex, paper.pdf and paper.docx respectively. These directories should only contain one file of this file extension.
1. To extract author and title information from Microsoft Word docx files, run `add_tex_via_docx.cmd` in the `papers` directory.
  On Linux you can run `add_tex_via_docx.sh`.
  Make sure you installed python-docx as described in system setup.
  The `add_tex_via_docx.cmd` script will create minimal paper.tex files (title and author only) for each paper.docx, which can be processed by the following scripts.
1. Create pax information
   * Linux: Execute `prepare-papers.sh`
   * Windows: Execute `prepare-papers.bat`
1. Check for all `paper.tex` that all authors are the format `\author[Firstname Lastname \and ...]{...}`
1. Copy the author information from each `paper.tex` into `proceedings.tex`:
   * Open a [git bash](https://git-for-windows.github.io/)
   * cd into `papers`
   * During fixup phase, run `/c/Python27/python ../addAuthTi.py ../proceedings.template ../proceedings.tex */paper.tex`.
     The proceedings.tex created by this script uses build ids as workshop titles which makes it easier to identify the specific papers causing issues.
   * To override the extraction of author and title for a specific paper, just put a the desired `\addpaper` statement into the `paper.tex` of that paper.
     Prefix it with `%` to ensure the normal latex run on that paper does not cause issues.
   * For final proceedings, fill the workshop table in `addAuthTiProduction.py` and run `python ../addAuthTiProduction.py ../proceedings.template ../proceedings.tex */paper.tex`.
     This will create a `proceedings.tex` with the real workshop titles instead of build ids.
1. Fix spaces before `\and` in `proceedings.tex`: Replace `SPACE\and` by `\and`, where `SPACE` denotes the [white space character](https://en.wikipedia.org/wiki/Whitespace_character).
   Reason: `\unskip` does nothing at `\texorpdfstring` in combination with hyperref
1. Execute `pdflatex -synctex=1 proceedings.tex` to see whether pdflatex gets through.
1. Check `proceedings.pdf` whether **all fonts are embedded**.
   In case some fonts are not embedded, follow folling steps:
    * go to the folder of the paper
    * locate the PDF containing the picture
    * embed the font using Acrobat Professional's preflight functionality
    * Recompile the paper (`pdflatex paper`, ...)
    * Recompile the proceedings (`pdflatex  -synctex=1 proceedings`)
1. Do the usual pdflatex, biblatex, texindy runs.
   pdflatex also generates `proceedings.bib` and thereby also generates the character sequence `\IeC` (see [Implementation documentation](#implementation-documentation)).
   These characters have to be removed for the final biblatex run.
   All these steps are automatically done by `make-proceedings`.
    * Linux: Execute `make-proceeding.sh` to execute all required steps
    * Windows: Execute `make-proceedings.bat` to execute all required steps
1. Check proceedings and make necessary adaptions.
    During the fixup phase, you can run `pdflatex -synctex=1 proceedings` to quickly build the proceedings.
    Nevertheless, run `make-proceedings.bat` every now and then to ensure a correctly generated index.
1. Finalize pax information
   * Linux: Execute `prepare-papers.sh`
   * Windows: Execute `prepare-papers.bat`
1. Compile the final proceedings
   * Linux: Execute `make-proceedings.sh` to execute all required steps
   * Windows: Execute `make-proceedings.bat` to execute all required steps
1. Shrink the size of the final pdf:
   * Rename `proceedings.pdf` to `proceedings-large.pdf`
   * Execute `./shrinkpdf.sh proceedings-large.pdf proceedings.pdf`

`proceedings.pdf` is now ready to be sent to the printing service.
See below.

The automated steps of this workflow are stated at [.circlci/config.yml](https://github.com/gi-ev/LNI-proceedings/blob/master/.circleci/config.yml#L9).

#### Generated files

During the process, following files are generated:

* `proceedings.pdf`
  * It is not recommended to version this file during the process of proceedings generation, because it gets very large.
  * The page size of this file is already the final page size of both the printed and the electronic proceedings.
    Delivering this format is agreed with the publisher.
* `proceedings.bib` - BibTeX bibliography of the proceedings.
* `proceedings.csv` - CSV containing some information on the proceedings.
* `papers.txt` - list of paper id and starting page.

#### Directory scheme

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

#### Advanced usage

It is possible to update the pages information in each paper's `paper.tex`.
Although this is uncessary, because of `cut-proceedings.sh`.
In case `cut-proceedings.sh` does not work on your side, this alternative way can be used.

1. Execute `generate-updatepages.sh-from-pages-txt.sh`.
   This generates `update-pages.sh`.
2. Execute `sh update-pages.sh`.
3. Recompile all pdfs.

### Submitting to the GI and the printing service

1. Submit `proceedings.pdf` and `LNI-Cover-Vorlage.ppt` (see step 2 above) to the GI for approval.
2. After the approval, submit to the printing service.

### Submitting to the "Digitale Bibliothek der GI"

1. Adapt BAND_TITEL, HRSG, LNI, DOI, ISSN, ISBN, YEAR, DATE and LOCATION in `metaExtract.py` according to your conference
1. Copy `proceedings.csv` created by `make-proceedings` to the `meta-extract` directory.
1. Fill the `ws.csv` according to your conference.
1. Fill the `papers.csv` with the meta data required (Build ID,Paper ID,Workshop ID,Autoren,Titel,Sprache,Keywords,Abstract).
   Instead of creating this file separately, it is helpful to keep track of your papers in a spreadsheet, including additional data such as status, problems, rights forms etc. and export the required meta data as CSV from this spreadsheet.
1. Run `python metaExtract.py papers.csv ws.csv proceedings.csv` in the `meta-extract` directory.
   This creates `meta-extract.csv` for submission to GI.
1. Cd into `slicing` directory and copy your `proceedings.pdf` and `proceedings.csv` here.
1. Run `python slicing.py proceedings.pdf proceedings.csv`. This requires pdftk to be installed (cf. System setup section).
   The script cuts the proceedings.pdf into separate pdfs, one per paper, according to the page numbers from `proceedings.csv`.
   The separate pdfs are placed in the `parts` directory and named according to their build ids.
1. Submit the `meta-extract.csv` and the PDFs in the `parts` directory to GI.

## FAQ

Q: Some papers do not contain the short author list (i.e., `\author{...authorlist...}` instead of `\author[...authorlist...]{...authorlist...}`.  
A: Use the online service <https://regex101.com/>.
  The regex is `(\\footnote{.*})|(\\footnotemark\[.\])|%.*|\\textsuperscript{.*}`.
  Paste the `\author` content to "Test String" and expand "Substituation" at the bottom.

Q: The number of pages changed. What should I do?  
A: `pdflatex proceedings`, do it twice to be sure that the TOC is created correctly and that the TOC has more than one page.
   Continue at "Update the page numbers" above

Q: What can I do if the hyperlinks in the proceedings do not work?  
A: Run `pdflatex proceedings` one more time, because pax needs one more run.

Q: What can I do if the hyperlinks in the cropped proceedings do not work?  
A: You hit an issue at pax with an interplay of `viewport` in includegraphics:
   The offset resulting of the viewport is not treated by pax.
   The link is in there. Just search a few lines below the link text.

Q: What if a paper needs adjustments?  
A : Sometimes, the GI required adjustments.
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

## Current minimal example

The current minimal example is built at [CircleCI](https://circleci.com/gh/gi-ev/LNI-proceedings/).
One can browse to the latest build and then to "Artifacts" to see the generated files.
These generated proceedings **do not** follow the guide lines:
The headings of each papers are too long, because the authors and titles are too long.
Manual adjustements using the `\addpaper` commands are required.
The minimal example should only show that the commands of the toolchain work.

## Implementation documentation

This section discusses some design decisions done when implementing this way to generate proceedings.

`\IeC` is written into `proceedings.bib`.
This issue is discussed at http://tex.stackexchange.com/q/234501/9075.
Since the file is encoded in ASCII characters, we just need to strip out `\IeC`.
This is done using [sed](https://en.wikipedia.org/wiki/Sed).

`slicing`: `cut-proceedings.sh` is an alternative script to `slicing.py`.
It was developed before `slicing.py`, but puts each paper to a separate sub directory.
Currently, it is not used, but left there, because it could get useful sometime.

## Considered alternatives

When designing this solution to typeset complete proceedings, several alternatives were investigated.
Nearly all possible alternatives are listed at <http://www.ctan.org/topic/confproc>.
In the following, evaluated alternatives are listed and discussed.

### confproc

[confproc](http://www.ctan.org/pkg/confproc) seems to the most suitable alternative.
Compared with this approach, it has following drawbacks:

* The PDFs of the papers do not take a proper heading (page numbers, editor).
* When clicking on a link in one included PDF, the linked PDF is opened instead of jumping to the link.
* Indexing of authors has to be done by manually.

### combine

The [combine](https://www.ctan.org/pkg/combine) class combines the sources of different LaTeX together.
Since there might be conflicting packges, we wanted to include each PDF on its own.
The PDFs can be typeset by itself.

### proc

[proc](http://www.ctan.org/pkg/proc) is a very basic class based on the article class.
No update since 1995.

### Springer Computer Science Proceedings

Springer offers help for proceedings authors at <https://www.springer.com/gp/computer-science/lncs/editor-guidelines-for-springer-proceedings>.
It uses makeindex instead of biblatex for index generation.
We opted for biblatex+texindy to be UTF-8 save and to directly be able to use the content of `\authors` for index generation.

## License

This work is licensed under [CC0](https://creativecommons.org/publicdomain/zero/1.0/), so you especially can create proceedings out of it.
Feedback is welcome at the [GitHub page](https://github.com/latextemplates/LNI-proceedings).

`shrinkpdf.sh` is BSD-licensed.

## Further reading

* tex.stackexchange: [Constructing conference proceedings](http://tex.stackexchange.com/q/124942/9075)
