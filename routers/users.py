from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponse], summary="유저 목록 조회")
def get_users(
    name: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if name:
        query = query.filter(User.name.contains(name))
    if min_age is not None:
        query = query.filter(User.age >= min_age)
    if max_age is not None:
        query = query.filter(User.age <= max_age)
    return query.offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse, summary="특정 유저 조회")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")
    return user


@router.post("", response_model=UserResponse, summary="유저 추가", status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일")
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="유저 전체 수정")
def update_user(user_id: int, body: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")
    for key, value in body.model_dump().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserResponse, summary="유저 일부 수정")
def patch_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", summary="유저 삭제", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")
    db.delete(user)
    db.commit()
