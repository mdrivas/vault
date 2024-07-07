import os
from dotenv import load_dotenv

load_dotenv()

# Reading environment variables
db_user = os.getenv('RDS_USERNAME')
db_host = os.getenv('RDS_HOST')
db_database = os.getenv('RDS_DATABASE')
db_port = os.getenv('RDS_PORT')
mail_server = os.getenv('MAIL_SERVER')
mail_port = os.getenv('MAIL_PORT')
mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')
mail_default_sender = os.getenv('MAIL_DEFAULT_SENDER')
mail_use_tls = os.getenv('MAIL_USE_TLS', 'false').lower() == 'true'

# Print environment variables for debugging
print(f"DB_USER: {db_user}")
print(f"DB_HOST: {db_host}")
print(f"DB_DATABASE: {db_database}")
print(f"DB_PORT: {db_port}")
print(f"MAIL_SERVER: {mail_server}")
print(f"MAIL_PORT: {mail_port}")
print(f"MAIL_USERNAME: {mail_username}")
print(f"MAIL_PASSWORD: {mail_password}")
print(f"MAIL_DEFAULT_SENDER: {mail_default_sender}")
print(f"MAIL_USE_TLS: {mail_use_tls}")
