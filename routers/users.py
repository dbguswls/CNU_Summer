from itertools import count
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/users", tags=["Users"])


class User(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(gt=0, lt=150)


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


users: list[dict] = [
    {"id": 1, "name": "홍길동", "email": "hong@example.com", "age": 30},
    {"id": 2, "name": "김철수", "email": "kim@example.com",  "age": 25},
    {"id": 3, "name": "이영희", "email": "lee@example.com",  "age": 28},
]
_id = count(start=4)


@router.get("", summary="유저 목록 조회")
def get_users(
    name: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    result = users
    if name:
        result = [u for u in result if name in u["name"]]
    if min_age is not None:
        result = [u for u in result if u["age"] >= min_age]
    if max_age is not None:
        result = [u for u in result if u["age"] <= max_age]
    return result[skip : skip + limit]


@router.get("/{user_id}", summary="특정 유저 조회")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")


@router.post("", summary="유저 추가", status_code=201)
def create_user(user: User):
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일")
    new_user = {"id": next(_id), **user.model_dump()}
    users.append(new_user)
    return new_user


@router.put("/{user_id}", summary="유저 전체 수정")
def update_user(user_id: int, user: User):
    for idx, v in enumerate(users):
        if v["id"] == user_id:
            users[idx] = {"id": user_id, **user.model_dump()}
            return users[idx]
    raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")


@router.patch("/{user_id}", summary="유저 일부 수정")
def patch_user(user_id: int, user: UserUpdate):
    for v in users:
        if v["id"] == user_id:
            v.update(user.model_dump(exclude_unset=True))
            return v
    raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")


@router.delete("/{user_id}", summary="유저 삭제", status_code=204)
def delete_user(user_id: int):
    for idx, v in enumerate(users):
        if v["id"] == user_id:
            users.pop(idx)
            return
    raise HTTPException(status_code=404, detail="유저를 찾을 수 없음")
