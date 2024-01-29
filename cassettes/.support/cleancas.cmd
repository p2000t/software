@rem batch file to clean all .cas files recursively
cd ..
for /r %%v in (*.cas) do ..\utilities\cassette-dumper\cleancas.exe "%%v"
pause
