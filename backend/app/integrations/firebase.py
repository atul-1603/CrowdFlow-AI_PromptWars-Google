import logging
import asyncio
import time
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 15

class FirebaseClient:
    """Handles communication with Firebase Firestore safely and securely, with TTL caching."""
    
    def __init__(self):
        self.db = None
        self.is_active = False
        self._cache = {}
        
        try:
            if not firebase_admin._apps:
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

    def _sync_get_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        docs = self.db.collection(collection_name).stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return results

    async def get_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """Fetch all documents in a collection in a single batch read, with caching."""
        if not self.is_active or not self.db:
            return []
            
        cache_key = f"collection_{collection_name}"
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if time.time() - entry['time'] < CACHE_TTL_SECONDS:
                logger.info(f"[FirebaseClient] Cache HIT for collection: {collection_name}")
                return entry['data']
            
        try:
            logger.info(f"[FirebaseClient] Cache MISS for collection: {collection_name}. Fetching from Firestore...")
            results = await asyncio.to_thread(self._sync_get_collection, collection_name)
            
            self._cache[cache_key] = {
                'time': time.time(),
                'data': results
            }
            return results
            
        except Exception as e:
            logger.error(f"Firebase API error fetching collection {collection_name}: {e}")
            return []

    def _sync_get_document(self, collection_name: str, doc_id: str) -> Dict[str, Any]:
        doc_ref = self.db.collection(collection_name).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return {}

    async def get_document(self, collection_name: str, doc_id: str) -> Dict[str, Any]:
        """Fetch a single document from Firestore, with caching."""
        if not self.is_active or not self.db:
            return {}
            
        cache_key = f"doc_{collection_name}_{doc_id}"
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if time.time() - entry['time'] < CACHE_TTL_SECONDS:
                logger.info(f"[FirebaseClient] Cache HIT for document: {collection_name}/{doc_id}")
                return entry['data']
            
        try:
            logger.info(f"[FirebaseClient] Cache MISS for document: {collection_name}/{doc_id}. Fetching from Firestore...")
            data = await asyncio.to_thread(self._sync_get_document, collection_name, doc_id)
            
            self._cache[cache_key] = {
                'time': time.time(),
                'data': data
            }
            return data
                
        except Exception as e:
            logger.error(f"Firebase API error fetching document {collection_name}/{doc_id}: {e}")
            return {}
