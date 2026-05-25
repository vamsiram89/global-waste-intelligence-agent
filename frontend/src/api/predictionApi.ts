import { apiClient } from "./apiClient";
import type { InventoryItemPayload } from "./inventoryApi";

export interface WastePrediction {
  id?: number | null;
  inventory_item_id?: number | null;
  product_name: string;
  category: string;
  risk_score: number;
  risk_level: "low" | "medium" | "high" | "critical" | string;
  predicted_waste_quantity: number;
  estimated_loss: number;
  reason: string;
  days_until_expiry: number;
  created_at?: string | null;
}

export async function predictWasteRisk(payload: InventoryItemPayload) {
  const response = await apiClient.post<WastePrediction>("/predict/waste-risk", payload);
  return response.data;
}

export async function predictAllWasteRisk() {
  const response = await apiClient.get<WastePrediction[]>("/predict/all");
  return response.data;
}
