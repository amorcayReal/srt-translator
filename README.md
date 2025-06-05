# SRT Translator with Ollama

A simple and efficient tool to translate SRT subtitle files using Ollama and the gemma3:12b model.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running with the gemma3:12b model
3. Internet connection to download Python dependencies

## Installation

1. Clone or download this project
2. Make sure Ollama is running:
   ```bash
   ollama serve
   ```
3. Verify that the gemma3:12b model is available:
   ```bash
   ollama list
   ```
   If not installed, download it:
   ```bash
   ollama pull gemma3:12b
   ```

## Usage

### Simple method (Windows)

Use the provided batch script:

```bash
# Translation from English to French (default)
translate.bat my_file.srt my_file_fr.srt

# Translation with specific languages
translate.bat my_file.srt my_file_es.srt english spanish
```

### Direct Python method

```bash
# Install dependencies
pip install -r requirements.txt

# Basic usage
python srt_translator.py input.srt output.srt

# With options
python srt_translator.py input.srt output.srt --source english --target french
python srt_translator.py input.srt output.srt -s english -t spanish
```

## Available options

- `--source` or `-s`: Source language (default: english)
- `--target` or `-t`: Target language (default: french)  
- `--url`: Ollama URL (default: http://localhost:11434)

## Usage examples

```bash
# English to French
python srt_translator.py movie_en.srt movie_fr.srt

# French to Spanish
python srt_translator.py movie_fr.srt movie_es.srt --source french --target spanish

# English to German
python srt_translator.py series_en.srt series_de.srt -s english -t german
```

## Features

- ✅ Automatically parses SRT files
- ✅ Preserves timing and numbering
- ✅ Handles different encodings (UTF-8, CP1252, Latin-1)
- ✅ Shows translation progress
- ✅ Uses local Ollama (no external API needed)
- ✅ Simple command-line interface

## Troubleshooting

### Ollama is not accessible
- Check that Ollama is running: `ollama serve`
- Verify that port 11434 is not blocked

### Model error
- Make sure gemma3:12b is installed: `ollama pull gemma3:12b`

### Encoding error
- The tool automatically tries multiple encodings
- If the problem persists, convert your SRT file to UTF-8

### Slow performance
- The gemma3:12b model is large, translation may take time
- For a faster version, you can modify the script to use a smaller model like `gemma3:2b` 