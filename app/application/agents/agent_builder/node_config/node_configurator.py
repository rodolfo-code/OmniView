from langgraph.graph import StateGraph
from app.application.agents.node_functions.orchestrator_node.orchestrator_node import orchestrator_node
from app.application.agents.node_functions.task_extraction_node.task_extraction_node import task_extraction_node


class EmailNodeConfigurator:

    @staticmethod
    def configure_nodes(workflow: StateGraph):
        workflow.add_node("ORCHESTRATOR_NODE", orchestrator_node)
        workflow.add_node("EXTRACT_TASKS_NODE", task_extraction_node)