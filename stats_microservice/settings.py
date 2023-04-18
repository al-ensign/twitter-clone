import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


TOKEN_TYPE = os.getenv('TOKEN_TYPE')
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE")



