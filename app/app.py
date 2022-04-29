from src import create_app
import os

app = create_app()


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return 'Welcome to Receipt Manager'


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
