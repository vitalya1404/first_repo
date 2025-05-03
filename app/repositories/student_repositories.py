from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db.student_session import session_factory
from app.models.student_model import StudentOrm
from app.path_to_json import path_to_json
from utils import json_to_dict_list

#CREATE
def insert_startpack_students() -> None:
    students = json_to_dict_list(path_to_json)
    for student in students:
        with session_factory() as session:
            new_student = StudentOrm(**student)
            session.add(new_student)
            session.commit()
    return None

def insert_student_to_orm(db: Session, student_data):
    student = StudentOrm(**student_data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

#READ
def get_student_by_filter_orm(
        db: Session,
        first_name: str | None = None,
        last_name: str | None = None) -> List[StudentOrm]:
    query = db.query(StudentOrm)

    if first_name:
        query = query.filter(StudentOrm.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(StudentOrm.last_name.ilike(f"%{last_name}%"))

    return query.order_by(StudentOrm.student_id).all()

def get_student_by_id_orm(
        db: Session,
        student_id: int ) -> StudentOrm:
    query = db.query(StudentOrm).filter_by(student_id=student_id)

    return query.first()



#UPDATE
def update_student_orm(
    db: Session,
    student_id: int,
    student_data
):
    student = db.query(StudentOrm).filter(StudentOrm.student_id == student_id).first()

    if not student:
        raise NoResultFound(f"Student with ID {student_id} not found.")

    for key, value in student_data.dict().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

#DELETE
def delete_student_orm(
        db: Session,
        student_id: int
):
    # Знайдемо студента за ID
    student = db.query(StudentOrm).filter(StudentOrm.student_id == student_id).first()

    if student:
        db.delete(student)  # Видалимо знайдений об'єкт
        db.commit()  # Підтвердимо зміни в базі даних
    else:
        print(f"Студента з ID {student_id} не знайдено.")




