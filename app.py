from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from config import Config
from models.db import Transaction

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route("/")
def index():
    return "¡Backend funcionando correctamente!"

@app.route("/balance/<int:user_id>", methods=["GET"])
def balance(user_id):
    try:
        total_deposit = db.session.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'deposit'
        ).scalar() or 0

        total_withdraw = db.session.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type.in_(['withdraw', 'service'])
        ).scalar() or 0

        balance = total_deposit - total_withdraw
        return jsonify({"user_id": user_id, "balance": float(balance)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
