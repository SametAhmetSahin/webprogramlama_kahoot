from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = APIRouter()

# Statik dosyaları hizmet etmek için ayarlayın
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates dizinini ayarlayın
templates = Jinja2Templates(directory="templates")

# Kullanıcı rotalarını dahil ediyoruz

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

from routers.users import get_user_id_from_token, get_user_from_token, get_user
from common import get_database

@app.get("/admin/users", response_class=HTMLResponse)
async def view_users(request: Request):
    can_access = ["admin"]
    if not "token" in request.cookies:
        return templates.TemplateResponse("unauthorized.html", {"request": request})
    
    token = request.cookies.get("token")
    print(get_user_from_token(token))
    if get_user_from_token(token)["role"] in can_access:
        db = get_database()
        users = db["users"]
        return templates.TemplateResponse("users.html", {"request": request, "users_list": users.find()})    
    return templates.TemplateResponse("unauthorized.html", {"request": request})


@app.get("/quizzes", response_class=HTMLResponse)
async def quizzes(request: Request):
    can_access = ["teacher", "admin"]
    
    if not "token" in request.cookies:
        return templates.TemplateResponse("unauthorized.html", {"request": request})
    
    token = request.cookies.get("token")
    if get_user_from_token(token)["role"] in can_access:
        db = get_database()
        quizzes = db["quiz"]
        quiz_list = list(quizzes.find())
        for q in quiz_list:
            q["owner"] = (await get_user(q["owner_id"], request))["user"]["username"]
        return templates.TemplateResponse("quizzes.html", {"request": request, "quizzes": quiz_list})
    return templates.TemplateResponse("unauthorized.html", {"request": request})
    


@app.get("/quiz/create", response_class=HTMLResponse)
async def createquiz(request: Request):
    can_access = ["teacher"]
    if not "token" in request.cookies:
        return templates.TemplateResponse("unauthorized.html", {"request": request})
    
    token = request.cookies.get("token")
    if get_user_from_token(token)["role"] in can_access:
        return templates.TemplateResponse("createquiz.html", {"request": request})
    return templates.TemplateResponse("unauthorized.html", {"request": request})

from routers.quiz import get_quiz_with_id
@app.get("/viewquiz", response_class=HTMLResponse)
async def viewquiz(request: Request, quiz_id: str):
    can_access = ["teacher", "admin"]
    if not "token" in request.cookies:
        return templates.TemplateResponse("unauthorized.html", {"request": request})
    
    token = request.cookies.get("token")
    if get_user_from_token(token)["role"] in can_access:
        quiz = await get_quiz_with_id(quiz_id, request)
        return templates.TemplateResponse("viewquiz.html", {"request": request, "quiz": quiz["quiz"]})
    
    return templates.TemplateResponse("unauthorized.html", {"request": request})

@app.get("/playquiz", response_class=HTMLResponse)
async def playquiz(request: Request):
    return templates.TemplateResponse("playquiz.html", {"request": request})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})
