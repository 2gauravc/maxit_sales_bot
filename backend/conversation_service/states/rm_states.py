from typing import TypedDict, List, Literal, Optional

# ===========================
# States for Peer Comparison
# ===========================

class PeerComparisonState(TypedDict, total=False):
    framework_id: Literal["peer_comparison"]
    query: str
    client_id: str
    peer_ids: List[str]
    industry_id: Optional[str]
    financials: dict  # Example: {ticker: {...}}
    comparison_results: dict  # task_name -> result summary
    missing_data: List[str]
    response_trace: List[str]
    memory_refs: List[str]

# ===========================
# States for Debt Profiling
# ===========================

class DebtProfilingState(TypedDict, total=False):
    framework_id: Literal["debt_profiling"]
    query: str
    client_id: str
    industry_id: Optional[str]
    financials: dict            # Example: { "XYZ": { "debt": ..., "cash": ..., ... } }
    debt_metrics: dict          # Example: { "Debt/Equity": 1.2, "NetDebt/EBITDA": 3.1 }
    benchmark_metrics: dict     # Industry or peer group averages
    interpretation: str         # Final LLM output, e.g., "Moderate leverage, room to borrow"
    memory_refs: List[str]

# ===========================
# State for RM Agent (Routing Layer)
# ===========================

class RMAgentState(TypedDict, total=False):
    query: str
    client_id: str
    framework_id: Literal["peer_comparison", "debt_profiling"]
    result: str
