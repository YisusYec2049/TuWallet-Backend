from flask_restful import Resource, reqparse
from models.db import db, Transaction, User, Service, ServiceTransaction

class TransactionsAPI(Resource):
    def get(self):
        transactions = Transaction.query.all()
        return [
            {"transaction_id": t.transaction_id, "user_id": t.user_id, 
             "recipient_id": t.recipient_id, "type": t.type, 
             "amount": str(t.amount), "description": t.description, 
             "created_at": str(t.created_at)}
            for t in transactions
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('type', required=True, choices=('deposit', 'withdraw', 'service', 'transfer'))
        parser.add_argument('amount', required=True, type=float)
        parser.add_argument('description', required=False, type=str)
        parser.add_argument('recipient_phone', required=False, type=str)
        parser.add_argument('service_id', required=False, type=int)
        args = parser.parse_args()
        
        user = User.query.get(args['user_id'])
        if not user:
            return {"message": "User not found"}, 404
        
        if args['type'] == 'service' and args['service_id']:
            service = Service.query.get(args['service_id'])
            if not service:
                return {"message": "service not found"}, 404
            
            if user.balance < service.cost:
                return {"message": "service not foind"}, 400
            
            user.balance -= service.cost
            db.session.add(user)

            new_transaction = Transaction(
                user_id = user.user_id,
                type='service',
                amount= service.cost,
                description=f"Package {service.name} purchased"
            )

            db.session.add(new_transaction)

            new_service_transaction = ServiceTransaction(
                transaction_id = new_transaction.transaction_id, 
                service_id = service.service_id
            )
            db.session.add(new_service_transaction)
            db.session.commit()

            return {"message": "Service transaction added successfully"}, 201


        if args['type'] == 'transfer':
            if not args['recipient_phone']:
                return {"message": "Recipient phone is required for transfers"}, 400

            recipient = User.query.filter_by(phone=args['recipient_phone']).first()
            if not recipient:
                return {"message": "Recipient not found"}, 404

            if user.balance < args['amount']:
                return {"message": "Insufficient balance"}, 400

            user.balance -= args['amount']
            recipient.balance += args['amount']
            db.session.add(user)
            db.session.add(recipient)

            new_transaction = Transaction(
                user_id=user.user_id,
                recipient_id=recipient.user_id,
                type='transfer',
                amount=args['amount'],
                description=args.get('description', f"Transfer to {recipient.username}")
            )
        else:
            if args['type'] == 'withdraw' and user.balance < args['amount']:
                return {"message": "Insufficient balance"}, 400

            if args['type'] == 'withdraw':
                user.balance -= args['amount']
            elif args['type'] == 'deposit':
                user.balance += args['amount']

            db.session.add(user)

            new_transaction = Transaction(
                user_id=user.user_id,
                type=args['type'],
                amount=args['amount'],
                description=args.get('description')
            )

        db.session.add(new_transaction)
        db.session.commit()

        return {"message": "Transaction added successfully"}, 201
