@echo off %debug%

:: renaming all pdfs and texs to paper.*
:: NOTE: all directories should contain only one .pdf, one .tex and one .docx
for /D %%i in (*) do (
	cd "%%i"
	ren *.tex paper.tex
	ren *.pdf paper.pdf
    ren *.docx paper.docx
	cd ..
)