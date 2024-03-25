from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Blogclass(BaseModel):
    title:str
    body:str

@app.post("/blog")
def Sample(request:Blogclass):
    return {"title":request.title,'body':request.body}


