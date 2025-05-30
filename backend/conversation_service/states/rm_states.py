from typing import TypedDict, List, Literal, Optional

# ===========================
# State for RM Agent (Routing Layer)
# ===========================

class RMAgentState(TypedDict, total=False):
    user_id: str
    query: str
    client_id: str
    framework_id: Literal["peer_comparison", "debt_profiling"]
    result: str
