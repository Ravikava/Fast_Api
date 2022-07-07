from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas, database,models,hashing
from sqlalchemy.orm import Session

get_db = database.get_db

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/',response_model=schemas.ShowUser)
def creat_user(request: schemas.User,db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=hashing.Hash.bcrypt(request.password)
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id: int,db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ID:- _{id}_ User is Not Found on this ID')
    return user