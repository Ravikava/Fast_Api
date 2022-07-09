from fastapi import HTTPException, Response,status
from sqlalchemy.orm import Session
from .. import models,schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request,db: Session):
    new_blog = models.Blog(title= request.title,body= request.body,user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

def destroy(id:int,db:Session,response:Response):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return 'Done Blog is Deleted..'

def update(id:int,request:schemas.Blog,db:Session):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.update({'title':request.title,'body':request.body})        
        db.commit()
        return "data upadated"
    
def show(id:int,db:Session):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}: Blog is Not Found on this ID')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'{id}: Blog is Not Found on this ID'}
    return blog