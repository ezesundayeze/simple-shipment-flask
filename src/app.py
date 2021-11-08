
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import jwt
import os
from dotenv import load_dotenv

# configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Shipment(db.Model):
    """
    Shipment Model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String(80))
    source = db.Column(db.String(120))
    current_location = db.Column(db.String(120))
    status = db.Column(db.String(120))
    item = db.Column(db.String(120))
    description = db.Column(db.String(120))
    tracking_number = db.Column(db.String(120), nullable=True)
    arrival = db.Column(db.String(120))

    def __repr__(self):
        return '<Shipment %r>' % self.item

    def __init__(self, description, source, current_location, status, item, tracking_number, arrival, destination):
        
        self.description =  description
        self.destination =  destination
        self.source = source
        self.current_location = current_location
        self.status = status
        self.item = item
        self.tracking_number = tracking_number
        self.arrival = arrival

class ShipmentSchema(ma.Schema):
    """
    Schema
    """
    class Meta:
        fields = (
        'id', 
        'item',
        'status', 
        'tracking_number',
        'current_location',
        'source',
        'destination',
        'description',
        'arrival'
        )

shipment_schema = ShipmentSchema()
shipments_schema = ShipmentSchema(many=True)

class ShipmentView(Resource):
    """
    Shipment management API
    """
    def get(self, id=None):
        """
        get Shipment
        """
        try:

            if id is None:
                shipment = Shipment.query.filter().all()
                shipment_schema =  ShipmentSchema(many=True)
                print(shipment_schema.dump(shipment))
                return shipment_schema.dump(shipment)
            else:
                shipment = Shipment.query.filter_by(id=id).first()
                shipment_schema = ShipmentSchema()
                return shipment_schema.dump(shipment)
        except Exception as e:
            jsonify({"error":"There was an error please contact the administrator"})

    def post(self):
    
        """
        Add shipment
        """
        data = request.get_json()

        try:
            new_shipment = Shipment(**data)
            db.session.add(new_shipment)
            db.session.commit()
            return shipment_schema.jsonify(new_shipment)
        except Exception as e:
            jsonify({"error":"There was an error please contact the administrator"})        
    
    def put(self, id):
        """
        Update shipment
        """
        try:
            
            data = request.get_json()
            if data.get("headers").get("Authorization"):
            
                del data['headers']
                shipment = Shipment.query.filter_by(id=id)
                shipment.update(data)
                db.session.commit()
                return jsonify(data)
        except Exception as e:
            jsonify({"error":"There was an error please contact the administrator"})# Routes


api.add_resource(ShipmentView, '/shipment/', '/shipment/<int:id>' )
if __name__ == '__main__':
    app.run(debug=True)