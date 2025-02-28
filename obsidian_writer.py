import requests
import os
import urllib.parse

def save_to_obsidian(filepath, content, mode="overwrite"):
    vault_path = os.getenv("VAULT_PATH")

    # 這裡只取「Vault內相對路徑」，然後做URL編碼
    relative_path = os.path.relpath(filepath, vault_path)
    encoded_path = urllib.parse.quote(relative_path)

    # 確保目標資料夾存在
    ensure_folder_exists(os.path.dirname(filepath))

    url = f"http://localhost:27123/vault/{encoded_path}"
    headers = {
        "Authorization": f"Bearer {os.getenv('OBSIDIAN_API_KEY')}",
        "Content-Type": "text/markdown"
    }

    if mode == "append":
        response = requests.post(url, headers=headers, data=content)
    else:
        response = requests.put(url, headers=headers, data=content)

    if response.status_code not in (204, 200):
        raise RuntimeError(f"❌ 存檔失敗: {response.status_code}\n{response.text}")
    else:
        print(f"✅ 已成功寫入Obsidian: {relative_path}")

def ensure_folder_exists(folder_path):
    """確保資料夾存在，如果不存在則創建"""
    if not os.path.exists(folder_path) and folder_path:
        try:
            os.makedirs(folder_path)
            print(f"✅ 已創建資料夾: {folder_path}")
        except Exception as e:
            print(f"⚠️ 無法創建資料夾 {folder_path}: {str(e)}")