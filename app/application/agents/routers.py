from app.domain.email import Email
from app.application.agents.state.email_analysis_state import EmailAnalysisState

class OrchestratorRouter:
    def route_orchestrator(self, state: EmailAnalysisState) -> str:
        next_step = state.get("next_step")

        if not next_step:
            return "DEFAULT_END"
        
        return next_step