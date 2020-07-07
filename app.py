from flask import Flask
app= Flask(__name__)
@app.route('/')
def hello_worls():
    return 'Hello world'
