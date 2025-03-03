# LinkMind - Obsidian 智能筆記助手

![GitHub release (latest by date)](https://img.shields.io/github/v/release/hsh0615/LinkMind)
![GitHub all releases](https://img.shields.io/github/downloads/hsh0615/LinkMind/total)
![GitHub](https://img.shields.io/github/license/hsh0615/LinkMind)

一個 [Obsidian](https://obsidian.md) 插件，用於處理未解析連結（灰色節點）的點擊，並自動生成內容。現在完全在 Obsidian 內運行，無需外部 Python 後端！

## 新版本亮點 (v1.1.0)

- 🎉 **完全整合**：現在所有功能都整合在 Obsidian 內部，無需外部 Python 腳本
- 🖥️ **專用操作面板**：引入全新的專用操作界面，一站式管理所有功能
- 🔍 **未解析連結掃描**：一鍵掃描並管理所有未解析連結
- 📚 **自動索引生成**：為資料夾自動生成索引頁面
- 🧠 **相關概念探索**：發現並連接相關概念，加強知識網絡
- 📝 **內容豐富工具**：一鍵豐富現有筆記內容

## 功能

- 🔗 監控筆記中的未解析連結點擊
- 📊 檢測圖形視圖中灰色節點的點擊
- 📝 點擊未解析連結時創建空白筆記
- 🤖 使用 AI 自動生成內容（現在直接在 Obsidian 內完成！）
- 🔄 支持手動和自動化工作流程
- 📂 自動組織筆記到資料夾
- 🔍 掃描並批量管理未解析連結
- 📚 生成資料夾索引頁面

## 演示

![Demo GIF](https://raw.githubusercontent.com/hsh0615/LinkMind/main/assets/demo.gif)

## 安裝

### 從 Obsidian 社區插件

1. 打開 Obsidian 設置
2. 前往社區插件並禁用安全模式
3. 點擊瀏覽並搜索 "LinkMind"
4. 安裝插件並啟用它

### 手動安裝

1. 從 [releases 頁面](https://github.com/hsh0615/LinkMind/releases) 下載最新版本
2. 解壓縮到您的 Obsidian 插件文件夾：`.obsidian/plugins/`
3. 重新加載 Obsidian
4. 在社區插件設置中啟用插件

## 使用方法

### 操作面板

1. 點擊左側欄的大腦圖標或使用命令 `打開 LinkMind 操作面板`
2. 在操作面板中訪問所有功能：
   - 創建新筆記
   - 生成筆記內容
   - 豐富現有內容
   - 查找相關概念
   - 管理未解析連結
   - 生成資料夾索引

### 基本使用

1. 打開您的 Obsidian 知識庫
2. 點擊筆記中的任何未解析連結（顯示為灰色文本）
3. 插件將創建相同名稱的空白筆記
4. 如果啟用了自動生成內容功能，將自動使用 AI 生成內容

### AI 內容生成

現在 AI 內容生成完全在 Obsidian 內部完成！

1. 在設置中配置您的 OpenAI API 密鑰
2. 選擇您喜歡的 AI 模型（如 GPT-4 Turbo 或 GPT-3.5 Turbo）
3. 啟用自動生成內容選項（可選）
4. 點擊未解析連結或使用操作面板中的按鈕生成內容

## 配置

插件有一個設置頁面，您可以在其中：

- 配置 OpenAI API 密鑰
- 選擇 AI 模型
- 設置默認筆記資料夾
- 啟用/禁用自動生成內容
- 訪問文檔和更多選項

## 工作原理

1. 插件監聽未解析連結和圖形視圖中灰色節點的點擊事件
2. 當檢測到點擊時，它會創建一個空白筆記，僅包含標題
3. 如果啟用了自動生成內容，插件會調用 OpenAI API 生成詳細內容
4. 生成的內容保存到筆記中，創建一個完整、結構良好的筆記
5. 您可以使用操作面板進一步豐富內容、添加相關概念或管理筆記

## 貢獻

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 存儲庫
2. 創建您的功能分支：`git checkout -b feature/amazing-feature`
3. 提交您的更改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 打開一個 Pull Request

## 許可證

本項目使用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 文件。

## 致謝

- [Obsidian](https://obsidian.md) 創建了一個出色的知識管理工具
- OpenAI 提供了強大的 AI 模型
- 所有提供反饋和建議的貢獻者和用戶

---

<p align="center">
  <a href="https://github.com/sponsors/hsh0615">GitHub 贊助</a> •
  <a href="https://www.buymeacoffee.com/hsh0615">請我喝杯咖啡</a>
</p>
