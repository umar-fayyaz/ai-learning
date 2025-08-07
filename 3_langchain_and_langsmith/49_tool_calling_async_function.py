import asyncio
import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from rich.console import Console
# from llm import llm
from dotenv import load_dotenv
load_dotenv()
console = Console()


""" 01_tool_call.py implementation starts """ 
 
class CheckCalendarInput(BaseModel): 
    iso_datetime: str = Field(..., description="The date and time to check the calendar for in ISO 8601 format") 
    duration: int = Field(..., description="The duration of the event in minutes") 

@tool(args_schema=CheckCalendarInput)
async def check_calendar_availability(iso_datetime: str, duration: int) -> str:
    """ 
    Crucial Docstring for LLM to understand the tool - use the below format 
 
    What it does: A function that checks if a given time slot is available in the user's calendar. 
    When to use it: Use this to verify meeting times before scheduling them. 
    Additional information: 
    - The input is a string in ISO 8601 format 
    - Timeslots are based on the duration provided in minutes 
    - The output is a string indicating whether the time slot is available or not 
    """
     
    requested_time = datetime.datetime.fromisoformat(iso_datetime)

    try:
        pkt = datetime.timezone(datetime.timedelta(hours=5))
        requested_time = requested_time.astimezone(pkt)
        busy_slots = [
            datetime.datetime(2023, 6, 25, 10, 0, tzinfo=pkt), 
            datetime.datetime(2023, 6, 25, 14, 30, tzinfo=pkt),
            datetime.datetime(2023, 10, 4, 14, 30, tzinfo=pkt),
          ]
        console.print(f"Requested time in PKT: {requested_time}")
        console.print(f"Busy slots in PKT: {busy_slots}")
        is_busy = any(
             requested_time < busy_slot + datetime.timedelta(minutes=duration) and requested_time + datetime.timedelta(minutes=duration) > busy_slot 
             for busy_slot in busy_slots 
          )

        if is_busy:
            return f"The date {requested_time} is not available" 
        else:
            return f"The date {requested_time} is available for {duration} minutes"
    except ValueError as e:
        return "Error: Invalid ISO datetime format. Please use 'YYYY-MM-DDTHH:MM:SS' format."

""" 01_tool_call.py implementation ends """

# ------------------------------------------------------------------------------------------

async def main():
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    llm_with_tools = model.bind_tools([check_calendar_availability])

    prompt = PromptTemplate.from_template("Can you check the calendar availability at 2:30 PM PKT for me?")

    chain = prompt | RunnablePassthrough() | llm_with_tools

    console.rule("[bold yellow]--- Running Tool Call ---")
    console.print("=" * 50)
    console.print("STEP 1: Sending query to LLM...")
    console.print("=" * 50)

    initial_response = await chain.ainvoke({})

    console.print("LLM Response Type:", type(initial_response))
    console.print("LLM Response Content:", initial_response)

    messages = [initial_response]


    tool_call_count = 0
    tool_name_called = []

    while messages[-1].tool_calls:
        print("\n" + "=" * 50)
        print(f"STEP 2: LLM Requested tool calls...")
        print("=" * 50)

        tool_calls = messages[-1].tool_calls
        print(f"Number of tools calls requested: {len(tool_calls)}")

        for tool_call in tool_calls:
            tool_call_count += 1
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_name_called.append(tool_name)

            print(f"Tool Call {tool_call_count}:")
            print(f"Tool Name: {tool_name}")
            print(f"Tool Args: {tool_args}")

            if tool_name == "check_calendar_availability":
                result=  await check_calendar_availability.ainvoke(tool_args)
                # print(f"Tool Response: {tool_response}")
            else:
                result = f"Unknown tool called: {tool_name}"
            
            print(f"Tool Response: {result}")

            tool_message = ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
                name=tool_name,
            )
            messages.append(tool_message)

        print("\n" + "=" * 50)
        print(f"STEP 3: Sending tool responses back to LLM...")
        print("=" * 50)

        followup_response = await model.ainvoke(messages)
        messages.append(followup_response)

        if tool_call_count == 0:
            print("\n" + "=" * 50)
            print("Note: LLM provided a diect response without any tool calls.")
            print("=" * 50)

        print("\n" + "=" * 50)
        print("Final LLM Response:")
        print("=" * 50)
        print(messages[-1].content)

        print("\n" + "=" * 50) 
        print("TOOL CALL STATISTICS:") 
        print("=" * 50) 
        print(f"Total tool calls: {tool_call_count}") 
        print(f"Tools used: {', '.join(set(tool_name_called))}") 
        print(f"Tool call sequence: {' -> '.join(tool_name_called) if tool_name_called else 'None'}") 
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())