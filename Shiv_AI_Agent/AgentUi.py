import os
import requests
import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from tavily import TavilyClient
from langchain.agents import create_agent

# =========================================================
# Configuration
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="Shiv AI • City Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# Premium UI
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(59,130,246,.12), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(139,92,246,.12), transparent 30%),
            linear-gradient(135deg, #070b14 0%, #0b1020 45%, #080d18 100%);
        color: #eef2ff;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    [data-testid="stSidebar"] {
        background: rgba(7, 11, 20, .92);
        border-right: 1px solid rgba(148,163,184,.12);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .brand-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        box-shadow: 0 10px 30px rgba(37,99,235,.28);
    }

    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 4px;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            rgba(15,23,42,.92),
            rgba(15,23,42,.65)
        );
        border: 1px solid rgba(148,163,184,.13);
        box-shadow: 0 24px 70px rgba(0,0,0,.22);
        margin-bottom: 22px;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: rgba(34,197,94,.10);
        border: 1px solid rgba(34,197,94,.22);
        color: #86efac;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .5px;
        margin-bottom: 12px;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(30px, 4vw, 48px);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -1.8px;
        color: #f8fafc;
    }

    .hero h1 span {
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #94a3b8;
        max-width: 760px;
        font-size: 14px;
        line-height: 1.7;
        margin-top: 14px;
    }

    .capability {
        padding: 16px;
        border-radius: 17px;
        background: rgba(15,23,42,.55);
        border: 1px solid rgba(148,163,184,.10);
        margin-bottom: 10px;
    }

    .capability-title {
        font-size: 13px;
        font-weight: 700;
        color: #e2e8f0;
    }

    .capability-text {
        color: #94a3b8;
        font-size: 11px;
        line-height: 1.5;
        margin-top: 5px;
    }

    .status-card {
        padding: 14px 15px;
        border-radius: 16px;
        background: rgba(15,23,42,.60);
        border: 1px solid rgba(148,163,184,.11);
        margin-top: 14px;
    }

    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 7px 0;
        color: #94a3b8;
        font-size: 11px;
    }

    .status-value {
        color: #e2e8f0;
        font-weight: 600;
    }

    .online {
        color: #86efac;
    }

    .chat-shell {
        min-height: 520px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(15,23,42,.45);
        border: 1px solid rgba(148,163,184,.08);
        border-radius: 18px;
        margin-bottom: 10px;
    }

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    .suggestion {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 8px;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 11px;
        margin-top: 24px;
        padding: 12px;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,.14);
        background: rgba(15,23,42,.7);
        color: #cbd5e1;
        font-weight: 600;
    }

    div.stButton > button:hover {
        border-color: rgba(96,165,250,.45);
        color: #f8fafc;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Tools
# =========================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city in India."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "OpenWeather API key is not configured."

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city},IN&appid={api_key}&units=metric"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if str(data.get("cod")) != "200":
            return f"Weather error: {data.get('message', 'Could not fetch weather')}"

        temp = data["main"]["temp"]
        feels_like = data["main"].get("feels_like", temp)
        humidity = data["main"].get("humidity", "N/A")
        desc = data["weather"][0]["description"].capitalize()

        return (
            f"Weather in {city}: {desc}. "
            f"Temperature: {temp}°C, feels like {feels_like}°C, "
            f"humidity: {humidity}%."
        )

    except requests.RequestException as exc:
        return f"Weather service error: {exc}"


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Tavily API key is not configured."

    try:
        tavily_client = TavilyClient(api_key=api_key)

        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=5,
        )

        results = response.get("results", [])

        if not results:
            return f"No recent news found for {city}."

        news_list = []

        for item in results:
            title = item.get("title", "No title")
            url = item.get("url", "")
            snippet = item.get("content", "")

            news_list.append(
                f"- {title}\n"
                f"  Source: {url}\n"
                f"  {snippet[:220]}..."
            )

        return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

    except Exception as exc:
        return f"News service error: {exc}"


# =========================================================
# Agent
# =========================================================

@st.cache_resource
def build_agent():
    mistral_key = os.getenv("MISTRAL_API_KEY")

    if not mistral_key:
        return None

    llm = ChatMistralAI(
        model="mistral-small-2506",
        api_key=mistral_key,
    )

    return create_agent(
        llm,
        tools=[get_weather, get_news],
        system_prompt=(
            "You are Shiv AI, a helpful and professional city intelligence "
            "assistant. You can provide current weather and latest city news. "
            "Use the appropriate tool when the user asks for live information. "
            "Give concise, accurate, friendly answers. When presenting news, "
            "clearly distinguish sources from your own summary."
        ),
    )


agent = build_agent()

# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-title">Shiv AI</div>
                <div class="brand-subtitle">CITY INTELLIGENCE AGENT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Capabilities")

    st.markdown(
        """
        <div class="capability">
            <div class="capability-title">🌦️ Live Weather</div>
            <div class="capability-text">
                Get current temperature, conditions, humidity and feels-like data.
            </div>
        </div>

        <div class="capability">
            <div class="capability-title">📰 Latest News</div>
            <div class="capability-text">
                Search the web for recent news related to a city.
            </div>
        </div>

        <div class="capability">
            <div class="capability-title">🧠 AI Reasoning</div>
            <div class="capability-text">
                Mistral-powered agent decides which tool is useful for each request.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Agent Status")

    mistral_ok = bool(os.getenv("MISTRAL_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
    weather_ok = bool(os.getenv("OPENWEATHER_API_KEY"))

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-row">
                <span>Agent</span>
                <span class="status-value online">● Online</span>
            </div>
            <div class="status-row">
                <span>Mistral API</span>
                <span class="status-value">{'Connected' if mistral_ok else 'Missing'}</span>
            </div>
            <div class="status-row">
                <span>Tavily API</span>
                <span class="status-value">{'Connected' if tavily_ok else 'Missing'}</span>
            </div>
            <div class="status-row">
                <span>Weather API</span>
                <span class="status-value">{'Connected' if weather_ok else 'Missing'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# Main Header
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">● AI AGENT ONLINE</div>
        <h1>Your <span>City Intelligence</span> Assistant</h1>
        <p>
            Ask about weather, breaking city news, or anything related to
            a location. Shiv AI uses Mistral for reasoning, OpenWeather for
            live weather, and Tavily for web search.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# API Warning
# =========================================================

if agent is None:
    st.error(
        "MISTRAL_API_KEY is missing. Add your API keys to the .env file "
        "and restart the Streamlit application."
    )

# =========================================================
# Session State
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# Welcome Screen
# =========================================================

if not st.session_state.messages:
    st.markdown("### Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="capability">
                <div class="capability-title">🌤️ Weather</div>
                <div class="capability-text">
                    "What's the weather in Lucknow?"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="capability">
                <div class="capability-title">📰 News</div>
                <div class="capability-text">
                    "What's the latest news in Delhi?"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="capability">
                <div class="capability-title">🤖 Agent</div>
                <div class="capability-text">
                    "Tell me what do you want to know?"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# Conversation
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# Chat Input
# =========================================================

user_input = st.chat_input(
    "Ask Shiv AI about a city, weather, or latest news..."
)

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if agent is None:
            response_text = (
                "I can't start the AI agent because MISTRAL_API_KEY "
                "is missing from your .env file."
            )
            st.error(response_text)

        else:
            with st.spinner("Shiv AI is thinking..."):
                try:
                    result = agent.invoke(
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": user_input,
                                }
                            ]
                        }
                    )

                    messages = result.get("messages", [])

                    if messages:
                        final_message = messages[-1]

                        # If the last message is a tool result, find the
                        # most recent AI message instead.
                        if isinstance(final_message, ToolMessage):
                            for msg in reversed(messages):
                                if getattr(msg, "type", "") == "ai":
                                    final_message = msg
                                    break

                        response_text = getattr(
                            final_message,
                            "content",
                            "I couldn't generate a response.",
                        )

                        if isinstance(response_text, list):
                            response_text = "\n".join(
                                str(item) for item in response_text
                            )

                    else:
                        response_text = "I couldn't generate a response."

                except Exception as exc:
                    response_text = (
                        f"Something went wrong while running the agent:\n\n"
                        f"`{exc}`"
                    )

            st.markdown(response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )

# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div class="footer">
        Built with Mistral AI • LangChain • Tavily • OpenWeather • Streamlit
        <br>
        Shiv AI Agent
    </div>
    """,
    unsafe_allow_html=True,
)