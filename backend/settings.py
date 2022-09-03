from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.environ.get("DATABASE_NAME")
DB_USER = os.environ.get("DATABASE_USER")
