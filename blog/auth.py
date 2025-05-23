import config,models,utils,schema,database
from jose import JWTError, jwt  
from fastapi import  Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth_token=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth_token),db:Session=Depends(database.get_db)):
    try:
        payload=utils.verify_access_token(token)
        email:str=payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        
        user=db.query(models.user).filter(models.user.email==email).first()

        if user is None:
            raise HTTPException(status_code=401,detail="user not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate credentials")