# conversation_service/utils/entity_detector.py

from typing import List, Dict
from transformers import pipeline

# Load Huggingface NER model
ner_pipeline = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")

def detect_entities(text: str) -> List[Dict[str, float]]:
    """
    Detects named entities (ORG, PER, LOC) in the given text.
    Returns a list of {entity_name, confidence_score} dictionaries.
    """
    entities = ner_pipeline(text)
    detected = []

    for ent in entities:
        if ent["entity_group"] in ["ORG", "PER", "LOC"]:
            detected.append({
                "entity": ent["word"],
                "confidence": ent["score"],
                "type": ent["entity_group"]
            })
    print (detected)
    
    return detected

# ----------------------------------------------------------
# Main block for standalone testing
# ----------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m conversation_service.utils.entity_detector 'your query here'")
        sys.exit(1)

    query = sys.argv[1]
    results = detect_entities(query)

    if results:
        print("\n🔍 Detected Entities:")
        for r in results:
            print(f"• {r['entity']} (Type: {r['type']}, Confidence: {r['confidence']:.2f})")
    else:
        print("\n❓ No entities detected.")
