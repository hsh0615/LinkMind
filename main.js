const { Plugin } = require('obsidian');

/**
 * Unresolved Link Handler Plugin for Obsidian
 * 
 * This plugin monitors clicks on unresolved links (gray nodes) in Obsidian
 * and creates empty notes that can be populated by an external AI system.
 * 
 * @class UnresolvedLinkHandler
 * @extends {Plugin}
 */
class UnresolvedLinkHandler extends Plugin {
    /**
     * When the plugin is loaded
     * @async
     */
    async onload() {
        console.log('Loading Unresolved Link Handler plugin');
        
        // Register settings tab
        this.addSettingTab(new UnresolvedLinkHandlerSettingTab(this.app, this));
        
        // Register event listener for unresolved links in notes
        this.registerDomEvent(document, 'click', (evt) => {
            const target = evt.target;
            
            // Check if clicked element is an unresolved link
            if (target && target.classList && 
                target.classList.contains('internal-link') && 
                target.classList.contains('is-unresolved')) {
                
                const linkText = target.textContent;
                if (linkText) {
                    console.log(`Clicked on unresolved link: ${linkText}`);
                    this.createEmptyNote(linkText);
                }
            }
        });
        
        // Register event listener for graph view nodes
        this.registerDomEvent(document, 'click', (evt) => {
            const target = evt.target;
            
            // Check if clicked element is a graph node
            if (target && target.tagName === 'circle' && target.closest('svg.graph-view-container')) {
                // Check if it's a gray node (unresolved link)
                const isGrayNode = target.getAttribute('fill') === '#5a5a5a' || 
                                  target.getAttribute('fill') === '#808080' ||
                                  target.getAttribute('fill') === 'gray' ||
                                  target.getAttribute('fill') === '#666666';
                
                if (isGrayNode) {
                    // Try to get the node title
                    const titleElement = target.parentElement.querySelector('text.graph-view-node-label');
                    if (titleElement) {
                        const nodeName = titleElement.textContent;
                        console.log(`Clicked on gray node in graph view: ${nodeName}`);
                        this.createEmptyNote(nodeName);
                    }
                }
            }
        });
        
        // Add status bar item
        this.statusBarItem = this.addStatusBarItem();
        this.statusBarItem.setText('🔗 Link Handler Ready');
    }
    
    /**
     * Creates an empty note with the given name
     * @param {string} noteName - The name of the note to create
     * @async
     */
    async createEmptyNote(noteName) {
        try {
            // Always create notes in the root directory
            let notePath = noteName;
            console.log(`Creating note in root directory: ${noteName}`);
            
            // Check if note already exists
            const exists = await this.app.vault.adapter.exists(`${notePath}.md`);
            if (exists) {
                console.log(`Note already exists: ${notePath}`);
                const existingFile = this.app.vault.getAbstractFileByPath(`${notePath}.md`);
                if (existingFile) {
                    const leaf = this.app.workspace.getLeaf(false);
                    await leaf.openFile(existingFile);
                }
                return;
            }
            
            // Create empty note with just a title
            const file = await this.app.vault.create(`${notePath}.md`, `# ${noteName}\n`);
            console.log(`Successfully created empty note: ${notePath}`);
            
            // Update status bar
            this.statusBarItem.setText(`🔗 Created: ${noteName}`);
            setTimeout(() => {
                this.statusBarItem.setText('🔗 Link Handler Ready');
            }, 3000);
            
            // Open the newly created note
            const leaf = this.app.workspace.getLeaf(false);
            await leaf.openFile(file);
        } catch (error) {
            console.error(`Failed to create note: ${error}`);
            this.statusBarItem.setText('❌ Error creating note');
            setTimeout(() => {
                this.statusBarItem.setText('🔗 Link Handler Ready');
            }, 3000);
        }
    }

    /**
     * When the plugin is unloaded
     */
    onunload() {
        console.log('Unloading Unresolved Link Handler plugin');
    }
}

/**
 * Settings tab for the Unresolved Link Handler plugin
 * @class UnresolvedLinkHandlerSettingTab
 * @extends {SettingTab}
 */
class UnresolvedLinkHandlerSettingTab {
    constructor(app, plugin) {
        this.app = app;
        this.plugin = plugin;
    }

    display() {
        const {containerEl} = this;
        containerEl.empty();

        containerEl.createEl('h2', {text: 'Unresolved Link Handler Settings'});
        
        containerEl.createEl('p', {
            text: 'This plugin creates empty notes when you click on unresolved links or gray nodes in the graph view.'
        });
        
        containerEl.createEl('p', {
            text: 'To use with AI content generation, run the Python script from the companion repository.'
        });
        
        containerEl.createEl('a', {
            text: 'View Documentation',
            href: 'https://github.com/hsh0615/obsidian-unresolved-link-handler'
        });
    }
}

module.exports = UnresolvedLinkHandler; 