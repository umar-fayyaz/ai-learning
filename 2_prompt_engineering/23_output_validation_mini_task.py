# import asyncio
# from async_config import client
from rich.console import Console
from rich.markdown import Markdown
import json
from jsonschema import validate, ValidationError,FormatChecker

console = Console()

USER_PROFILE_SCHEMA = { 
    "type": "object", 
    "properties": { 
    "name": {"type": "string", "minLength": 1}, 
            "email": {"type": "string", "format": "email"}, 
            "age": {"type": "number", "minimum": 19} # Must be > 18, so minimum 19 
        }, 
        "required": ["name", "email", "age"] 
} 

def validate_user_profile(profile_json_string:str,schema:dict)->bool:
    try:
        profile_data = json.loads(profile_json_string)
        validate(instance=profile_data, schema=schema,format_checker=FormatChecker())
        console.print(Markdown(f"Profile '{profile_json_string}' is VALID"))
        return True
    except json.JSONDecodeError:
        print(f"Profile '{profile_json_string}' is NOT valid JSON")
        return False
    
    except ValidationError as e:
        print(f"Profile '{profile_json_string}' FAILED SCHEMA VALIDATION: {e}")
        return False
    
valid_profile_str = '{"name": "Alice Wonderland", "email": "alice@example.com", "age": 30}' 
invalid_profile_str_bad_email = '{"name": "Bob The Builder", "email": "bob@", "age": 25}' # Bad email format 
invalid_profile_str_young_age = '{"name": "Charlie Brown", "email": "charlie@example.com", "age": 18}' # Age too young 
invalid_profile_str_missing_field = '{"name": "Diana Prince", "email": "diana@example.com"}' # Missing age

console.rule(f"[bold green]--- Testing User Profile Validation ---")

console.rule("[yellow]Test Case 1")
validate_user_profile(valid_profile_str, USER_PROFILE_SCHEMA)

console.rule("[yellow]Test Case 2")
validate_user_profile(invalid_profile_str_bad_email, USER_PROFILE_SCHEMA)

console.rule("[yellow]Test Case 3")
validate_user_profile(invalid_profile_str_young_age, USER_PROFILE_SCHEMA)

console.rule("[yellow]Test Case 4")
validate_user_profile(invalid_profile_str_missing_field, USER_PROFILE_SCHEMA)