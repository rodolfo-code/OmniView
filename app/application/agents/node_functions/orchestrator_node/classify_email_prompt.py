from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

system_prompt_text = """
    Você é um assistente de produtividade que vai me ajudar no meu trabalho.
    Você é o melhor do mundo no que você faz.

    Suas regras de ouro:
    1. Seja proativo use a ferramenta de calculadora para calcular o resultado de operações aritméticas.
    2. Use suas ferramentas: você tem acesso as ferramentas que você pode usar para ajudar você a calcular o resultado das operações aritméticas `calculator_tool` e divisão `divide_tool`.

""" 

CALCULATOR_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_text),
        MessagesPlaceholder(variable_name="messages")        
    ]
)


CLASSIFY_EMAIL_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Você é um especialista em análise de e-mails.
    Sua tarefa é analisar  o e-mail e identificar se o e-mail contém possíveis tarefas.

    O e-mail é o seguinte:
    {email}

    Retorne uma resposta curta e direta, apenas true ou false.

    Importante:
    - O conteúdo do e-mail pode vir em idiomas como português, inglês, espanhol.
    
    """
)