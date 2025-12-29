
import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# You need to set GOOGLE_API_KEY in your .env or environment
# Verify Zen Browser path or fallback to default Chrome

ZEN_PATH = "/home/lxvi/.var/app/app.zen_browser.zen/current/active/files/bin/zen"
# If Zen is not found or fails, playwrght usually defaults to chromium, 
# but we try to point to the user's best browser if possible.

async def main():
    print(">>> Initializing Ultrathink Agentic Browser...")

    # 1. Initialize LLM (Gemini 2.0 Flash is recommended for speed/cost in agents)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", # Or gemini-1.5-pro-latest
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.0
    )

    # 2. Define Ultrathink Persona
    system_prompt = """
    You are the Ultrathink Browser Agent.
    Your traits:
    - PLANNER: Break down complex web tasks into steps.
    - IMPLEMENTER: Execute actions precisely.
    - REVIEWER: Verify the page state before assuming success.
    
    You have full permission to navigate, interact, and extract data to fulfill the user's request.
    """

    # 3. Configure Browser (Headful for demonstration)
    browser = Browser(
        headless=False, # User wants to see it action
        # chrome_instance_path="/usr/bin/firefox", # Utilizing installed Firefox/Zen if compatible, else standard chrome
    )

    # 4. Create Agent
    agent = Agent(
        task="Go to https://news.ycombinator.com, find the top 3 stories, and save their titles and links to a file called 'hn_top3.md'",
        llm=llm,
        browser=browser,
    )

    print(">>> Starting Task: HN Top 3 Fetch")
    history = await agent.run()
    print(">>> Task Complete!")

if __name__ == "__main__":
    asyncio.run(main())
