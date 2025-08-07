from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field 
from enum import Enum
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

class SentimentCategory(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"

class SentimentAnalysis(BaseModel):
    sentiment: SentimentCategory = Field(description="The sentiment of the text.")
    justification:str = Field(description="1 sentence explanation of the sentiment.")

parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)

format_instructions = parser.get_format_instructions()
console.print(Markdown(format_instructions))

sentiment_classification_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert sentiment analysis assistant. Your task is to analyze an email and classify it into one of the following categories: Positive, Negative, or 
    Neutral. Justify Answer in 1 sentence.
    You must provide your response in a JSON format that adheres to the following 
    schema. 
    Do NOT include any other text, explanations, or apologies. Only the JSON object. 
    {format_instructions}"""),
    ("human", """Please analyze the following email: 
    From: {sender} 
    Subject: {subject} 
    Body: 
    {body}""")
])

final_template = sentiment_classification_template.partial(format_instructions=format_instructions)

model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)
analysis_chain = final_template | model | parser

sample_email = { 
    "sender": "newsletter@promo.com", 
    "subject": "Great Work on the Presentation!", 
    "body": "Hi team, Just wanted to say that your presentation today was absolutely fantastic. The client loved it, and I’m really proud of the effort you all put in. Let’s keep this momentum going!" 
}

sample_email1 = { 
    "sender": "umarfayyaz@gmail.com", 
    "subject": "Great Report", 
    "body": "I reviewed the report you submitted, and it’s missing several critical sections. This has caused delays in our timeline, and I expect this to be addressed immediately. This is not up to standard." 
}

sample_email2 = { 
    "sender": "umarfayyaz@gmail.com", 
    "subject": "Meeting Scheduled for Thursday", 
    "body": "Hi all, The client meeting has been scheduled for Thursday at 2 PM. Please make sure to review the agenda beforehand. Let me know if you have any conflicts." 
}

try:
    result = analysis_chain.invoke(sample_email)       
    console.rule(f"[bold green]\n--- Sentiment Analysis Classification Result {result.sentiment}---") 
    print(f"Category: {result.sentiment}") 
    print(f"Justification: {result.justification}") 
    print(f"Type of result: {type(result)}") 

    result = analysis_chain.invoke(sample_email1)       
    console.rule(f"[bold green]\n--- Sentiment Analysis Classification Result {result.sentiment}---") 
    print(f"Category: {result.sentiment}") 
    print(f"Justification: {result.justification}") 
    print(f"Type of result: {type(result)}") 

    result = analysis_chain.invoke(sample_email2)       
    console.rule(f"[bold green]\n--- Sentiment Analysis Classification Result {result.sentiment}---") 
    print(f"Category: {result.sentiment}") 
    print(f"Justification: {result.justification}") 
    print(f"Type of result: {type(result)}") 
except Exception as e:
    print(f"Error during classification: {e}")