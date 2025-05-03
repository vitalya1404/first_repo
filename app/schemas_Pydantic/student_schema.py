from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class NewStudentSchema(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone_number: str
    address: str
    enrollment_year: int
    major: str
    course: int
    special_notes: Optional[str] = None
    photo: Optional[str] = Field(None, max_length=100, description="Фото студента")


class StudentSchema(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone_number: str
    address: str
    enrollment_year: int
    major: str
    course: int
    special_notes: Optional[str] = None
    photo: Optional[str] = Field(None, max_length=100, description="Фото студента")

