import { 
  Vehicle, InsertVehicle, 
  VehicleStatus, InsertVehicleStatus,
  alerts,
  Alert,
} from "../schema/data";


export interface IStorage {
  createVehicle(vehicle: InsertVehicle): Promise<Vehicle>;
  getVehicles(): Promise<Vehicle[]>;
  getVehicleByVehicleId(vehicleId: string): Promise<Vehicle | undefined>;
  deleteVehicle(id: number): Promise<boolean>;

  getVehicleStatuses(): Promise<VehicleStatus[]>;
  getVehicleStatus(vehicleId: number): Promise<VehicleStatus | undefined>;
  createVehicleStatus(status: InsertVehicleStatus): Promise<VehicleStatus>;
}

export class VehicleManagement implements IStorage{
  private vehicles: Map<number, Vehicle>;
  private vehicleStatuses: Map<number, VehicleStatus>;
  private vehicleCurrentId: number;
  private vehicleStatusCurrentId: number;
  private alerts: Map<number, any> = new Map(); // new
  private alertCurrentId = 1;

  constructor(){
    this.vehicles = new Map();
    this.vehicleStatuses = new Map();
    this.vehicleCurrentId = 1;
    this.alerts = new Map();
    this.alertCurrentId = 1;
  }
  
  async getVehicles(): Promise<Vehicle[]> {
    return Array.from(this.vehicles.values());
  }

  async getVehicleByVehicleId(vehicleId: string): Promise<Vehicle | undefined> {
    return Array.from(this.vehicles.values()).find((vehicle)=> vehicle.vehicalID==vehicleId)
  }
  async createVehicle(insertVehicle: InsertVehicle): Promise<Vehicle> {
    const id = this.vehicleCurrentId++;
    const createdAt = new Date();
    const vehicle: Vehicle = { insertVehicle, id, createdAt };
    this.vehicles.set(id, vehicle);
    return vehicle;
  }
   async deleteVehicle(id: number): Promise<boolean> {
    return this.vehicles.delete(id);
  }
   async getVehicleStatuses(): Promise<VehicleStatus[]> {
    return Array.from(this.vehicleStatuses.values());
  }
  async getVehicleStatus(vehicleId: number): Promise<VehicleStatus | undefined> {
    return Array.from(this.vehicleStatuses.values()).find((status)=>status.vehicalID===vehicleId)
  }
  async createVehicleStatus(insertStatus: InsertVehicleStatus): Promise<VehicleStatus> {
    const id=this.vehicleStatusCurrentId++;
    const timestamp=new Date();
    const status:VehicleStatus={insertStatus,id,timestamp};
    this.vehicleStatuses.set(id,status);

  if (insertStatus.speed> 100) {
    alerts.push({
      vehicleId: insertStatus.vehicleId,
      type: "SpeedViolation",
      message: `Speed exceeded: ${insertStatus.speed} km/h`
    });
  }

  if (insertStatus.fuelLevel < 15) {
    alerts.push({
      vehicleId: insertStatus.vehicleId,
      type: "LowFuel",
      message: `Low fuel level: ${insertStatus.fuelLevel}%`
    });
  }
  return status;

}
  async getAlerts(): Promise<Alert> {
    return Array.from(this.alerts.values());
  }
  async getVehicleAlerts(vehicleId: number): Promise<Alert[]> {
    return Array.from(this.alerts.values()).filter(
      (alert) => alert.vehicleId === vehicleId,
    );
  }
}