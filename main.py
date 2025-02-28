import os
import time
import threading
from dotenv import load_dotenv
from content_generator import generate_content
from obsidian_writer import save_to_obsidian
from relation_manager import add_related_links, get_existing_notes, create_note
from utils import generate_index_page

load_dotenv()

def main():
    print("選擇操作模式:")
    print("1. 生成新主題筆記")
    print("2. 監控未解析連結 (點擊灰色節點時自動生成)")
    
    mode = input("請選擇 (1/2): ").strip()
    
    if mode == "1":
        generate_new_topic()
    elif mode == "2":
        monitor_unresolved_links()
    else:
        print("❌ 無效選擇")

def generate_new_topic():
    topic = input("請輸入要生成的筆記主題：").strip()
    
    # 選擇學習方法
    print("\n選擇學習方法:")
    print("1. Top-Down (從整體到細節)")
    print("2. Bottom-Up (從細節到整體)")
    
    while True:
        learning_approach = input("請選擇 (1/2): ").strip()
        if learning_approach in ["1", "2"]:
            break
        print("❌ 無效選擇，請輸入 1 或 2")
    
    # 詢問是否生成子問題
    generate_subquestions = input("是否自動生成延伸子問題？(y/n): ").strip().lower() == 'y'
    
    # 自動創建資料夾，使用主題名稱作為資料夾名
    folder_name = topic
    
    vault_path = os.getenv("VAULT_PATH")
    
    # 構建檔案路徑
    filepath = os.path.join(vault_path, folder_name, f"{topic}.md")
    # 設定資料夾路徑作為標籤，方便關聯
    folder_tag = f"#{folder_name.replace(' ', '')}"
    
    # 生成內容
    content = generate_content(
        topic, 
        folder_tag, 
        learning_approach=learning_approach, 
        generate_subquestions=generate_subquestions
    )
    
    # 保存到 Obsidian
    save_to_obsidian(filepath, content)
    
    # 處理關聯連結並創建不存在的筆記
    # 將關聯筆記也放入同一資料夾
    add_related_links(os.path.relpath(filepath, vault_path), content, folder_name)
    
    # 生成索引頁面
    generate_index_page(folder_name, vault_path)

    print(f"✅ 筆記已生成並存入 {os.path.relpath(filepath, vault_path)}，並自動創建關聯筆記")
    print(f"✅ 已生成索引頁面: {folder_name}/index.md")

def monitor_unresolved_links():
    """監控未解析連結，當檢測到點擊時自動生成內容"""
    # 重新載入環境變數
    load_dotenv(override=True)
    vault_path = os.getenv("VAULT_PATH")
    
    print("🔍 開始監控未解析連結...")
    print(f"📁 監控的保險庫路徑: {vault_path}")
    print("提示: 在 Obsidian 中點擊灰色節點或未解析連結時，系統將自動生成內容")
    print("按 Ctrl+C 停止監控")
    
    # 獲取初始筆記列表
    initial_notes = set(get_existing_notes())
    print(f"📝 初始筆記數量: {len(initial_notes)}")
    
    # 獲取可用的資料夾列表
    available_folders = []
    for root, dirs, files in os.walk(vault_path):
        rel_root = os.path.relpath(root, vault_path)
        if rel_root != '.' and not rel_root.startswith('.'):
            available_folders.append(rel_root)
    
    print("\n可用資料夾列表:")
    for i, folder in enumerate(available_folders):
        print(f"{i+1}. {folder}")
    print("0. 根目錄 (不移動)")
    print("-1. 創建新資料夾 (使用筆記名稱)")
    
    # 直接讓用戶選擇預設資料夾
    while True:
        folder_choice = input(f"請選擇預設資料夾 (-1, 0, 1-{len(available_folders)}): ").strip()
        
        if folder_choice.isdigit() and 1 <= int(folder_choice) <= len(available_folders):
            # 選擇現有資料夾
            selected_folder = available_folders[int(folder_choice) - 1]
            print(f"✅ 已預選資料夾: {selected_folder}")
            break
        elif folder_choice == "0":
            # 根目錄
            selected_folder = None
            print("✅ 已預選資料夾: 根目錄")
            break
        elif folder_choice == "-1":
            # 創建新資料夾
            selected_folder = "CREATE_NEW"
            print("✅ 已預選選項: 創建新資料夾")
            break
        else:
            print(f"❌ 無效選擇，請輸入 -1, 0 或 1-{len(available_folders)} 之間的數字")
    
    try:
        while True:
            # 重新載入環境變數
            load_dotenv(override=True)
            vault_path = os.getenv("VAULT_PATH")
            
            # 獲取當前筆記列表
            current_notes = set(get_existing_notes())
            
            # 檢查是否有新筆記
            new_notes = current_notes - initial_notes
            if new_notes:
                print(f"🔎 檢測到 {len(new_notes)} 個新筆記: {', '.join(new_notes)}")
            
            # 檢查是否有新的空白筆記（用戶點擊了未解析連結）
            new_empty_notes = []
            
            for note in new_notes:
                # 檢查筆記是否為空或僅包含標題
                note_path = os.path.join(vault_path, f"{note}.md")
                
                if os.path.exists(note_path):
                    with open(note_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    print(f"📄 檢查筆記 '{note}' 內容: {len(content)} 字符")
                    
                    # 如果筆記為空或僅包含標題，則視為新點擊的未解析連結
                    if not content or (content.startswith('# ') and len(content.split('\n')) <= 3):
                        print(f"✅ 筆記 '{note}' 是空白筆記或僅包含標題")
                        new_empty_notes.append(note)
                    else:
                        print(f"❌ 筆記 '{note}' 不是空白筆記")
            
            # 為新的空白筆記生成內容
            for note in new_empty_notes:
                print(f"🔄 檢測到點擊未解析連結: {note}")
                
                # 獲取主題名稱
                if '/' in note:
                    # 如果筆記路徑已包含資料夾，提取主題名稱和資料夾
                    folder_name = os.path.dirname(note)
                    topic_name = os.path.basename(note)
                    print(f"📂 筆記已在資料夾中: {folder_name}")
                else:
                    # 如果筆記在根目錄，則使用預選資料夾
                    topic_name = note
                    
                    # 使用預選資料夾
                    if selected_folder == "CREATE_NEW":
                        # 創建新資料夾
                        folder_name = topic_name
                        print(f"📂 將為筆記創建新資料夾: {folder_name}")
                    elif selected_folder is not None:
                        # 使用預選資料夾
                        folder_name = selected_folder
                        print(f"📂 使用預選資料夾: {folder_name}")
                    else:
                        # 根目錄
                        folder_name = None
                        print("📂 筆記將保留在根目錄")
                
                # 預設使用 Bottom-Up 學習方法（選項 2）
                learning_approach = "2"
                
                # 創建筆記，直接在指定資料夾中創建
                note_path = create_note(topic_name, folder_name, learning_approach=learning_approach)
                print(f"✅ 已為 '{note}' 生成內容")
                
                # 如果原始筆記在根目錄，且已在其他資料夾創建了新筆記，則刪除根目錄的原始筆記
                if folder_name and '/' not in note:
                    old_path = os.path.join(vault_path, f"{topic_name}.md")
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                            print(f"✅ 已刪除根目錄中的原始空白筆記: {old_path}")
                        except Exception as e:
                            print(f"⚠️ 無法刪除根目錄中的原始筆記: {str(e)}")
            
            # 更新初始筆記列表
            if new_empty_notes:
                initial_notes = set(get_existing_notes())
            
            # 暫停一段時間再檢查
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n🛑 已停止監控未解析連結")

if __name__ == "__main__":
    main()