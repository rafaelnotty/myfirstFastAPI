from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await default_exception_handler(request, exc)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("excepciones.html", {"request": request, "exc": exc}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_ip = request.client.host
    context = {
        "request": request,
        "user_ip": user_ip
    }
    return templates.TemplateResponse("index.html", context=context)