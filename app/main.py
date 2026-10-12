from fastapi import FastAPI

from app.routers import auth, todos

app = FastAPI()
app.include_router(todos.router)
app.include_router(auth.router)
