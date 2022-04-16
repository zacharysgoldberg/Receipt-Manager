from src import create_app
from flask import Flask


app = create_app()


@app.route('/')
def hello():
    return 'Hello'


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000)
