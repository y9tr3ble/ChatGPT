# AI Assistant Bot v2.0 🤖

A powerful Telegram bot that combines multiple AI models to provide intelligent conversations, code assistance, and image generation.

## Features ✨

### Multiple AI Models
- **GPT-4** 🤖 - Advanced language model from OpenAI
- **Gemini** ✨ - Google's latest AI model
- **GPT-4O** 🔮 - Optimized GPT-4 version
- **GPT-4O-mini** 🎯 - Faster, lighter version
- **Claude 3.5 Sonnet** 🎭 - Anthropic's latest model
- **Claude 3.5 Haiku** 🎋 - Fast and efficient version

### Core Features
- Multi-language support (English 🇬🇧, Russian 🇷🇺, Ukrainian 🇺🇦)
- Code block formatting with syntax highlighting
- Image generation capabilities
- Smart conversations with context awareness
- User preferences persistence
- Chat statistics tracking

## Setup 🛠️

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token
- API keys for AI services:
  - OpenAI API key
  - Google Gemini API key
  - Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-assistant-bot.git
cd ai-assistant-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API keys:
```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

4. Run the bot:
```bash
python main.py
```

## Usage 💡

### Available Commands
- `/start` - Initialize the bot
- `/help` - Show available commands
- `/model` - Change AI model
- `/language` - Change interface language
- `/newtopic` - Start new conversation
- `/image` - Generate images
- `/stats` - Show chat statistics
- `/about` - About the bot

### Quick Access Buttons
- ❓ Help
- 🔄 Change Model
- 🌐 Language
- ℹ️ About
- 🆕 New Topic
- 🎨 Generate Image

### Code Formatting
The bot supports code blocks with syntax highlighting for multiple languages:
- Python
- C++
- JavaScript
- HTML/CSS
- Java
- Rust
- Go
- And more...

Example:
\```python
def hello_world():
    print("Hello, World!")
\```

### Image Generation
Use the `/image` command followed by your description to generate images:
```
/image A futuristic city at night with neon lights
```

## Features in Detail 📝

### AI Models
- **GPT-4**: Best for complex tasks and detailed explanations
- **Gemini**: Excellent for general-purpose conversations
- **GPT-4O**: Optimized for better performance
- **GPT-4O-mini**: Fast responses for simple queries
- **Claude Sonnet**: Advanced reasoning and analysis
- **Claude Haiku**: Quick and efficient responses

### Language Support
- 🇬🇧 English: Full support with all features
- 🇷🇺 Russian: Complete localization
- 🇺🇦 Ukrainian: Full interface translation

### Message Handling
- Smart message chunking for long responses
- Code block preservation
- Inline code formatting
- Anti-flood protection
- Error handling and retries

### User Experience
- Persistent user preferences
- Chat history management
- Response time tracking
- Usage statistics
- Model-specific optimizations

## Technical Details 🔧

### Architecture
- Built with aiogram 3.15.0
- Asynchronous design
- Modular service structure
- State management system
- Message queue implementation

### Storage
- User preferences persistence
- Chat history management
- Statistics tracking
- Model usage metrics

### Security
- API key protection
- Content safety checks
- Error message sanitization
- Rate limiting

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

If you have any questions or need help, feel free to:
- Open an issue
- Contact @your_username on Telegram
- Send an email to your@email.com

## Acknowledgments 🙏

- OpenAI for GPT-4
- Google for Gemini
- Anthropic for Claude
- The aiogram community
