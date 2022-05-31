import os
from api import create_app
from api.models import User
from flask_jwt_extended import jwt_required


app = create_app()


@app.route("/home")
@jwt_required(optional=True)
def index():
    resp = "Welcome to Stub-Manager"
    return resp


app.app_context().push()

email = os.environ.get('ADMIN')
# [create admin if they do not exist]
# if User.query.get(1) is None:
#     User.create_user(
#         email=email,
#         password=os.environ.get('MAIL_PASSWORD'),
#         access=2
#     )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
