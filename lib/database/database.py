from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


# database url
DATABASE_URL = 'mysql+pymysql://root:12345678@localhost:3306/lms'

# create engine
engine = create_engine(DATABASE_URL)

# instance of session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a database object
Base = declarative_base()
