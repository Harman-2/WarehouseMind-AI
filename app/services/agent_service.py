import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.errors import ClientError
from google.genai.types import Content, Part
from sqlalchemy.orm import Session

from app.agents.coordinator_agent import coordinator_agent
from app.services import conversation_service

session_service = InMemorySessionService()

MAX_AGENT_RETRIES = 3
RATE_LIMIT_RETRY_DELAYS = (15, 30, 60)


class AgentRateLimitError(Exception):
    pass


class AgentUnavailableError(Exception):
    pass


def _is_rate_limit_error(exc: BaseException) -> bool:
    if isinstance(exc, ClientError) and getattr(exc, "code", None) == 429:
        return True

    cause = exc.__cause__
    if isinstance(cause, ClientError) and getattr(cause, "code", None) == 429:
        return True

    message = str(exc).lower()
    return "429" in message or "resource_exhausted" in message or "quota exceeded" in message


async def run_coordinator(
    message: str,
    db: Session | None = None,
    session_id: int | None = None,
    user_id: str = "demo-user",
) -> tuple[str, int | None]:
    prompt = message

    if db and session_id:
        history = conversation_service.get_recent_messages(db, session_id, limit=8)
        history_text = conversation_service.format_history(history)
        if history_text:
            prompt = f"{history_text}\n\nCurrent question:\n{message}"

    last_error: Exception | None = None

    for attempt in range(MAX_AGENT_RETRIES):
        adk_session = await session_service.create_session(
            app_name="warehousemind",
            user_id=user_id,
        )
        runner = Runner(
            agent=coordinator_agent,
            app_name="warehousemind",
            session_service=session_service,
        )
        user_content = Content(role="user", parts=[Part(text=prompt)])

        try:
            final_response = ""
            async for event in runner.run_async(
                user_id=user_id,
                session_id=adk_session.id,
                new_message=user_content,
            ):
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    final_response += event.content.parts[0].text

            response_text = final_response.strip()

            if db:
                if not session_id:
                    chat_session = conversation_service.create_session(db, user_id=user_id)
                    session_id = chat_session.id
                conversation_service.add_message(db, session_id, "user", message)
                conversation_service.add_message(
                    db, session_id, "assistant", response_text or "No response returned."
                )

            return response_text, session_id

        except Exception as exc:
            last_error = exc
            if _is_rate_limit_error(exc) and attempt < MAX_AGENT_RETRIES - 1:
                await asyncio.sleep(RATE_LIMIT_RETRY_DELAYS[attempt])
                continue
            break

    if last_error and _is_rate_limit_error(last_error):
        raise AgentRateLimitError(
            "Gemini API rate limit reached. Please wait about a minute and try again."
        ) from last_error

    raise AgentUnavailableError(
        "Agent temporarily unavailable. Please try again shortly."
    ) from last_error
