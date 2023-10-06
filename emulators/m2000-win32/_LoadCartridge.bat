@echo off
if "%~1"=="" (
  echo Drag-and-drop a .bin cartridge file on '_LoadCartridge.bat' to start the program in the M2000 emulator directly
  pause&exit
)
cd %~dp0
m2000.exe -ram 64k -video 1 "%~1"