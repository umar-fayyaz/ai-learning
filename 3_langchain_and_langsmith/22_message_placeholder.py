from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

chat_template_with_history = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant. Answer the user's questions."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{user_input}")
])

conversation_history = [
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="Paris is the capital of France.")
]

final_message = chat_template_with_history.format_messages(
    history=conversation_history,
    user_input="What is a famous landmark there"
)

print(final_message)