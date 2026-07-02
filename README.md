# 📦 WarehouseMind AI

WarehouseMind AI is a **multi-agent AI system** that automates warehouse decision-making using intelligent coordination between specialized agents.

It helps warehouse managers:

Monitor inventory levels
Detect staffing risks
Access warehouse SOPs and safety policies
Generate actionable operational insights

The system uses **Google ADK (Agent Development Kit)** with **Gemini 2.5 Flash** and integrates a **Model Context Protocol (MCP) tool** layer for real-world data execution.

---
## 🧠 Problem Statement

Warehouse operations involve multiple independent systems:

Inventory tracking
Workforce management
Policy/SOP lookup

Manually analyzing these systems is:

Slow
Error-prone
Not scalable

WarehouseMind AI solves this by introducing a **coordinated multi-agent system** that automatically routes queries to the correct domain expert agent.

---
## 🤖 AI Agent Architecture
 **🔹 Coordinator Agent (Main Brain)**
Routes user queries to correct sub-agent
Combines responses into final output
***🔹 Sub-Agents**

**1. Inventory Agent**

Detects low stock items
Identifies restock risks
Uses check_inventory() MCP tool

**2. Worker Agent**

Monitors shift attendance
Detects early departures
Uses check_worker_status() tool

**3. Knowledge Agent**

Retrieves SOPs and warehouse policies
Uses search_warehouse_documents() tool

---
## ⚙️ MCP Tool Layer (Important Concept)

This project uses Model Context Protocol (MCP) to connect AI agents with real backend logic.

**📌 server.py**
Acts as the MCP server
Exposes tools to agents
Handles tool execution requests
**📌 tools.py**

Contains actual business logic:

Inventory threshold checks
Worker status analysis
Document retrieval
**🔁 Why MCP is used**
Decouples AI reasoning from backend logic
Makes system modular and scalable
Allows tool reuse across agents

---
## 🔄 System Workflow

User Query
   ↓
Coordinator Agent (Gemini 2.5 Flash)
   ↓
Routes to Sub-Agent
   ↓
Sub-Agent calls MCP Tool
   ↓
server.py executes tool
   ↓
tools.py runs logic
   ↓
Response returned to agent
   ↓
Final structured answer → UI

---
## 🚀 Key Features

* **Multi-Agent Orchestration:** Intelligent routing between Inventory, Worker, and Knowledge agents.
* **Inventory Monitoring:** Real-time tracking of stock levels with threshold-based risk analysis.
* **Worker Optimization:** Automated detection of staffing risks and operational impacts.
* **Knowledge Retrieval:** Instant access to warehouse SOPs, safety manuals, and compliance policies.
* **Actionable Intelligence:** Provides specific recommendations and next steps for warehouse managers.

---
## 🏗 System Architecture

* **Frontend:** React-based interactive chat interface.
* **Backend:** FastAPI (Python) serving as the bridge between the UI and the agent framework.
* **Agent Brain:** Google ADK running on Gemini 2.5 Flash.

---
### Agent Responsibilities

| Agent                 | Responsibility                       | Primary Tool                     |
| :-------------------- | :----------------------------------- | :------------------------------- |
| **Coordinator** | Routes queries & integrates findings | N/A                              |
| **Inventory**   | Monitors stock & detects thresholds  | `check_inventory()`            |
| **Worker**      | Tracks attendance & staffing risks   | `check_worker_status()`        |
| **Knowledge**   | Retrieves SOPs & safety policies     | `search_warehouse_documents()` |

---
## ⚙️ Tech Stack

* **Language:** Python 3.10+
* **AI Framework:** Google ADK (Agents)
* **LLM:** Gemini 2.5 Flash
* **API:** FastAPI
* **Frontend:** Vite + React
* **MCP** Tool execution layer for agent-to-function communication
* **ASGI Server:** Uvicorn (for running FastAPI backend)

---
## 🖥️ How to Run Locally

### 1. Backend

```bash
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
---
###  Example Queries

> **Inventory Check:**
> "Which products are currently below threshold and what is the restocking risk?"

> **Workforce Analysis:**
> "Can you list the workers who left early today and explain the operational impact?"

> **Policy Retrieval:**
> "What is the safety procedure for hazardous material spills?"
