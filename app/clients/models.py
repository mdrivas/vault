from app.db import db

class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.relationship('Tasks', backref='client', lazy=True)
