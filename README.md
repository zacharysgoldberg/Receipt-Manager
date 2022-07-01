# Stub-Manager

Submit receipts to account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calculated respectively.

## Design

Backend Flask REST API and microservice using flask-migrate, flask-mail (forget password), SQLAlchemy, Unittest tests, Docker, and flask-jwt-extended. PostgreSQL for both primary and test databases.
Integration of [Receipt-OCR](https://github.com/Asprise/receipt-ocr) API for scanning uploaded receipt files and retrieving/parsing relevant data.

## Test Endpoints

Install dependencies `pip install -r requirements.txt`, import json collection file into Postman, and run `gunicorn app:app` in app directory.

## Hosted


