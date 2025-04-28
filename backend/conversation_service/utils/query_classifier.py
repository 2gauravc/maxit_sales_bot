# conversation_service/utils/query_classifier.py

from conversation_service.frameworks.peer_comparison_framework import PeerComparisonFramework
from conversation_service.frameworks.debt_profiling_framework import DebtProfilingFramework
from typing import TypedDict, List, Literal, Optional

FRAMEWORK_CLASSES = {
    "peer_comparison": PeerComparisonFramework,
    "debt_profiling": DebtProfilingFramework,
}

def classify_query_intent(query: str) -> Optional[str]:
    query_lower = query.lower()

    for framework_id, framework_class in FRAMEWORK_CLASSES.items():
        keywords = framework_class.intent_keywords
        if any(keyword in query_lower for keyword in keywords):
            return framework_id

    return None


