from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

question_prompt = ChatPromptTemplate.from_template("Generate a concise question about {topic}.")

fasts_prommpt = ChatPromptTemplate.from_template("List two brief, important facts about {topic}.")

parallel_chain = RunnableParallel(
    question = question_prompt | llm,
    facts = fasts_prommpt | llm
)
console = Console()
results = parallel_chain.invoke({"topic":"AI safety"})
print(results)
# console.print(Markdown(f"Question: {results['question'].content}"))
# console.print(Markdown(f"Answer: {results['facts'].content}"))