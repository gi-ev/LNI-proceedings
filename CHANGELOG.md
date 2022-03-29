# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).
This project follows [Calendar Versioning](https://calver.org/).
Befor, this project adhered to [Semantic Versioning](http://semver.org/).

## [unreleased]

### Fixed

- DOI with underscores now correctly contained in `proceedings.bib`

### Changed

- Updated to [docker texlive image@latest](https://github.com/dante-ev/docker-texlive)
- Switched from [pax](https://ctan.org/pkg/pax) to [newpax](https://ctan.org/pkg/newpax)
- Switch to lualatex
- Switch from `viewport` to `trim` (which works better with newpax and probably pax, too)
- Restructured documentation
- Update to Python3
- Changed the repository type to "Template" allowing users to create a new repository based on the repository's current content.
- Updated `LNI-Startseiten.docx` and `LNI-Startseiten.pdf` based on GI's new `docx`.

### Added

- Add pacakge [selnolig](https://ctan.org/pkg/selnolig) to ensure correct ligatures.

### Removed

- `prepare-papers.*`, because of the switch from pax to newpax.

## [2.4.0] - 2018-01-10

### Fixed

- Fixed CC icon on first page of each paper (CC-BY-NC -> CC-BY-SA)
- "Titelseite" PDF bookmark now on page 3 also in `proceedings-template.tex`. Before, it was on page 1. In `proceedings.tex`, it still is on page 3.

## [2.3.0] - 2018-01-09

### Changed

- Update `LNI-Startseiten.docx` using the version of <https://gi.de/fileadmin/GI/Hauptseite/Service/Publikationen/LNI/LNI-Startseiten.docx>: License statement changed from CC-BY-NC 3.0 to CC-BY-SA 4.0.
- Add PDF bookmarks for "Titelseite", "Vorwort", "Sponsoren", "Tagungsleitung", "Programmkomitee", and "Organisationsteam"
- Minor improvements in `README.md`

## [2.2.0] - 2017-09-21

### Changed

- Improve position of text on page: Move papers 11.0mm up and move head 17.4mm up

## [2.1.0] - 2017-09-07

### Changed

- Proceedings are output in the format 23,5 x 15,5 cm required by the publisher and the digital library.
- Remove `cropproceedings.sh` and `proceedings-cropped.tex`

## [2.0.0] - 2017-09-03

### Added

- Meta Data Extraction (`metaExtract.py`): Automatic extraction of dublin core based meta data table for submission to GI digital library
- Slicing (`slicing.py`): Slicing of proceedings into separate papers for submission to GI digital library
- Support for Microsoft Word papers (`add_tex_via_docx.cmd`): Extraction of Author and Title from DOCX papers
- Papers Renaming (`papers_rename.cmd`): Automatic renaming of paper files in papers sub-folders for convenience
- Support of `%\addpaper` in `paper.tex` to force a specific `\addpaper` statement
- Cuts away license statement and DOI number
- `prepare-papers.sh` now uses `kpsewhich` to determine `pax` directory
- Add `add_tex_via_docx.sh`
- Add `cropproceedings.sh` and `proceedings-cropped.tex` to ease cropping the final proceedings.
- Reference to [docker image](https://github.com/koppor/docker-texlive), which provides a working environment to typeset the proceedings.

### Changed

- Author and title extraction script (`addAuthTi.py`)
  - encoding and texify of special characters
  - adds all papers from papers folder in the correct order to proceedings.tex
  - adds \addchap for every new top level, e.g. between B13-4 and C1-0
  - production version uses lookup table for build ids and workshops and fills `proceedings.tex` with workshop titles
- Directory naming scheme `[Category][NumberOfSubcategory]-[NumberWithinSession]` is now required.
- Papers are positioned 1mm higher to ensure correct positioning on the page
- Refined `README.md`

### Fixed

- Add `make-proceedings.sh` and `prepare-papers.sh`
- Corrected GI DOI Prefix
- Correct command for not using DOIs in `config.tex`

## [1.3.0] - 2017-04-30

### Added

- Support for generating and showing DOI on each paper

## [1.2.0] - 2017-04-22

### Added

- Support for showing page corner marks using the [crop package](https://www.ctan.org/pkg/crop).

### Fixed

- Use `proceedings.bib` also in `make-proceedings.bat`

## [1.1.0] - 2017-04-22

### Added

- Refined documentation
  - add link to example generated proceedings
  - list generated files
  - installation hints for curl and wget

### Changed

- Table of contents is now more MS-Word-like
- `authors.bib` is now called `proceedings.bib`
- `proceedings.bib` now has proper newlines

## [1.0.0] - 2017-04-07

First release of the template

[unreleased]: https://github.com/gi-ev/LNI-proceedings/compare/v2.4.0...master
[2.4.0]: https://github.com/gi-ev/LNI-proceedings/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/gi-ev/LNI-proceedings/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/gi-ev/LNI-proceedings/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/gi-ev/LNI-proceedings/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/gi-ev/LNI/releases/tag/v1.0.0
