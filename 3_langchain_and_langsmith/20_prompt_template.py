from langchain_core.prompts import PromptTemplate

template_string = "Write a one sentence witty summary of the following topic: {topic}"
llm_prompt = PromptTemplate.from_template(template_string)

print(f"Input variables: {llm_prompt.input_variables}")

formatted_prompt = llm_prompt.format(topic="Large Language Models")

print(f"Formatted Prompt: {formatted_prompt}")