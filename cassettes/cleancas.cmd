@rem batch file to clean all .cas files recursively
for /r %%v in (*.cas) do ..\utilities\tapeconv\cleancas.exe "%%v"
pause