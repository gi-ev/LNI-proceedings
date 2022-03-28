---
nav_order: 4
---
# System setup

This section describes the setup of software required.
This howto is based on a Windows environment.
Linux users should have ready most of the tools required.

## Using Docker

On both Windows and Linux, one can use [Docker](https://www.docker.com/) for a fully configured Linux environment being able to build the proceedings.
For inspection, the docker image can be found at <https://hub.docker.com/r/danteev/texlive/>.
Assuming, the proceedings reside in `c:\git-repositories\LNI-proceedings`, following command leads to a bash shell enabling running the required commands:

```terminal
docker run -v c:\git-repositories\LNI-proceedings:/var/texlive -it danteev/texlive:edge bash
```

## Manual Setup on Windows

### Recommended setup of MiKTeX

MiKTeX should be installed in a single-user setup to avoid troubles when updating packages.
Furthermore, it should be installed at `C:\MiKTeX` to have an easy path access.
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

### Python 3

This is required to automatically extract the authors and title from the papers source texs.

1. Install Python: `choco install python`
1. Install `pyparsing`
   * `pip install pyparsing` (or `pip3 install pyparsing`)
1. Install `python-docx`
   * `pip install python-docx` (or `pip3 install python-docx`)

### Linux commands available at cmd.exe

We need `sed` being available at a cmd.exe shell.
This should be available when you executed `choco install git`.

### PDFtk

This is required for to cut the proceedings.pdf into separate PDF files, one per paper, to submit to "Digitale Bibliothek der GI".

* Install PDFtk using `choco install pdftk`
