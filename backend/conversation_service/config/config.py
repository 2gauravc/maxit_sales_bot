# conversation_service/config/config.py

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
    POSTGRES_DB = "maxit_db"
    POSTGRES_USER = "maxit_user"
    POSTGRES_PASSWORD = "maxit_pass"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"

# Global instance
CONFIG = Config()
