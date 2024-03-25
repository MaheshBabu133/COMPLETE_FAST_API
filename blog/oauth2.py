from fastapi import Depends,HTTPException,status

from . import JWToken

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate creadential'
                                         )
    

    
    return JWToken.verify_token(token,credential_exception)
    