from fastapi import APIRouter, Request, UploadFile, Cookie

app = APIRouter()

from common import get_database, JSONEncoder, generate_random_string

from hashlib import sha256

from pydantic import BaseModel

"""     
http://192.168.4.107:8004/docs

https://beanieodm.github.io/bunnet/
"""

#from models import Answer, Question, Quiz

import uuid


from routers.users import get_user_id_from_token

@app.post("/quiz")
async def create_quiz(request: Request):
    if not "token" in request.cookies:
        {"message": "not authorized", "success": False}
    print(request.cookies)
    parsed = await request.json()

    #print(parsed)
    #print(parsed.keys())
    
    db = get_database()
    
    quizzes = db["quiz"]

    quiz_id = str(uuid.uuid4())

    questions = []
    for question in parsed["questions"]:
        answers = []
        for answer in question["answers"]:
            new_answer = {"text": answer["text"], "correct": answer["correct"]}
            answers.append(new_answer)
        questions.append({"text": question["text"], "answers": answers})
        
    
    new_quiz = {
        "quiz_id": str(uuid.uuid4()),
        "name": parsed["text"],
        "owner_id": get_user_id_from_token(request.cookies.get("token")),
        "questions": questions,
        "results": [
            {"correct": 0, "incorrect": 0} for i in range(len(questions))
        ]
    }
    
    quizzes.insert_one(new_quiz)

    return quiz_id



@app.get("/quiz/{id}")
async def get_quiz_with_id(id: str, request: Request):
    if not "token" in request.cookies:
        {"message": "not authorized", "success": False}
    db = get_database()
    
    quizzes = db["quiz"]
    quiz = quizzes.find_one({"quiz_id": id})
    #parsed = await request.json()
    #quiz = Quiz.find_one(id)
    del(quiz["_id"])
    if quiz:
        return {"message": "", "status": True, "quiz": quiz}
    return {"message": "", "status": False}

@app.post("/quiz/results/{id}")
async def add_results_to_quiz(request: Request, id: str):
    
    parsed = await request.json()
    db = get_database()
    
    quizzes = db["quiz"]
    quiz = quizzes.find_one({"quiz_id": id})
    print(parsed)
    for i, e in enumerate(parsed):
        print(e)
        if e == True:
            field = "correct"
        else:
            field = "incorrect"
        
        quizzes.update_one(update={"$inc": {f"results.{i}.{field}": 1}}, filter={"quiz_id": quiz["quiz_id"]})
    
    return {"message": "updated with results", "status": True}

from random import randint

@app.post("/quiz/start")
async def start_quiz(request: Request):
    if not "token" in request.cookies:
        {"message": "not authorized", "success": False}
    parsed = await request.json()
    db = get_database()

    qid = parsed["id"]
    print(qid)
    quizzes = db["quiz"]

    quiz = quizzes.find_one({"quiz_id": qid})

    play_number = randint(100000, 999999)

    print(quiz)

    for i in range(len(quiz["results"])):
        
        quizzes.update_one(update={"$set": {f"results.{i}.correct": 0, f"results.{i}.incorrect": 0, "play_number": play_number}}, filter={"quiz_id": qid})

    return {"message": "started quiz", "status": True, "play_number": play_number}


@app.get("/quiz/with_number/{play_number}")
async def get_quiz_with_playnumber(play_number: int, request: Request):
    db = get_database()
    
    quizzes = db["quiz"]
    quiz = quizzes.find_one({"play_number": play_number})

    del(quiz["_id"])
    if quiz:
        return {"message": "", "status": True, "quiz": quiz}
    return {"message": "", "status": False}


from gemini import generate_question

@app.post("/quiz/generate_question")
async def generate_question_api(request: Request):
    if not "token" in request.cookies:
        {"message": "not authorized", "success": False}
    parsed = await request.json()
    try:
        question = generate_question(parsed["prompt"])

        
        return {"message": "", "status": True, "question": question}
    except:
        return {"message": "", "status": False}

"""
@app.get("/quiz/{tur}/")
async def gettur(tur: str, request: Request):
    
    db = get_database()
    users = db["users"]
    res = []
    for i in users.find({"tur": tur}):
        i["_id"] = str(i["_id"])
        res.append(i)
    return res
"""