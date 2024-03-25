from typing import List
from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schemas,database,models
from sqlalchemy.orm import session
from .. oauth2 import get_current_user




from ..repository import Reposit_blog
router = APIRouter()
get_db = database.get_db



@router.post("/blog",status_code=201,tags=['blogs'])
def Create_row(request:schemas.BlogClass,db:session=Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    return Reposit_blog.Create_row(request,db)




#To get all table data
@router.get("/allblogdata",response_model=List[schemas.Customized_Blog],tags=['blogs'])
def all_blogs_history(db:session=Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return  Reposit_blog.all_blogs_history(db)


#response method 5
@router.get("/singleblogdata/{id}",status_code= status.HTTP_202_ACCEPTED,response_model=schemas.Customized_Blog,tags=['blogs'])
def Specific_blog_history(id,response:Response,db:session=Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    return Reposit_blog.Specific_blog_history(id,response,db)


@router.put("/Updatedblog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def Update_blog_data(id,request:schemas.BlogClass,db:session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    return Reposit_blog.Update_blog_data(id,request,db)




#method 2
@router.delete("/delteblog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def Delete_blog_data(id,db:session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    return Reposit_blog.Delete_blog_data(id,db)
    