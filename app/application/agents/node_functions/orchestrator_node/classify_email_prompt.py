from langchain_core.prompts import ChatPromptTemplate

CLASSIFY_EMAIL_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Você é um sistema de triagem de e-mails para um conjunto de agentes de IA, processando comunicações que chegam de clientes para as equipes de Comunicação ou Desenvolvimento. Sua tarefa é analisar o conteúdo de cada e-mail e classificá-lo rigorosamente em uma das três categorias abaixo. Sua decisão determinará o próximo nó (ou agente) para onde o e-mail será direcionado.

    **Categorias de Classificação:**

    1.  **TAREFA:** O e-mail do cliente contém uma solicitação clara e direta para que uma ação seja realizada pelas equipes de Comunicação ou Desenvolvimento. Inclui um entregável explícito ou implícito (como uma funcionalidade, correção, material de comunicação) e detalhes suficientes para iniciar o trabalho ou abrir um ticket.
        * **Indicadores-chave:** Pedidos de "nova funcionalidade X", "corrigir bug Y", "precisamos de material de comunicação sobre Z", "desenvolver integração com W", "realizar análise de A". Geralmente vêm com alguma descrição do problema ou da necessidade.
    2.  **NAO_TAREFA:** O e-mail do cliente é meramente informativo, um agradecimento, uma notificação, um feedback geral (que não exige ação imediata de desenvolvimento ou comunicação), um convite para discussão não relacionada a um projeto específico, ou qualquer comunicação que não exija um entregável ou uma ação imediata das equipes.
        * **Indicadores-chave:** "Obrigado pelo suporte", "Recebemos sua mensagem", "Nosso sistema está funcionando bem", "Feedback: achamos interessante X", "Convidando para um webinar" (sem solicitação de ação).
    3.  **INCERTEZA:** O e-mail do cliente sugere uma possível necessidade ou problema que pode se transformar em uma tarefa, mas a solicitação é ambígua, faltam detalhes cruciais, o contexto é insuficiente, ou a mensagem exige mais esclarecimentos da parte do cliente para que as equipes possam atuar.
        * **Indicadores-chave:** Linguagem vaga (ex: "temos um problema com o sistema", "precisamos de algo parecido com...", "gostaríamos de discutir uma ideia", "o que podemos fazer sobre..."), pedidos de status que não levam a uma ação clara, ou e-mails que claramente demandam um contato inicial para entender a real necessidade.

    Seu retorno deve ser **APENAS uma das três categorias**:
    TASK
    NOT_TASK
    UNCERTAIN
    

    O e-mail é o seguinte:
    {email}


    """
)

# CLASSIFY_EMAIL_TEMPLATE = ChatPromptTemplate.from_template(
#     """
#     Você é um especialista em análise de e-mails.
#     Sua tarefa é analisar  o e-mail e identificar se o e-mail contém possíveis tarefas.

#     O e-mail é o seguinte:
#     {email}

#     Retorne uma resposta curta e direta, apenas true ou false.

#     Importante:
#     - O conteúdo do e-mail pode vir em idiomas como português, inglês, espanhol.
    
#     """
# )