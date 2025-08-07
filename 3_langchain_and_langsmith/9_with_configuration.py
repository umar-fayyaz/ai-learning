from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
# import asyncio


from dotenv import load_dotenv
load_dotenv()
console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

string_parser = StrOutputParser()

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner.")

explanation_chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)

configured_explanation_chain = explanation_chain.with_config( 
    tags=["explanation_module", "v1.0"], 
    metadata={"source_script": "section_3_1_2_example_2.py"} 
) 

try:
    console.rule("\n[bold blue]--- Invoke with Config ---")
    result_with_config = configured_explanation_chain.invoke( 
        {"user_topic": "data science"}, 
        config={"metadata": {"invocation_specific": True, "user_id": "test_user_002"}} 
    )
    print(f"Result (check LangSmith for tags/metadata): {result_with_config}") 

    configured_batch_chain = explanation_chain.with_config(max_concurrency=2) 

    inputs_for_configured_batch = [       
        {"user_topic": "ai"}, {"user_topic": "ml"},
        {"user_topic": "dev ops"}, {"user_topic": "mlops"} 
    ]
    
    batch_results_configured = configured_batch_chain.batch(inputs_for_configured_batch)
    
    print("\nBatch results with configured max_concurrency=2 (behavioral, not printed output)") 
    print(batch_results_configured)

except Exception as e:
    print(f"Error during sync invocation (ensure API key is set): {e}")