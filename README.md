<div align="center">

[![Stars](https://img.shields.io/github/stars/instavm/clickclickclick?color=yellow&style=flat&label=%E2%AD%90%20stars)](https://github.com/instavm/clickclickclick/stargazers)
[![License](http://img.shields.io/:license-MIT-green.svg?style=flat)](https://github.com/instavm/clickclickclick/blob/master/LICENSE)

</div>

# ClickClickClick

**A robust framework enabling autonomous Android and computer control using any LLM (local or remote)**

![click3](https://github.com/user-attachments/assets/493a6d39-c9d1-4e7c-b413-7f01140bbadb)

## 🚀 Features

- **Multi-platform support**: Android devices and macOS computers
- **Multiple LLM providers**: OpenAI, Anthropic Claude, Google Gemini, and local Ollama models
- **Flexible interfaces**: CLI, API, and web-based Gradio interface
- **Visual automation**: Screenshot-based element detection and interaction
- **Configurable execution**: Customizable timeouts, delays, and coordinate settings

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Web Interface (Gradio)](#web-interface-gradio)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
  - [REST API](#rest-api)
- [Configuration](#-configuration)
- [Model Recommendations](#-model-recommendations)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Quick Start

1. **Install the package**:
   ```bash
   pip install git+https://github.com/instavm/clickclickclick.git
   ```

2. **Set up API keys** (choose one):
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   # OR
   export ANTHROPIC_API_KEY="your-anthropic-key"
   # OR
   export GEMINI_API_KEY="your-gemini-key"
   ```

3. **Run a simple task**:
   ```bash
   click3 run "open Gmail and check for new messages"
   ```

## 📋 Prerequisites

### For Android Control
- **ADB (Android Debug Bridge)**: Install Android SDK Platform Tools
- **USB Debugging**: Enable on your Android device
- **USB Connection**: Connect device to computer

### For macOS Control
- **Python 3.11+**: Required for all functionality
- **Accessibility Permissions**: Grant to Terminal/IDE when prompted

### System Requirements
- Python 3.11 or higher
- 4GB+ RAM recommended
- Internet connection for cloud LLM providers

## 📦 Installation

### Option 1: Direct Installation
```bash
pip install git+https://github.com/instavm/clickclickclick.git
```

### Option 2: Development Installation
```bash
git clone https://github.com/instavm/clickclickclick
cd clickclickclick
pip install -e .
```

### Verify Installation
```bash
click3 --help
```

## 🎮 Usage

### Web Interface (Gradio)

Launch the interactive web interface:
```bash
click3 gradio
```

Features:
- Visual task input and monitoring
- Real-time screenshot feedback
- Model selection and configuration
- Task history and logs

![Gradio interface](https://github.com/user-attachments/assets/1205eb1a-b334-4238-83a3-35d3fa18d8fe)

### Command Line Interface

**Basic Usage:**
```bash
click3 run "your task description"
```

**Advanced Options:**
```bash
click3 run "open calculator and compute 25 * 47" \
  --platform=android \
  --planner-model=openai \
  --finder-model=gemini
```

**Available Options:**
- `--platform`: Target platform (`android` or `osx`)
- `--planner-model`: Planning LLM (`openai`, `anthropic`, `gemini`, `ollama`)
- `--finder-model`: Element detection LLM (`openai`, `anthropic`, `gemini`, `ollama`)

### Python API

```python
from clickclickclick.config import get_config
from clickclickclick.planner.task import execute_task
from clickclickclick.utils import get_executor, get_planner, get_finder

# Configure execution
config = get_config("android", "openai", "gemini")
executor = get_executor("android")
planner = get_planner("openai", config, executor)
finder = get_finder("gemini", config, executor)

# Execute task
success = execute_task(
    "open the weather app",
    executor, planner, finder, config
)
```

### REST API

**Start the API server:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

**Execute tasks via HTTP:**
```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "task_prompt": "open calculator",
    "platform": "android",
    "planner_model": "openai",
    "finder_model": "gemini"
  }'
```

**Response:**
```json
{"result": true}
```

## ⚙️ Configuration

Configuration is managed through `config/models.yaml`. Key settings include:

### Model Configuration
```yaml
openai:
  api_key: !ENV OPENAI_API_KEY
  model_name: gpt-4o-mini
  image_width: 512
  image_height: 512

gemini:
  api_key: !ENV GEMINI_API_KEY
  model_name: gemini-1.5-flash
  image_width: 768
  image_height: 768
```

### Executor Configuration
```yaml
executor:
  android:
    screen_center_x: 500
    screen_center_y: 1000
    scroll_distance: 1000
    swipe_distance: 600
    long_press_duration: 1000
```

### Environment Variables
Required API keys (set one or more):
- `OPENAI_API_KEY`: OpenAI GPT models
- `ANTHROPIC_API_KEY`: Anthropic Claude models
- `GEMINI_API_KEY`: Google Gemini models
- `OLLAMA_MODEL_NAME`: Local Ollama model name

## 🎯 Model Recommendations

Based on performance testing:

| Use Case | Recommended Setup | Performance |
|----------|------------------|-------------|
| **Best Overall** | Planner: GPT-4o, Finder: Gemini Flash | ⭐⭐⭐⭐⭐ |
| **Cost Effective** | Planner: GPT-4o-mini, Finder: Gemini Flash | ⭐⭐⭐⭐ |
| **Privacy Focused** | Planner: Ollama, Finder: Ollama | ⭐⭐⭐ |
| **Speed Optimized** | Planner: Gemini Flash, Finder: Gemini Flash | ⭐⭐⭐⭐ |

![model recommendations](https://github.com/user-attachments/assets/460e9f52-749c-4f2a-997a-57cb04879420)

**Notes:**
- Gemini Flash offers 15 free API calls daily
- GPT-4o provides the most reliable planning
- Ollama enables fully offline operation
- Anthropic Claude offers balanced performance

## 📱 Examples

### Android Examples

**Gmail Task:**
```bash
click3 run "create a draft email to someone@gmail.com asking about lunch plans for Saturday at 1PM"
```

**Navigation:**
```bash
click3 run "open Google Maps and find bus stops in Alanson, MI"
```

**Gaming:**
```bash
click3 run "start a 3+2 chess game on lichess"
```

### macOS Examples

**Web Browsing:**
```bash
click3 run "open Safari, go to news.ycombinator.com and read the top story" --platform=osx
```

**System Tasks:**
```bash
click3 run "open System Preferences and check the current display resolution" --platform=osx
```

## 🔧 Troubleshooting

### Common Issues

**ADB Connection Problems:**
```bash
# Check device connection
adb devices

# Restart ADB server
adb kill-server
adb start-server
```

**API Key Issues:**
```bash
# Verify environment variables
echo $OPENAI_API_KEY
echo $GEMINI_API_KEY

# Set keys temporarily
export OPENAI_API_KEY="your-key-here"
```

**Permission Errors (macOS):**
- Grant Accessibility permissions in System Preferences > Security & Privacy
- Allow Terminal or your IDE to control other applications

**Model-Specific Issues:**
- **Ollama**: Ensure the model is downloaded (`ollama pull llama3.2-vision`)
- **Gemini**: Check API quota at [Google AI Studio](https://aistudio.google.com/apikey)
- **OpenAI**: Verify billing and usage limits

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

- Reduce image resolution in `config/models.yaml`
- Increase `TASK_DELAY` for slower devices
- Use smaller models for faster response times

## 🤝 Contributing

We welcome contributions! Please:

1. **Open an issue** to discuss your idea
2. **Fork the repository**
3. **Create a feature branch**
4. **Make your changes** with tests
5. **Submit a pull request**

### Development Setup
```bash
git clone https://github.com/instavm/clickclickclick
cd clickclickclick
pip install -e ".[test]"
pytest
```

## 📈 Roadmap

- [ ] iOS support via WebDriverAgent
- [ ] Windows support with Win32 APIs
- [ ] Voice command integration
- [ ] Multi-device orchestration
- [ ] Enhanced error recovery
- [ ] Plugin system for custom actions

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the examples and configuration sections
- 🐛 **Bug Reports**: [Create an issue](https://github.com/instavm/clickclickclick/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/instavm/clickclickclick/discussions)
- ⭐ **Star the repo** if you find it useful!

---

<div align="center">
Made with ❤️ by InstaVM | Follow us for updates!
</div>
