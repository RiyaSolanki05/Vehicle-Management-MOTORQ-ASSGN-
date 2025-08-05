# CONVERTED TO MONGODB(LOCAL) FROM PYTHON DICTIONAREIS

from datetime import datetime
from typing import List, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.fleet

class VehicleManagement:
    def __init__(self):
        self.vehicles = db.vehicles
        self.vehicle_statuses = db.vehicle_statuses
        self.alerts = db.alerts

    def create_vehicle(self, data: dict) -> dict:
        data["createdAt"] = datetime.now()
        result = self.vehicles.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    def get_vehicles(self) -> List[dict]:
        return [self._format_id(v) for v in self.vehicles.find()]

    def get_vehicle_by_id(self, vehicle_id: str) -> Optional[dict]:
        v = self.vehicles.find_one({"_id": ObjectId(vehicle_id)})
        return self._format_id(v) if v else None

    def delete_vehicle(self, vehicle_id: str) -> bool:
        result = self.vehicles.delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0

    def create_vehicle_status(self, data: dict) -> dict:
        data["timestamp"] = datetime.now()
        self.vehicle_statuses.insert_one(data)

        existing = self.get_vehicle_alerts(data['vehicleId'])
        unresolved = [a for a in existing if not a.get('resolved')]
        unresolved_types = {a['type'] for a in existing if not a.get('resolved')}

        # Speed Alert Logic
        if data.get('speed', 0) > 100:
            if "SpeedViolation" not in unresolved_types:
                self._create_alert(data['vehicleId'], "SpeedViolation",
                                   f"Speed exceeded: {data['speed']} km/h")
        else:
            for a in unresolved:
                if a['type'] == "SpeedViolation":
                    self.resolve_alert(a['_id'])

        # Fuel Alert Logic
        if data.get('fuelLevel', 100) < 15:
            if "LowFuel" not in unresolved_types:
                self._create_alert(data['vehicleId'], "LowFuel",
                                   f"Low fuel level: {data['fuelLevel']}%")
        else:
            for a in unresolved:
                if a['type'] == "LowFuel":
                    self.resolve_alert(a['_id'])

        return data

    def _create_alert(self, vehicle_id: str, alert_type: str, message: str):
        alert = {
            "vehicleId": vehicle_id,
            "type": alert_type,
            "message": message,
            "timestamp": datetime.utcnow(),
            "resolved": False
        }
        self.alerts.insert_one(alert)
    
    def _create_alert(self, vehicle_id: str, alert_type: str, message: str):
        alert = {
            "vehicleId": vehicle_id,
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now(),
            "resolved": False
        }
        self.alerts.insert_one(alert)

    def resolve_alert(self, alert_id: str) -> bool:
        result = self.alerts.update_one({"_id": ObjectId(alert_id)}, {"$set": {"resolved": True}})
        return result.modified_count > 0
    def get_alerts(self) -> List[dict]:
        return [self._format_id(a) for a in self.alerts.find()]

    def get_vehicle_alerts(self, vehicle_id: str) -> List[dict]:
        return [self._format_id(a) for a in self.alerts.find({"vehicleId": vehicle_id})]

    def get_vehicle_statuses(self) -> List[dict]:
        return [self._format_id(s) for s in self.vehicle_statuses.find()]