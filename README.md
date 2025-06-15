# AI HTML Generator

A Streamlit web application that generates HTML code from natural language descriptions using multiple AI approaches.

## Features

- 🎨 Generate HTML web apps from simple English descriptions
- 🤖 Multiple AI generation methods:
  - **Lightweight AI models** (DialoGPT Small, DistilGPT2) - Optimized for Streamlit
  - OpenAI GPT models (if API key provided)
  - Smart template-based generation (always available)
  - Hybrid AI+Template enhancement for best results
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

For enhanced AI generation with lightweight models:

```bash
pip install transformers torch
```

For OpenAI API support, set your API key:
```bash
set OPENAI_API_KEY=your_api_key_here
```

**Note**: Lightweight models (DialoGPT Small, DistilGPT2) are optimized for Streamlit and require minimal resources (~500MB disk space, ~2GB RAM).

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

The app uses a multi-tier approach optimized for Streamlit:

1. **Lightweight AI models** (if installed) - DialoGPT Small/DistilGPT2 for fast generation
2. **OpenAI API** (if configured) - High-quality AI generation
3. **Hybrid AI+Template** - Combines AI creativity with template reliability
4. **Smart templates** (always available) - Instant, professional results

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
