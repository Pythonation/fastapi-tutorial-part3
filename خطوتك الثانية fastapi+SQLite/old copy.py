from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
  id: int
  name: str
  grade: int

students = [
  Student(id=1, name="karim ali", grade=5),
  Student(id=2, name="khadija ahmed", grade=3),
]

@app.get("/students/")
def read_students():
  return students

@app.post("/students/")
def create_student(student: Student):
  students.append(student)
  return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
  for index, s in enumerate(students):
    if s.id == student_id:
      students[index] = student
      return student
  return {"error": "Student not found"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
  for index, s in enumerate(students):
    if s.id == student_id:
      del students[index]
      return {"message": "Student deleted"}
  return {"error": "Student not found"}