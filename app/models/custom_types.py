import re
from sqlalchemy.types import TypeDecorator, String


class EmailType(TypeDecorator):
    """Кастомний тип для перевірки email."""

    # Це вказує, що тип даних, який буде використовуватись у базі, це String (текстове поле).
    impl = String  # Визначаємо тип бази даних (String для MySQL, PostgreSQL)

    def __init__(self, length=255):
        """
        Ініціалізатор для кастомного типу.

        :param length: максимальна довжина рядка для email (за замовчуванням 255 символів).
        """
        self.length = length  # Зберігаємо максимальну довжину
        super().__init__()  # Викликаємо конструктор базового класу TypeDecorator

    def process_bind_param(self, value, dialect):
        """
        Цей метод викликається перед тим, як значення буде записано в базу даних.

        :param value: значення, яке буде збережено в базі даних (email).
        :param dialect: діалект SQL (не використовується у цьому методі, але необхідно для роботи з SQLAlchemy).
        :return: перевірене і обрізане значення, якщо воно валідне.

        В даному випадку ми перевіряємо, чи є значення email валідним. Якщо значення валідне, ми обмежуємо його до
        максимального розміру (за замовчуванням 255 символів).
        """
        if value is not None:
            # Перевірка валідності email через регулярний вираз
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                # Якщо email не валідний, викидаємо помилку
                raise ValueError(f"Invalid email address: {value}")
        # Якщо email валідний, повертаємо його з обмеженням довжини
        return value[:self.length] if value else None  # обмеження довжини до self.length

    def process_result_value(self, value, dialect):
        """
        Цей метод викликається після того, як значення буде отримано з бази даних.

        :param value: значення, яке ми отримали з бази даних (email).
        :param dialect: діалект SQL (не використовується в даному випадку).
        :return: значення без змін (email).

        Цей метод повертає значення email, яке ми отримали з бази. Тут немає необхідності змінювати його.
        """
        return value
