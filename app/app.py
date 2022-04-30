from api import create_app
import os

app = create_app()


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return 'Welcome to Receipt Manager'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
