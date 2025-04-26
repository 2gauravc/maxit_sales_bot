import argparse
from langgraph.graph import START, StateGraph
from typing import TypedDict

# Define sub-graph peer-comparison 

from typing import TypedDict, List, Literal, Optional
class PeerComparisonState(TypedDict, total=False):
    framework_id: Literal["peer_comparison"]
    query: str
    client_id: str
    peer_ids: List[str]
    industry_id: Optional[str]
    financials: dict  # {ticker: {...}} format
    comparison_results: dict  # task_name -> result summary
    missing_data: List[str]
    response_trace: List[str]
    memory_refs: List[str]


from langgraph.graph import StateGraph
class PeerComparisonGraph:
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(PeerComparisonState)

        graph.add_node("load_financials", self.load_financial_data)
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

        return graph

    def load_financial_data(self, state: PeerComparisonState) -> PeerComparisonState:
        # Pulls data from external/ar, internal/c360, etc.
        updated_state=None
        return updated_state

    def revenue_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        updated_state=None
        return updated_state

    def cost_structure_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        updated_state=None
        return updated_state

    def profitability_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        updated_state=None
        return updated_state

    def leverage_comparison(self, state: PeerComparisonState) -> PeerComparisonState:
        updated_state=None
        return updated_state

    def peer_scoring_summary(self, state: PeerComparisonState) -> PeerComparisonState:
        final_state=None
        return final_state


# Define Sub-Graph 'Debt Profiling'

from typing import TypedDict, List, Optional, Literal
class DebtProfilingState(TypedDict, total=False):
    framework_id: Literal["debt_profiling"]
    query: str
    client_id: str
    industry_id: Optional[str]
    financials: dict            # { "XYZ": { "debt": ..., "cash": ..., ... } }
    debt_metrics: dict          # e.g., { "Debt/Equity": 1.2, "NetDebt/EBITDA": 3.1 }
    benchmark_metrics: dict     # e.g., industry or peer group averages
    interpretation: str         # final LLM output: "Moderate leverage, room to borrow"
    memory_refs: List[str]

from langgraph.graph import StateGraph

class DebtProfilingGraph:
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self):
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

        return graph

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

from typing import TypedDict, Literal
from langgraph.graph import START, StateGraph

class RMAgentState(TypedDict, total=False):
    query: str
    client_id: str
    framework_id: Literal["peer_comparison", "debt_profiling"]
    result: str

def detect_framework(state: RMAgentState) -> RMAgentState:
    # Dummy logic for example purposes
    if "compare" in state["query"]:
        state["framework_id"] = "peer_comparison"
    else:
        state["framework_id"] = "debt_profiling"
    return state

def route_to_subgraph(state: RMAgentState) -> str:
    return state["framework_id"]  # Must match subgraph node names

def finalize_response(state: RMAgentState) -> RMAgentState:
    return state 
def build_rm_agent_graph():
    # Import your sub-agent graphs
    peer_comparison_graph = PeerComparisonGraph().graph.compile()
    debt_profiling_graph = DebtProfilingGraph().graph.compile()

    # Build the parent RM Agent graph
    rm_graph_builder = StateGraph(RMAgentState)

    rm_graph_builder.add_node("detect_framework", detect_framework)

    # Add sub-agent graphs by name
    rm_graph_builder.add_node("peer_comparison", peer_comparison_graph)
    rm_graph_builder.add_node("debt_profiling", debt_profiling_graph)

    # Routing logic
    rm_graph_builder.set_entry_point("detect_framework")
    rm_graph_builder.add_conditional_edges("detect_framework", route_to_subgraph)

    # Ending State 
    rm_graph_builder.add_node("finalize_response", finalize_response)
    rm_graph_builder.add_edge("peer_comparison", "finalize_response")
    rm_graph_builder.add_edge("debt_profiling", "finalize_response")
    rm_graph_builder.add_edge("finalize_response", "__end__")

    # Final graph
    rm_agent_graph = rm_graph_builder.compile()
    return rm_agent_graph

def save_graph_image(graph, filename="rm_agent_graph.png", xray=1):
    """
    Save the LangGraph graph visualization to disk.
    
    Args:
        graph: The compiled LangGraph object.
        filename: The filename to save the PNG as.
        xray: Whether to show nested graphs (1 for yes, 0 for no).
    """
    png_data = graph.get_graph(xray=xray).draw_mermaid_png()
    with open(filename, "wb") as f:
        f.write(png_data)
    print(f"Graph saved to {filename}")

# Get the PNG image bytes
#png_data = rm_agent_graph.get_graph(xray=1).draw_mermaid_png()
# Save it to disk
#with open("rm_agent_graph.png", "wb") as f:
#    f.write(png_data)
#print("Saved to rm_agent_graph.png")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Maxit RM Agent.")
    
    parser.add_argument(
        "--query",
        type=str,
        required=False,
        default="How does XYZ compare on profitability?",
        help="The question/query to analyze."
    )
    parser.add_argument(
        "--client_id",
        type=str,
        required=False,
        default="xyz",
        help="The client ID associated with the query."
    )
    
    parser.add_argument(
        "--save_graph",
        type=str,
        choices=["yes", "no"],
        default="yes",
        help="Whether to save the agent graph visualization (yes/no)."
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    initial_state = {
        "query": args.query,
        "client_id": args.client_id
    }
    #Build the RM agent graph 
    rm_agent_graph = build_rm_agent_graph()

    # Call RM agent
    res_state = rm_agent_graph.invoke(initial_state)
    
    print("\n--- Final State ---")
    print(res_state)
    
    # Save graph if requested
    if args.save_graph.lower() == "yes":
        save_graph_image(rm_agent_graph)
    else:
        print("Graph saving skipped as per argument.")

if __name__ == "__main__":
    main()



