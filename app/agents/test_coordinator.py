import asyncio
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.coordinator_agent import coordinator_agent


APP_NAME = "warehouse_app"
USER_ID = "demo_user"


async def main():

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    runner = Runner(
        agent=coordinator_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    inventory_report = """
Inventory Report

Keyboard : 15 remaining
Mouse : 120 remaining
Monitor : 8 remaining

Inventory Risks

Keyboard below threshold.
Monitor critically low.
"""

    worker_report = """
Worker Report

Morning Shift : 42 workers

Night Shift : 30 workers

2 workers left early.

Packing Zone has worker shortage.
"""

    prompt = f"""
Analyze the warehouse.

Inventory Agent Report:

{inventory_report}

Worker Agent Report:

{worker_report}
"""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ],
        ),
    ):

        if event.is_final_response():

            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())