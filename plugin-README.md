# Obsidian Unresolved Link Handler

This plugin automatically handles clicks on unresolved links in Obsidian, creating notes and integrating with an external AI content generation system.

## Features

- 🔗 Monitors clicks on unresolved links in notes
- 📊 Detects clicks on gray nodes in the graph view
- 📝 Creates empty notes when unresolved links are clicked
- 🤖 Integrates with a Python-based AI system for automatic content generation

## How to Use

### Basic Usage

1. Install and enable the plugin
2. Click on any unresolved link (appears as gray text) in your notes
3. The plugin will create an empty note with the same name
4. Start writing in the newly created note

### AI Content Generation

For automatic content generation:

1. Set up the companion Python script (see below)
2. Run the Python script in monitoring mode
3. Click on unresolved links in Obsidian
4. The Python script will detect the new empty notes and automatically generate content

## Companion Python Script

This plugin works best with the companion Python script that provides AI-powered content generation:

1. Clone the [Obsidian Knowledge Assistant repository](https://github.com/hsh0615/obsidian-knowledge-assistant)
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure your `.env` file with your Obsidian vault path and API keys
4. Run the script: `python main.py`
5. Select option 2 to monitor unresolved links

## Configuration

The plugin has minimal configuration. Simply install and enable it to start using.

Future versions may include additional configuration options.

## Troubleshooting

- If notes are not being created, check that the plugin is enabled
- If AI content is not being generated, ensure the Python script is running in monitoring mode
- For issues with the Python script, check the console output for error messages

## Support

For support, feature requests, or bug reports:

- Open an issue on [GitHub](https://github.com/hsh0615/obsidian-unresolved-link-handler/issues)
- Contact the developer via [GitHub](https://github.com/hsh0615)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  <a href="https://github.com/sponsors/hsh0615">GitHub Sponsors</a> •
  <a href="https://www.buymeacoffee.com/hsh0615">Buy Me a Coffee</a>
</p> 