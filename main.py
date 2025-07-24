from fastapi import FastAPI, requests
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
import http.server
import json

app = FastAPI()


@app.get("/hello")
def read_hello(request: Request,name: str = "Non Defini"):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    if name == "Non Defini":
        return JSONResponse({"message": "welcome"}, status_code=200)
    else:
        return JSONResponse({"message": f"welcome {name}"},status_code=200)


class WelcomeRequest(BaseModel):
    name: str

class Student(BaseModel):
    Reference: str
    FirstName: str
    LastName: str
    Age: int

students = []

@app.post("/students", response_model=list[Student], status_code=201)
async def add_students(new_students: list[Student]):
    students.extend(new_students)
    return JSONResponse(content=students, status_code=201)

@app.get("./student", response_model=list[Student], status_code=200)
def get_students():
    return JSONResponse(content=students, status_code=200)

@app.put("/students", response_model=list[Student], status_code=200)
async def update_or_add_student(student: Student):
    for i, existing_student in enumerate(students):
        if existing_student.Reference == student.Reference:

            if (existing_student.FirstName != student.FirstName or
                    existing_student.LastName != student.LastName or
                    existing_student.Age != student.Age):
                students[i] = student

            return JSONResponse(content=students, status_code=200)


    students.append(student)
    return JSONResponse(content=students, status_code=200)