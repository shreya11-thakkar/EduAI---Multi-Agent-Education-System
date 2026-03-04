# multi_agent.py
from database import create_table, save_note, get_note
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
# Disable telemetry to avoid signal/thread errors
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# Set Gemini API Key (better to store in environment variable)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from crewai import Agent, Task, Crew, Process

MODEL = "gemini/gemini-2.5-flash"


def run_education_system(topic: str):

    # Create table if not exists
    create_table()

    # 🔍 Check if topic already exists
    existing_note = get_note(topic)

    if existing_note:
        return existing_note

    # ----------- Run Agents -----------
    researcher = Agent(
        role="Education Researcher",
        goal="Research educational topics",
        backstory="Expert academic researcher",
        verbose=False,
        allow_delegation=False,
        llm=MODEL
    )

    writer = Agent(
        role="Education Content Writer",
        goal="Create structured study notes",
        backstory="Expert teacher",
        verbose=False,
        allow_delegation=False,
        llm=MODEL
    )

    research_task = Task(
        description=f"""
        Research topic: {topic}
        Provide definition, explanation, key points, examples, applications
        """,
        expected_output="Complete research data",
        agent=researcher
    )

    writing_task = Task(
        description=f"""
        Create structured notes on {topic}
        """,
        expected_output="Structured study notes",
        agent=writer
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential
    )

    result = str(crew.kickoff())

    # 💾 Save to database
    save_note(topic, result)

    return result
