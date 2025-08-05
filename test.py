from storage import VehicleManagement
from datetime import datetime, timedelta

vm = VehicleManagement()

# Create 2 vehicles
v1 = vm.create_vehicle({"manufacturer": "Tesla", "vehicleId": "T100", "registrationstatus": "active", "fleetid": 1, "owner": "Elon"})
v2 = vm.create_vehicle({"manufacturer": "Ford", "vehicleId": "F200", "registrationstatus": "active", "fleetid": 1, "owner": "Henry"})


vm.create_vehicle_status({
    "vehicleId": v1["id"],"latitude": 12.34,
    "longitude": 56.78,
    "speed": 110,
    "fuelLevel": 50,
    "status": "active"
})
vm.create_vehicle_status({
    "vehicleId": v1["id"],"latitude": 12.34,
    "longitude": 56.78,
    "speed": 120,
    "fuelLevel": 50,
    "status": "active"
})
vm.create_vehicle_status({
    "vehicleId": v1["id"],"latitude": 12.34,
    "longitude": 56.78,
    "speed": 80,
    "fuelLevel": 50,
    "status": "active"
})
vm.create_vehicle_status({
    "vehicleId": v1["id"],"latitude": 12.34,
    "longitude": 56.78,
    "speed": 101,
    "fuelLevel": 50,
    "status": "active"
})
print(vm.get_fleet_analytics())


