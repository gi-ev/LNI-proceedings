#`-file-line-error` is similar to `--interaction nonstopmode`, but shows the concrete line number
#Remove it, it you want pdflatex to stop on errors
$pdflatex = 'lualatex -shell-escape -file-line-error --synctex=-1 %O %S';

#Use SumatraPDF instead of the default PDF viewer
$pdf_previewer = 'start "C:\Program Files\SumatraPDF\SumatraPDF.exe"';

#SumatraPDF updates automatically
$preview_mode = 0;

#automatically call pdflatex (instead of latex)
$pdf_mode = 1;

# source: https://tex.stackexchange.com/a/335509/9075
$makeindex = 'texindy -C utf8 %O -o %D %S';

#remove more files than in the default configuration
@generated_exts = qw(acn acr alg aux code ist fls glg glo gls idx ind lof lot out thm toc tpt);
