from app.domain.email import Email
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from langgraph.graph import END

class Router:
    def graph_router(self, state: EmailAnalysisState) -> str:
        next_step = state.get("next_step")
        
        if not next_step:
            return "DEFAULT_END"
        
        return next_step
    
    def tool_router(self, state: EmailAnalysisState):
        messages = state["messages"]

        last_message = messages[-1]
        
        if last_message.tool_calls:
            return "TOOL_NODE"
        return END