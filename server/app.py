#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.get_or_404(id)
        data = request.get_json()
        if 'name' in data:
            plant.name = data['name']
        if 'image' in data:
            plant.image = data['image']
        if 'price' in data:
            plant.price = data['price']
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
