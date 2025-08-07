from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("Generate a report for {company} in the {quarter} of {year}.")

partial_template = template.partial(year="2025")

print("Original variables:", template.input_variables)  
print("Partial variables:", partial_template.input_variables)

# first_partial = partial_template.partial(quarter="Q2")

# print("Original variables:", partial_template.input_variables)  
# print("Partial variables:", first_partial.input_variables)

# print(first_partial.format(company="Quantum Leap Inc"))

# second_partial = first_partial.partial(company="Leap Inc")

# print("Original variables:", first_partial.input_variables)  
# print("Partial variables:", second_partial.input_variables)

# print(second_partial.format())

# print(first_partial.format(company="Quantum Leap Inc"))
