from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from rich.console import Console
from dotenv import load_dotenv
load_dotenv()

console = Console()

factual_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.1)
creative_model = ChatOpenAI(model="gpt-4.1-nano", temperature=1.2)

message = [HumanMessage(content="Write a single sentence describing a cat.")]

def test_model(model, label):
    console.rule(f"[bold blue]Results from {label}")
    for i in range(3):
        result = model.invoke(message)
        print(f"{i+1}. {result.content}")

test_model(factual_model, "Factual Model (temp=0.1)")
test_model(creative_model, "Creative Model (temp=1.2)")
