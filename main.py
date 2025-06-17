from lib.database import tables,database
from fastapi import FastAPI
from lib.routers import users

app= FastAPI()

tables.Base.metadata.create_all(bind=database.engine)


@app.get('/')
def root():
    return{"message":"Hello Loan management system"}

app.include_router(users.router)

# .\fastapi\Scripts\activate
# pip install fastapi[all] sqlalchemy alembic pymysql
# uvicorn main:app --reload
# pip install -r requirements.txt
# .\venv\Scripts\Activate


# Remove-Item -Recurse -Force venv
# python -m venv venv
# .\venv\Scripts\Activate
# pip install -r requirements.txt