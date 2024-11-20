from flask_restful import Resource, reqparse
from models.db import db, User
from werkzeug.security import generate_password_hash, check_password_hash

class UsersAPI(Resource):
    def get(self):
        users = User.query.all()
        return [
            {"user_id": u.user_id, "username": u.username, "email": u.email, 
             "created_at": str(u.created_at)}
            for u in users
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        password_hash = generate_password_hash(args['password'])
        new_user = User(username=args['username'], email=args['email'], password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

class UserAuthAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()
        if user and check_password_hash(user.password_hash, args['password']):
            return {"message": "Authentication successful"}, 200
        else:
            return {"message": "Invalid email or password"}, 401
