@echo off
:: 1. 物理重定向
set OPENAI_API_BASE=http://127.0.0.1:4000/v1
set OPENAI_API_KEY=sk-bridge-active

:: 2. 暴力启动（去掉所有多余符号，直接呼叫文件名）
openclaw

pause