# 🚀 QuanTerminal

<div align="center">

![QuanTerminal](https://img.shields.io/badge/QuanTerminal-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen)
![Shell](https://img.shields.io/badge/Shell-Bash%20%7C%20Zsh-orange)
![License](https://img.shields.io/badge/License-MIT-green)
[![Author](https://img.shields.io/badge/Author-Shalom%20Obongo-purple)](https://shalomobongo.tech)

<h3>🤖 Transform Natural Language into Terminal Commands with AI</h3>

[Installation](#installation) •
[Usage](#usage) •
[Documentation](#technical-details) •
[Contributing](#contributing)

---

<p align="center">
  <i>Interact with your terminal in plain English.<br>
  Let AI handle the complex command syntax.</i>
</p>

</div>

## 🌟 Overview

QuanTerminal revolutionizes command-line interaction by bridging the gap between natural human language and terminal commands. Powered by Groq's cutting-edge Llama3.3 70B model, it transforms simple English descriptions into precise terminal commands, with intelligent context awareness of your current environment.

### ✨ Why QuanTerminal?

- 🗣️ **Natural Language First**: Describe what you want in plain English
- 🧠 **Context-Aware**: Automatically adapts to your project environment
- ⚡ **Zero Latency**: Instant command generation
- 🛡️ **Safe by Design**: Built-in command validation
- 🔄 **Interactive**: Edit commands before execution
- 🌐 **Universal**: Works with both Bash and Zsh

## 🎯 Features

### 🔥 Core Capabilities
- 🤖 Natural language to command conversion
- 🖊️ Interactive command editing
- 🌍 Global command availability
- 🛡️ Intelligent safety checks
- ⚡ Zero-latency suggestions

### 🧠 Smart Context Detection
- 📂 **Project Type Recognition**
  - Automatically detects Node.js, Python, Docker, Rust, Go projects
  - Suggests appropriate package managers and tools
  - Adapts commands to project structure

- 🔄 **Git-Aware Commands**
  - Understands repository status
  - Tracks modified, staged, and untracked files
  - Optimizes Git commands based on current state

- 🐚 **Shell Environment Integration**
  - Considers current shell type (Bash/Zsh)
  - Aware of environment variables
  - Respects shell aliases and configurations

### 💫 User Experience
- 🔌 Seamless shell integration
- 📝 Direct command insertion
- 👀 Command preview capability
- 🎨 Shell-specific optimizations

### ⚙️ Technical Features
- 🏰 Isolated Python environment
- 🧠 Context-aware generation
- 🔧 Persistent configuration
- 📊 Comprehensive error handling

## 🚀 Installation

### Prerequisites
- 🐍 Python 3.6+
- 🐚 Bash or Zsh shell
- 🔑 Groq API key ([Get one here](https://console.groq.com))

### Quick Start
1. Clone the repository
2. Add your Groq API key to `.env`
3. Run the installer:
   ```bash
   ./install.sh
   ```
4. Restart your terminal or run:
   ```bash
   source ~/.local/bin/ai
   ```

## 🎮 Usage

### Basic Command
```bash
ai "your command description"
```

### 🌟 Context-Aware Examples

| Context | Command | Result |
|---------|---------|--------|
| Node.js Project | `ai "install dependencies"` | `npm install` |
| Python Project | `ai "install dependencies"` | `pip install -r requirements.txt` |
| Git (with changes) | `ai "commit all changes"` | `git add . && git commit -m "..."` |
| Docker Project | `ai "build container"` | `docker build -t project-name .` |
| Any Directory | `ai "find large files"` | `find . -type f -size +100M` |

## 🔧 Technical Architecture

### 🏗️ Command Pipeline
1. 🧠 **Context Analysis**
   - Project type detection
   - Git status analysis
   - Shell environment inspection

2. ⚙️ **Command Synthesis**
   - Context-aware generation
   - Parameter optimization
   - Shell compatibility

3. 🔌 **Shell Integration**
   - Environment preservation
   - State management
   - Command injection

## 🛡️ Security & Performance

### Security
- 🔒 Command validation
- 🏰 Environment isolation
- 🔑 Secure credential storage
- 👮 Permission handling

### Performance
- 🚀 Minimal dependencies
- ⚡ Efficient integration
- 💾 Smart resource management
- 🧠 Context caching

## 🔄 Future Roadmap

1. 📚 **Command Learning**
   - History analysis
   - Preference learning
   - Context pattern recognition

2. 🔌 **Enhanced Integration**
   - More project type support
   - Additional shell compatibility
   - Plugin system

3. 🎯 **Advanced Features**
   - Command explanations
   - Interactive tutorials
   - Custom context rules

## 🤝 Contributing

Contributions are welcome! Check out our [Contributing Guidelines](CONTRIBUTING.md).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Author
**Shalom Obongo**
- 🌐 [Website](https://shalomobongo.tech)
- 💻 [GitHub](https://github.com/ShalomObongo)

### Technologies
- 🤖 [Groq](https://groq.com) - AI capabilities
- 🐍 Python ecosystem
- 🐚 Shell community

---

<div align="center">

Made by [Shalom Obongo](https://shalomobongo.tech)

</div> 