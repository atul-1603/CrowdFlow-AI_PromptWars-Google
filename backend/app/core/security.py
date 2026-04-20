from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import logging
from app.models.schemas import User
from app.core.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()

import firebase_admin
from firebase_admin import credentials

def verify_token(credentials_obj: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Verifies the Firebase ID token and returns a User object."""
    token = credentials_obj.credentials
    try:
        if not settings.FIREBASE_PROJECT_ID:
            logger.warning("Firebase not configured. Bypassing auth for local development.")
            return User(user_id="local_dev", email="local@dev.com")
            
        # Ensure Firebase app is initialized before verifying token
        if not firebase_admin._apps:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': settings.FIREBASE_PROJECT_ID,
            })
            
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token.get("uid")
        email = decoded_token.get("email")
        
        return User(user_id=user_id, email=email)
        
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Error verifying Firebase token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

