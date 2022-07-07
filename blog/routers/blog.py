from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from .. import schemas,database,models
from sqlalchemy.orm import Session
from ..repository import blog

get_db = database.get_db

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

@router.get('/',response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)
    

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    
    new_blog = models.Blog(title= request.title,body= request.body,user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response: Response,db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return 'Done Blog is Deleted..'
    
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.update({'title':request.title,'body':request.body})        
        db.commit()
        return "data upadated"
    

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id: int,response: Response,db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}: Blog is Not Found on this ID')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'{id}: Blog is Not Found on this ID'}
    return blog