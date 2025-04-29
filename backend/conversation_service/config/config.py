# conversation_service/config/config.py
import os
from dotenv import load_dotenv
# Load .env into environment
load_dotenv()

class Config:
    """
    Global configuration for the Maxit backend.
    """

    # Huggingface Zero-Shot Classifier Settings
    INTENT_CLASSIFIER_MODEL = "facebook/bart-large-mnli"
    INTENT_CLASSIFIER_THRESHOLD = 0.7

    # Entity Recognition Settings
    ENTITY_RECOGNITION_MODEL = "dslim/bert-base-NER"
    ENTITY_CONFIDENCE_THRESHOLD = 0.8
    ENTITY_ALLOWED_TYPES = ["ORG"]  # Model return type = ORG for companies

    # Database Settings (Optional if you want)
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Global instance
CONFIG = Config()
