#!/bin/bash
:<<'BATCH'
@echo off
cd /d "%~dp0"
python main.py
if errorlevel 1 pause
goto :eof
BATCH
cd "$(dirname "$0")"
python3 main.py
