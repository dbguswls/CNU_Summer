from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import SessionLocal
from models import Item, User
from routers import items, users


def seed():
    db = SessionLocal()
    try:
        if db.query(Item).count() == 0:
            db.add_all([
                Item(name="사과",   price=1500,    category="과일",    stock=100),
                Item(name="바나나", price=800,     category="과일",    stock=80),
                Item(name="노트북", price=1200000, category="전자기기", stock=10),
                Item(name="마우스", price=35000,   category="전자기기", stock=50),
                Item(name="우유",   price=2500,    category="유제품",  stock=30),
            ])
        if db.query(User).count() == 0:
            db.add_all([
                User(name="홍길동", email="hong@example.com", age=30),
                User(name="김철수", email="kim@example.com",  age=25),
                User(name="이영희", email="lee@example.com",  age=28),
            ])
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed()
    yield


app = FastAPI(title="쇼핑몰 API", lifespan=lifespan)

app.include_router(items.router)
app.include_router(users.router)
