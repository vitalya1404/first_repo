from datetime import date

from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String
from app.models.custom_types import EmailType


class Base(DeclarativeBase):
    pass

class StudentOrm(Base):
    __tablename__ = 'student'

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column()
    email: Mapped[str] = mapped_column(EmailType(255))  # Використовуємо кастомний тип
    phone_number: Mapped[str] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(String(255))
    enrollment_year: Mapped[int] = mapped_column()
    major: Mapped[str] = mapped_column(String(100))
    course: Mapped[int] = mapped_column()
    special_notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    photo: Mapped[str | None] = mapped_column(String(100), nullable=True)
