import sys
import os
from flask_migrate import Migrate
from app import create_app
from app.db import db
from app.clients.models import Client
from app.tasks.models import Tasks, StatusEnum

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
