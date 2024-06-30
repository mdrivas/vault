from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Date
from flask_cors import CORS
from flask_mail import Mail, Message
import logging
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_HOST'] = os.getenv('DB_HOST')
app.config['DB_DATABASE'] = os.getenv('DB_DATABASE')
app.config['DB_PORT'] = os.getenv('DB_PORT')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
# Set default for MAIL_USE_TLS or handle NoneType
mail_tls = os.getenv('MAIL_MAIL_TLS')
app.config['MAIL_USE_TLS'] = mail_tls and mail_tls.lower() == 'true'



# Configure CORS to allow requests from localhost:3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}@{host}:{port}/{database}'.format(
    user=app.config['DB_USER'],
    host=app.config['DB_HOST'],
    port=app.config['DB_PORT'],
    database=app.config['DB_DATABASE']
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.Column(db.JSON, nullable=True, default=list)  # Default to a list

# Create the database schema within the application context
with app.app_context():
    db.create_all()

@app.route('/add_client', methods=['POST'])
def add_client():
    data = request.json
    logging.info(f"Received data: {data}")
    new_client = Client(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        tasks={}
    )
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

@app.route('/send_email', methods=['POST'])
def send_email():
    #Fetch client
    client = Client.query.filter_y(id=2).first()
    print("Sending client: ", client) 

    #Fetch content
    content = "TEST CONTENT" #Placeholder
    
    #Generate email 
    email_content = generate_email_content(client, content)

    #Send email
    send_email(client.email, "FSW Email", email_content)
    print("email sent for: ", client)
    return

def generate_email_content(client, content):
    return f"""
    Hello {client.first_name} {client.last_name},

    Here is your personalized email:

    {content}

    Regards, 
    FSW Team
    """


def send_email(to, subeject, body):
    msg = Message(subeject, recipients=[to])
    msg.body = body
    mail.send(msg)
    return "Email sent successfully"
@app.route('/api/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    
    client_data = {
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email,
        'tasks': client.tasks
    }
    return jsonify(client_data)

@app.route('/api/client/<int:client_id>/tasks', methods=['POST'])
def add_task(client_id):
    data = request.json
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404

    # Ensure tasks is a dictionary
    if client.tasks is None or isinstance(client.tasks, list):
        client.tasks = {}

    # Add new task
    client.tasks[data['taskName']] = data['assignee']
    db.session.commit()
    return jsonify({'message': 'Task added successfully!'}), 201



if __name__ == '__main__':
    app.run(debug=True)
