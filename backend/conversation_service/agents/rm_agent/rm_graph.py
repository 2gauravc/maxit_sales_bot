from langgraph.graph import StateGraph
from conversation_service.states.rm_states import RMAgentState
from conversation_service.agent_infrastructure.maxit_agent import MaxitAgent

# Import workflows (now independent)
from conversation_service.frameworks.peer_comparison_workflow import PeerComparisonWorkflow
from conversation_service.frameworks.debt_profiling_workflow import DebtProfilingWorkflow

def detect_framework(state: RMAgentState) -> RMAgentState:
    if "compare" in state["query"]:
        state["framework_id"] = "peer_comparison"
    else:
        state["framework_id"] = "debt_profiling"
    return state

def route_to_workflow(state: RMAgentState) -> RMAgentState:
    """
    Instead of wiring workflows statically, dynamically call the appropriate workflow based on framework_id.
    """
    framework = state.get("framework_id")
    if framework == "peer_comparison":
        workflow = PeerComparisonWorkflow() #Returns compiled graph 
    elif framework == "debt_profiling":
        workflow = DebtProfilingWorkflow() # Returns compiled graph 
    else:
        raise ValueError(f"Unknown workflow {framework}")

    # Invoke the workflow's compiled graph
    result_state = workflow.graph.invoke(state)

    # Merge results back into RM Agent state
    state["result"] = result_state
    return state

def finalize_response(state: RMAgentState) -> RMAgentState:
    return state

def build_rm_agent_graph(framework: str = "langgraph"):
    rm_graph_builder = StateGraph(RMAgentState)

    rm_graph_builder.add_node("detect_framework", detect_framework)
    rm_graph_builder.add_node("route_to_workflow", route_to_workflow)
    rm_graph_builder.add_node("finalize_response", finalize_response)

    rm_graph_builder.set_entry_point("detect_framework")
    rm_graph_builder.add_edge("detect_framework", "route_to_workflow")
    rm_graph_builder.add_edge("route_to_workflow", "finalize_response")
    rm_graph_builder.add_edge("finalize_response", "__end__")

    return rm_graph_builder.compile()

class RMMaxitAgent(MaxitAgent):
    def __init__(self, framework: str = "langgraph"):
        super().__init__(agent_type=framework, build_graph_func=build_rm_agent_graph)
