from src import create_app


app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000)
