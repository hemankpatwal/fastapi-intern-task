from fastapi import FastAPI
from app.routes import users
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Define a route for the root path
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/style.css">
        </head>
        <body>
            <h1>Welcome to FastAPI!</h1>
        </body>
    </html>
    """