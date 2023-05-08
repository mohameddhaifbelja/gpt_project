import os
from typing import List
import json


def create_files(parent_folder: str, files: List[str]):
    """ Create files inside a parent folder"""
    files = [os.path.join(parent_folder, file) for file in files]

    for path in files:

        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        f = open(path, "w")


def text_to_json(text):
    # Remove the outer curly braces
    text = text.strip()[1:-1]
    text = text.replace('\n', '')
    # Split the text into a list of file entry strings
    file_entries = text.split("},")

    # Iterate through file entries and convert them to dictionaries
    file_dicts = []
    for entry in file_entries:
        entry = entry.strip()
        if entry[-1] != '}':
            entry += '}'

        file_dict = json.loads(entry)
        file_dicts.append(file_dict)

    # Save the list of dictionaries as a JSON file
    with open("project_structure.json", "w") as json_file:
        json.dump(file_dicts, json_file, indent=4)


def read_json(file_path="project_structure.json"):
    with open(file_path) as f:
        content = f.read()
    with open(file_path) as f:
        data = json.load(f)
    if not isinstance(data, list):
        return [], content

    return data, content

import ast

def get_functions_with_docstrings(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    functions_with_docstrings = []
    for node in ast.walk(ast.parse(file_contents)):
        if isinstance(node, ast.FunctionDef):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):

                functions_with_docstrings.append((node.name, node.body[0].value.s.strip()))
    return functions_with_docstrings

def post_process_pseudo_code(code):
    """
    Clean the code
    :param code:
    :return:
    """

    code = code.strip().split('\n')
    if code[0].startswith('```'):
        code = code[1:]
    if code[-1].startswith('```'):
        code = code[:-2]

    code = "\n".join(code)
    return code

if __name__ == "__main__":
    print(get_functions_with_docstrings("project1/app/csv_processor.py"))
