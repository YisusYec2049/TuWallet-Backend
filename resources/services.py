from flask_restful import Resource, reqparse
from models.db import db, Service

class ServicesAPI(Resource):
    def get(self):
        services = Service.query.all()
        return [
            {"service_id": s.service_id, "name": s.name, "description": s.description, 
             "cost": str(s.cost), "created_at": str(s.created_at)}
            for s in services
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('description', required=False, type=str)
        parser.add_argument('cost', required=True, type=float)
        args = parser.parse_args()

        new_service = Service(**args)
        db.session.add(new_service)
        db.session.commit()
        return {"message": "Service added successfully"}, 201
