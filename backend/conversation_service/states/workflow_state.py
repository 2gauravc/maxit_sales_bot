from typing import TypedDict, List

class WorkflowState(TypedDict, total=False):
    """
    Common base state for all workflows.
    """
    query: str
    client_id: str
    response_trace: List[str]
    memory_refs: List[str]
