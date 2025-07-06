# LLM Agent

AI coding assistant built with Google Gemini 2.0 that can explore codebases, read files, write code, and execute Python scripts through function calling.

## Features

- **File Operations**: List directories, read/write files
- **Python Execution**: Run scripts with arguments
- **Multi-turn Conversations**: Maintains context across function calls
- **Sandboxed Environment**: Secure execution within working directory

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Add your Gemini API key to `.env`:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Basic usage:
```bash
uv run main.py "your prompt here"
```

With verbose output:
```bash
uv run main.py "your prompt here" --verbose
```

## Examples

```bash
# Analyze code
uv run main.py "explain how the calculator works"

# Run tests
uv run main.py "run tests.py and show results"

# File operations
uv run main.py "create a hello world script"

# Explore codebase
uv run main.py "list all files and show me the main entry point"
```

## Available Functions

- `get_files_info` - List directory contents
- `get_files_content` - Read file contents  
- `write_file` - Create/overwrite files
- `run_python` - Execute Python scripts

## How It Works

1. User provides natural language prompt
2. LLM plans and executes function calls
3. Results are added to conversation context
4. Process repeats until task is complete
5. Final comprehensive response provided

## Security

- All operations constrained to `./calculator` directory
- 30-second timeout on script execution
- Path validation prevents directory traversal


Done alongisde help from courses made by the the www.bootdev.com team!
