@echo off
echo ============================================================
echo CROP IMAGES SETUP
echo ============================================================
echo.
echo This will add images for all crops in your system.
echo.
echo Choose an option:
echo   1. Download real images (requires internet)
echo   2. Create placeholder images (offline, fast)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Installing required packages...
    pip install Pillow requests
    echo.
    echo Downloading images...
    python download_crop_images.py
) else (
    echo.
    echo Installing Pillow...
    pip install Pillow
    echo.
    echo Creating placeholder images...
    python create_placeholder_images.py
)

echo.
echo ============================================================
echo Done! Restart your Flask app to see the images.
echo ============================================================
pause
