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

from routers import quiz, users, webui

app.include_router(quiz.app, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(webui.app)
@app.get("/")
def index():
    return "index"

@app.get("/time/")
def time():
    now = datetime.now()
    return {"second": now.second, "minute": now.minute, "hour": now.hour, "fullstr": now.strftime("%d/%m/%Y %H:%M:%S")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)#, reload=True)
