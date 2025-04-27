from typing import TypedDict, List, Optional

class ProductAdvisorState(TypedDict, total=False):
    query: str
    client_id: str
    product_recommendations: List[str]
    rationale: str
    memory_refs: List[str]
