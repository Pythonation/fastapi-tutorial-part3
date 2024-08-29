import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
  id: int = None
  name: str
  grade: int

def setup_database():
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS students (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              grade INTEGER
          )
      ''')
      conn.commit()
      conn.close()
  except sqlite3.Error as e:
      print(f"Database setup error: {e}")

# Call setup_database at the start of the application
setup_database()

@app.get("/students/")
async def read_students():
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM students")
      rows = cursor.fetchall()
      conn.close()
      return rows
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to fetch students"}

@app.post("/students/")
async def create_student(student: Student):
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
      conn.commit()
      conn.close()
      return {"message": "Student added successfully"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to create student"}
  
@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (student.name, student.grade, student_id))
      conn.commit()
      conn.close()
      return {"id": student_id, **student.dict()}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to update student"}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
      conn.commit()
      conn.close()
      return {"message": "Student deleted"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to delete student"}