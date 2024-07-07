# app/client/controllers.py
from flask import Blueprint, request, jsonify
from .models import Client, db
import logging

client_bp = Blueprint('client', __name__)

@client_bp.route('/add_client', methods=['POST'])
def add_client():
    data = request.json
    logging.info(f"Received data: {data}")
    new_client = Client(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Client added successfully!'}), 201

@client_bp.route('/api/data', methods=['GET'])
def get_data():
    clients = Client.query.all()
    clients_list = [{
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email
    } for client in clients]
    return jsonify(clients_list)

@client_bp.route('/api/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    
    client_data = {
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email
    }
    return jsonify(client_data)
