from openai import OpenAI


with open("openai_token.txt") as tokenfile:
    key = tokenfile.read()
client = OpenAI(api_key=key)

# Define the system message
system_msg = 'You are a digital quiz creator who will generate questions and answers for education and learning.'

# Define the user message
user_msg = """Please generate a simple math question for elementary schoolers, with the following JSON format:
{"text": question_text, "answers": [
{"text": answer1_text, "correct": is_correct}, {"text": answer2_text, "correct": is_correct},
]}"""

# Create a dataset using GPT

completion = client.chat.completions.create(model="gpt-3.5-turbo",response_format={ "type": "json_object" },
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])

print(completion.choices[0].message)

"""{"name": name,
"questions": [
{"text": question_text, "answers": [
{"text": answer1_text, "correct": is_correct}, {"text": answer2_text, "correct": is_correct},
]}
]}"""

"""
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
        """