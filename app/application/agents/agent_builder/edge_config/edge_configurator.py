from langgraph.graph import StateGraph, END
from app.application.agents.agent_builder.routers import OrchestratorRouter


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
                # "SEND_TASK": "SEND_TASK_NODE",
                "DEFAULT_END": END,
            }
        )
        workflow.add_edge("EXTRACT_TASKS_NODE", "ORCHESTRATOR_NODE")