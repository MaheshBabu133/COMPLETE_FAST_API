from sqlalchemy.orm import session
from .. import models,schemas
from fastapi import HTTPException,status,Response

from .. hashing import Hash





    
    

def create_user(request:schemas.User,db:session):
    new_user = models.User(name = request.name,email = request.email,
                           password = Hash.bcrypt(request.password)
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#fetching the all users
def all_user(db:session):
    all_users = db.query(models.User).all()
    return all_users


#fetching the single user
def single_user(id:int,db:session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id} user not found') 
    return user
   