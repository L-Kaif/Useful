@echo off
setlocal

:: Folder to install tools
set INSTALL_DIR=D:\Softwares\yt-dlp

echo.
echo =========================================
echo  Installing yt-dlp and ffmpeg for Windows
echo =========================================
echo.

:: Create directory if not exists
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

cd /d "%INSTALL_DIR%"

:: Download yt-dlp.exe
echo Downloading yt-dlp.exe...
powershell -Command "Invoke-WebRequest -Uri https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -OutFile yt-dlp.exe"

:: Download ffmpeg zip (static build)
echo Downloading ffmpeg...
powershell -Command "Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip"

:: Extract ffmpeg
echo Extracting ffmpeg...
powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath . -Force"

:: Move ffmpeg.exe files up one level
for /r %%f in (ffmpeg.exe) do copy "%%f" "%INSTALL_DIR%" >nul

:: Cleanup
rmdir /s /q "%INSTALL_DIR%\ffmpeg*" >nul 2>&1
del ffmpeg.zip >nul 2>&1

:: Add to PATH (system-wide)
echo Adding to PATH...
setx /M PATH "%PATH%;%INSTALL_DIR%"

echo.
echo =========================================
echo  Installation Complete!
echo =========================================
echo.
echo yt-dlp and ffmpeg are now available in PATH.
echo You may need to restart your terminal.
echo.
pause
