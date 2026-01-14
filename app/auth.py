from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

SECRET_KEY = "your-secret-key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
