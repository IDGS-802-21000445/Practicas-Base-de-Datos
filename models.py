from flask_sqlalchemy import SQLAlchemy
import datetime
import json

db=SQLAlchemy()

class Alumnos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())

class Maestros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    amaterno = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    materia = db.Column(db.String(50))

class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    tamaño = db.Column(db.String(20))
    pizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    dia = db.Column(db.String(20))
    mes = db.Column(db.String(20))
    ingredientes = db.relationship('Ingrediente', backref='orden', lazy=True)


class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)
