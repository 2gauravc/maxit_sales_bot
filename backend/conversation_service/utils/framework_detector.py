# conversation_service/utils/query_classifier.py

from typing import Optional, Dict
from transformers import pipeline
from conversation_service.frameworks.framework_registry import FRAMEWORK_CLASSES

# Load Huggingface Zero-Shot Classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_framework(query: str, confidence_threshold: float = 0.7) -> Optional[str]:
    """
    Classify the user query to detect framework intent.
    Now matches against framework display names instead of intent keywords.
    Returns framework_id if confident enough, else None.
    """

    query_lower = query.lower()

    # Step 1: Build candidate labels from framework display names
    candidate_labels = []
    label_to_framework: Dict[str, str] = {}

    for framework_id, framework_entry in FRAMEWORK_CLASSES.items():
        display_name = framework_entry["display_name"]
        candidate_labels.append(display_name)
        label_to_framework[display_name] = framework_id

    # Step 2: Run zero-shot classification
    result = classifier(query_lower, candidate_labels)

    # Step 3: Collect all matches
    matches = []
    for label, score in zip(result["labels"], result["scores"]):
        matches.append({
            "label": label,
            "framework_id": label_to_framework[label],
            "confidence": score
        })
    
    # Step 4: Check if confident enough
    return matches 

# --------------------------------------------
# For standalone testing (optional)
# --------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python query_classifier.py 'your query here'")
        sys.exit(1)

    query = sys.argv[1]
    matches = classify_query_intent(query)

    for match in matches:
        print(f"• {match['framework_id']} ({match['label']}) → Confidence: {match['confidence']:.2f}")