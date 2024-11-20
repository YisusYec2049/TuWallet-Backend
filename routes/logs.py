from flask_restful import Resource, reqparse
from models.db import db, Log

class LogsAPI(Resource):
    def get(self):
        logs = Log.query.all()
        return [
            {"log_id": l.log_id, "table_name": l.table_name, "operation": l.operation, 
             "details": l.details, "timestamp": str(l.timestamp)}
            for l in logs
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('table_name', required=True, type=str)
        parser.add_argument('operation', required=True, choices=('INSERT', 'UPDATE', 'DELETE'))
        parser.add_argument('details', required=True, type=str)
        args = parser.parse_args()

        new_log = Log(**args)
        db.session.add(new_log)
        db.session.commit()
        return {"message": "Log added successfully"}, 201
