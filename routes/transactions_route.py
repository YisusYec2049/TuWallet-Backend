from flask import request, jsonify
from models.db import db, Transaction, User
from datetime import datetime

def create_transaction_route():
    data = request.get_json()
    user_id = data.get('user_id')
    type = data.get('type')
    amount = data.get('amount')
    description = data.get('description', "")
    recipient_phone = data.get('recipient_phone')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if type == 'withdraw' and user.balance < amount:
        return jsonify({'message': 'Insufficient funds'}), 400

    if type == 'transfer':
        if not recipient_phone:
            return jsonify({'message': 'Recipient phone is required for transfers'}), 400

        recipient = User.query.filter_by(phone=recipient_phone).first()
        if not recipient:
            return jsonify({'message': 'Recipient not found'}), 404

        if user.balance < amount:
            return jsonify({'message': 'Insufficient funds'}), 400

        user.balance -= amount
        recipient.balance += amount
        db.session.add(user)
        db.session.add(recipient)

        new_transaction = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            description=description or f"Transfer to {recipient.username}"
        )
    else:
        if type == 'deposit':
            user.balance += amount
        elif type == 'withdraw':
            user.balance -= amount

        new_transaction = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            description=description
        )

        db.session.add(user)

    db.session.add(new_transaction)
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
