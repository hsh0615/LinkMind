/**
 * Obsidian 未解析連結處理器 - 簡化版
 */

class UnresolvedLinkHandler {
    constructor() {
        this.app = window.app;
    }

    async onload() {
        console.log('載入未解析連結處理器插件');
        
        // 簡單的事件監聽器
        document.addEventListener('click', (event) => {
            const target = event.target;
            
            // 檢查是否點擊了未解析連結
            if (target.classList && target.classList.contains('internal-link') && target.classList.contains('is-unresolved')) {
                const linkText = target.textContent;
                if (linkText) {
                    console.log(`點擊了未解析連結: ${linkText}`);
                    this.createEmptyNote(linkText);
                }
            }
        });
    }

    async createEmptyNote(noteName) {
        try {
            // 使用 Obsidian API 創建空白筆記
            const file = await this.app.vault.create(`${noteName}.md`, `# ${noteName}\n`);
            console.log(`已創建空白筆記: ${noteName}`);
            
            // 打開新創建的筆記
            await this.app.workspace.getLeaf().openFile(file);
        } catch (error) {
            console.error(`創建筆記失敗: ${error}`);
        }
    }

    onunload() {
        console.log('卸載未解析連結處理器插件');
    }
}

module.exports = UnresolvedLinkHandler; 