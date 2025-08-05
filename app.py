from flask import Flask, request, jsonify
from storage import VehicleManagement

storage = VehicleManagement() 
app = Flask(__name__)

@app.route('/api/vehicles', methods=['GET'])
def list_vehicles():
    try:
        return jsonify(storage.getVehicles())
    except Exception as e:
        return jsonify({"message": "Failed to get vehicles"}), 500

@app.route('/api/vehicles/<int:id>', methods=['GET'])
def get_vehicle_by_id(id):
    try:
        vehicle = storage.getVehicleByVehicleId(id)
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404
        return jsonify(vehicle)
    except:
        return jsonify({"message": "Failed to get vehicle"}), 500

@app.route('/api/vehicles', methods=['POST'])
def create_new_vehicle():
    data = request.json
    validation = storage.insertVehicleSchema.safe_parse(data)
    if not validation.success:
        return jsonify({"message": "Invalid vehicle data", "errors": validation.error.errors}), 400

    vehicle = storage.createVehicle(validation.data)
    if data.get("latitude") and data.get("longitude"):
        storage.create_vehicle_status({
            "vehicleId": vehicle['id'],
            "latitude": data['latitude'],
            "longitude": data['longitude'],
            "status": "idle"
        })
    return jsonify(vehicle), 201
@app.route('/api/vehicles/<int:id>', methods=['DELETE'])
def delete_existing_vehicle(id):
    storage.deleteVehicle(id)
    return jsonify({"message": "Vehicle deleted"})
@app.route('/api/vehicles', methods=['GET'])
def list_alerts():
    try:
        return jsonify(storage.get_alerts())
    except Exception as e:
        return jsonify({"message": "Failed to get alerts"}), 500

@app.route('/api/vehicles', method=['GET'])
def get_analtics():
    try:
        return jsonify(storage.get_alerts())
    except Exception as e:
        return jsonify({"message": "Failed to get Analytics Report"}), 500




