import { apiClient } from "./apiClient";

export interface InventoryItemPayload {
  product_name: string;
  category: string;
  quantity: number;
  unit: string;
  expiry_date: string;
  purchase_date: string;
  avg_daily_sales: number;
  cost_per_unit: number;
  storage_condition: string;
  demand_level: string;
  weather_factor: string;
  event_factor: string;
}

export interface InventoryItem extends InventoryItemPayload {
  id: number;
}

export async function getInventory() {
  const response = await apiClient.get<InventoryItem[]>("/inventory");
  return response.data;
}

export async function addInventoryItem(payload: InventoryItemPayload) {
  const response = await apiClient.post<InventoryItem>("/inventory/add", payload);
  return response.data;
}
