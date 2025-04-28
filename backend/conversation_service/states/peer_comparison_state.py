# ===========================
# States for Peer Comparison
# ===========================

from typing import TypedDict, List, Literal, Optional
from conversation_service.states.workflow_state import WorkflowState

class PeerComparisonState(WorkflowState):
    framework_id: Literal["peer_comparison"]
    peer_ids: List[str]
    industry_id: Optional[str]
    financials: dict  # Example: {ticker: {...}}
    comparison_results: dict  # task_name -> result summary
    missing_data: List[str]
    
