from fastapi import Depends, FastAPI, status,Response,HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def creat(request:schemas.Blog, db: Session = Depends(get_db)):
    
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response: Response,db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return 'Done Blog is Deleted..'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id}: Blog is Not Found on this ID! please enter a Valid ID...')
    
    else:
        blog.update({'title':request.title,'body':request.body})        
        db.commit()
        return "data upadated"

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200)
def show(id: int,response: Response,db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}: Blog is Not Found on this ID')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'{id}: Blog is Not Found on this ID'}
    return blog
    
