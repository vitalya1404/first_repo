from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.exc import NoResultFound

from app.db.student_session import get_db
from app.path_to_json import path_to_json
from app.repositories.student_repositories import insert_student_to_orm, get_student_by_filter_orm, update_student_orm, \
    delete_student_orm
from app.schemas_Pydantic.student_schema import NewStudentSchema
from utils import json_to_dict_list
from sqlalchemy.orm import Session

students_router = APIRouter(prefix='/students', tags=['Students'])

#READ
@students_router.get("/")
def get_all_students(
        db: Session = Depends(get_db),
        first_name: str | None = None,
        last_name: str | None = None):
    return get_student_by_filter_orm(db, first_name, last_name)

@students_router.get("/filter_by/{course}", response_model=List[dict])
def filter_students(
    course: int,
    major: str | None = None,
    enrollment_year: int | None = None
):
    students = json_to_dict_list(path_to_json)
    filtered_students = [s for s in students if s["course"] == course]

    if major:
        filtered_students = [
            s for s in filtered_students if s['major'].lower() == major.lower()
        ]

    if enrollment_year:
        filtered_students = [
            s for s in filtered_students if s['enrollment_year'] == enrollment_year
        ]

    return filtered_students

#CREATE
@students_router.post("/new_user")
def create_student(
    student_data: NewStudentSchema,
    db: Session = Depends(get_db)  # FastAPI сам створить сесію і передасть сюди
):
    return insert_student_to_orm(db, student_data)

#UPDATE
@students_router.post("/update_student")
def update_student(
    student_data: NewStudentSchema,
    student_id: int,
    db: Session = Depends(get_db)  # FastAPI сам створить сесію і передасть сюди
):
    try:
        # Викликаємо функцію для оновлення студента в базі даних
        updated_student = update_student_orm(db, student_id, student_data)
        return {"message": "Student updated successfully", "student": updated_student}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )


#DELETE
@students_router.post("/delete_student")
def delete_student(
        student_id: int,
        db: Session = Depends(get_db)
):
    delete_student_orm(db, student_id)
    return {"message":"Student deleted successfully"}
