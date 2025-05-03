import shutil
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.api.student_router import create_student
from app.db.student_session import get_db
from app.repositories.student_repositories import get_student_by_filter_orm, get_student_by_id_orm, update_student_orm, \
    delete_student_orm, insert_student_to_orm
from app.schemas_Pydantic.student_schema import NewStudentSchema

pages_router = APIRouter(prefix='/pages', tags=['Frontend'])
templates = Jinja2Templates(directory='app/templates')

@pages_router.post('/add_photo')
async def add_student_photo(file: UploadFile, image_name: int, type_file: str):
    with open(f"app/static/images/{image_name}.{type_file}", "wb+") as photo_obj:
        shutil.copyfileobj(file.file, photo_obj)

#GET ALL STUDENTS
@pages_router.get("/students/", response_class=HTMLResponse)
def get_students_by_filter(
        request: Request,
        db: Session = Depends(get_db),
        first_name: str | None = None,
        last_name: str | None = None):
    students = get_student_by_filter_orm(db, first_name, last_name)
    return templates.TemplateResponse("get_students_by_filter.html", {
        "request": request,
        "students": students,
        "first_name": first_name,
        "last_name": last_name,
    })

#GET INFO FOR 1 STUDENT
@pages_router.get("/students/{student_id}", response_class=HTMLResponse)
def get_student_by_id(
        request: Request,
        student_id: int,
        db: Session = Depends(get_db),
):
    student = get_student_by_id_orm(db, student_id)
    return templates.TemplateResponse("get_student_full_info.html", {
        "request": request,
        "student": student,
    })

@pages_router.get("/students/add/", response_class=HTMLResponse)
def add_students_form(
        request: Request
):
    return templates.TemplateResponse("add_student_form.html", {
        "request": request
    })

@pages_router.post("/students/add/", response_class=HTMLResponse)
def add_students_to_db(
        request: Request,
        db: Session = Depends(get_db),
        first_name: str = Form(...),
        last_name: str = Form(...),
        date_of_birth: str = Form(...),  # в форматі YYYY-MM-DD
        email: EmailStr = Form(...),
        phone_number: str = Form(...),
        address: str = Form(...),
        enrollment_year: int = Form(...),
        major: str = Form(...),
        course: int = Form(...),
        special_notes: str = Form(None),
        photo: str = Form(...)
):
    # Перетворення строки у дату
    try:
        parsed_dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
        return HTMLResponse(content="Invalid date format. Use YYYY-MM-DD.", status_code=400)


    student_data = NewStudentSchema(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=parsed_dob,
        email=email,
        phone_number=phone_number,
        address=address,
        enrollment_year=enrollment_year,
        major=major,
        course=course,
        special_notes=special_notes,
        photo=photo
    )

    # Викликаємо функцію створення студента
    response = insert_student_to_orm(student_data=student_data, db=db)

    return RedirectResponse(
        url=f"/pages/students/{response.student_id}/success/add",
        status_code=303
    )

#UPDATE
@pages_router.get("/students/{student_id}/edit", response_class=HTMLResponse)
def update_student_form(
        request: Request,
        student_id: int,
        db: Session = Depends(get_db),
):
    student = get_student_by_id_orm(db, student_id)
    return templates.TemplateResponse("update_student_form.html",{
        "request": request,
        "student": student
    })

@pages_router.post("/students/{student_id}/edit", response_class=HTMLResponse)
def update_student_to_db(
        request: Request,
        student_id: int,
        db: Session = Depends(get_db),
        first_name: str = Form(...),
        last_name: str = Form(...),
        date_of_birth: str = Form(...),  # в форматі YYYY-MM-DD
        email: EmailStr = Form(...),
        phone_number: str = Form(...),
        address: str = Form(...),
        enrollment_year: int = Form(...),
        major: str = Form(...),
        course: int = Form(...),
        special_notes: str = Form(None),
        photo: str = Form(...)
):
    # Перетворення строки у дату
    try:
        parsed_dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
        return HTMLResponse(content="Invalid date format. Use YYYY-MM-DD.", status_code=400)

    student_data = NewStudentSchema(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=parsed_dob,
        email=email,
        phone_number=phone_number,
        address=address,
        enrollment_year=enrollment_year,
        major=major,
        course=course,
        special_notes=special_notes,
        photo=photo
    )

    student = update_student_orm(db, student_id, student_data)
    return RedirectResponse(
        url=f"/pages/students/{student_id}/success/update",
        status_code=303
    )

#DELETE
@pages_router.get("/students/{student_id}/delete_user")
def delete_student(
        request: Request,
        student_id: int,
        db: Session = Depends(get_db),
):
    student = get_student_by_id_orm(db,student_id)
    delete_student_orm(db,student_id)
    return templates.TemplateResponse("student_success.html", {
        "request": request,
        "student": student,
        "message": "Студента успішно видалено!",
        "action": "delete"
    })


# SUCCESS
@pages_router.get("/students/{student_id}/success/{action}", response_class=HTMLResponse)
def student_success(
        request: Request,
        student_id: int,
        action: str,
        db: Session = Depends(get_db)
):
    student = get_student_by_id_orm(db, student_id)
    # Повідомлення для кожної дії
    messages = {
        "add": "Студента успішно додано!",
        "update": "Студента успішно оновлено!",
    }
    message = messages.get(action, "Операція виконана успішно.")

    return templates.TemplateResponse("student_success.html", {
        "request": request,
        "student": student,
        "message": message,
        "action": action
    })





