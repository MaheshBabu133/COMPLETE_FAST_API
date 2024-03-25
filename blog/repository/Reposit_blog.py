from sqlalchemy.orm import session
from .. import models,schemas
from fastapi import HTTPException,status,Response



def Create_row(request:schemas.BlogClass,db:session):
    user_info = db.query(models.User).all()
    User_List = [a.id for a in user_info]

    if (request.user_id < 1) or (request.user_id not in User_List ) :
        print(db.query(models.User).all())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{request.user_id} user not found') 
    
    new_blog = models.Blog(title=request.title,body = request.body,user_id = request.user_id)
    db.add(new_blog) #it will add the data to the table
    db.commit() #It will saves the data
    db.refresh(new_blog)#it will refresh the sqlite3 software with new data
    return new_blog




def all_blogs_history(db:session):
    blogs = db.query(models.Blog).all()
    return blogs


def Specific_blog_history(id,response:Response,db:session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id : {id} --> not found')
    return blogs



def Update_blog_data(id,request:schemas.BlogClass,db:session):
    blog = db.query(models.Blog).filter(models.Blog.id == id )
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} is not found')
    blog.update({"title":request.title,"body":request.body})
    db.commit()
    return "Data updated successfully"


def Delete_blog_data(id:int,db:session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} is not found')
    blog.delete(synchronize_session = False)
    db.commit()

    return f'{id} deleted succssfully'
