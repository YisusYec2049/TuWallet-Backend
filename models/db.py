from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    type = db.Column(db.Enum('deposit', 'withdraw', 'service', name='transaction_type'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Service(db.Model):
    __tablename__ = 'Services'
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Log(db.Model):
    __tablename__ = 'Logs'
    log_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50), nullable=False)
    operation = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE', name='log_operation'), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class ServiceTransaction(db.Model):
    __tablename__ = 'ServiceTransactions'
    service_transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('Transactions.transaction_id'), nullable=False) 
    service_id = db.Column(db.Integer, db.ForeignKey('Services.service_id'), nullable=False)
