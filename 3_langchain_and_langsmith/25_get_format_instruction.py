from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field 
from enum import Enum

from dotenv import load_dotenv
load_dotenv()

class EmailCategory(str, Enum):
    PRIMARY = "Primary" 
    SPAM = "Spam" 
    ACTIONABLE = "Actionable" 
    PROMOTIONAL = "Promotional" 

class SimpleClassification(BaseModel):
    category: EmailCategory = Field(description="The main classification of the email.")
    confidence:float = Field(description="A confidence score between 0.0 to 1.0 for the classification")

parser = PydanticOutputParser(pydantic_object=SimpleClassification)

format_instructions = parser.get_format_instructions()
print(format_instructions)

email_classification_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert email analysis assistant. Your task is to analyze an 
    email and classify it into one of the following categories: Primary, Spam, Actionable, or 
    Promotional. 
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

final_prompt_template = email_classification_template.partial(format_instructions=format_instructions)

model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)
classification_chain = final_prompt_template | model | parser

sample_email = { 
    "sender": "newsletter@promo.com", 
    "subject": " 🔥 50% OFF EVERYTHING! Don't Miss Out!", 
    "body": "Our biggest sale of the year is here! Click now to shop deals on all your favorite products. This offer ends Friday." 
}

try:
    result = classification_chain.invoke(sample_email)       
    print("\n--- Email Classification Result ---") 
    print(f"Category: {result.category}") 
    print(f"Confidence: {result.confidence}") 
    print(f"Type of result: {type(result)}") 
except Exception as e:
    print(f"Error during classification: {e}")