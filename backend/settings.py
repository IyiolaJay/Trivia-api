from dotenv import load_dotenv
import os
load_dotenv()

db_name = os.environ.get("database")
db_user=os.environ.get("user")
db_password = os.environ.get("password")