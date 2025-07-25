import tiktoken 

def count_tokens(text: str, model_name: str = "gpt-4o-mini")->int:
    """Returns the number of tokens in a text string for a_given model.""" 
    try:
        # For gpt-4o-mini, gpt-4o, gpt-4, gpt-3.5-turbo, text-embedding-3-small/large 
        # the encoding is 'cl100k_base'. 
        # Using encoding_for_model is generally safer as tiktoken updates. 
        encoding = tiktoken.encoding_for_model(model_name) 
    except KeyError:
        print(f"Warning: Model {model_name} not found in tiktoken. Using cl100k_base as a fallback.") 
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = len(encoding.encode(text))
    return num_tokens

my_prompt_text = "The wind whispered through the trees, carrying the scent of rain. Birds chirped softly, hidden among the branches. Leaves rustled underfoot as I walked the quiet path. A squirrel darted past, vanishing into the bushes. Peace settled over the forest, wrapping everything in a gentle, calming stillness. I smiled, content." 
token_count = count_tokens(my_prompt_text) 
print(f"The text '{my_prompt_text}' has approximately {token_count} tokens for gpt-4o-mini.") 


# For ChatCompletions, remember that the actual prompt token count also includes 
# tokens for roles, message structures, etc. Tiktoken on raw text is an estimate. 
# OpenAI's cookbook has more precise methods for chat messages. 
# For a rough estimate of a user message: 
# tokens_per_message = 3  
# tokens_per_name = 1 (if using name field) 
# actual_tokens = count_tokens(message_content) + tokens_per_message 
