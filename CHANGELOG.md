# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased]

### Added
- Meta Data Extraction (`metaExtract.py`): Automatic extraction of dublin core based meta data table for submission to GI digital library
- Slicing (`slicing.py`): Slicing of proceedings into separate papers for submission to GI digital library
- Support for Word papers (`add_tex_via_docx.cmd`): Extraction of Author and Title from DOCX papers
- Papers Renaming (`papers_rename.cmd`): Automatic renaming of paper files in papers sub-folders for convenience

### Changed
- Fix typo in README.md
- Author and title extraction script (`addAuthTi.py`)
  - encoding and texify of special characters
  - adds all papers from papers folder in the correct order to proceedings.tex
  - adds \addchap for every new top level, e.g. between B13-4 and C1-0
  - production version uses lookup table for build ids and workshops and fills `proceedings.tex` with workshop titles

### Fixed
- Add `make-proceedings.sh` and `prepare-papers.sh`. Refine README.md accordingly.
- Corrected GI DOI Prefix

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

[unreleased]: https://github.com/gi-ev/LNI-proceedings/compare/v1.3.0...master
[1.3.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/gi-ev/LNI-proceedings/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/gi-ev/LNI/releases/tag/v1.0.0
