# conversation_service/frameworks/framework_registry.py

from conversation_service.frameworks.peer_comparison_framework import PeerComparisonFramework
from conversation_service.frameworks.debt_profiling_framework import DebtProfilingFramework

FRAMEWORK_CLASSES = {
    "peer_comparison": {
        "class": PeerComparisonFramework,
        "display_name": "Compare to peers or industry"
    },
    "debt_profiling": {
        "class": DebtProfilingFramework,
        "display_name": "Profile the debt obligations"
    },
}

