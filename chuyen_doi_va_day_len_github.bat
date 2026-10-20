@echo off
chcp 65001 >nul
title TỰ ĐỘNG CHUYỂN ĐỔI VÀ ĐẨY NHẠC LÊN GITHUB - XIAOZHI AI

echo ======================================================================
echo    BỘ CÔNG CỤ QUẢN LÝ KHO NHẠC TỰ ĐỘNG CHO ROBOT XIAOZHI
echo    Repo: https://github.com/thaihuy1101/Kho_nhac
echo ======================================================================
echo.

cd /d "%~dp0"

set "PYTHON_EXE=python"
if exist "C:\Espressif\tools\python\v6.1\venv\Scripts\python.exe" (
    set "PYTHON_EXE=C:\Espressif\tools\python\v6.1\venv\Scripts\python.exe"
)

echo [1/3] Đang quét và nén các file nhạc MP3 sang định dạng OGG Opus...
"%PYTHON_EXE%" chuyen_nhac.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LỖI] Quá trình chuyển đổi nhạc gặp sự cố!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Đang đóng gói dữ liệu và cập nhật Git...
git add .
git commit -m "Cap nhat kho nhac Xiaozhi"

echo.
echo [3/3] Đang đẩy dữ liệu lên GitHub (git push origin main)...
git push origin main

echo.
echo ======================================================================
echo [THÀNH CÔNG] Kho nhạc đã được cập nhật lên GitHub thành công!
echo Con robot Xiaozhi của bạn sẽ tự động thấy các bài hát mới này.
echo ======================================================================
echo.
pause
