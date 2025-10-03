# LangChain Chatbot with Groq

A Streamlit-based chatbot application that demonstrates LangChain basics using Groq's ultra-fast inference.

## Features

- 🤖 **AI Chat Interface** - Powered by Groq's LLM models
- 📚 **Enhanced Chat History** - Search, save, and load conversations
- 💾 **Conversation Management** - Save important chats for later
- 📊 **Chat Statistics** - Track message counts and response lengths
- 🔍 **Search Functionality** - Find specific messages in your chat history
- 🎨 **Modern UI** - Clean, responsive interface with Streamlit

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

**Option A: Using .env file (Recommended)**
1. Copy `env_template.txt` to `.env`
2. Edit `.env` and add your GROQ API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```
3. Get your free API key at [console.groq.com](https://console.groq.com)

**Option B: Environment Variable**
```bash
export GROQ_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

## Security Features

- ✅ **No API keys in code** - All keys stored in environment variables
- ✅ **Secure configuration** - Uses python-dotenv for safe key management
- ✅ **User-friendly setup** - Clear instructions for API key configuration

## Available Models

- **llama3-8b-8192** - Fast, efficient Llama 3 model
- **gemma2-9b-it** - Google's Gemma 2 model for instruction following

## Usage

1. **Start Chatting** - Type your questions in the chat input
2. **Search History** - Use the search bar to find specific messages
3. **Save Conversations** - Click "Save Chat" to preserve important discussions
4. **Load Previous Chats** - Access your saved conversations from the sidebar
5. **View Statistics** - Monitor your chat activity with real-time metrics

## Project Structure

```
Langchain-basic/
├── app.py              # Main Streamlit application
├── env_template.txt    # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

- **API Key Not Found**: Ensure your `.env` file exists and contains the correct API key
- **Model Initialization Failed**: Verify your API key is valid and has sufficient credits
- **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## Built With

- **LangChain** - LLM application framework
- **Groq** - Ultra-fast inference platform
- **Streamlit** - Web application framework
- **Python** - Programming language





