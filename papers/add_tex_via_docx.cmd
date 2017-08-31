@echo off %debug%

:: renaming all pdfs and texs to paper.*
:: NOTE: all directories should contain only one .pdf and one .tex
for /D %%i in (*) do (
	cd "%%i"
	for %%j in (*.docx) do (
		cd ..
		python add_tex_via_docx.py "%%i" "%%j"
		cd "%%i"
	)
	cd ..
)