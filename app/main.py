import uvicorn
from fastapi import FastAPI

from app.api.student_router import students_router
from app.db.init_db import create_tables, delete_tables
from app.repositories.student_repositories import insert_startpack_students
from pages.pages import pages_router
from fastapi.staticfiles import StaticFiles


# Функція для створення додатку
def create_app() -> FastAPI:
    # # Викликаємо функцію для створення таблиць в базі даних
    # create_tables()
    # print('База даних створена!')
    #
    # # Додаємо початкових учнів
    # insert_startpack_students()
    # print('Учні додані!')

    # delete_tables()
    # print('База даних удалена!')

    # Створюємо FastAPI додаток
    app = FastAPI()
    print('FastAPI додаток створений!')
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Підключаємо маршрути
    app.include_router(students_router)
    app.include_router(pages_router)

    return app


# Якщо ми не використовуємо створення додатку на рівні модуля, можемо це зробити ось так:
def main():
    app = create_app()  # Створюємо додаток
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)  # Запуск сервера


if __name__ == "__main__":
    main()  # Викликаємо main для запуску
