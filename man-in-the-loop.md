### Resumo do Fluxo de Dados

Ida: LangGraph -> Pausa -> Gera ID -> Salva Estado com ID -> Envia ID para o Teams.

Volta: Teams -> Ação do Usuário -> Envia ID para o Bot -> Bot usa ID para buscar Estado -> Atualiza Estado -> Reinvoca LangGraph com Estado atualizado.

Este padrão desacopla completamente a lógica do seu agente de IA da interface de usuário no Teams. O LangGraph não precisa saber nada sobre o Teams, e o Teams não precisa saber nada sobre o LangGraph. Sua aplicação principal atua como a cola que une os dois, usando o ID de Correlação como o elo.
