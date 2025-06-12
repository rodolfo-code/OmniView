from langgraph.graph import StateGraph, END
from app.application.agents.routers import OrchestratorRouter


class EmailEdgeConfigurator:

    @staticmethod
    def configure_edges(workflow: StateGraph, routers: OrchestratorRouter):
        workflow.add_conditional_edges(
            "ORCHESTRATOR_NODE",
            routers.route_orchestrator,
            {
                "TASK": "EXTRACT_TASKS_NODE",
                "NOT_TASK": END,
                "UNCERTAIN": END,
                "DEFAULT_END": END,
            }
        )