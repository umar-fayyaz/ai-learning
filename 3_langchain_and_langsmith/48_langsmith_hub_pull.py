from langchain import hub
from dotenv import load_dotenv

load_dotenv()

prompt = hub.pull("hwchase17/react")  

print(prompt)

