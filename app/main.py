from fastapi import FastAPI
from app.routes import users
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(users.router, prefix="/api", tags=["Users"])
