import logging
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Handles communication with Firebase Firestore safely and securely."""
    
    def __init__(self):
        self.db = None
        self.is_active = False
        
        try:
            # Check if default app is already initialized to prevent duplicate initialization
            if not firebase_admin._apps:
                # In Google Cloud Run, Application Default Credentials are used automatically.
                # If running locally, you must set GOOGLE_APPLICATION_CREDENTIALS.
                # No hardcoded JSON keys are used.
                if settings.FIREBASE_PROJECT_ID:
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred, {
                        'projectId': settings.FIREBASE_PROJECT_ID,
                    })
                else:
                    logger.warning("No Firebase Project ID found. Initializing with generic defaults.")
                    firebase_admin.initialize_app()
            
            self.db = firestore.client()
            self.is_active = True
            logger.info("Firebase Firestore Client initialized successfully.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Client: {e}")

    async def get_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """Fetch all documents in a collection in a single batch read."""
        if not self.is_active or not self.db:
            return []
            
        try:
            # Firestore client in Python is synchronous by default unless using async firestore
            # For this architecture, we run the blocking call, which is acceptable in small datasets
            # but ideally would be wrapped in `asyncio.to_thread` for high concurrency.
            docs = self.db.collection(collection_name).stream()
            
            results = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                results.append(data)
                
            return results
            
        except Exception as e:
            logger.error(f"Firebase API error fetching collection {collection_name}: {e}")
            return []

    async def get_document(self, collection_name: str, doc_id: str) -> Dict[str, Any]:
        """Fetch a single document from Firestore."""
        if not self.is_active or not self.db:
            return {}
            
        try:
            doc_ref = self.db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                return data
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Firebase API error fetching document {collection_name}/{doc_id}: {e}")
            return {}
