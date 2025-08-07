from langchain.memory import ConversationBufferWindowMemory

window_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)

window_memory.save_context(
    {"input": "Hi, I'm Bob."},  
    {"output": "Hello Bob! How can I help you today?"} 
)

window_memory.save_context( 
    {"input": "What's my name?"}, 
    {"output": "Your name is Bob."} 
) 

memory_variable = window_memory.load_memory_variables({}) 
print(memory_variable)