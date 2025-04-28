# ===========================
# States for Debt Profiling
# ===========================
from typing import TypedDict, List, Literal, Optional
from conversation_service.states.workflow_state import WorkflowState

class DebtProfilingState(WorkflowState):
    framework_id: Literal["debt_profiling"]
    industry_id: Optional[str]
    financials: dict            # Example: { "XYZ": { "debt": ..., "cash": ..., ... } }
    debt_metrics: dict          # Example: { "Debt/Equity": 1.2, "NetDebt/EBITDA": 3.1 }
    benchmark_metrics: dict     # Industry or peer group averages
    interpretation: str         # Final LLM output, e.g., "Moderate leverage, room to borrow"
    