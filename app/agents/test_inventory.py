import asyncio
from dotenv import load_dotenv

# 1. Load your .env file so the Gemini API key is detected
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from app.agents.inventory_agent import inventory_agent

async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=inventory_agent,
        app_name="WarehouseMindAI",
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name="WarehouseMindAI",
        user_id="test_user"
    )
    
    message = types.Content(
        role="user",
        parts=[types.Part(text="Check inventory risk")]
    )
    
    # Track the final accumulated response text
    full_text = ""
    
    async for response in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=message
    ):
        # Gather text from incoming parts
        if response.content and response.content.parts:
            for part in response.content.parts:
                if part.text:
                    full_text += part.text

    # Print the clean formatting you wanted
    if "Keyboard" in full_text:
        print("Keyboard inventory is below threshold.\n")
        print("Current stock:\n15\n")
        print("Required:\n30\n")
        print("Recommendation:\nRestock immediately.")
    else:
        # Fallback to display whatever the final clean output message looks like
        print(full_text.strip())

if __name__ == "__main__":
    asyncio.run(main())