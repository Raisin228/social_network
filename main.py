from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt, decode_jwt
from database_comands import register_user_in_db, user_exist_in_db, change_user_profil_information

app = FastAPI(title='Social_network')


@app.post('/login')
def login_user(login, password):
	"""вход пользователя в систему при успехе user получает новый jwt"""
	inform_user_was_reg = user_exist_in_db(login)

	# если пользователь есть в системе отсылаем ему новый jwt
	if len(inform_user_was_reg) != 0 and inform_user_was_reg[4] != password:
		raise HTTPException(status_code=401, detail='Unauthorized (неверный пароль)')
	elif not inform_user_was_reg:
		raise HTTPException(status_code=401,
							detail='Unauthorized (неверный логин или пользователя с таким логином не существует)')
	else:
		return {'status': 200, 'access_token': sign_jwt(inform_user_was_reg[3], login)}


@app.post('/registration')
def register_user(login, password):
	"""роут для регистрации пользователя в бд
	в случае ошибки возвращается код 401"""

	reg_user_in_db = register_user_in_db(login, password)
	if reg_user_in_db == -1:
		raise HTTPException(status_code=401, detail='Unauthorized (Пользователь с таким логином существует)')
	else:
		return {'access_token': sign_jwt(login, reg_user_in_db)}


@app.get('/profile', dependencies=[Depends(JWTBearer())])
def get_inform_about_user(token: str = Depends(JWTBearer())):
	"""Роут для получения информации о пользователе
	Защищённый эндпоинт информацию с которого могут получать только валидные токены"""
	inform_from_token = decode_jwt(token)
	user_inform = user_exist_in_db(inform_from_token['user_name'])

	return {'status': 200,
			'user_information': {'first_name': user_inform[0], 'last_name': user_inform[1],
								 'username': user_inform[2], 'user_password': user_inform[4]}
			}


@app.put('/profile', dependencies=[Depends(JWTBearer())])
def change_user_inform(first_name=None, last_name=None, user_password=None, token: str = Depends(JWTBearer())):
	"""Изменяет некоторую пользовательскую информацию"""
	inform_from_token = decode_jwt(token)

	return change_user_profil_information(inform_from_token['user_id'], first_name, last_name, user_password)



if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
