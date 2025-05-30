from typing import TypedDict
from app.domain.email import Email
from langgraph.graph import StateGraph, END

from app.application.agents.node_functions.email_processing_summarize_node import summarize_node
from app.application.agents.node_functions.email_processing_categorize_node import categorize_node
from app.application.agents.node_functions.email_processing_action_items_node import action_items_node
from app.application.agents.state.email_analysis_state import EmailAnalysisState


class EmailAgentBuilder:
    """
    Classe para construir o agente de análise de email.
    """

    def __init__(self):
        """
        Inicializa e constrói o grafo do agente de análise de email.
        """
        self.workflow = StateGraph(EmailAnalysisState)

        self._build_graph()

        self.app = self.workflow.compile()

    def _build_graph(self):
        """
        Adiciona os nós e define as arestas para o workflow do agente.
        """
        self._build_node()
        self.workflow.set_entry_point("summarizer")
        self._build_edges()     

    def _build_node(self):
        """
        Adiciona os nós.
        """
        self.workflow.add_node("summarizer", summarize_node)
        self.workflow.add_node("categorizer", categorize_node)
        self.workflow.add_node("action_items_extractor", action_items_node)

    def _build_edges(self):
        """
        Adiciona as arestas.
        """
        self.workflow.add_edge("summarizer", "categorizer")
        self.workflow.add_edge("categorizer", "action_items_extractor")
        self.workflow.add_edge("action_items_extractor", END) 

    def get_app(self):
        """
        Retorna o aplicativo compilado do agente de análise de email.
        """
        return self.app









