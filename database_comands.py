import psycopg2
from fastapi import HTTPException

from config import db_host, db_user, db_password, db_name


def get_information_about_server():
	"""Получаем версию бд на сервере"""
	try:
		# подключаемся к бд
		with psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name) as connection:

			# создаём курсор для выполнения запроса к бд
			with connection.cursor() as cursor:
				cursor.execute('SELECT version();')
				print(cursor.fetchone())

	except Exception as _ex:
		print(f'[INFO] Error while working with PostgresSQL {_ex}')


def user_exist_in_db(user_login: str) -> list:
	"""Функция для проверки наличия пользователя в бд
		если пользователь существует возвращается его id иначе -1"""
	try:
		with psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name) as connection:

			cursor = connection.cursor()
			cursor.execute("SELECT * FROM users")

			for user_in_db in cursor.fetchall():
				if user_in_db[2].lower() == user_login.lower():
					return user_in_db
	except:
		return []
	finally:
		cursor.close()
	return []


def register_user_in_db(newuser_login, newuser_password):
	"""Функция которая записывает данные о пользователе в бд
	если пользователя с таким логином и паролем не существует"""

	try:
		# подключение к бд
		with psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name) as connection:

			# создаём курсор для выполнения запроса к бд
			with connection.cursor() as cursor:
				cursor.execute('SELECT * FROM users;')

				# проверяем уникальность логина нового пользователя
				flag = user_exist_in_db(newuser_login)

				if flag:
					print('[INFO] пользователь с таким логином уже существует')
					return -1
				else:
					# добавляем пользователя в бд если такого же не существует
					cursor.execute(
						f"INSERT INTO users (username, user_password) VALUES ('{newuser_login}', '{newuser_password}');"
					)
					connection.commit()
					return cursor.execute(
						f"SELECT id FROM users where username='{newuser_login}'"
					)
	except Exception as _ex:
		print(f'[ERROR] что-то пошло не так O_o {_ex}')
		return -1


def change_user_profil_information(id_user, firs_name, las_name, pasword):
	# Проверяем нужно ли что то менять
	ans = []
	if firs_name is not None or las_name is not None or pasword is not None:
		old_data = [None, None, None]
		try:
			# подключение к бд
			with psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name) as connection:

				# создаём курсор для выполнения запроса к бд
				with connection.cursor() as cursor:

					# меняем нужные данные
					if firs_name is not None:
						cursor.execute(f"SELECT first_name from users WHERE id={id_user};")
						old_data[0] = cursor.fetchone()[0]
						cursor.execute(f"UPDATE users SET first_name = '{firs_name}' WHERE id={id_user};")
					if las_name is not None:
						cursor.execute(f"SELECT last_name from users WHERE id={id_user};")
						old_data[1] = cursor.fetchone()[0]
						cursor.execute(f"UPDATE users SET last_name = '{las_name}' WHERE id={id_user};")
					if pasword is not None:
						cursor.execute(f"SELECT user_password from users WHERE id={id_user};")
						old_data[2] = cursor.fetchone()[0]
						cursor.execute(f"UPDATE users SET user_password = '{pasword}' WHERE id={id_user};")
		# в случае если что то пошло не так
		except:
			return HTTPException(status_code=500, detail='Internal server error')

		if old_data[0] is not None:
			ans.append(f'{old_data[0]} изменено на -> {firs_name}')
		if old_data[1] is not None:
			ans.append(f'{old_data[1]} изменено на -> {las_name}')
		if old_data[2] is not None:
			ans.append(f'{old_data[2]} изменено на -> {pasword}')
		return ans
	else:
		return ans


#print(change_user_profil_information(9, None, 'aaaaaaa', 'bbbbbb'))
# get_information_about_server()
# register_user_in_db('elizavet', 'joty')
