from dotenv import load_dotenv
import os

load_dotenv()
user = os.environ["MYSQL_USER"]
password = os.environ["MYSQL_PASSWORD"]
host = os.environ["MYSQL_HOST"]
port = os.environ["MYSQL_PORT"]
database = os.environ["MYSQL_DATABASE"]

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{database}"
