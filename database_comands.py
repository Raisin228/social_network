import psycopg2
from config import host, user, password, db_name


def get_information_about_server():
	"""Получаем версию бд на сервере"""
	try:
		# подключаемся к бд
		with psycopg2.connect(host=host, user=user, password=password, database=db_name) as connection:

			# создаём курсор для выполнения запроса к бд
			with connection.cursor() as cursor:
				cursor.execute('SELECT version();')
				print(cursor.fetchone())

	except Exception as _ex:
		print(f'[INFO] Error while working with PostgresSQL {_ex}')


def register_user_in_db(newuser_login, newuser_password):
	"""Функция которая записывает данные о пользователе в бд
	если пользователя с таким логином и паролем не существует"""

	try:
		# подключение к бд
		with psycopg2.connect(host=host, user=user, password=password, database=db_name) as connection:
			flag = True

			# создаём курсор для выполнения запроса к бд
			with connection.cursor() as cursor:
				cursor.execute('SELECT * FROM users;')

				# проверяем уникальность логина нового пользователя
				for user_in_db in cursor.fetchall():
					if user_in_db[2].lower() == newuser_login.lower():
						flag = False
						break

				if not flag:
					print('[INFO] пользователь с таким логином уже существует')
				else:
					# добавляем пользователя в бд если такого же не существует
					cursor.execute(
						f"INSERT INTO users (username, user_password) VALUES ('{newuser_login}', '{newuser_password}');"
					)
					connection.commit()
	except Exception:
		print('[ERROR] что-то пошло не так O_o')

# get_information_about_server()
# register_user_in_db('elizavet', 'joty')
