import os
from api import create_app, load
from flask import render_template
from api.models import User
from flask_jwt_extended import jwt_required


app = create_app()

app.app_context().push()


@app.route("/")
@jwt_required(optional=True)
def index():
    return render_template('home.html')


# [create admin account if not exist]

"""if User.query.get(1) is None:
    @app.before_first_request
    def create_admin():
            email = os.getenv('ADMIN')
            User.create_user(
                email=email,
                password=os.getenv('MAIL_PASSWORD'),
                access=2
            )"""


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
