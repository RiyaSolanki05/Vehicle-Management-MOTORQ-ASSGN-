import { pgTable, text, serial, integer, boolean, timestamp, jsonb, real, varchar } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
// Vehicle schema

export const vehicles = pgTable("vehicles", {
  id: serial("id").primaryKey(),
  fleetid: serial("id").primaryKey().notNull(),
  Manufacturer: text("manufacturer").notNull(),
  vehicleId: text("vehicleId").notNull().unique(),
  Ownner: text("Owner").notNull(),
  registrationstatus: text("registrationstatus").notNull(),
});

export const insertVehicleSchema = createInsertSchema(vehicles).pick({
  Manucturer: true,
  vehicleId: true,
  registrationstatus: true,
  fleetidId: true,
  Ownner: true,
});

// Vehicle Status schema
export const vehicleStatus = pgTable("vehicleStatus", {
  id : serial("id").primaryKey,
  vehicleId: integer("vehicleId").notNull().references(() => vehicles.id),
  timestamp: timestamp("timestamp").defaultNow(),
  latitude: real("latitude").notNull(),
  longitude: real("longitude").notNull(),
  speed: real("speed"),
  fuelLevel: real("fuelLevel"),
  status: text("status").notNull(),
  diagnosticCodes: real("diagnosticCodes") // active, idle, offline
});
export const insertVehicleStatusSchema = createInsertSchema(vehicleStatus).pick({
  vehicleId: true,
  latitude: true,
  longitude: true,
  speed: true,
  fuelLevel: true,
  status: true,
  diagnosticCodes: true,
  timestamp: true
});
export type InsertVehicle = z.infer<typeof insertVehicleSchema>;
export type Vehicle = typeof vehicles.$inferSelect;

export type InsertVehicleStatus = z.infer<typeof insertVehicleStatusSchema>;
export type VehicleStatus = typeof vehicleStatus.$inferSelect;