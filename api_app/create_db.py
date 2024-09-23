from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://root:password@postgres:5432/mydb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

'''


docker run -d -p 5432:5432 -e POSTGRES_DB=mydb -e POSTGRES_USER=root -e 
POSTGRES_PASSWORD=password --name my-postgres postgres:latest


'''
