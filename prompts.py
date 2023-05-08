from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# The first prompts in the chain
architect_system_prompt = SystemMessage(content=
                                        """you are a senior software architect, with deep knowledge in the field of 
                                        Artificial intelligence. when you are given a project description, 
                                        you output the architecture of the project: folders containing script files, 
                                        and you give a description of the functionalities in each file.  You 
                                        . your output must follow a json format:
                                        - [
                                            { "file_name": file_name,
                                            "description": description,
                                            "dependencies": list of files that the current file depends on.
                                            },
                                            ]


preferred technologies: python, HTML, CSS, fast API, js, openai
                                            
                                        """
                                        )

# Give one example so the LLM's output would be in the correct format
architect_userex_prompt = HumanMessage(content="""

project description: a web application to summarize input text

""")


architect_aiex_prompt = AIMessage(content="""
{
{"file_name": "requirements.txt",
"description":"Contains the required libraries and their versions for the project."
},

{"file_name": "app/main.py",
"description": "Initializes FastAPI application, defines the API routes and handles the incoming requests to summarize the text."
}
}
""")

architect_user_prompt = HumanMessagePromptTemplate.from_template(template="project description: {description}")

architect_chat = ChatPromptTemplate.from_messages([architect_system_prompt,
                                                    architect_user_prompt])


pseudo_developer_system = SystemMessage(content=
                                        """you are a talented software developer with deep knowledge in AI, 
python scripting, web development, and mobile development. when given a project description, the project's structure, 
current filename, and description. You define all the function headers in the file_name with their corresponding 
docstring. no implementation. your output is only the content of the file and nothing else. """
                                        )

pseudo_developer_user = HumanMessagePromptTemplate.from_template(template="""project description: {description}
project structure: {structure}
current file name: {file_name}
current file description: {file_description}
""")

pseudo_developer_chat = ChatPromptTemplate.from_messages([pseudo_developer_system, pseudo_developer_user])