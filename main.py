from lib.database import tables,database
from fastapi import FastAPI
from lib.routers import transactions, users,auth, loans, loan_plans,over_payments,faqs

app = FastAPI()

# creating tables in database
tables.Base.metadata.create_all(bind=database.engine)


@app.get('/')
def root():
    return{"message":"Hello Loan management system"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(loan_plans.router)
app.include_router(loans.router)
app.include_router(transactions.router)
app.include_router(over_payments.router)
app.include_router(faqs.router)



# .\fastapi\Scripts\activate
# pip install fastapi[all] sqlalchemy alembic pymysql
# uvicorn main:app --reload
# pip install -r requirements.txt
# .\venv\Scripts\Activate


# Remove-Item -Recurse -Force venv
# python -m venv venv
# .\venv\Scripts\Activate
# pip install -r requirements.txt
# pip freeze > requirements.txt    this lists all the installed packages


# Initialize Alembic (once):	alembic init alembic
# Generate migration:	alembic revision --autogenerate -m "add amount_paid"
# Apply migration:	alembic upgrade head
# reverse schema changes: alembic downgrade -1


# alembic stamp head
# alembic revision --autogenerate -m "initial"
# alembic upgrade head

# SHOW CREATE TABLE transactions\G
# ALTER TABLE transactions DROP FOREIGN KEY fk_transactions_user_phone;
# ALTER TABLE transactions DROP INDEX ix_transactions_user_phone;

