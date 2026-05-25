import { apiClient } from "./apiClient";

export interface AnalyticsSummary {
  total_products_monitored: number;
  high_risk_products: number;
  estimated_waste_value: number;
  estimated_food_saved: number;
  suggested_donation_quantity: number;
  plastic_waste_avoided: number;
  critical_alerts: string[];
}

export async function getAnalyticsSummary() {
  const response = await apiClient.get<AnalyticsSummary>("/analytics/summary");
  return response.data;
}
