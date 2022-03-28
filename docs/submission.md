---
nav_order: 6
---
# Submission to GI e.V.

The submission consists of two steps outlined below.

## Submitting to the GI and the printing service

1. Submit `proceedings.pdf` and `LNI-Cover-Vorlage.ppt` (see step 2 in [Generation of the proceedings](proceedings-generation.md)) to the GI for approval.
2. After the approval, submit to the printing service.

## Submitting to the "Digitale Bibliothek der GI"

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
