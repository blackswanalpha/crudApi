from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models
import schema
from  user import userRoute
from database import engine, get_db

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(userRoute.router)
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schema.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', response_model=schema.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=
                            status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # response.status_code =   status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} is not available"}

    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    # db.query(models.Blog).filter(models.Blog.id == id).update({'title': 'updated tiltle'})
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==
                                        id).delete(synchronize_session=False)

    db.commit()
    return {"done"}
