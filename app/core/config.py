from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Визначаємо кореневу директорію проєкту (на 2 рівні вище від цього файлу)
BASE_DIR = Path(__file__).parent.parent
# Формуємо повний шлях до файлу бази даних SQLite
DB_PATH = BASE_DIR / "db.sqlite3"
load_dotenv()

# Окрема модель для зберігання шляхів до JWT ключів
class AuthJWT(BaseModel):
    # Шлях до приватного ключа для підпису JWT
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    # Шлях до публічного ключа для перевірки підпису JWT
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str ="RS256"

# Основна конфігураційна модель, яка читає змінні з .env
class Settings(BaseSettings):
    # Змінна для підключення до бази даних
    database_url: str

    # Конфігурація вказує, звідки брати змінні середовища
    class Config:
        env_file = ".env"  # автоматичне завантаження .env файлу

# Ініціалізація конфігураційного класу з .env
settings = Settings()

# Ініціалізація JWT конфігурації зі шляхами до ключів
auth_jwt = AuthJWT()
