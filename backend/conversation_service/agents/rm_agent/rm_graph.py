from langgraph.graph import StateGraph
from conversation_service.states.rm_states import RMAgentState
from conversation_service.agents.rm_agent.peer_comparison_graph import PeerComparisonGraph
from conversation_service.agents.rm_agent.debt_profiling_graph import DebtProfilingGraph
from conversation_service.frameworks.maxit_agent import MaxitAgent

def detect_framework(state: RMAgentState) -> RMAgentState:
    if "compare" in state["query"]:
        state["framework_id"] = "peer_comparison"
    else:
        state["framework_id"] = "debt_profiling"
    return state

def route_to_subgraph(state: RMAgentState) -> str:
    return state["framework_id"]

def finalize_response(state: RMAgentState) -> RMAgentState:
    return state

def build_rm_agent_graph(framework: str = "langgraph"):
    peer_comparison_graph = PeerComparisonGraph(framework=framework).graph
    debt_profiling_graph = DebtProfilingGraph(framework=framework).graph

    rm_graph_builder = StateGraph(RMAgentState)
    rm_graph_builder.add_node("detect_framework", detect_framework)
    rm_graph_builder.add_node("peer_comparison", peer_comparison_graph)
    rm_graph_builder.add_node("debt_profiling", debt_profiling_graph)
    rm_graph_builder.set_entry_point("detect_framework")
    rm_graph_builder.add_conditional_edges("detect_framework", route_to_subgraph)
    rm_graph_builder.add_node("finalize_response", finalize_response)
    rm_graph_builder.add_edge("peer_comparison", "finalize_response")
    rm_graph_builder.add_edge("debt_profiling", "finalize_response")
    rm_graph_builder.add_edge("finalize_response", "__end__")
    return rm_graph_builder.compile()

class RMMaxitAgent(MaxitAgent):
    def __init__(self, framework: str = "langgraph"):
        super().__init__(agent_type=framework, build_graph_func=build_rm_agent_graph)
