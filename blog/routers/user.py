from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,models,hashing
from sqlalchemy.orm import session
from .. hashing import Hash
from .. oauth2 import get_current_user



router = APIRouter()
get_db = database.get_db





@router.post('/createuser',tags=['users'])
def create_user(request:schemas.User,db:session=Depends(get_db)):
    new_user = models.User(name = request.name,email = request.email,
                           password = Hash.bcrypt(request.password)
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#fetching the all users
@router.get('/alluser',response_model=List[schemas.Customized_User],tags=['users'])
def all_user(db:session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    all_users = db.query(models.User).all()
    return all_users


#fetching the single user
@router.get('/singleuser/{id}',response_model=schemas.Customized_User,tags=['users'])
def single_user(id:int,db:session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id} user not found') 
    return user
   