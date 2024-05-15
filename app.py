from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

import json

from common import get_database, JSONEncoder


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


kullanicilar = [
    {"email": "sametahmetsahin1212@gmail.com", "password": "12345678"},
    {"email": "nusretyildiz2003@gmail.com", "password": "12345678"}
]

from routers import users

app.include_router(users.app)

@app.get("/")
def index():
    return "index"

@app.get("/time/")
def time():
    now = datetime.now()
    return {"second": now.second, "minute": now.minute, "hour": now.hour, "fullstr": now.strftime("%d/%m/%Y %H:%M:%S")}

@app.get("/dbtest/")
def dbtest():
    db = get_database()
    users = db["users"]
    print(users)
    for i in users.find():
        print(i)
    return JSONEncoder().encode(i)
    
    pass

"""
def DanismanEsle():
    puan = []
    for i in range(len(id)):
        puan.append(0)
        for j in hedefler:
            if j in profesion[i]
                puan[i] = puan[i] + 11
    kalan 
    """