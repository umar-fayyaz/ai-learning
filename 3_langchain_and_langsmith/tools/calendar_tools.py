from pydantic.v1 import BaseModel, Field
import datetime
from langchain_core.tools import tool
from rich.console import Console
console = Console()

class CalendarCheckInput(BaseModel):
    iso_datetime:str = Field(description="The proposed meeting time in ISO 8601 format, e.g., '2025-07-04T14:30:00'.")

    duration_minutes:int = Field(description="The duration of the meeting in minutes.", default=30)

@tool(args_schema=CalendarCheckInput)
async def check_calendar_availability(iso_datetime: str, duration_minutes: int = 30) -> str:
    """ 
    Checks if a given time slot is available in the user's calendar.  
    Use this to verify meeting times before scheduling them. 
    """
    console.rule(f"[bold yellow]--- TOOL: Checking calendar for {iso_datetime} for {duration_minutes} minutes ---")

    try:
        requested_time = datetime.datetime.fromisoformat(iso_datetime)

        busy_slots = [
            datetime.datetime(2025, 6, 25, 10, 0), 
            datetime.datetime(2025, 6, 25, 14, 30),
        ]
        is_busy = any(
            busy_time <= requested_time < busy_time + datetime.timedelta(minutes=60) 
            for busy_time in busy_slots 
        )

        if is_busy:
            console.print(f"[bold red]Time slot {iso_datetime} is busy.")
            return f"Time slot {iso_datetime} is busy. Please choose another time."
        else:
            console.print(f"[bold green]Time slot {iso_datetime} is available.")
            return f"Time slot {iso_datetime} is available for {duration_minutes} minutes."
        
    except ValueError as e:
        return "Error: Invalid ISO datetime format. Please use 'YYYY-MM-DDTHH:MM:SS' format."