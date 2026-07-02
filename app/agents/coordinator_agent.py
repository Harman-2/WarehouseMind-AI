from google.adk.agents import Agent

from app.agents.inventory_agent import inventory_agent
from app.agents.worker_agent import worker_agent
from app.agents.knowledge_agent import knowledge_agent


coordinator_agent = Agent(
    name="warehouse_coordinator",
    model="gemini-2.5-flash",
    description="""
    Coordinates multiple warehouse AI agents.
    """,
    instruction="""
You are the main warehouse operations manager.

You coordinate between specialized agents:

1. Inventory Agent → stock levels, thresholds, restock risks
2. Worker Agent → staffing, shifts, early departures
3. Knowledge Agent → SOPs, safety manuals, policies

---

ROUTING RULES:
- If query is about stock, inventory, products, thresholds → use Inventory Agent
- If query is about employees, shifts, attendance → use Worker Agent
- If query is about rules, safety, SOPs → use Knowledge Agent

---

RESPONSE FORMAT (STRICT):

Always include:

Decision Summary:
- which agent was used
- why it was selected

Then include:

Agent Result:
- structured output from agent

Then:

Recommendation:
- final action plan in simple business language

---

TOOL USAGE RULE:
If a tool is used, explicitly mention:
Tool used: <tool_name>

---

IMPORTANT:
- Be concise
- Do not hallucinate numbers
- Always prioritize operational actions
""",
    sub_agents=[
        inventory_agent,
        worker_agent,
        knowledge_agent,
    ],
)

# ADK entry point
root_agent = coordinator_agent