from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot that provides creative recipes. You should respond in a cheerful tone."),
    ("human", "I have these ingredients: {ingredients}. What can I make?")
])

formatted_messages = chat_template.format_messages(ingredients="chicken, rice, and broccoli")

print(formatted_messages)