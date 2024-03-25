'''from fastapi import FastAPI,Depends,status,Response,HTTPException 
from typing import List
from . import schemas,models # '.' represents the same directoty
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import session
from . hashing import Hash


app = FastAPI()
models.Base.metadata.create_all(engine) #This will creates the Table when refresh the server if tables are not there




def get_db():    #This function is used to create session 
    db = SessionLocal()
    try:
        yield db #This will get the related object
    finally:
        db.close()


@app.post("/blog")
def Inside_sample_function(request:schemas.BlogClass):
    return {"title":request.title,'body':request.body}






#Creating the Blog
@app.post("/blog",status_code=201,tags=['blogs'])
def Create_row(request:schemas.BlogClass,db:session=Depends(get_db)):
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




#To get all table data
@app.get("/allblogdata",response_model=List[schemas.Customized_Blog],tags=['blogs'])
def all_blogs_history(db:session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#To get specific table data

#response method 2
@app.get("/singleblogdata/{id}",status_code= status.HTTP_202_ACCEPTED)
def Specific_blog_history(id,db:session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blogs

    


#response method 3
@app.get("/singleblogdata/{id}",status_code= status.HTTP_202_ACCEPTED)
def Specific_blog_history(id,response:Response,db:session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":f'id : {id} not found'}
    return blogs

    

#response method 4
@app.get("/singleblogdata/{id}",status_code= status.HTTP_202_ACCEPTED)
def Specific_blog_history(id,response:Response,db:session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":f'id : {id} not found'}
    return blogs



#response method 5
@app.get("/singleblogdata/{id}",status_code= status.HTTP_202_ACCEPTED,response_model=schemas.Customized_Blog,tags=['blogs'])
def Specific_blog_history(id,response:Response,db:session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id : {id} --> not found')
    return blogs


@app.put("/Updatedblog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def Update_blog_data(id,request:schemas.BlogClass,db:session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id )
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} is not found')
    blog.update({"title":request.title,"body":request.body})
    db.commit()
    return "Data updated successfully"
 


#method 1
@app.delete("/delteblog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def Delete_blog_data(id,db:session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return f"{id}deletd successfully"



#method 2
@app.delete("/delteblog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def Delete_blog_data(id,db:session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} is not found')
    blog.delete(synchronize_session = False)
    db.commit()

    return f'{id} deleted succssfully'


#with out creating hashing.py file

from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated='auto')

@app.post('/createuser',tags=['users'])
def create_user(request:schemas.User,db:session=Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)

    new_user = models.User(name = request.name,email = request.email,
                           password = hashed_password
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#with creating hashing.py file
@app.post('/createuser',tags=['users'])
def create_user(request:schemas.User,db:session=Depends(get_db)):
    new_user = models.User(name = request.name,email = request.email,
                           password = Hash.bcrypt(request.password)
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#fetching the all users
@app.get('/alluser',response_model=List[schemas.Customized_User],tags=['users'])
def all_user(db:session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users


#fetching the single user
@app.get('/singleuser/{id}',response_model=schemas.Customized_User,tags=['users'])
def single_user(id:int,db:session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id} user not found') 
    return user
   
'''

#After API Router

from fastapi import FastAPI
from .import models
from .database import engine
from .routers import blog,user,Authentication
app = FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(Authentication.router)
