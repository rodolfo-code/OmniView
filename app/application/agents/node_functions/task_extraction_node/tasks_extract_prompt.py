from langchain_core.prompts import ChatPromptTemplate

TASKS_EXTRACT_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Você é um assistente especializado em extrair tarefas de emails.
    
    Analise o conteúdo do email fornecido e extraia todas as possíveis tarefas identificadas.
    Para cada tarefa, forneça:
    - Um título conciso
    - Uma descrição detalhada
    - A empresa envolvida (se mencionada)
    - A pessoa responsável (se mencionada)

    Email para análise:
    {email_content}

    Retorne um JSON com a seguinte estrutura para cada tarefa identificada:
    {{
        "title": "título da tarefa",
        "description": "descrição detalhada",
        "sender": "remetente",
        "company": "empresa remetente",
        "in_charge": "pessoa responsável"
    }}

    Se não for possível identificar algum dos campos, use "Não especificado".
    Retorne um array de tarefas, mesmo que encontre apenas uma.

    Lembre-se:
    - Seja específico e detalhado nas descrições
    - Mantenha os títulos concisos
    - Identifique claramente responsáveis e empresas quando mencionados
    - Considere prazos e prioridades mencionados no email

    Importante:
    - O remetente é a pessoa que enviou o email
    - Retorne apenas o JSON com as tarefas identificadas
    - NÃO inclua ```json ou qualquer outra formatação markdown
    - Retorne APENAS o JSON puro
    - O in_charge é a pessoa que recebeu o email
    - O sender é a pessoa que enviou o email
    - O company é a empresa da pessoa que enviou o email
    """
)