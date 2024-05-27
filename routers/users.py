from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from hashlib import sha256
import uuid
import jwt
import starlette.status as status

from common import get_database, generate_random_string

# JWT oluşturmak ve doğrulamak için kullanılan gizli anahtar
SECRET_KEY = "kahootklonu"

# APIRouter oluşturuluyor
router = APIRouter()

from datetime import datetime, timedelta, timezone

# Kullanıcı kayıt olma işlevi
@router.post("/users/register")
async def register(request: Request):

    parsed = await request.json()
    
    db = get_database()
    users = db["users"]

    if users.find_one({"username": parsed["username"]}):
        return {"message": "user already exists", "success": False}
    
    insert_results = users.insert_one({
        "user_id": str(uuid.uuid4()),
        "username": parsed["username"],
        "hashed_password": sha256(parsed["password"].encode()).hexdigest(),
        "role": parsed["role"],
        "token_ttl": "",
    })

    return {"message": "inserted user with id", "user_id": str(insert_results.inserted_id), "success": True}

# Kullanıcı giriş yapma işlevi
@router.post("/users/login")
async def login(request: Request):
    
    parsed = await request.json()
    
    db = get_database()
    users = db["users"]

    if not users.find_one({"username": parsed["username"]}):
        return {"message": "user does not exist", "success": False}
    found_user = users.find_one({"username": parsed["username"]})
    if found_user["hashed_password"] != sha256(parsed["password"].encode()).hexdigest():
        return {"message": "invalid username or passowrd", "success": False}

    # JWT oluşturuluyor
    
    token = jwt.encode({"user_id": found_user["user_id"], "exp": datetime.now(tz=timezone.utc) + timedelta(hours=2)}, SECRET_KEY, algorithm="HS256")
    return {"message": "login successful", "token": token, "success": True}

# Kullanıcı kimliğini JWT'den çıkaran yardımcı işlev
def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        #raise HTTPException(status_code=401, detail="Token has expired")
        return RedirectResponse(url="/login", status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return RedirectResponse(url="/login", status_code=status.HTTP_401_UNAUTHORIZED)
    
def get_user_from_token(token: str):
        
    db = get_database()
    users = db["users"]

    user_id = get_user_id_from_token(token)
    return users.find_one({"user_id": user_id})
    
# Kullanıcı bilgilerini alma işlevi
@router.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    if not "token" in request.cookies:
        {"message": "not authorized", "success": False}
    db = get_database()
    users = db["users"]

    if get_user_id_from_token(request.cookies["token"]) != user_id:
        found = users.find_one({"user_id": get_user_id_from_token(request.cookies["token"]), "role": "admin"})
        if found:
            return {"user": users.find_one({"user_id": user_id}), "success": True}
    return {"user": users.find_one({"user_id": user_id}), "success": True}