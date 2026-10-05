from qdrant_client import QdrantClient
from config.settings import QDRANT_URL, QDRANT_COLLECTION

class MemoryEngine:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        
    def query_policy(self, query_text: str) -> str:
        # Mocking semantic retrieval logic for policy documents
        return "Policy rule: Debt-to-Income ratio must not exceed 45% for personal loans."
