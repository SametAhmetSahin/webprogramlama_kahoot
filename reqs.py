import requests

import gemini

prompt = """Please generate a simple chemistry quiz for elementary schoolers, consisting of 5 questions with 3 answers each, with the following JSON format:
{"name": quiz_name,
"questions": [
{"text": question_text, "answers": [
{"text": answer1_text, "correct": is_correct}, {"text": answer2_text, "correct": is_correct},
]}
]}"""

response = gemini.ask_gemini(prompt)

print(response)

requests.post("http://0.0.0.0:8004/quiz/", json=response)

