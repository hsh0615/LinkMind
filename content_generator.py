from google import genai
from google.genai import types
import os
import datetime
import re

def generate_content(topic, folder_tag=None, learning_approach="1", generate_subquestions=False):
    client = genai.Client(
        vertexai=True,
        project="amazing-bonbon-444411-s2",
        location="us-central1"
    )
    # 先掃Obsidian Vault內有哪些筆記
    existing_notes = scan_existing_notes()
    
    tag_instruction = f"\n    - 添加標籤 {folder_tag}" if folder_tag else ""
    
    # 根據學習方法選擇不同的提示
    if learning_approach == "1":  # Top-Down
        approach_instruction = """
        使用Top-Down方法（從整體到細節）：
        1. 先提供主題的整體概念和框架
        2. 然後逐步深入探討各個組成部分
        3. 最後連結到具體的細節和應用
        """
    else:  # Bottom-Up
        approach_instruction = """
        使用Bottom-Up方法（從細節到整體）：
        1. 先介紹基本概念和核心元素
        2. 然後解釋這些元素如何組合和相互作用
        3. 最後展示如何形成完整的系統或理論
        """
    
    # 子問題生成指令
    subquestions_instruction = """
    在筆記末尾添加「延伸學習」部分，列出5-8個系統性的子問題，這些問題應該：
    - 涵蓋主題的不同方面和層次
    - 從基礎到進階，有邏輯順序
    - 每個問題都使用 [[子問題]] 格式，以便自動創建關聯筆記
    - 簡短說明每個子問題的重要性或學習價值
    """ if generate_subquestions else ""
    
    prompt = f"""
    為「{topic}」生成詳細的學習筆記：
    
    {approach_instruction}
    
    筆記結構：
    1. 概念定義和重要性（清晰簡潔的介紹）
    2. 核心原理和組成部分（詳細解釋每個關鍵概念）
    3. 應用場景和實例（具體例子說明如何應用）
    4. 優缺點或挑戰（客觀分析）
    5. 相關概念和連結（使用 [[概念名稱]] 格式）
    {subquestions_instruction}
    
    已有筆記：{", ".join(existing_notes)}
    
    注意：
    - 內容要詳細但有條理，使用標題、子標題組織內容
    - 使用粗體、斜體、列表等格式增強可讀性
    - 確保連結格式正確以建立知識圖譜
    - 每個段落應該有明確的焦點和目的{tag_instruction}
    - 添加實用的代碼示例、公式或圖表說明（如適用）
    """
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=8192,  # 增加輸出長度以獲得更詳細的內容
        response_modalities=["TEXT"]
    )

    generated_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-001",
        contents=[prompt],
        config=generate_content_config
    ):
        generated_text += chunk.text

    # 添加 YAML 前置元數據
    yaml_header = f"""---
title: {topic}
created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags: {folder_tag.replace('#', '') if folder_tag else 'general'}
aliases: [{topic}, {topic.lower()}]
learning_approach: {"Top-Down" if learning_approach == "1" else "Bottom-Up"}
---

"""
    
    # 提取子問題，以便後續處理
    if generate_subquestions:
        extract_and_save_subquestions(topic, generated_text, folder_tag)
    
    return yaml_header + generated_text

def extract_and_save_subquestions(main_topic, content, folder_tag=None):
    """提取子問題並保存到待處理列表"""
    # 尋找所有 [[子問題]] 格式的連結
    subquestions = re.findall(r'\[\[([^\]]+)\]\]', content)
    
    # 將子問題保存到文件中，以便後續處理
    if subquestions:
        vault_path = os.getenv("VAULT_PATH")
        folder_name = folder_tag.replace('#', '') if folder_tag else None
        
        # 確保資料夾存在
        if folder_name:
            os.makedirs(os.path.join(vault_path, folder_name), exist_ok=True)
            # 保存子問題列表到指定資料夾
            subquestions_file = os.path.join(vault_path, folder_name, f"{main_topic}_subquestions.txt")
        else:
            # 保存子問題列表到根目錄
            subquestions_file = os.path.join(vault_path, f"{main_topic}_subquestions.txt")
        
        with open(subquestions_file, 'w', encoding='utf-8') as f:
            for q in subquestions:
                f.write(f"{q}\n")
        
        print(f"✅ 已提取 {len(subquestions)} 個子問題，保存至 {subquestions_file}")

def scan_existing_notes():
    import requests
    headers = {"Authorization": f"Bearer {os.getenv('OBSIDIAN_API_KEY')}"}
    response = requests.get("http://localhost:27123/vault/", headers=headers)

    if response.status_code != 200:
        print(f"⚠️ 無法取得Vault檔案列表，僅使用空白連結：{response.status_code}")
        return []

    files = response.json()["files"]
    notes = [f for f in files if f.endswith(".md")]
    return [note.replace(".md", "") for note in notes]