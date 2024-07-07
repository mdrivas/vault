# app/email/controllers.py
from flask import Blueprint, jsonify
from flask_mail import Mail, Message
from app.clients.models import Client, db

email_bp = Blueprint('email', __name__)
mail = Mail()

def generate_email_content(client, content):
    return f"""
    Hello {client.first_name} {client.last_name},

    Here is your personalized email:

    {content}

    Regards, 
    FSW Team
    """

def create_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
    return "Email created successfully"

@email_bp.route('/send_email', methods=['POST'])
def send_email():
    # Fetch client
    client = Client.query.filter_by(id=2).first()
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    print("Sending to client: ", client)

    # Fetch content
    content = "TEST CONTENT"  # Placeholder
    
    # Generate email 
    email_content = generate_email_content(client, content)

    # Send email
    create_email(client.email, "FSW Email", email_content)
    print("email sent for: ", client)
    return jsonify({'message': 'Email sent successfully'}), 200
