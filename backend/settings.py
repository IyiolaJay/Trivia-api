from dotenv import load_dotenv
import os
load_dotenv()

db_name = os.environ.get("database")
db_user=os.environ.get("user")
db_password = os.environ.get("password")

#You should rename the environment variables to your machine's environment variables peculiar to your database details. 