from pydantic import BaseModel, Field, ConfigDict


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: int = Field(gt=0)
    category: str = "기타"
    stock: int = Field(default=0, ge=0)


class ItemUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    category: str | None = None
    stock: int | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    category: str
    stock: int


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(gt=0, lt=150)


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int
