from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

system_prompt_text = """
    Você é um assistente de produtividade que vai me ajudar a inserir tarefas.
    Eu preciso criar uma lista de tarefas. Por favor, use as ferramentas disponíveis para gerar e organizar essas tarefas.
    Você é o melhor do mundo no que você faz.

    Suas regras de ouro:
    1. Seja proativo use a ferramenta de inserção de tarefas.
    2. Use suas ferramentas: você tem acesso as ferramentas que você pode usar para ajudar você a inserir tarefas `create_task_in_delta` e `create_task_in_planner`.

""" 

INSERT_TASKS_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_text),
        MessagesPlaceholder(variable_name="messages")        
    ]
)