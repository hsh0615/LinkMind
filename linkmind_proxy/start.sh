#!/bin/bash
# 這個腳本用於啟動 Gemini API 代理伺服器

# 進入腳本所在目錄
cd "$(dirname "$0")"

# 清理並重新安裝依賴
echo "正在清理並重新安裝相依套件..."
pip install -r requirements.txt

# 設置 Google Cloud 認證
echo "設置 Google Cloud 認證..."
gcloud auth application-default login

# 啟動代理伺服器
echo "啟動 Gemini API 代理伺服器..."
echo "服務器將在端口 8080 上運行"
echo "健康檢查: http://localhost:8080/health"
python3 gemini_proxy.py 