import os
import requests
import urllib.parse
import re
from content_generator import generate_content

def add_related_links(filename, content=None, folder_name=None):
    """添加關聯連結並創建不存在的筆記"""
    if content is None:
        content = read_note_content(filename)
    
    # 提取連結並創建不存在的筆記
    related_notes = create_missing_notes(content, folder_name)
    
    # 更新反向連結
    if related_notes:
        topic = os.path.basename(filename).replace('.md', '')
        update_backlinks(topic, related_notes, folder_name)
    
    return content

def read_note_content(filename):
    encoded = urllib.parse.quote(filename)
    url = f"http://localhost:27123/vault/{encoded}"
    headers = {"Authorization": f"Bearer " + os.getenv('OBSIDIAN_API_KEY')}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"❌ 讀取筆記失敗: {response.status_code}\n{response.text}")

    return response.text

def save_to_obsidian(filename, content):
    encoded = urllib.parse.quote(filename)
    url = f"http://localhost:27123/vault/{encoded}"
    headers = {
        "Authorization": f"Bearer " + os.getenv('OBSIDIAN_API_KEY'),
        "Content-Type": "text/markdown"
    }
    
    response = requests.put(url, headers=headers, data=content)
    if response.status_code != 204:
        raise RuntimeError(f"❌ 儲存筆記失敗: {response.status_code}\n{response.text}")

def create_missing_notes(content, folder_name=None):
    """從內容中提取連結，並為不存在的連結創建筆記"""
    # 提取所有 Markdown 連結 [文字](檔名.md)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
    # 提取所有 Obsidian 連結 [[檔名]]
    obsidian_links = re.findall(r'\[\[([^\]]+)\]\]', content)
    
    # 獲取現有筆記列表
    existing_notes = get_existing_notes()
    created_notes = []
    
    # 處理 Markdown 連結
    for title, link in links:
        note_name = link.replace('.md', '')
        if note_name not in existing_notes and note_name not in created_notes:
            # 使用相同的資料夾，不創建同名資料夾
            create_note(note_name, folder_name, learning_approach="2")
            created_notes.append(note_name)
    
    # 處理 Obsidian 連結
    for link in obsidian_links:
        if link not in existing_notes and link not in created_notes:
            # 使用相同的資料夾，不創建同名資料夾
            create_note(link, folder_name, learning_approach="2")
            created_notes.append(link)
    
    return created_notes

def get_existing_notes():
    """獲取 Vault 中現有的筆記列表"""
    headers = {"Authorization": f"Bearer {os.getenv('OBSIDIAN_API_KEY')}"}
    try:
        response = requests.get("http://localhost:27123/vault/", headers=headers)

        if response.status_code != 200:
            print(f"⚠️ 無法取得Vault檔案列表: {response.status_code}")
            return []

        files = response.json()["files"]
        notes = [f for f in files if f.endswith(".md")]
        note_names = [note.replace(".md", "") for note in notes]
        print(f"📚 從 Obsidian API 獲取到 {len(note_names)} 個筆記")
        return note_names
    except Exception as e:
        print(f"❌ 連接 Obsidian API 時出錯: {str(e)}")
        
        # 嘗試直接從文件系統讀取
        try:
            vault_path = os.getenv("VAULT_PATH")
            all_files = []
            
            # 遍歷所有文件夾和子文件夾
            for root, dirs, files in os.walk(vault_path):
                for file in files:
                    if file.endswith(".md"):
                        # 獲取相對於保險庫根目錄的路徑
                        rel_path = os.path.relpath(os.path.join(root, file), vault_path)
                        # 保留完整路徑（包括資料夾）
                        all_files.append(rel_path)
            
            # 保留完整路徑，但移除 .md 副檔名
            note_names = [f.replace(".md", "") for f in all_files]
            print(f"📚 從文件系統獲取到 {len(note_names)} 個筆記")
            return note_names
        except Exception as e2:
            print(f"❌ 從文件系統讀取筆記時出錯: {str(e2)}")
            return []

def create_note(topic, folder_name=None, learning_approach=None, generate_subquestions=True):
    """為指定主題創建新筆記"""
    print(f"🔄 正在創建關聯筆記: {topic}")
    
    # 檢查是否為子問題
    is_subquestion = False
    parent_topic = None
    
    # 檢查是否有子問題文件，並查找此主題是否為子問題
    vault_path = os.getenv("VAULT_PATH")
    if folder_name:
        folder_path = os.path.join(vault_path, folder_name)
        if os.path.exists(folder_path):
            subquestion_files = [f for f in os.listdir(folder_path) if f.endswith('_subquestions.txt')]
            
            for sq_file in subquestion_files:
                parent_topic = sq_file.replace('_subquestions.txt', '')
                with open(os.path.join(folder_path, sq_file), 'r', encoding='utf-8') as f:
                    subquestions = [line.strip() for line in f.readlines()]
                    if topic in subquestions:
                        is_subquestion = True
                        break
    
    # 設定資料夾標籤
    folder_tag = f"#{folder_name.replace(' ', '')}" if folder_name else None
    
    # 為子問題添加額外標籤
    if is_subquestion and parent_topic:
        parent_tag = f"#{parent_topic.replace(' ', '')}"
        if folder_tag:
            folder_tag = f"{folder_tag}, {parent_tag}"
        else:
            folder_tag = parent_tag
    
    # 使用 content_generator 生成內容
    # 如果提供了學習方法，則使用提供的方法
    # 否則，子問題使用與父主題相同的學習方法，或默認使用 Top-Down
    if learning_approach:
        approach = learning_approach
    else:
        approach = detect_parent_learning_approach(parent_topic, folder_name) if is_subquestion else "1"
    
    content = generate_content(
        topic, 
        folder_tag, 
        learning_approach=approach,
        generate_subquestions=(not is_subquestion)  # 子問題不再生成更多子問題
    )
    
    # 根據資料夾設置確定筆記路徑
    if folder_name:
        # 確保資料夾存在
        folder_path = os.path.join(vault_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        # 在指定資料夾中創建筆記
        filepath = os.path.join(folder_path, f"{topic}.md")
        print(f"📂 直接在資料夾 '{folder_name}' 中創建筆記")
    else:
        # 在根目錄創建筆記
        filepath = os.path.join(vault_path, f"{topic}.md")
        print(f"📂 在根目錄創建筆記")
    
    from obsidian_writer import save_to_obsidian
    save_to_obsidian(filepath, content)
    
    print(f"✅ 已創建關聯筆記: {topic}")
    return filepath

def detect_parent_learning_approach(parent_topic, folder_name):
    """檢測父主題使用的學習方法"""
    if not parent_topic or not folder_name:
        return "1"  # 默認使用 Top-Down
    
    vault_path = os.getenv("VAULT_PATH")
    parent_path = os.path.join(vault_path, folder_name, f"{parent_topic}.md")
    
    if not os.path.exists(parent_path):
        return "1"
    
    try:
        with open(parent_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "learning_approach: Top-Down" in content:
                return "1"
            elif "learning_approach: Bottom-Up" in content:
                return "2"
    except Exception as e:
        print(f"⚠️ 無法讀取父主題學習方法: {str(e)}")
    
    return "1"  # 默認使用 Top-Down

def update_backlinks(topic, related_topics, folder_name=None):
    """更新相關筆記中的反向連結"""
    vault_path = os.getenv("VAULT_PATH")
    
    for related in related_topics:
        # 構建相關筆記路徑
        if folder_name:
            related_path = os.path.join(vault_path, folder_name, f"{related}.md")
        else:
            related_path = os.path.join(vault_path, f"{related}.md")
        
        # 檢查筆記是否存在
        if not os.path.exists(related_path):
            continue
        
        # 讀取筆記內容
        with open(related_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有反向連結
        if f"[[{topic}]]" in content or f"[{topic}]({topic}.md)" in content:
            continue
        
        # 添加反向連結
        backlink_section = f"\n\n## 相關連結\n- [[{topic}]]\n"
        
        if "## 相關連結" in content:
            # 在現有相關連結區塊添加
            content = re.sub(r'(## 相關連結\n)(.+)', f'\\1- [[{topic}]]\n\\2', content)
        else:
            # 添加新的相關連結區塊
            content += backlink_section
        
        # 保存更新後的內容
        with open(related_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新反向連結: {related} -> {topic}")