from fastapi import APIRouter, Request, UploadFile, Cookie

app = APIRouter()

from common import get_database, JSONEncoder, generate_random_string, brandname

from hashlib import sha256

@app.post("/users/login/")
async def login(request: Request):
    parsed = await request.json()

    db = get_database()
    users = db["users"]

    res = users.find_one({"email": parsed["email"], "password": sha256(parsed["password"].encode()).hexdigest()})
    print(res)
    if res:
        return {"valid": True, "id": str(res["_id"])}
    return False
    
import emailsender
@app.post("/users/resetpassword/")
async def sifreyenile(request: Request):
    parsed = await request.json()
    
    email = parsed["email"]
    newpass = generate_random_string(8)
    print(email, " kullanıcısı için yeni şifre", newpass)

    hashed = sha256(newpass.encode()).hexdigest()
    print("hashed", hashed)
    
    db = get_database()
    users = db["users"]
    res = users.update_one({"email": email}, {"$set": {"password": hashed}})
    
    if res.modified_count == 0:
        return {"valid": False, "message": "Bu emaile sahip bir kullanıcı bulunmamaktadır."}
    res = users.find_one({"email": email, "password": hashed})
    
    emailsender.send_email(f"{brandname} - Şifre Yenileme", f"""
Merhaba {res["name"]}!
{brandname} hesabınız için şifre yenileme talebi oluşturdunuz.
{res["email"]} emailli hesabınız için yeni şifreniz: {newpass}
Sağlıkla kalın!""", recipients=[email])
    return {"valid": True, "message": f"{email} mailine şifre yenileme maili gönderilmiştir."}

import shutil
@app.post("/users/upload_profile_picture/")
def upload_profile_picture(file: UploadFile):
    with open(f"img/{file.filename}", "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"filename": "img/"+file.filename}

mesaj = {"kimden": "",
         "tarih": "",
         "icerik": ""}

import os
@app.post("/users/create/")
async def create_user(request: Request):


    parsed = await request.json()

    newpass = generate_random_string(8)

    
    
    db = get_database()
    users = db["users"]
    parsed["password"] = sha256(newpass.encode()).hexdigest()

    newuser = {
    "email": parsed["email"],
    "password": parsed["password"],
    "name": parsed["name"],
    "tur": parsed["tur"],
    "birthdate": parsed["birthdate"],
    "phonenumber": parsed["phonenumber"],
    "gender": parsed["gender"],
    "egzersizler": [],
    "beslenmeduzeni": [[]],
    "mesajlar": [],
}

    res = users.insert_one(newuser)
    
    emailsender.send_email(f"{brandname} - Şifre Yenileme", f"""
Merhaba {parsed["name"]}!
{brandname} hesabınız için şifre yenileme talebi oluşturdunuz.
{parsed["email"]} emailli hesabınız için yeni şifreniz: {newpass}
Sağlıkla kalın!""", recipients=[parsed["email"]])
    
    print(parsed["photoname"])
    print(f"""img/{parsed["photoname"]}""", f"""img/{res.inserted_id}.png""")
    os.rename(f"""img/{parsed["photoname"]}""", f"""img/{res.inserted_id}.png""")
    return {"id": str(res.inserted_id)}

from bson import ObjectId
@app.get("/users/{id}/")
async def get_user(id: str, request: Request):
    
    db = get_database()
    users = db["users"]

    res = users.find_one({"_id": ObjectId(id)})
    if res:
        print(res)
        res["_id"] = str(res["_id"])
        return res
    else:
        return False
"""{
    _id: ObjectId('656bea118d22e499d78b60d8'),
    email: 'sametahmetsahin1212@gmail.com',
    password: '45523bff12244e03ed64a55fd5953a868f814ba864df13b2b86aa07304be8f7c',
    display_name: 'Samet Ahmet Şahin',
    user_type: 1,
    birth_date: '2023/12/1',
    phone_number: '05387902535',
    profile_picture_id: 'default',
    gender: 1,
    egitmenid: ''
}"""

@app.post("/users/update/{id}/")
async def update(id: str, request: Request):
    try:
        parsed = await request.json()

        print(parsed)
        
        db = get_database()
        users = db["users"]
        res = users.update_one({"_id": ObjectId(id)}, {"$set": parsed})

        print(parsed["photoname"])
        print(f"""img/{parsed["photoname"]}""", f"""img/{id}.png""")
        os.rename(f"""img/{parsed["photoname"]}""", f"""img/{id}.png""")
        return True
    except:
        return False

@app.get("/users/")
async def gettur(request: Request):
    
    db = get_database()
    users = db["users"]
    res = []
    for i in users.find({}):
        i["_id"] = str(i["_id"])
        res.append(i)
    return res

@app.get("/users/{tur}/")
async def gettur(tur: str, request: Request):
    
    db = get_database()
    users = db["users"]
    res = []
    for i in users.find({"tur": tur}):
        i["_id"] = str(i["_id"])
        res.append(i)
    return res