# LinkMind - Obsidian Unresolved Link Handler

![GitHub release (latest by date)](https://img.shields.io/github/v/release/hsh0615/LinkMind)
![GitHub all releases](https://img.shields.io/github/downloads/hsh0615/LinkMind/total)
![GitHub](https://img.shields.io/github/license/hsh0615/LinkMind)

An [Obsidian](https://obsidian.md) plugin that handles clicks on unresolved links (gray nodes) and integrates with an external AI system to automatically generate content.

## Features

- 🔗 Monitors clicks on unresolved links in notes
- 📊 Detects clicks on gray nodes in the graph view
- 📝 Creates empty notes when unresolved links are clicked
- 🤖 Integrates with a Python-based AI system for automatic content generation
- 🔄 Supports both manual and automated workflows

## Demo

![Demo GIF](https://raw.githubusercontent.com/hsh0615/LinkMind/main/assets/demo.gif)

## Installation

### From Obsidian Community Plugins

1. Open Obsidian Settings
2. Go to Community Plugins and disable Safe Mode
3. Click Browse and search for "LinkMind"
4. Install the plugin and enable it

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/hsh0615/LinkMind/releases)
2. Extract the ZIP file to your Obsidian plugins folder: `.obsidian/plugins/`
3. Reload Obsidian
4. Enable the plugin in the Community Plugins settings

## Usage

### Basic Usage

1. Open your Obsidian vault
2. Click on any unresolved link (appears as gray text) in your notes
3. The plugin will create an empty note with the same name
4. Start writing in the newly created note

### Integration with AI Content Generation

For automatic content generation, this plugin works with a companion Python script:

1. Install the Python script from this repository
2. Configure the script with your Obsidian vault path and API keys
3. Run the Python script in monitoring mode
4. Click on unresolved links in Obsidian
5. The Python script will detect the new empty notes and automatically generate content

## Configuration

The plugin has a simple settings page where you can:

- View documentation
- Access links to the companion Python repository
- Configure additional options (in future versions)

## How It Works

1. The plugin listens for click events on unresolved links and gray nodes in the graph view
2. When a click is detected, it creates an empty note with just a title
3. If the companion Python script is running, it monitors the vault for new empty notes
4. When a new empty note is detected, the Python script generates content using AI
5. The generated content is saved to the note, creating a complete, well-structured note

## Python Backend

The full power of this plugin comes from its Python backend, which:

- Monitors your vault for new empty notes
- Uses AI to generate detailed, structured content
- Creates bidirectional links between related notes
- Generates index pages for folders
- Supports different learning approaches

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Obsidian](https://obsidian.md) for creating an amazing knowledge management tool
- All contributors and users who provide feedback and suggestions

---

<p align="center">
  <a href="https://github.com/sponsors/hsh0615">GitHub Sponsors</a> •
  <a href="https://www.buymeacoffee.com/hsh0615">Buy Me a Coffee</a>
</p>
