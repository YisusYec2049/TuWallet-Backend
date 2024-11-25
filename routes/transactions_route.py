from flask import request, jsonify
from models.db import db, Transaction, User
from sqlalchemy import func

def create_transaction_route():
    data = request.get_json()
    user_id = data.get('user_id')
    type = data.get('type')
    amount = data.get('amount')
    description = data.get('description')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if type == 'withdraw' and user.balance < amount:
        return jsonify({'message': 'Insufficient funds'}), 400

    new_transaction = Transaction(
        user_id=user_id,
        type=type,
        amount=amount,
        description=description
    )
    db.session.add(new_transaction)

    if type == 'deposit':
        user.balance += amount
    elif type == 'withdraw':
        user.balance -= amount

    db.session.commit()
    return jsonify({'message': 'Transaction created successfully'}), 201

def get_transactions_route(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    if not transactions:
        return jsonify({'message': 'No transactions found'}), 404

    transaction_list = [{
        'transaction_id': t.transaction_id,
        'type': t.type,
        'amount': float(t.amount),
        'description': t.description,
        'created_at': t.created_at
    } for t in transactions]

    return jsonify({'transactions': transaction_list}), 200
