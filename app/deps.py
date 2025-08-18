from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .config import settings
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")
def current_user(token: str = Depends(oauth2)):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return {"id": int(data["sub"]), "name": data["name"], "role": data.get("role", "Lawyer")}
    except JWTError:
        raise HTTPException(401, "Invalid token")
