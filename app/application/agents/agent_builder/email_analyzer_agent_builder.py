from typing import TypedDict
from app.application.agents.agent_builder.edge_config.edge_configurator import EmailEdgeConfigurator
from app.application.agents.agent_builder.node_config.node_configurator import EmailNodeConfigurator
from app.application.agents.routers import OrchestratorRouter
from app.domain.email import Email
from langgraph.graph import StateGraph, END

from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.application.agents.node_functions.task_extraction_node.task_extraction_node import task_extraction_node
from app.application.agents.node_functions.orchestrator_node.orchestrator_node import orchestrator_node


class EmailAgentBuilder:

    def __init__(self):
        """
        Inicializa e constrói o grafo do agente de análise de email.
        """
        self.routers = OrchestratorRouter()
        self.workflow = StateGraph(EmailAnalysisState)

        self.node_configurator = EmailNodeConfigurator()
        self.edge_configurator = EmailEdgeConfigurator()

        self._build_graph()
        self._build_agent = self.workflow.compile()

    def _build_graph(self):
        """
        Adiciona os nós e define as arestas para o workflow do agente.
        """
        self.node_configurator.configure_nodes(self.workflow)

        self.workflow.set_entry_point("ORCHESTRATOR_NODE")
        
        self.edge_configurator.configure_edges(self.workflow, self.routers)

    def build_agent(self):
        print(self._build_agent.get_graph().draw_mermaid())
        return self._build_agent










