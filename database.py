from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

## Load environment variables from .env file
load_dotenv()



## Create the database engine and session and importing db url from env file
engine = create_engine(os.getenv("db_url"))
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)