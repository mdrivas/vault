from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum


db = SQLAlchemy()

class StatusEnum(enum.Enum):
    not_assigned = "Not Assigned"
    in_progress = "In Progress"
    completed = "Completed"


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignee = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    status = db.Column(Enum(StatusEnum), nullable=False, default=StatusEnum.not_assigned)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
