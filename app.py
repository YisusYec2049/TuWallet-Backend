from flask import Flask, request, jsonify
from models.db import db
from routes.transactions_route import create_transaction_route, get_transactions_route
from routes.user_route import (
    login_route,
    register_route,
    get_balance_route,
    update_balance_route
)
from config import Config
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def index():
    return "¡Backend funcionando correctamente!"

@app.route("/balance/<int:user_id>", methods=["GET"])
def get_balance(user_id):
    return get_balance_route(user_id)

@app.route("/update_balance/<int:user_id>", methods=["POST"])
def update_balance(user_id):
    return update_balance_route(user_id)

@app.route("/register", methods=["POST"])
def register():
    return register_route()

@app.route("/login", methods=["POST"])
def login():
    return login_route()

@app.route("/create_transaction_route", methods =["POST"])
def create_transaction():
    return create_transaction_route()

@app.route('/users/<int:user_id>/transactions', methods=['GET'])
def get_transactions(user_id):
    print(f"Request for user_id: {user_id}")
    print(f"Full URL: {request.url}")
    return get_transactions_route(user_id)

if __name__ == "__main__":
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1")).fetchone()
                print(f"Resultado de la prueba de conexión: {result}")
        print("¡Conexión exitosa a la base de datos!")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
    
    app.run(debug=True)
