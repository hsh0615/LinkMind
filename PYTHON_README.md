# LinkMind Python Backend

This is the Python backend for the LinkMind Obsidian plugin. It monitors your Obsidian vault for new empty notes created by clicking on unresolved links and automatically generates content using AI.

## Installation

1. Make sure you have Python 3.8 or higher installed.
2. Clone this repository:
   ```
   git clone https://github.com/hsh0615/LinkMind.git
   cd LinkMind
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Or use the setup.py:
   ```
   pip install -e .
   ```

## Configuration

1. Create a `.env` file in the root directory with the following variables:
   ```
   VAULT_PATH=/path/to/your/obsidian/vault
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   DEFAULT_MODEL=gpt-4-turbo
   ```

2. Replace the values with your own:
   - `VAULT_PATH`: The absolute path to your Obsidian vault
   - `OPENAI_API_KEY`: Your OpenAI API key (get one at https://platform.openai.com/)
   - `ANTHROPIC_API_KEY`: Your Anthropic API key (optional)
   - `DEFAULT_MODEL`: The default AI model to use (e.g., gpt-4-turbo, claude-3-opus-20240229)

## Usage

1. Run the Python script:
   ```
   python main.py
   ```

2. Select option 2 to monitor unresolved links.

3. Choose a folder where new notes will be created.

4. In Obsidian, click on any unresolved link (gray text) or gray node in the graph view.

5. The Python script will detect the new empty note and automatically generate content using AI.

## How It Works

1. The Obsidian plugin creates an empty note when you click on an unresolved link.
2. The Python script monitors your vault for new empty notes.
3. When a new empty note is detected, the script generates content using AI.
4. The generated content is saved to the note, creating a complete, well-structured note.
5. The script also creates bidirectional links between related notes and can generate index pages for folders.

## Files

- `main.py`: The main script that handles the monitoring and coordination
- `content_generator.py`: Handles the AI content generation
- `relation_manager.py`: Manages the relationships between notes
- `obsidian_writer.py`: Handles writing to Obsidian notes
- `utils.py`: Utility functions

## Troubleshooting

- **API Key Issues**: Make sure your API keys are correctly set in the `.env` file.
- **Path Issues**: Ensure the `VAULT_PATH` in your `.env` file is the absolute path to your Obsidian vault.
- **Empty Notes Not Detected**: Make sure the Python script is running while you're clicking on unresolved links in Obsidian.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 