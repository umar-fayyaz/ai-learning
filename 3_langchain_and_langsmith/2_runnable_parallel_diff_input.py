from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

str_parser = StrOutputParser()

question_chain = ChatPromptTemplate.from_template("Generate a concise question about {topic}.") | llm | str_parser

facts_chain = ChatPromptTemplate.from_template("List two brief, important facts about {topic}.") | llm | str_parser

combine_chain_with_assign = RunnablePassthrough.assign(
    question = question_chain,
    facts = facts_chain
    )

console = Console()

initial_input= {"topic": "Large Language Models"}

results = combine_chain_with_assign.invoke(initial_input)
console.rule("[bold blue]---First Response---")
print(results)

final_prompt = ChatPromptTemplate.from_template( 
    "Original Topic: {topic}\n\n" 
    "Generated Question: {question}\n\n" 
    "Generated Facts: {facts}\n\n" 
    "Provide a one-sentence synthesis of this information." 
)

full_synthesis_chain = combine_chain_with_assign | final_prompt | llm | str_parser 

synthesis_output = full_synthesis_chain.invoke({"topic": "CRISPR gene editing"}) 

console.rule("[bold blue]---Final Response---")

print(synthesis_output) 