# Stub-Manager

Submit receipts to personal account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calulated respectively.

## Design

Backend Flask REST API using flask-migrate, flask-mail (forget password), SQLAlchemy (ORM), unittest, and flask-jwt-extended. PostgreSQL for database, cookies for JWT storage, administrator priveledges, and Docker management.

## How to test endpoints in postman
Install Python 3+, dependencies `pip install requirements.txt`\
import json collection file into postman\
and run `gunicorn app:app` or `flask run` in app directory.\
Funtional templates not available at this time.

## Future Improvements

To integrate templates, and Py-Tesseract-OCR for scanning uploaded receipts for relevant data migration.
