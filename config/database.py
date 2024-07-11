import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Se instala sqlalchemy el cual nos permite conectarnos de manera sencilla a una base de datos y usar ORM
# Se configura 
sqlite_file_name = "database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

engine = create_engine(database_url,echo=True)

session = sessionmaker(bind=engine)

Base =  declarative_base()