from api import create_app
from api.models.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

app.app_context().push()

seed = User(firstname='Firstname',
            lastname='Lastname',
            email='admin@domain.com',
            password=generate_password_hash(
                'admin123'),
            authenticated=False)

db.session.add(seed)
db.session.commit()
