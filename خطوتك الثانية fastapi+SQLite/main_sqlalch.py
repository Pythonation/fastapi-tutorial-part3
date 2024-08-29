from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grade = Column(Integer)

Base.metadata.create_all(bind=engine)

# Pydantic model
class Student(BaseModel):
    id: int = None
    name: str
    grade: int

    class Config:
        orm_mode = True

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()
    return students

@app.post("/students/")
def create_student(student: Student, db: Session = Depends(get_db)):
    db_student = StudentDB(name=student.name, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": "Student added successfully", "student": db_student}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.grade = student.grade
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}