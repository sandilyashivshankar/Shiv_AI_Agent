# 🤖 Shiv AI — City Intelligence Agent

<p align="center"><b>A real-time AI city assistant for weather, latest city news, and location-based questions.</b></p>

<p align="center">
<a href="https://shivaiagent.streamlit.app/">🚀 Live Demo</a> •
<a href="https://github.com/sandilyashivshankar/Shiv_AI_Agent">💻 GitHub Repository</a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Mistral%20AI-LLM-7C3AED?style=for-the-badge">
<img src="https://img.shields.io/badge/LangChain-Agent-1F2937?style=for-the-badge">
<img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
<img src="https://img.shields.io/badge/Tavily-Web%20Search-111827?style=for-the-badge">
<img src="https://img.shields.io/badge/OpenWeather-Live%20Weather-0EA5E9?style=for-the-badge">
</p>

---

## 🌆 About the Project

**Shiv AI** is an agentic AI application that turns natural-language city questions into useful, live-data answers.

The application combines **Mistral AI** for reasoning, **LangChain** for agent/tool orchestration, **OpenWeather** for current weather, **Tavily** for web search, and **Streamlit** for the interactive frontend.

Unlike a static chatbot, Shiv AI can use external tools when a request needs fresh information. The current application focuses on two main capabilities: **live weather** and **latest city news**.

The project demo PDF included in the repository shows the complete interface and a sample conversation for Lucknow, including weather details, news results, API status, and the final chat interface.

---

## ✨ Features

### 🌦️ Live Weather
Fetch current weather for cities in India:

- Temperature
- Feels-like temperature
- Weather condition
- Humidity

### 📰 Latest City News
Search the web for recent city-related news using Tavily and return source URLs with short content snippets.

### 🧠 AI Agent Reasoning
Mistral AI decides when a live-information tool is appropriate and works with LangChain tools to produce the final answer.

### 💬 Modern Chat Experience
- Chat-style interface
- Conversation history during the session
- Clear conversation button
- Suggested questions
- API connection indicators
- Friendly AI responses

### 🎨 Premium Streamlit UI
The interface uses a dark, modern AI-product design with:

- Gradient hero section
- Glass-style cards
- Capability panels
- Agent status panel
- Custom CSS
- Responsive layout

---

## 🖼️ Project Demo

A complete UI demonstration is available inside the repository:

`Shiv_AI_Agent/Shiv AI • City Intelligence Agent.pdf`

The four-page demonstration contains:

1. **Landing / Assistant screen** — Shiv AI branding, capabilities, agent status, and introduction.
2. **Live weather example** — Lucknow weather including condition, temperature, feels-like temperature, and humidity.
3. **Latest news example** — recent Lucknow news grouped by sources such as Amar Ujala, Hindustan Times, Dainik Bhaskar, NDTV, and Times of India.
4. **Conversation completion screen** — final assistant response and chat input area.

---

## 🏗️ Architecture

```text
                         USER
                          │
                          ▼
                 ┌─────────────────┐
                 │  Streamlit UI   │
                 │  Chat Interface │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ LangChain Agent │
                 │   Mistral AI    │
                 └────────┬────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
        ┌──────────────┐    ┌──────────────┐
        │ Weather Tool │    │  News Tool   │
        │ OpenWeather  │    │    Tavily    │
        └──────┬───────┘    └──────┬───────┘
               │                   │
               └─────────┬─────────┘
                         ▼
                 ┌───────────────┐
                 │ Agent Response│
                 └───────┬───────┘
                         ▼
                    Streamlit
```

---

## 🔧 How It Works

1. A user asks a question through the Streamlit chat input.
2. The LangChain agent receives the request through Mistral AI.
3. The agent determines whether the request requires current weather or recent news.
4. `get_weather()` calls OpenWeather for live weather data.
5. `get_news()` uses Tavily to search for recent web results.
6. Tool results are returned to the agent.
7. Mistral generates a concise, friendly response.
8. Streamlit displays the result in the conversation.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core programming language |
| **Mistral AI** | LLM / agent reasoning |
| **LangChain** | Agent and tool orchestration |
| **OpenWeather API** | Live weather data |
| **Tavily** | Web search / latest news |
| **Streamlit** | Frontend and deployment |
| **Requests** | HTTP API requests |
| **python-dotenv** | Environment configuration |
| **Rich** | Console output utility |

The repository also contains LangChain learning/experimentation modules covering runnable sequences, passthroughs, parallel execution, sequencing, and tool calling.

---

## 📁 Project Structure

```text
Shiv_AI_Agent/
│
├── README.md
├── requirements.txt
│
└── Shiv_AI_Agent/
    ├── AgentUi.py
    ├── Agents.py
    ├── newssummarizer.py
    ├── owntool.py
    ├── parallelrunnable.py
    ├── runnablepassthrough.py
    ├── sequencerunnable.py
    ├── toolcalling.py
    └── Shiv AI • City Intelligence Agent.pdf
```

### Core Files

- **`AgentUi.py`** — main Streamlit application, custom UI, tools, agent setup, and chat flow.
- **`Agents.py`** — console-based Mistral/LangChain city agent.
- **`newssummarizer.py`** — news-related functionality.
- **`owntool.py`** — custom tool implementation/example.
- **`parallelrunnable.py`** — LangChain parallel runnable example.
- **`runnablepassthrough.py`** — runnable passthrough example.
- **`sequencerunnable.py`** — runnable sequence example.
- **`toolcalling.py`** — tool-calling example.
- **`requirements.txt`** — Python dependencies.
- **PDF file** — complete application screenshots/demo.

---

## 🔑 API Keys & Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### Security

**Never upload real API keys to GitHub.** Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

For Streamlit deployment, add the same credentials through the application's secrets/settings rather than committing them to the repository.

---

## 🚀 Run Locally

### 1. Clone

```bash
git clone https://github.com/sandilyashivshankar/Shiv_AI_Agent.git
cd Shiv_AI_Agent
```

### 2. Create virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Add:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 5. Run the application

```bash
streamlit run Shiv_AI_Agent/AgentUi.py
```

The application will open in your browser.

---

## 💡 Example Questions

```text
What's the weather in Lucknow?
```

```text
Tell me the latest news in Delhi.
```

```text
What is the current weather situation of Kanpur?
```

```text
Give me recent news about Mumbai.
```

```text
Tell me what's happening in Lucknow today.
```

---

## ☁️ Live Deployment

The application is deployed on **Streamlit Community Cloud**.

### 🚀 Try Shiv AI

**https://shivaiagent.streamlit.app/**

### Deployment Entry Point

```text
Shiv_AI_Agent/AgentUi.py
```

Add these secrets before deployment:

```text
MISTRAL_API_KEY
TAVILY_API_KEY
OPENWEATHER_API_KEY
```

---

## ⚠️ Limitations

- Live weather depends on the OpenWeather service.
- News quality and freshness depend on Tavily and available web sources.
- API credentials are required for live functionality.
- The current weather tool is designed around Indian cities.
- The application is primarily a city-intelligence assistant, not a general-purpose search engine.

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- AI agent development
- LLM integration
- LangChain agents
- Tool calling
- Real-time API integration
- Web search integration
- Prompt/system instruction design
- Streamlit application development
- Environment-variable management
- AI product UI/UX

---

## 👨‍💻 Author

### Shiv Shankar Tiwari

**Data Analyst | Data Science & AI | AI/ML | Prompt Engineering**

- GitHub: https://github.com/sandilyashivshankar
- Project Repository: https://github.com/sandilyashivshankar/Shiv_AI_Agent
- Live Application: https://shivaiagent.streamlit.app/

---

## ⭐ Support

If you like **Shiv AI — City Intelligence Agent**, please consider:

- ⭐ Starring the repository
- 🍴 Forking the project
- 🐛 Opening issues for bugs
- 💡 Suggesting new city-intelligence features

Every star and contribution helps the project grow.

---

## 🔮 Future Improvements

Possible future upgrades include:

- 🌍 International city support
- 🗺️ Interactive city maps
- 📍 GPS/location detection
- 🚦 Traffic intelligence
- 🏥 Nearby hospitals and emergency services
- ✈️ Flight and travel information
- 📊 Weather forecasts and historical trends
- 📰 Better news categorization and summarization
- 🎙️ Voice input/output
- 🌐 Multilingual support
- 🧠 More specialized city tools

---

## 📄 License

No license file is currently included. Add an open-source license such as MIT if you want to explicitly define reuse and distribution permissions.

---

<p align="center">
<b>Shiv AI • City Intelligence Agent</b><br>
Built with Mistral AI • LangChain • Tavily • OpenWeather • Streamlit
</p>
