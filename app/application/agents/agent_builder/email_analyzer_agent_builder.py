from app.application.agents.agent_builder.edge_config.edge_configurator import EmailEdgeConfigurator
from app.application.agents.agent_builder.node_config.node_configurator import EmailNodeConfigurator
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.application.agents.agent_builder.routers import Router
from langgraph.graph import StateGraph



class EmailAgentBuilder:

    def __init__(self):
        self.routers = Router()
        self.workflow = StateGraph(EmailAnalysisState)

        self.node_configurator = EmailNodeConfigurator()
        self.edge_configurator = EmailEdgeConfigurator()

        self._build_graph()
        self._build_agent = self.workflow.compile()

    def _build_graph(self):
        self.node_configurator.configure_nodes(self.workflow)

        self.workflow.set_entry_point("ORCHESTRATOR_NODE")

        self.edge_configurator.configure_edges(self.workflow, self.routers)

    def build_agent(self):
        print(self._build_agent.get_graph().draw_mermaid())
        return self._build_agent


def get_email_analyzer_agent():
    builder = EmailAgentBuilder()
    agent = builder.build_agent()
    return agent





