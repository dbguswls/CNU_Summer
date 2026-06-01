from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(30), default="기타")
    stock: Mapped[int] = mapped_column(Integer, default=0)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[int] = mapped_column(Integer)
