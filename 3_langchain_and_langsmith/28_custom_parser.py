from langchain_core.output_parsers import BaseOutputParser
from typing import Dict, Any

class KeyValueParser(BaseOutputParser):
    """Parses a simple key: value format, one per line.""" 

    def parse(self, text: str) -> Dict[str, Any]:
        lines = text.strip().split('\n')
        parsed_dict = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_dict[key.strip()] = value.strip()
        return parsed_dict
    
    def get_format_instructions(self) -> str:
        """Instructions for the LLM.""" 

        return "Your response must be a list of key-value pairs, with each pair on a new line. For example:\n\nName: John Doe\nAge: 30"
    
custom_parser = KeyValueParser()

print(custom_parser.get_format_instructions())
print(custom_parser.parse("Name: John Doe\nAge: 30"))