# AI HTML Generator

A Streamlit web application that generates HTML code from natural language descriptions using multiple AI approaches.

## Features

- 🎨 Generate HTML web apps from simple English descriptions
- 🤖 Multiple AI generation methods:
  - **DeepSeek Coder 6.7B** (primary - excellent for code generation)
  - OpenAI GPT models (if API key provided)
  - Lightweight transformer models (fallback)
  - Smart template-based generation (always available)
- 🚀 Live preview of generated HTML
- 📥 Download generated code as HTML files
- ☁️ Ready for Streamlit Cloud deployment

## Quick Start

### Local Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd "Agent ai"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```
Or double-click `run_app.bat` on Windows.

### Optional: Add AI Model Support

For enhanced AI generation with DeepSeek Coder model:

```bash
pip install transformers torch accelerate
```

For OpenAI API support, set your API key:
```bash
set OPENAI_API_KEY=your_api_key_here
```

**Note**: DeepSeek Coder 6.7B provides excellent code generation but requires ~13GB of disk space and 8GB+ RAM.

## Usage

1. Enter a description of the web app you want to create
2. Click "Generate App" to create the HTML code
3. View the live preview and download the generated HTML file

## Example Prompts

- "Create a simple to-do list app with add and delete functionality"
- "Build a calculator with basic arithmetic operations"
- "Make a contact form with name, email, and message fields"

## Deployment Options

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Connect your GitHub repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click
4. Optionally add OpenAI API key in secrets

### Local Network

Run with network access:
```bash
streamlit run app.py --server.address 0.0.0.0
```

## Architecture

The app uses a multi-tier approach:

1. **DeepSeek Coder 6.7B** (if installed) - State-of-the-art code generation
2. **OpenAI API** (if configured) - High-quality AI generation
3. **Local transformer models** (if installed) - Offline AI generation  
4. **Smart templates** (always available) - Reliable fallback with intelligent matching

## Requirements

- Python 3.8+
- Streamlit (required)
- Requests (required)
- Transformers + PyTorch (optional, for local AI models)
- OpenAI API key (optional, for GPT models)

## Troubleshooting

### Installation Issues

If you encounter build errors with transformers/torch:
1. The app will work fine with just the base requirements
2. Templates provide reliable HTML generation
3. Add AI models later if needed

### Model Loading Issues

The app gracefully handles missing dependencies:
- No transformers? Uses template-based generation
- No OpenAI key? Falls back to local generation
- All methods fail? Uses smart fallback templates

## License

MIT License
