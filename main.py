from fastapi import FastAPI
from routers import items, users

app = FastAPI(title="쇼핑몰 API")

app.include_router(items.router)
app.include_router(users.router)
