from model import Shipment, db
from schema import ShipmentSchema
from flask import Flask, jsonify, request

def get(id=None):
    """
    get Shipment
    """
    try:
        if id is None:
            shipment = Shipment.query.filter().all()
            shipment_schema =  ShipmentSchema(many=True)
            return shipment_schema.jsonify(shipment)
        else:
            shipment = Shipment.query.filter_by(id=id).first()
            shipment_schema = ShipmentSchema()
            return shipment_schema.jsonify(shipment)
    except Exception as e:
        jsonify({"error":"There was an error please contact the administrator"})
        

def post():
    
    """
    Add shipment
    """
    data = request.get_json()
    try:
        new_shipment = Shipment(**data)
        shipment_schema = ShipmentSchema()
        db.session.add(new_shipment)
        db.session.commit()
        return shipment_schema.jsonify(new_shipment)
    except Exception as e:
        print(e)
        jsonify({"error":"There was an error please contact the administrator"})        


def put(id):
    """
    Update shipment
    """
    try:
            
        data = request.get_json()
        shipment = Shipment.query.filter_by(id=id).first()
        shipment = Shipment.query.filter_by(id=id)
        shipment.update(data)
        db.session.commit()
                
        return jsonify(data)
    except Exception as e:
        jsonify({"error":"There was an error please contact the administrator"})# Routes
        