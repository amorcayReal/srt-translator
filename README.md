# 🎬 SRT Translator - Modern Interface

An advanced and modern tool to translate your SRT subtitle files with **Ollama**, featuring an intuitive web interface and professional capabilities.

## ✨ Features

### 🌐 Modern Web Interface (Streamlit)
- **Clean and responsive** graphical interface
- **Multilingual support** (French/English) with instant switching
- **Intuitive drag & drop** for files
- **Real-time progress** with line-by-line details
- **Cancellation function** at any time
- **File preview** before and after translation

### 📦 Processing Modes
- **📄 Single file** : Translation of one SRT file
- **🔄 Batch processing** : Translation of multiple files simultaneously
- **📥 ZIP download** : Automatic archive for batch processing

### 🎯 Advanced Features
- **Detailed progress** : `"5/342 : <text being translated>"`
- **Robust error handling** with explicit messages
- **Multiple encoding support** (UTF-8, CP1252, Latin-1)
- **Timing and numbering preservation** in SRT format
- **Smart naming convention** : `filename-FR.srt`

## 🚀 Installation

### Prerequisites
- **Python 3.9+**
- **Ollama** installed and running
- **gemma3:12b** model (or another model of your choice)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Ollama Configuration
```bash
# Start Ollama
ollama serve

# Check/install model
ollama list
ollama pull gemma3:12b  # If needed
```

## 🎮 Usage

### 🌟 Web Interface (Recommended)

#### Quick Start
```bash
# Windows
run_streamlit.bat

# Command line
python -m streamlit run streamlit_app.py
```

#### Web Interface Workflow
1. **🌐 Choose interface language** (FR/EN)
2. **⚙️ Configure Ollama** in the sidebar
3. **📂 Select mode** : Single file or Batch
4. **📁 Upload** your SRT files
5. **🌍 Define** source/target languages
6. **🚀 Start** translation
7. **📥 Download** the result

### 📋 Command Line Interface

#### Single file
```bash
python srt_translator.py input.srt output.srt --source english --target french
```

#### With advanced options
```bash
python srt_translator.py movie.srt movie_fr.srt \
  --source english \
  --target french \
  --url http://localhost:11434
```

## 🎯 Usage Examples

### Web Interface - Batch Mode
1. Select **"Batch processing"**
2. Upload multiple files: `episode01.srt`, `episode02.srt`, `episode03.srt`
3. Choose: **English** → **French**
4. Click **"Start translation"**
5. Download: `subtitles-FR.zip` containing:
   - `episode01-FR.srt`
   - `episode02-FR.srt` 
   - `episode03-FR.srt`

### Web Interface - Detailed Progress
```
🔄 Batch processing (1/3): episode01.srt
127/342 : Hello, how are you doing today?
[████████████░░░░░░░░░] 45%   [🛑 Cancel]
```

### Command Line - Examples
```bash
# English to French
python srt_translator.py movie_en.srt movie_fr.srt

# French to Spanish  
python srt_translator.py movie_fr.srt movie_es.srt -s french -t spanish

# With custom Ollama URL
python srt_translator.py series.srt series_de.srt --url http://192.168.1.100:11434
```

## ⚙️ Configuration

### Supported Languages
- **french**, **english**, **spanish**, **italian**, **german**
- **portuguese**, **chinese**, **japanese**, **korean**, **russian**

### Recommended Ollama Models
- `gemma3:12b` (default, accurate)
- `gemma3:2b` (faster)
- `llama3.2` (alternative)
- `qwen2.5` (advanced multilingual)

### File Structure
```
srt-translator/
├── streamlit_app.py          # Modern web interface
├── srt_translator.py         # Translation module
├── run_streamlit.bat         # Windows launcher
├── translate.bat             # Command line launcher
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Advanced Options

### Interface Variables
- **Processing mode** : Single or Batch
- **Interface language** : French/English
- **Ollama URL** : Configurable in interface
- **Model** : Dynamically selectable

### Command Line Parameters
```bash
python srt_translator.py [INPUT_FILE] [OUTPUT_FILE] [OPTIONS]

Options:
  --source, -s    Source language (default: english)
  --target, -t    Target language (default: french)  
  --url          Ollama URL (default: http://localhost:11434)
```

## 🚨 Troubleshooting

### Web Interface
**Port already in use:**
```bash
python -m streamlit run streamlit_app.py --server.port 8502
```

**Ollama not accessible:**
- Test connection via button in interface
- Check that Ollama is started: `ollama serve`

### Command Line
**Model error:**
```bash
ollama pull gemma3:12b
```

**Encoding issue:**
- Tool automatically tries multiple encodings
- Convert to UTF-8 if necessary

### Performance
- **gemma3:12b** : Accurate but slower
- **gemma3:2b** : Faster for testing
- Use **smaller files** for testing

## 📈 Technical Features

### Streamlit Interface
- **Real-time progress callbacks**
- **State management** with `session_state`
- **Multiple upload** with validation
- **Automatic ZIP download**
- **Custom CSS** for design

### Intelligent Processing
- **Robust SRT parser** with regex
- **Granular error handling** per file
- **Automatic cleanup** of temporary files
- **Standardized naming convention**

### Modular Architecture
- **Separation of concerns** : UI / Logic
- **Callbacks** for progress/cancellation
- **Cross-platform support** Windows/Linux/Mac
- **Complete internationalization**

## 🤝 Contributing

This project is designed to be easily extensible:
- Add languages in `TRANSLATIONS`
- Integrate other Ollama models
- Customize CSS interface
- Extend subtitle formats

## 📄 License

Open source project - Use and modify freely!

---

**🎬 Enjoy your translated subtitles with style!** 