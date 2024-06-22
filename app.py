from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

app = Flask(__name__)
# Configure CORS to allow requests from localhost:3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mattdrivas@localhost:54320/financial_planning'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.Column(db.JSON, nullable=True)

# Create the database schema within the application context
with app.app_context():
    db.create_all()

@app.route('/add_client', methods=['OPTIONS', 'POST'])
def add_client():
    
    if request.method == 'POST':
        data = request.json
        logging.info(f"Received data: {data}")
        new_client = Client(name=data['name'], email=data['email'], tasks={})
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'message': 'Client added successfully!'}), 201

@app.route('/api/data', methods=['GET'])
def get_data():
    clients = Client.query.all()
    clients_list = []
    for client in clients:
        clients_list.append({
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'tasks': client.tasks
        })
    return jsonify(clients_list)




if __name__ == '__main__':
    app.run(debug=True)
