import jwt
from app.core.config import auth_jwt, settings


def encode_jwt(
        payload,
        private_key: str = auth_jwt.private_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded

def decode_jwt(
        token: str | bytes,
        public_key: str = auth_jwt.public_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded  