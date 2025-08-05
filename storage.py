from typing import List, Dict, Optional
from datetime import datetime

class VehicleManagement:
    def __init__(self):
        self.vehicles: Dict[int, dict] = {}
        self.vehicle_statuses: Dict[int, dict] = {}
        self.alerts: Dict[int, dict] = {}
        self.vehicle_id_counter = 1
        self.status_id_counter = 1
        self.alert_id_counter = 1

    def get_vehicles(self) -> List[dict]:
        return list(self.vehicles.values())

    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[dict]:
        return self.vehicles.get(vehicle_id)

    def create_vehicle(self, vehicle_data: dict) -> dict:
        vehicle_data['id'] = self.vehicle_id_counter
        vehicle_data['createdAt'] = datetime.utcnow()
        self.vehicles[self.vehicle_id_counter] = vehicle_data
        self.vehicle_id_counter += 1
        return vehicle_data

    def delete_vehicle(self, vehicle_id: int) -> bool:
        return self.vehicles.pop(vehicle_id, None) is not None

    def get_vehicle_statuses(self) -> List[dict]:
        return list(self.vehicle_statuses.values())

    def get_vehicle_status(self, vehicle_id: int) -> Optional[dict]:
        for status in self.vehicle_statuses.values():
            if status['vehicleId'] == vehicle_id:
                return status
        return None

    def create_vehicle_status(self, status_data: dict) -> dict:
        status_data['id'] = self.status_id_counter
        status_data['timestamp'] = datetime.utcnow()
        self.vehicle_statuses[self.status_id_counter] = status_data
        self.status_id_counter += 1

        # Alert Generation Logic
        if status_data.get('speed', 0) > 100:
            self._create_alert(status_data['vehicleId'], "SpeedViolation",
                f"Speed exceeded: {status_data['speed']} km/h")

        if status_data.get('fuelLevel', 100) < 15:
            self._create_alert(status_data['vehicleId'], "LowFuel",
                f"Low fuel level: {status_data['fuelLevel']}%")

        return status_data

    def _create_alert(self, vehicle_id: int, alert_type: str, message: str):
        alert = {
            "id": self.alert_id_counter,
            "vehicleId": vehicle_id,
            "type": alert_type,
            "message": message,
            "timestamp": datetime.utcnow()
        }
        self.alerts[self.alert_id_counter] = alert
        self.alert_id_counter += 1

    def get_alerts(self) -> List[dict]:
        return list(self.alerts.values())

    def get_vehicle_alerts(self, vehicle_id: int) -> List[dict]:
        return [alert for alert in self.alerts.values() if alert['vehicleId'] == vehicle_id]
