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
        vehicle_data['createdAt'] = datetime.now()
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
        status_data['timestamp'] = datetime.now()
        self.vehicle_statuses[self.status_id_counter] = status_data
        self.status_id_counter += 1

        existing_alerts = self.get_vehicle_alerts(status_data['vehicleId'])
        unresolved_types = {alert['type'] for alert in existing_alerts if not alert.get('resolved', False)}

        if status_data.get('speed', 0) > 100 and "SpeedViolation" not in unresolved_types:
            self._create_alert(status_data['vehicleId'], "SpeedViolation",
                f"Speed exceeded: {status_data['speed']} km/h")

        if status_data.get('fuelLevel', 100) < 15 and "LowFuel" not in unresolved_types:
            self._create_alert(status_data['vehicleId'], "LowFuel",
                f"Low fuel level: {status_data['fuelLevel']}%")


        return status_data

    def _create_alert(self, vehicle_id: int, alert_type: str, message: str):
        alert = {
            "id": self.alert_id_counter,
            "vehicleId": vehicle_id,
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now(),
            "resolved": False
            }
        self.alerts[self.alert_id_counter] = alert
        self.alert_id_counter += 1

    def resolve_alert(self, alert_id: int) -> bool:
        alert = self.alerts.get(alert_id)
        if alert:
            alert['resolved'] = True
            return True
        return False

    def get_alerts(self) -> List[dict]:
        return list(self.alerts.values())

    def get_vehicle_alerts(self, vehicle_id: int) -> List[dict]:
        return [alert for alert in self.alerts.values() if alert['vehicleId'] == vehicle_id]
    def get_fleet_analytics(self) -> dict:
        now = datetime.now()
        cutoff = now - datetime.time(hours=24)

        active, inactive = 0, 0
        fuel_levels = []
        total_distance = 0.0
        alert_summary = {}

        # Determine active/inactive and average fuel level
        for status in self.vehicle_statuses.values():
            if status['timestamp'] >= cutoff:
                active += 1
                if 'fuelLevel' in status:
                    fuel_levels.append(status['fuelLevel'])
                if 'speed' in status:
                    total_distance += (status['speed'] or 0) * (1 / 60)  # assuming 1 min update = speed * time
            else:
                inactive += 1

        for alert in self.alerts.values():
            key = alert['type']
            alert_summary[key] = alert_summary.get(key, 0) + 1

        return {
            "activeVehicles": active,
            "inactiveVehicles": inactive,
            "averageFuelLevel": sum(fuel_levels) / len(fuel_levels) if fuel_levels else 0,
            "distanceLast24Hours": round(total_distance, 2),
            "alertSummary": alert_summary
        }



