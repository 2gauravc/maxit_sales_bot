from langgraph.graph import StateGraph
from conversation_service.states.debt_profiling_state import DebtProfilingState

GRAPH_BUILD_HANDLERS = {
    "langgraph": "build_with_langgraph",
    "llamaindex": "build_with_llamaindex"  # Future
}

class DebtProfilingFramework:
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
        graph = StateGraph(DebtProfilingState)

        # Add LangGraph nodes
        graph.add_node("load_financial_data", self.load_financial_data)
        graph.add_node("calculate_debt_metrics", self.calculate_debt_metrics)
        graph.add_node("fetch_peer_benchmarks", self.fetch_peer_benchmarks)
        graph.add_node("compare_vs_benchmark", self.compare_vs_benchmark)
        graph.add_node("synthesize_debt_profile", self.synthesize_debt_profile)

        # Wire up nodes
        graph.set_entry_point("load_financial_data")
        graph.add_edge("load_financial_data", "calculate_debt_metrics")
        graph.add_edge("calculate_debt_metrics", "fetch_peer_benchmarks")
        graph.add_edge("fetch_peer_benchmarks", "compare_vs_benchmark")
        graph.add_edge("compare_vs_benchmark", "synthesize_debt_profile")
        
        return graph.compile()

    def load_financial_data(self, state: DebtProfilingState) -> DebtProfilingState:
        # Pull from namespace like external/ar/company/{ticker}
        # Extract Total Debt, Cash, EBITDA, Equity
        financials = {
            "total_debt": 3200,
            "cash": 800,
            "ebitda": 1020,
            "equity": 2700,
        }
        state["financials"] = financials
        return state

    def calculate_debt_metrics(self, state: DebtProfilingState) -> DebtProfilingState:
        f = state["financials"]
        state["debt_metrics"] = {
            "Debt/Equity": round(f["total_debt"] / f["equity"], 2),
            "NetDebt/EBITDA": round((f["total_debt"] - f["cash"]) / f["ebitda"], 2),
        }
        return state

    def fetch_peer_benchmarks(self, state: DebtProfilingState) -> DebtProfilingState:
        # Dummy industry or peer benchmarks
        state["benchmark_metrics"] = {
            "Debt/Equity": 1.1,
            "NetDebt/EBITDA": 2.7
        }
        return state

    def compare_vs_benchmark(self, state: DebtProfilingState) -> DebtProfilingState:
        # Optionally store deltas or annotate deviations
        metrics = state["debt_metrics"]
        peers = state["benchmark_metrics"]
        interpretation = {
            k: "above average" if metrics[k] > peers[k] else "below average"
            for k in metrics
        }
        state["interpretation_summary"] = interpretation
        return state

    def synthesize_debt_profile(self, state: DebtProfilingState) -> DebtProfilingState:
        interpretation = state.get("interpretation_summary", {})
        summary = (
            f"Debt/Equity is {interpretation.get('Debt/Equity')}, "
            f"Net Debt/EBITDA is {interpretation.get('NetDebt/EBITDA')} — "
            f"overall leverage is {'moderate to high' if 'above average' in interpretation.values() else 'within industry norms'}."
        )
        state["interpretation"] = summary
        return state
