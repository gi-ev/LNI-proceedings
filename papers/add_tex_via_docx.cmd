@echo off %debug%

for /D %%i in (*) do (
	cd "%%i"
	for %%j in (*.docx) do (
		cd ..
		python add_tex_via_docx.py "%%i" "%%j"
		cd "%%i"
	)
	cd ..
)