# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.clients.models import db, Client
from app.tasks.models import Tasks, StatusEnum
from app.clients.controllers import client_bp
from app.email.controllers import email_bp
from app.tasks.controllers import tasks_bp
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DB_USER=os.getenv('RDS_USERNAME'),
        DB_HOST=os.getenv('RDS_HOST'),
        DB_DATABASE=os.getenv('RDS_DATABASE'),
        DB_PORT=os.getenv('RDS_PORT'),
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=os.getenv('MAIL_PORT'),
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER'),
        MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'false').lower() == 'true',
        SQLALCHEMY_DATABASE_URI=f"postgresql://{os.getenv('RDS_USERNAME')}@{os.getenv('RDS_HOST')}:{os.getenv('RDS_PORT')}/{os.getenv('RDS_DATABASE')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    mail = Mail(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(client_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    return app
