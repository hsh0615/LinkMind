#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 導入 Google API 庫
from google import genai
from google.genai import types
import base64

# 創建 Flask 應用
app = Flask(__name__)
# 允許跨域請求
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({"status": "ok", "message": "Gemini API 代理正在運行"})

@app.route('/generate', methods=['POST'])
def generate_content():
    """生成內容的端點"""
    try:
        # 獲取請求數據
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "缺少必要的 'prompt' 參數"}), 400
        
        prompt = data['prompt']
        model_name = data.get('model', 'gemini-1.5-pro')
        temperature = data.get('temperature', 0.3)
        top_p = data.get('top_p', 0.95)
        top_k = data.get('top_k', 40)
        max_output_tokens = data.get('max_output_tokens', 4096)
        
        # 記錄請求
        print(f"Received request for model {model_name}")
        print(f"Prompt: {prompt[:100]}...")
        
        # 使用 Vertex AI 客戶端
        client = genai.Client(
            vertexai=True,
            project="amazing-bonbon-444411-s2",
            location="us-central1",
        )
        
        # 設置生成內容的配置
        generate_content_config = types.GenerateContentConfig(
            temperature = temperature,
            top_p = top_p,
            max_output_tokens = max_output_tokens,
            response_modalities = ["TEXT"],
        )
        
        # 使用流式輸出獲取響應
        full_response = ""
        for chunk in client.models.generate_content_stream(
            model = model_name,
            contents = [prompt],
            config = generate_content_config,
        ):
            if chunk.text:
                full_response += chunk.text
        
        # 返回結果
        return jsonify({
            "content": full_response,
            "model": model_name
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 獲取端口，默認為 5000
    port = int(os.getenv('PORT', 5000))
    print(f"Starting Gemini API proxy server on port {port}")
    print(f"Health check: http://localhost:{port}/health")
    app.run(host='0.0.0.0', port=port, debug=True) 