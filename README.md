# 🤖 Gemini Chat Application

An intelligent command-line chat application powered by Google's Gemini AI with full conversation context support, conversation history management, and cross-platform compatibility.

# ✨ Features

 - 🧠 Full Context Support - The AI remembers your entire conversation
 - 💾 Save & Load - Save conversations as JSON files and load them later
 - 📊 Statistics - Track message count, character count, and more
 - 📁 Organized Storage - Conversations saved in a dedicated conversations/ folder
 - 🔑 Persistent API Key - Save your API key for future sessions
 - 🎨 Clean Interface - Simple, intuitive command-line interface
 - 📱 Cross-Platform - Works on Android (Termux), Linux, macOS, and Windows
 - 🛡️ Error Handling - Clear error messages and graceful recovery

# 📋 Requirements

 - Python 3.8 or higher
 - Google AI Studio API key (Get it free)
 - Internet connection

# 🚀 Installation

### Common Steps (All Platforms)

1. Get your API Key:
   - Visit Google AI Studio
   - Click "Create API Key"
   - Copy your API key
2. Clone or download this project:
   ```bash
   git clone https://github.com/omar-haidar/gemini-chat-app-console.git
   cd gemini-chat-app-console
   ```
   Or download and extract the ZIP file.

---

### 🐧 Linux (Ubuntu/Debian)

```bash
# 1. Install Python and venv if not already installed
sudo apt update
sudo apt install python3-full python3-venv -y

# 2. Navigate to project folder
cd gemini-chat-app

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install required packages
pip install google-generativeai

# 6. Run the application
python main.py
```

For future runs:

```bash
source venv/bin/activate
python main.py
```

---

### 📱 Android (Termux)

```bash
# 1. Install Termux from F-Droid (recommended) or GitHub
# Do NOT use Google Play Store version (outdated)

# 2. Update packages
pkg update && pkg upgrade

# 3. Install Python
pkg install python

# 4. Navigate to project folder
cd /storage/emulated/0/path/to/gemini-chat-app

# 5. Install required packages
pip install google-generativeai

# 6. Run the application
python main.py
```

Note for Android users:

- If you get externally-managed-environment error, use:
  ```bash
  pip install google-generativeai --break-system-packages
  ```
- Make sure Termux has storage permission:
  ```bash
  termux-setup-storage
  ```
- A `cryptography` error may appear when installing on Termux. This error occurs because the cryptography library needs a `Rust compiler` and some components are compiled, and this is not fully supported in Termux on Android.

### The solution is to install the missing packages.

 ```bash
 # تحديث الحزم الأساسية
pkg update && pkg upgrade -y

# تثبيت الأدوات المطلوبة
pkg install python rust binutils build-essential cmake -y

# تثبيت المكتبات المطلوبة للتشفير
pkg install openssl libffi -y

# تعيين متغيرات البيئة
export CARGO_BUILD_TARGET=aarch64-linux-android
export OPENSSL_DIR=$PREFIX

# الآن حاول تثبيت المكتبة
pip install cryptography

# ثم ثبت google-generativeai
pip install google-generativeai
```

---

### 🍎 macOS

```bash
# 1. Install Python if not installed (using Homebrew)
brew install python@3

# 2. Navigate to project folder
cd gemini-chat-app

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install required packages
pip install google-generativeai

# 6. Run the application
python main.py
```

---

### 🪟 Windows

```bash
# 1. Install Python from python.org (check "Add to PATH")

# 2. Open Command Prompt or PowerShell

# 3. Navigate to project folder
cd C:\path\to\gemini-chat-app

# 4. Create virtual environment
python -m venv venv

# 5. Activate virtual environment
venv\Scripts\activate

# 6. Install required packages
pip install google-generativeai

# 7. Run the application
python main.py
```

---

### 📖 Usage

First Run

On first run, you'll be prompted to enter your Google AI Studio API key. You can choose to save it for future sessions.

# Commands

 - /help Show available commands
 - /clear Clear conversation context
 - /save Save current conversation
 - /load Load a previous conversation
 - /list List all saved conversations
 - /stats Show conversation statistics
 - /context Show current conversation context
 - /exit Exit the application

# Example Session

```
🤖 Gemini Chat Application
   Intelligent Chat with Context Support

👤 You: Hello! My name is Alice.
🤖 Assistant:
Hello Alice! It's nice to meet you. How can I help you today?

👤 You: What's my name?
🤖 Assistant:
Your name is Alice! We just discussed that a moment ago.

👤 You: /save
💾 Conversation saved to: conversations/conversation_20260116_143022.json

👤 You: /exit
👋 Goodbye!
Save conversation before exit? (y/n): n
```

---

# 📁 Project Structure

```
gemini-chat-app/
├── config.py              # Configuration settings
├── chat_manager.py        # Chat management with context
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── settings.txt          # API key storage (auto-generated)
├── conversations/        # Saved conversations directory
│   ├── conversation_20260116_143022.json
│   └── ...
└── venv/                 # Virtual environment (not tracked in git)
```

---

# ❓ Common Issues & Solutions

### 1. "externally-managed-environment" Error

Cause: Python environment is system-protected (common in Linux/Android)

Solution:

```bash
# Option A: Use virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate
pip install google-generativeai

# Option B: Override protection (Not recommended)
pip install google-generativeai --break-system-packages
```

---

### 2. "ModuleNotFoundError: No module named 'google'"

Cause: The google-generativeai package is not installed

Solution:

```bash
pip install google-generativeai
```

---

### 3. "404 models/gemini-pro is not found"

Cause: Using deprecated model name

Solution:
The model name has been updated in the latest version. Current model: gemini-1.5-flash

```python
# Old (deprecated)
model = genai.GenerativeModel('gemini-pro')

# New (current)
model = genai.GenerativeModel('gemini-3-flash-preview')
```

---

### 4. "400 BAD_REQUEST - Invalid API key"

Cause: API key is incorrect or has extra spaces/newlines

Solution:

- Copy the API key directly from Google AI Studio
- Ensure no extra spaces or newlines
- Delete settings.txt and re-enter the key
- If persistent, create a new API key

---

### 5. "Permission Denied" on Android

Cause: Termux doesn't have storage permissions

Solution:

```bash
termux-setup-storage
# Grant permission when prompted
```

---

### 6. API Key Not Saving

Cause: Write permissions issue or file system error

Solution:

- Ensure the project directory is writable
- Check disk space
- Try manual creation:
  ```bash
  echo "API_KEY=your_key_here" > settings.txt
  ```

---

### 7. Slow Responses

Cause: Network issues or model selection

Solution:

- Use gemini-1.5-flash for faster responses
- Check your internet connection
- For complex queries, expect longer processing times

---

### 8. "Conversation not found" When Loading

Cause: The conversations/ folder might be deleted or moved

Solution:

- Check if conversations/ folder exists
- Use /list to see available conversations
- Ensure you're in the correct project directory

---

### 9. Characters Displaying Incorrectly

Cause: Terminal encoding issues (common on Windows)

Solution:

- Windows: Use Windows Terminal instead of Command Prompt
- Linux/Mac: Ensure UTF-8 encoding
- Android: Use Termux's default terminal

---

### 10. Rate Limiting Errors

Cause: Too many requests to the API

Solution:

- Wait a few seconds between requests
- The free tier has rate limits
- Consider upgrading your API plan if needed

---

# 🔒 Security Notes

 - ⚠️ Never commit settings.txt to version control
 - ⚠️ Never share your API key publicly
 - ✅ Add settings.txt to .gitignore:
  ```
  settings.txt
  conversations/
  __pycache__/
  *.pyc
  ```
- ✅ Rotate your API key regularly
- ✅ Use environment variables in production:
  ```bash
  export GOOGLE_API_KEY="your_key_here"
  ```

---

# 🔄 Updating

To update the application:

```bash
# Pull latest changes (if using git)
git pull

# Update dependencies
pip install --upgrade google-generativeai

# Clear old conversations if needed
rm -rf conversations/
```

---

# 📝 Conversation File Format

Saved conversations are stored in JSON format:

```json
{
  "session_id": "20260116_143022",
  "timestamp": "2026-01-16T14:30:22",
  "messages": [
    {
      "role": "user",
      "content": "Hello!",
      "timestamp": "2026-01-16T14:30:22"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2026-01-16T14:30:23"
    }
  ]
}
```

---

# 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

# 📄 License

This project is open-source and available under the MIT License.

---

# 🙏 Acknowledgments

- Google Generative AI for the Gemini API
- Google AI Studio for API key management

---

# 📞 Support

If you encounter any issues not covered here:

1. Check the Google AI documentation
2. Visit Google AI Studio Help
3. Open an issue in this repository

---

### Made by OMAR HAIDAR