from langgraph.graph import StateGraph
from conversation_service.states.peer_comparison_state import PeerComparisonState

GRAPH_BUILD_HANDLERS = {
    "langgraph": "build_with_langgraph",
    "llamaindex": "build_with_llamaindex"  # Future
}

class PeerComparisonWorkflow:
    def __init__(self, framework: str = "langgraph"):
        if framework not in GRAPH_BUILD_HANDLERS:
            raise ValueError(f"Unknown framework: {framework}")
        
        self.framework = framework
        build_method_name = GRAPH_BUILD_HANDLERS[framework]
        build_method = getattr(self, build_method_name, None)
        if not build_method:
            raise NotImplementedError(f"Build method {build_method_name} not implemented.")
        self.graph = build_method()

    def build_with_langgraph(self):
        graph = StateGraph(PeerComparisonState)
        graph.add_node("load_financials", self.load_financials)
        graph.add_node("revenue_comparison", self.revenue_comparison)
        graph.add_node("cost_structure_comparison", self.cost_structure_comparison)
        graph.add_node("profitability_comparison", self.profitability_comparison)
        graph.add_node("leverage_comparison", self.leverage_comparison)
        graph.add_node("peer_scoring_summary", self.peer_scoring_summary)
        graph.set_entry_point("load_financials")
        graph.add_edge("load_financials", "revenue_comparison")
        graph.add_edge("revenue_comparison", "cost_structure_comparison")
        graph.add_edge("cost_structure_comparison", "profitability_comparison")
        graph.add_edge("profitability_comparison", "leverage_comparison")
        graph.add_edge("leverage_comparison", "peer_scoring_summary")
        return graph.compile()

    def build_with_llamaindex(self):
        raise NotImplementedError("LlamaIndex version not implemented yet.")

    # Node Methods
    def load_financials(self, state: PeerComparisonState) -> PeerComparisonState:
        return state

    def revenue_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        return state

    def cost_structure_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        return state

    def profitability_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        return state

    def leverage_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        return state

    def peer_scoring_summary(self, state: PeerComparisonState) -> PeerComparisonState:
        return state
