from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

system_instruction = SystemMessage(
    content="You are a helpful assistant that translates English to French."
)

user_request = HumanMessage(
    content="I love programming."
)

ai_example_response = AIMessage(
    content="J'adore la programmation."
)

tool_call_output = ToolMessage( 
    content="5",  # The result of the tool call 
    tool_call_id="call_abc123" # An ID to match the tool call request from the AI 
) 

conversation = [system_instruction, user_request, ai_example_response, tool_call_output] 

print(conversation)