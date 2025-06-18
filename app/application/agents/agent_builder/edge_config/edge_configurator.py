from langgraph.graph import StateGraph, END, START
from app.application.agents.agent_builder.routers import OrchestratorRouter
from app.application.agents.state.email_analysis_state import EmailAnalysisState

from langgraph.prebuilt import ToolNode


def should_continue(state: EmailAnalysisState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "TOOL_NODE"
    return END

class EmailEdgeConfigurator:

    @staticmethod
    def configure_edges(workflow: StateGraph, routers: OrchestratorRouter):
        workflow.add_edge(START, "ORCHESTRATOR_NODE")
        # workflow.add_edge("ORCHESTRATOR_NODE", "CLASSIFY_NODE")
        workflow.add_conditional_edges("ORCHESTRATOR_NODE", should_continue, ["TOOL_NODE", END])

        workflow.add_edge("TOOL_NODE", "ORCHESTRATOR_NODE")
                