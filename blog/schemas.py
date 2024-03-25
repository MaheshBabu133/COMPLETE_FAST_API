from pydantic import BaseModel

from typing import List,Optional




class BlogClass(BaseModel):
    title:str
    body:str
    user_id:int = 1

class Blog(BlogClass):
     class Conf():
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str


class Customized_User(BaseModel):
    name:str
    email:str
    blogs:List[Blog] = []
    class Conf():
        orm_mode = True


class Customized_User_Data(BaseModel):
    name:str
    email:str
    #blogs:List[Blog] = []
    class Conf():
        orm_mode = True


class Customized_Blog(BaseModel):
    title:str
    body:str
    creator : Customized_User_Data
    class Conf():
        orm_mode = True





       
        
class Login(BaseModel):
    username : str
    password : str



class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    email:Optional[str] = None
    