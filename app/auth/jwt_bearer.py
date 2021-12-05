# The function of this file is to check whether the request is authorized or not 
# [Verification  of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

#jwtBearer is a subclass of HTTPBearer

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error = auto_Error)
        
    async def __call__(self,request: Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, details= "Invalid or Expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, details= "Invalid or Expired token")
            
    
    def verify_jwt(self, jwtoken:str):
        isTokenValid : bool = False
        if decodeJWT(jwtoken):
            isTokenValid = True
        return isTokenValid
    
    