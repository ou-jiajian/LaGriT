@echo off
chcp 65001 > nul
REM LaGriT 环境变量设置

set "PATH=C:\msys64\mingw64\bin;%PATH%"
set "PATH=C:\msys64\usr\bin;%PATH%"

set "CC=C:\msys64\mingw64\bin\gcc.exe"
set "CXX=C:\msys64\mingw64\bin\g++.exe"
set "FC=C:\msys64\mingw64\bin\gfortran.exe"
set "CMAKE_C_COMPILER=C:\msys64\mingw64\bin\gcc.exe"
set "CMAKE_CXX_COMPILER=C:\msys64\mingw64\bin\g++.exe"
set "CMAKE_Fortran_COMPILER=C:\msys64\mingw64\bin\gfortran.exe"

echo LaGriT 环境变量已设置