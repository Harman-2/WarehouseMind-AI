import asyncio

from dotenv import load_dotenv

load_dotenv()


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


from app.agents.worker_agent import worker_agent



async def main():


    session_service = InMemorySessionService()


    runner = Runner(

        agent=worker_agent,

        app_name="WarehouseMindAI",

        session_service=session_service

    )


    session = await session_service.create_session(

        app_name="WarehouseMindAI",

        user_id="test_user"

    )


    message = types.Content(

        role="user",

        parts=[

            types.Part(

                text="Check worker shift risks"

            )

        ]

    )


    # Track the final accumulated response text
    full_text = ""
    
    async for response in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=message
    ):
        # Accumulate the clean text from incoming parts
        if response.content and response.content.parts:
            for part in response.content.parts:
                if part.text:
                    full_text += part.text

    # Print the clean output directly
    print(full_text.strip())



asyncio.run(main())