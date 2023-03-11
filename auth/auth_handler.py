import time
import jwt
from config import SECRET, ALGORITHM

JWT_SECRET = SECRET
JWT_ALGORITHM = ALGORITHM


def sign_jwt(user_id: int, user_name: str):
	"""создание jwt-токена и отправка пользователю"""
	payload = {
		'user_id': user_id,
		'user_name': user_name,
		'expires_at': time.time() + 3600
	}
	token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

	return token


def decode_jwt(token: str) -> dict:
	"""функция для декодирования jwt-токенов"""
	try:
		decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		return decoded_token if decoded_token['expires_at'] >= time.time() else None

	except Exception as _ex:
		return {f'{_ex}': 422}

# f = signJWT('12', 'bog')
# print(f)
# print(decodeJWT('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIiLCJ1c2VyX25hbWUiOiJib2ciLCJleHBpcmVzX2F0IjoxNjc4NTYzNDA5Ljg4ODQzNDZ9.KyBSyYbt-yGzFBmDpmb59RrWx_xdrJIhToG3129HuGQ'))
