"""
from bunnet import Document
from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    answer_text: str
    correct: bool

    def __init__(self, text: str, correct: bool):
        self.answer_text = text
        self.correct = correct

class Question(BaseModel):
    question_text: str
    answers: List[Answer]

    def __init__(self, text: str, answers: List[Answer]):
        self.question_text = text
        self.answers = answers

class Quiz(Document):
    quiz_id: str
    name: str
    owner_id: str
    questions: List[Question]

    def __init__(self, quiz_id: str, name: str, owner_id: str, questions: List[Question]):
        self.quiz_id=quiz_id
        self.name=name
        self.owner_id=owner_id
        self.questions=questions
        
class User(Document):
    user_id: str
    username: str
    hashed_password: str
    role: str  # Kullanıcı rolü: 'user' veya 'admin'

    def __init__(self, username: str, password: str, role: str = "user"):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.hashed_password = sha256(password.encode()).hexdigest()
        self.role = role
        
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"
"""