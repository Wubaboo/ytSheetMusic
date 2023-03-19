from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def hello_world():
    return "<h1>Hello World!</h1>"

@app.post('/<test>')
def post(test):
    print(test)
    data = request.get_json()
    return data