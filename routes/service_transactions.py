from flask_restful import Resource, reqparse
from models.db import db, ServiceTransaction

class ServiceTransactionsAPI(Resource):
    def get(self):
        service_transactions = ServiceTransaction.query.all()
        return [
            {"service_transaction_id": st.service_transaction_id, 
             "transaction_id": st.transaction_id, "service_id": st.service_id}
            for st in service_transactions
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('transaction_id', required=True, type=int)
        parser.add_argument('service_id', required=True, type=int)
        args = parser.parse_args()

        new_service_transaction = ServiceTransaction(**args)
        db.session.add(new_service_transaction)
        db.session.commit()
        return {"message": "Service Transaction added successfully"}, 201
