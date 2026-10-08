import os
import time
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ddgs import DDGS

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)

# Free-tier allowance for this model is much higher than gemini-3.5-flash.
MODEL_NAME = "gemini-3.5-flash-lite"

# Stores the conversation between the user and Gemini.
conversation_history = []


def make_search_tools(sources):
    """Creates the search tools Gemini can call. Every link found is
    added to the 'sources' list so we can show it to the user."""

    def news_search(query: str) -> dict:
        """Search recent news articles. Use for headlines, current events
        and anything that happened recently."""
        print("[tool called] news_search:", query)
        try:
            results = DDGS().news(query, max_results=6, timelimit="w")
        except Exception as error:
            print("news_search error:", error)
            return {"error": "News search is currently unavailable."}

        items = []
        for r in results:
            items.append({
                "title": r.get("title"),
                "date": r.get("date"),
                "source": r.get("source"),
                "snippet": r.get("body"),
                "url": r.get("url"),
            })
            if r.get("url"):
                sources.append({"title": r.get("title"), "url": r.get("url")})
        return {"results": items}

    def web_search(query: str) -> dict:
        """Search the general web for facts, prices, documentation or
        anything that is not news."""
        print("[tool called] web_search:", query)
        try:
            results = DDGS().text(query, max_results=5)
        except Exception as error:
            print("web_search error:", error)
            return {"error": "Web search is currently unavailable."}

        items = []
        for r in results:
            items.append({
                "title": r.get("title"),
                "url": r.get("href"),
                "snippet": r.get("body"),
            })
            if r.get("href"):
                sources.append({"title": r.get("title"), "url": r.get("href")})
        return {"results": items}

    return [news_search, web_search]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat_message():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "error": "Please enter a message."
        }), 400

    # Add the user's message to the conversation.
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)]
    )
    conversation_history.append(user_content)

    # Gemini does not know today's date, so we tell it on every request.
    today = datetime.now().strftime("%A, %d %B %Y")
    system_instruction = (
        f"Today is {today}. You are a helpful work assistant. "
        "For anything recent or time-sensitive (news, prices, current events, "
        "'latest', 'today'), use the search tools: news_search for news and "
        "web_search for other facts. Prefer at most two searches per answer. "
        "Base answers about current events only on the search results and "
        "mention the source names. If a search fails, say so honestly."
    )

    sources = []

    try:
        response = None

        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation_history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        tools=make_search_tools(sources),
                    ),
                )
                break

            except Exception as error:
                if "503" in str(error) and attempt < 3:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    raise

        assistant_message = response.text

        if not assistant_message:
            raise ValueError("Gemini returned an empty response.")

        # Add Gemini's response to the conversation.
        conversation_history.append(
            types.Content(
                role="model",
                parts=[types.Part.from_text(text=assistant_message)]
            )
        )

        # Remove duplicate links, keeping the original order.
        seen = set()
        unique_sources = []
        for source in sources:
            if source["url"] not in seen:
                seen.add(source["url"])
                unique_sources.append(source)

        return jsonify({
            "response": assistant_message,
            "sources": unique_sources
        })

    except Exception as error:

        if conversation_history and conversation_history[-1] == user_content:
            conversation_history.pop()

        print("Gemini Error:", error)

        error_message = str(error)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return jsonify({
                "error": "Gemini API quota has been reached. "
                         "Please try again later."
            }), 429

        return jsonify({
            "error": "Gemini is temporarily unavailable. "
                     "Please try again."
        }), 503


@app.route("/clear", methods=["POST"])
def clear_conversation():

    conversation_history.clear()

    return jsonify({
        "message": "Conversation cleared successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)