import os
import re
from obsidian_writer import save_to_obsidian

def generate_index_page(folder_name, vault_path):
    """為資料夾生成索引頁面"""
    folder_path = os.path.join(vault_path, folder_name)
    
    # 確保資料夾存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"✅ 已創建資料夾: {folder_path}")
    
    # 獲取資料夾中的所有 .md 文件
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md') and f != 'index.md']
    
    # 檢查是否有子問題文件
    subquestion_files = [f for f in os.listdir(folder_path) if f.endswith('_subquestions.txt')]
    
    # 生成索引內容
    content = f"# {folder_name} 知識索引\n\n"
    content += f"#{folder_name.replace(' ', '')}\n\n"
    
    # 添加學習方法說明
    content += "## 學習方法\n\n"
    content += "本知識庫使用以下學習方法組織內容：\n\n"
    content += "- **Top-Down（從整體到細節）**：先提供整體概念和框架，然後逐步深入探討各個組成部分\n"
    content += "- **Bottom-Up（從細節到整體）**：先介紹基本概念和核心元素，然後解釋這些元素如何組合形成完整系統\n\n"
    
    # 主要筆記部分
    content += "## 主要筆記\n\n"
    
    # 找出主筆記（與資料夾同名的筆記）
    main_note = f"{folder_name}.md"
    if main_note in md_files:
        file_path = os.path.join(folder_path, main_note)
        note_name = main_note.replace('.md', '')
        
        # 讀取筆記內容，提取學習方法和第一段作為描述
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            # 提取學習方法
            learning_approach = "未指定"
            approach_match = re.search(r'learning_approach: (.*)', file_content)
            if approach_match:
                learning_approach = approach_match.group(1)
            
            # 嘗試提取第一段非標題文字
            description = ""
            lines = file_content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('!') and not line.startswith('[[') and not line.startswith('---'):
                    description = line[:150] + "..." if len(line) > 150 else line
                    break
        
        content += f"- [[{note_name}]] - **學習方法**: {learning_approach}\n  {description}\n\n"
    
    # 相關筆記部分
    content += "## 相關筆記\n\n"
    
    # 排除主筆記和索引筆記
    related_notes = [f for f in md_files if f != main_note]
    
    # 按照學習方法分類筆記
    topdown_notes = []
    bottomup_notes = []
    other_notes = []
    
    for md_file in related_notes:
        note_name = md_file.replace('.md', '')
        file_path = os.path.join(folder_path, md_file)
        
        # 讀取筆記內容，提取學習方法和第一段作為描述
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            # 提取學習方法
            learning_approach = "未指定"
            approach_match = re.search(r'learning_approach: (.*)', file_content)
            if approach_match:
                learning_approach = approach_match.group(1)
            
            # 嘗試提取第一段非標題文字
            description = ""
            lines = file_content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('!') and not line.startswith('[[') and not line.startswith('---'):
                    description = line[:100] + "..." if len(line) > 100 else line
                    break
        
        note_info = f"- [[{note_name}]] - {description}\n"
        
        # 根據學習方法分類
        if "Top-Down" in learning_approach:
            topdown_notes.append(note_info)
        elif "Bottom-Up" in learning_approach:
            bottomup_notes.append(note_info)
        else:
            other_notes.append(note_info)
    
    # 添加分類後的筆記
    if topdown_notes:
        content += "### Top-Down 筆記\n\n"
        content += "".join(topdown_notes) + "\n"
    
    if bottomup_notes:
        content += "### Bottom-Up 筆記\n\n"
        content += "".join(bottomup_notes) + "\n"
    
    if other_notes:
        content += "### 其他筆記\n\n"
        content += "".join(other_notes) + "\n"
    
    # 添加學習路徑
    content += "## 建議學習路徑\n\n"
    
    # 如果有子問題文件，提取子問題作為學習路徑
    if subquestion_files:
        content += "按照以下順序學習可以系統性地掌握本主題：\n\n"
        content += f"1. [[{folder_name}]] - 主題概述\n"
        
        # 從第一個子問題文件中提取子問題
        sq_file = subquestion_files[0]
        with open(os.path.join(folder_path, sq_file), 'r', encoding='utf-8') as f:
            subquestions = [line.strip() for line in f.readlines()]
            for i, sq in enumerate(subquestions, 2):
                content += f"{i}. [[{sq}]] - 子主題\n"
    else:
        content += "從主筆記開始，然後探索相關筆記以深入理解主題。\n\n"
    
    # 添加關聯圖視圖
    content += "\n## 知識關聯圖\n\n"
    content += f"```dataview\nGRAPH\nFROM #{folder_name.replace(' ', '')}\n```\n"
    
    # 添加標籤雲
    content += "\n## 相關標籤\n\n"
    content += f"```dataview\nTABLE WITHOUT ID file.tags as 標籤\nFROM #{folder_name.replace(' ', '')}\nFLATTEN file.tags as 標籤\nGROUP BY 標籤\n```\n"
    
    # 保存索引頁面
    index_path = os.path.join(folder_path, "index.md")
    save_to_obsidian(index_path, content)
    print(f"✅ 已生成索引頁面: {folder_name}/index.md")

def extract_learning_path(folder_name, vault_path):
    """從筆記中提取學習路徑"""
    folder_path = os.path.join(vault_path, folder_name)
    
    # 獲取資料夾中的所有 .md 文件
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md') and f != 'index.md']
    
    # 建立筆記之間的連結關係
    links = {}
    for md_file in md_files:
        note_name = md_file.replace('.md', '')
        file_path = os.path.join(folder_path, md_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 提取所有 Obsidian 連結 [[檔名]]
            obsidian_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            # 只保留資料夾內的連結
            folder_links = [link for link in obsidian_links if f"{link}.md" in md_files]
            
            links[note_name] = folder_links
    
    # 找出入度最低的筆記作為起點
    in_degrees = {note: 0 for note in [f.replace('.md', '') for f in md_files]}
    for note, outlinks in links.items():
        for link in outlinks:
            if link in in_degrees:
                in_degrees[link] += 1
    
    # 按入度排序
    sorted_notes = sorted(in_degrees.items(), key=lambda x: x[1])
    
    return [note for note, _ in sorted_notes]
