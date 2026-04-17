# AI-First CRM HCP Module

This project is a full-stack AI-first Customer Relationship Management (CRM) module specifically designed for Healthcare Professionals (HCPs). It allows field representatives to easily log, view, and analyze interactions with doctors through both a structured UI form and a natural-language conversational interface.

## Tech Stack
- **Frontend**: React (Vite) + Redux Toolkit + Tailwind CSS + Google Inter font.
- **Backend**: Python + FastAPI.
- **AI Framework**: LangGraph.
- **LLM Models**: Groq APIs (specifically `gemma2-9b-it` for routing/suggestions and `llama-3.3-70b-versatile` for deep extraction).
- **Database**: MySQL.

---

## The Role of LangGraph Agent in HCP Interactions

The LangGraph agent acts as the intelligent orchestration layer between the field representative's natural language input and the CRM's structured database. 
Instead of requiring reps to manually fill out dozens of fields after a tiring hospital visit, the LangGraph agent:
1. **Classifies Intent**: Instantly determines if the user is trying to log a new meeting, edit an existing one, look up history, or search for an HCP.
2. **Extracts Entities (Information Extraction)**: Parses messy, unstructured voice notes or text (e.g., "Met Dr. Sharma, she liked the OncoBoost brochure") into a strictly structured JSON schema (hcp_name, topics, sentiment, materials).
3. **Decides Tool Execution**: Automatically routes the extracted data to specific backend database tools using its state graph.
4. **Contextual Intelligence**: Feeds the interaction context back into the LLM to proactively suggest "Follow-up Actions" (e.g., "Schedule next visit in 2 weeks") based on the sentiment and outcomes discussed.

---

## Defined LangGraph Tools (Minimum 5)

The LangGraph agent has access to 5 specific tools to manage sales-related activities:

#### 1. Log Interaction Tool
**Purpose**: Captures new interaction data.
**How it works**: When the agent classifies a "log" intent, the LLM first summarizes the unstructured text and extracts key entities (HCP Name, Date, Topics, Sentiment, Materials Shared). This tool then takes that clean, extracted JSON payload and executes an asynchronous SQLAlchemy database insertion into the `interactions` table, associating it with the correct HCP ID. It returns the newly created interaction ID.

#### 2. Edit Interaction Tool
**Purpose**: Allows modification of already logged data.
**How it works**: If a user realizes they made a mistake (e.g., "Change the sentiment to positive for the last meeting"), the agent extracts the fields that need updating. This tool queries the database for the active interaction, applies a partial update via SQL `UPDATE` to the specific fields, and commits the transaction without overwriting unchanged data.

#### 3. Get HCP History Tool
**Purpose**: Retrieves historical context.
**How it works**: Takes an HCP name or ID and queries the database for the last 5 interactions, returning a summary of dates, topics, and outcomes to brief the rep before their next meeting.

#### 4. Suggest Follow-ups Tool
**Purpose**: Acts as an AI sales coach.
**How it works**: Passes the context of the current interaction to the LLM and asks it to generate 3 actionable, specific next steps (e.g., "Email clinical trial data tomorrow"). It returns these to the UI as selectable action items.

#### 5. Search HCP Tool
**Purpose**: Helps reps find contacts in their territory.
**How it works**: Performs a fuzzy search against the MySQL `hcps` table based on name, specialty, or hospital, returning a formatted list of matching doctors so the rep knows exactly who they are dealing with.

---

## Local Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL Server (running locally)

### 1. Database Setup
1. Open your MySQL client (e.g., MySQL Workbench).
2. Execute the `db/init.sql` script to create the `hcp_crm` database and seed it with dummy HCP data.

### 2. Backend Setup
1. Navigate to the `backend` folder: `cd backend`
2. Create and activate a virtual environment: `python -m venv env` and `env\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your **Groq API Key** and your **MySQL Database URL** (e.g., `mysql+aiomysql://root:yourpassword@localhost/hcp_crm`).
5. Run the server: `uvicorn main:app --reload --port 8000`

### 3. Frontend Setup
1. Navigate to the `frontend` folder: `cd frontend`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
4. Open `http://localhost:5173` in your browser.


## Clear DataBase
```
python -c "import asyncio; from core.database import SessionLocal; from sqlalchemy import text; async def clear(): async with SessionLocal() as session: await session.execute(text('TRUNCATE TABLE interactions')); await session.commit(); print('✅ Database cleared for video!'); asyncio.run(clear())"
```