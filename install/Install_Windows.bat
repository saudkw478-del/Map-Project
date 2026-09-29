@echo off
chcp 65001 >nul
title Install Game of Thrones - Westeros
set "SRC=%~dp0GoT_Westeros"
set "DEST=%APPDATA%\.minecraft\saves\GoT_Westeros"

if not exist "%SRC%\level.dat" (
  echo Could not find the GoT_Westeros folder next to this file.
  echo Extract the whole zip first, then run this file again.
  pause
  exit /b 1
)
if exist "%DEST%" (
  echo The world is already installed at:
  echo   %DEST%
  echo Delete that folder first if you want a fresh copy.
  pause
  exit /b 0
)
xcopy "%SRC%" "%DEST%\" /E /I /Y >nul
if errorlevel 1 (
  echo Copy failed. Is Minecraft Java Edition installed?
  pause
  exit /b 1
)
echo.
echo Done! Now open Minecraft Java Edition ^(1.21 or newer^):
echo   Singleplayer ^> "Game of Thrones - Westeros"
echo.
pause
