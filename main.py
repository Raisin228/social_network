from fastapi import FastAPI

app = FastAPI(
	title='Social_network'
)


@app.post('/registration')
def login_user(login, password):
	return {'status': 200, 'login': login, 'password': password}
