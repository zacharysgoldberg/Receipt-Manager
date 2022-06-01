# Stub-Manager

Submit receipts to personal account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calulated respectively.

## Design

Backend Flask REST API using flask-migrate, flask-mail (forget password), SQLAlchemy (ORM), pytest, and flask-jwt-extended. PostgreSQL for database, cookies for JWT storage, administrator priveledges, and Docker management.

## How to test endpoints in postman
Install dependencies and run gunicorn app:app or flask run in app dir.
Templates in-progress.

## Future Improvements

To integrate templates, and Py-Tesseract-OCR for scanning uploaded receipts for relevant data migration.
