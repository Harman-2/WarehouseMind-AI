from google.adk.agents import Agent

from app.agents.knowledge_tools import search_warehouse_documents


knowledge_agent = Agent(
    name="knowledge_agent",
    model="gemini-2.5-flash",
    description="""
    Retrieves answers from warehouse SOPs, safety manuals,
    and inventory policies stored in the knowledge base.
    """,
    instruction="""
    You are a warehouse compliance and operations expert.

    Use the knowledge search tool to find relevant policy text.

    Answer using only retrieved document content when possible.

    Cite the document type and title in your response.
    """,
    tools=[search_warehouse_documents],
)
