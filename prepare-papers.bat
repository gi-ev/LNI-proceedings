@echo off

echo "Starting..." > status.log

perl C:\MiKTeX\scripts\pax\pdfannotextractor.pl LNI-Startseiten

cd papers

for /D %%i in (*) do (
  cd "%%i"
  echo Processing %%i...
  echo Processing %%i... >> status.log
  perl C:\MiKTeX\scripts\pax\pdfannotextractor.pl paper
  echo .
  echo Finished with %%i
  echo.
  cd ..
)

cd ..

echo "Finished everything" >> status.log
