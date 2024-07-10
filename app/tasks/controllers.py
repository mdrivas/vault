from flask import Blueprint, request, jsonify
from .models import Tasks, StatusEnum
from app.clients.models import Client
from app.db import db

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

@tasks_bp.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.json
    task = Tasks.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    try:
        new_status = StatusEnum[data['status']]
    except KeyError:
        return jsonify({'error': 'Invalid status'}), 400

    task.status = new_status
    db.session.commit()
    return jsonify({'message': 'Status updated successfully!'})

@tasks_bp.route('/api/tasks/pending', methods=['GET'])
def get_pending_tasks_count():
    count = Tasks.query.filter(Tasks.status != 'completed').count()
    return jsonify({'count': count})

@tasks_bp.route('/api/recent-activities', methods=['GET'])
def get_recent_activities():
    activities = [
        "Client Theo Drivas added",
        "Task 'Prepare Financial Report' completed",
        "Email sent to client Alex Drivas"
    ]
    return jsonify({'activities': activities})