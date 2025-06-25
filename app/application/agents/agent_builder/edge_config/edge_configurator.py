from langgraph.graph import StateGraph, END, START
from app.application.agents.agent_builder.routers import Router
from app.application.agents.state.email_analysis_state import EmailAnalysisState

def should_continue(state: EmailAnalysisState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "TOOL_NODE"
    return END

class EmailEdgeConfigurator:

    @staticmethod
    def configure_edges(workflow: StateGraph, router: Router):
        workflow.add_edge(START, "ORCHESTRATOR_NODE")
        workflow.add_edge("ORCHESTRATOR_NODE", "CLASSIFY_NODE")

        workflow.add_conditional_edges(
            "CLASSIFY_NODE", 
            router.graph_router,
            {
                "TASK": "TASK_EXTRACT_NODE",
                "NOT_TASK": END
            }
        )
        workflow.add_edge("TASK_EXTRACT_NODE", "FORMAT_TEMPLATE_NODE")
        # workflow.add_edge("FORMAT_TEMPLATE_NODE", END)

        workflow.add_conditional_edges("FORMAT_TEMPLATE_NODE", should_continue, ["TOOL_NODE", END])

        workflow.add_edge("TOOL_NODE", "FORMAT_TEMPLATE_NODE")
                