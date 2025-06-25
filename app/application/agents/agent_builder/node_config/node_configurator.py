from langgraph.graph import StateGraph
from app.application.agents.node_functions.classify_node.classify_node import classify_node
from app.application.agents.node_functions.format_template_node.format_template_node import format_template_node
from app.application.agents.node_functions.orchestrator_node.orchestrator_node import orchestrator_node
from app.application.agents.node_functions.task_extraction_node.task_extraction_node import task_extraction_node
from app.application.agents.tools.delta_api_tool import create_task_in_delta

from langgraph.prebuilt import ToolNode

from app.application.agents.tools.planner_api_tool import create_task_in_planner


tool_node = ToolNode([create_task_in_delta, create_task_in_planner])

class EmailNodeConfigurator:

    @staticmethod
    def configure_nodes(workflow: StateGraph):
        workflow.add_node("ORCHESTRATOR_NODE", orchestrator_node)
        workflow.add_node("CLASSIFY_NODE", classify_node)
        workflow.add_node("TASK_EXTRACT_NODE", task_extraction_node)
        workflow.add_node("FORMAT_TEMPLATE_NODE", format_template_node)
        workflow.add_node("TOOL_NODE", tool_node)
        # workflow.add_node("EXTRACT_TASKS_NODE", task_extraction_node)