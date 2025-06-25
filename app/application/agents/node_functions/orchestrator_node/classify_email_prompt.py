from langchain_core.prompts import ChatPromptTemplate


CLASSIFY_EMAIL_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Você é um especialista em análise de e-mails.
    Sua tarefa é analisar  o e-mail e identificar se o e-mail contém possíveis tarefas.

    O e-mail é o seguinte:
    {email}

    Retorne uma resposta curta e direta, apenas TASK ou NOT_TASK.

    Importante:
    - O conteúdo do e-mail pode vir em idiomas como português, inglês, espanhol.
    
    """
)