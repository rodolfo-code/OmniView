from langgraph.graph import StateGraph
from app.application.agents.node_functions.classify_node.classify_node import classify_node
from app.application.agents.node_functions.orchestrator_node.orchestrator_node import orchestrator_node
from app.application.agents.node_functions.task_extraction_node.task_extraction_node import task_extraction_node

from langgraph.prebuilt import ToolNode

from app.application.agents.tools.calculator_tool import calculator_tool, divide_tool

tool_node = ToolNode([calculator_tool, divide_tool])

class EmailNodeConfigurator:

    @staticmethod
    def configure_nodes(workflow: StateGraph):
        workflow.add_node("ORCHESTRATOR_NODE", orchestrator_node)
        # workflow.add_node("CLASSIFY_NODE", classify_node)
        workflow.add_node("TOOL_NODE", tool_node)
        # workflow.add_node("EXTRACT_TASKS_NODE", task_extraction_node)