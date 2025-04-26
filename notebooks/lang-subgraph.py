import argparse
from langgraph.graph import START, StateGraph
from typing import TypedDict
from typing import TypedDict, List, Literal, Optional


# Define all graph states 

class RMAgentState(TypedDict, total=False):
    query: str
    client_id: str
    framework_id: Literal["peer_comparison", "debt_profiling"]
    result: str

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

GRAPH_BUILD_HANDLERS = {
    "langgraph": "build_with_langgraph",
    "llamaindex": "build_with_llamaindex"  # Future
}

# Define Peer Comparison sub-graph

class PeerComparisonGraph:
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


# Define 'Debt Profiling' sub-graph

class DebtProfilingGraph:
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

# Define common nodes (RM Agent)

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

def build_rm_agent_graph(framework: str = "langgraph"):
    # Import your sub-agent graphs
    peer_comparison_graph = PeerComparisonGraph(framework=framework).graph.compile()
    debt_profiling_graph = DebtProfilingGraph(framework=framework).graph.compile()

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

AGENT_TYPE_HANDLERS = {
    "langgraph": {
        "build_graph": build_rm_agent_graph,
        "invoke_method": "invoke"
    },
    "llamaindex": {
        "build_graph": None,          # Placeholder for future
        "invoke_method": "query"
    }
}

# Define RM Agent wrapper 

class MaxitAgent:
    def __init__(self, agent_type: str = "langgraph"):
        if agent_type not in AGENT_TYPE_HANDLERS:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        self.agent_type = agent_type
        handler_info = AGENT_TYPE_HANDLERS[self.agent_type]
        
        # Build graph
        build_func = handler_info["build_graph"]
        if build_func is None:
            raise NotImplementedError(f"Graph building for {self.agent_type} not implemented.")
        self.graph = build_func(framework=agent_type)  # dynamic build

        # Save invoke method name
        self.invoke_method = handler_info["invoke_method"]

    def invoke(self, initial_state: dict):
        return getattr(self.graph, self.invoke_method)(initial_state)

    def save_graph_image(self, filename="rm_agent_graph.png", xray=1):
        if hasattr(self.graph, "get_graph"):
            png_data = self.graph.get_graph(xray=xray).draw_mermaid_png()
            with open(filename, "wb") as f:
                f.write(png_data)
            print(f"Graph saved to {filename}")
        else:
            print(f"Saving graph not supported for agent type {self.agent_type}")


# CLI 

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
    parser.add_argument(
        "--framework",
        type=str,
        required=False,
        default="langgraph",
        help="Which agent framework you are using (langgraph)"
    )


    return parser.parse_args()

def main():
    args = parse_arguments()
    
    initial_state = {
        "query": args.query,
        "client_id": args.client_id
    }
    
    agent = MaxitAgent(agent_type=args.framework.lower())
    res_state = agent.invoke(initial_state)
    
    print("\n--- Final State ---")
    print(res_state)
    
    # Save graph if requested
    if args.save_graph.lower() == "yes":
        agent.save_graph_image()
    else:
        print("Graph saving skipped as per argument.")

if __name__ == "__main__":
    main()



