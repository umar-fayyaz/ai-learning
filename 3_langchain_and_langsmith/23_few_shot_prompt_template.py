from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

examples = [
    {
        "input":"A happy sentence.",
        "output":"The sun is shining and the birds are singing."
    },
    { 
        "input": "A sad sentence.", 
        "output": "The rain fell gently on the empty streets." 
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a master of writing sentences with a specific mood. Emulate the user's examples."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

formatted_chat_prompt = final_prompt.format(input="An excited sentence.") 
print(formatted_chat_prompt) 