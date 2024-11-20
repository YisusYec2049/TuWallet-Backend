from flask_restful import Resource, reqparse
from models.db import db, Transaction

class TransactionsAPI(Resource):
    def get(self):
        transactions = Transaction.query.all()
        return [
            {"transaction_id": t.transaction_id, "user_id": t.user_id, "type": t.type, 
             "amount": str(t.amount), "description": t.description, 
             "created_at": str(t.created_at)}
            for t in transactions
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('type', required=True, choices=('deposit', 'withdraw', 'service'))
        parser.add_argument('amount', required=True, type=float)
        parser.add_argument('description', required=False, type=str)
        args = parser.parse_args()

        new_transaction = Transaction(**args)
        db.session.add(new_transaction)
        db.session.commit()
        return {"message": "Transaction added successfully"}, 201
