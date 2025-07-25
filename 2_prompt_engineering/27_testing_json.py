import json 
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def load_and_print_specific_prompt(filepath, variant_name, field_to_print="user_template"): 
    try: 
        with open(filepath, "r") as f:
            prompts =json.load(f)

            if variant_name in prompts: 
                if field_to_print in prompts[variant_name]: 
                    console.rule(f"[italic yellow on white]--- {field_to_print} for '{variant_name}' ---") 
                    console.print(Markdown(prompts[variant_name][field_to_print])) 
                else: 
                    console.print(Markdown(f"Field '{field_to_print}' not found in variant '{variant_name}'.")) 
            else: 
                console.print(Markdown(f"Variant '{variant_name}' not found in '{filepath}'."))
        
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")



# Assuming you created "my_qa_prompts.json" with the example content. 
# If not, create it first before running this. For example: 
# example_qa_prompts = { 
#   "QA_Direct": { "user_template": "Context: {context}\n\nQuestion: {question}\n\nAnswer:" }, 
#   "QA_RolePlay_Expert": { "system": "You are an expert.", "user_template": "Context: {context}\n\nQuestion: {question}" } 
# } 
# with open("my_qa_prompts.json", "w") as f: 
#    json.dump(example_qa_prompts, f, indent=2) 

load_and_print_specific_prompt("2_prompt_engineering/27_testing_json/my_qa_prompts.json", "QA_RolePlay_Expert") 
load_and_print_specific_prompt("2_prompt_engineering/27_testing_json/my_qa_prompts.json", "QA_Direct", "user_template") 



