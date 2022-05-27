import os
from api import create_app
from api.models import User

app = create_app()

app.app_context().push()

email = os.environ.get('ADMIN')
# [create admin if they do not exist]
if User.query.get(1) is None:
    User.create_user(
        email=email,
        password=os.environ.get('MAIL_PASSWORD'),
        access=2
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
