from src import create_app


app = create_app()


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return 'Hello'


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000)
