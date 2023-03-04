from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get_hello(name='Bogdan'):
    return f'Hello world! {name}'
