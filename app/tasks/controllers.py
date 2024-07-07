# app/tasks/controllers.py
from flask import Blueprint, request, jsonify
from .models import Tasks, StatusEnum, db
from app.clients.models import Client

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/client/<int:client_id>/tasks', methods=['POST'])
def add_task(client_id):
    data = request.json
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404

    new_task = Tasks(
        assignee=data['assignee'],
        task=data['taskName'],
        status=StatusEnum.not_assigned,
        client_id=client_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully!'}), 201

@tasks_bp.route('/api/client/<int:client_id>/tasks', methods=['GET'])
def get_tasks(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    
    tasks = Tasks.query.filter_by(client_id=client_id).all()
    tasks_list = [{'id': task.id, 'assignee': task.assignee, 'task': task.task, 'status': task.status.name} for task in tasks]
    return jsonify(tasks_list)
