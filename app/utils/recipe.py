import re

def get_ingredients_list(ingredients):
    return [item.strip() for item in ingredients.split(',')]

def get_instructions_list(instructions):
    instructions = re.split(r'\.\s*,\s*',   instructions.strip())
    return [i if i.endswith('.') else i + '.' for i in instructions]
