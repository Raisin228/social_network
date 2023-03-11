import psycopg2
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

# get_information_about_server()
# register_user_in_db('elizavet', 'joty')
