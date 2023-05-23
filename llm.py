import os

from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from utils import text_to_json, read_json, create_files, post_process_pseudo_code
from prompts import architect_chat, pseudo_developer_chat

llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key="",
    model_name="gpt-4"
)


def generate_architecture(description: str):
    result = llm(architect_chat.format_prompt(description=description).to_messages()).content
    text_to_json(result)


def generate_pseudo_code(description: str, structure: str, current_file: str, current_description: str):
    result = llm(
        pseudo_developer_chat.format_prompt(description=description, structure=structure, file_name=current_file,
                                            file_description=current_description).to_messages()).content
    return result

def write_pseudo_code(description, project_name):
    files_list, structure = read_json()

    create_files(parent_folder=project_name, files=[ file['file_name'] for file in files_list])
    for file in files_list:

        # Requirements will be treated in a special manner
        if 'requirements.txt' in file['file_name']:
            print('requirements is skipped!')
            pass
        print(file)
        code = generate_pseudo_code(description= description, structure= structure, current_file = file['file_name'], current_description=file['description'] )
        with open(os.path.join(project_name,file['file_name']),'w') as f:
            code = post_process_pseudo_code(code)
            f.write(code)

    return True

if __name__ == "__main__":

    description = "A web application that has an input box, after a person submit his input, the application returns a summary of the input"
    generate_architecture(description=description)
    write_pseudo_code(description= description, project_name="project3")
