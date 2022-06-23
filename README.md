# Stub-Manager

Submit receipts to personal account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calulated respectively.

## Design

Backend Flask REST API using flask-migrate, flask-mail (forget password), SQLAlchemy, unittest tests, and flask-jwt-extended. PostgreSQL, JWT cookie storage, and Docker.

## How to test endpoints in postman

Install dependencies `pip install -r requirements.txt`, import json collection file into postman, and `run gunicorn app:app` or `flask run` in app directory.

## Future Improvements

Integration of [Receipt-OCR](https://github.com/Asprise/receipt-ocr) API for scanning uploaded receipt files and retrieving/parsing relevant data.
