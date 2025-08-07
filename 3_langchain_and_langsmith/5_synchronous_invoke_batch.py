from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner.")

string_parser = StrOutputParser()

explanation_chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)

# Synchronous single invoke
try:
    resul_single = explanation_chain.invoke({"user_topic": "artificial intelligence"})
    print("-----Single Invoke-----")
    print(resul_single)
except Exception as e:
    print(f"Error during sync invocation (ensure API key is set): {e}")

input_batch = [
    {"user_topic": "machine learning"}, 
    {"user_topic": "deep learning"}, 
    {"user_topic": "neural networks"} 
]

try:
    result_batch = explanation_chain.batch(input_batch)
    print("-----Batch Invoke-----")
    print(result_batch)
except Exception as e:
    print(f"Error during batch invocation (ensure API key is set): {e}")


# Batch invocation with error handling 
inputs_with_potential_error = [ 
    {"user_topic": "reinforcement learning"}, 
    {"malformed_input_key": "this will likely cause an error in the prompt template"},
    {"user_topic": "reinforcement learning"}
] 
try: 
    results_with_error_handling = explanation_chain.batch( 
        inputs_with_potential_error, 
        return_exceptions=True 
    ) 

    print("\nBatch with Error Handling Results:") 
    for res in results_with_error_handling: 
        if isinstance(res, Exception): 
            print(f"Encountered an error: {res}") 
        else: 
            print(f"Success: {res[:50]}...") 
except Exception as e: 
    # This top-level try-except might catch issues with batch setup itself 
    print(f"Overall error in batch with error handling: {e}") 
