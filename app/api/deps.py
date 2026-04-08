from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.core.token_blacklist import is_token_blacklisted

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token is logged out")

    try:
        payload = decode_token(token)
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")



