import { apiClient } from "./apiClient";

export interface RecommendationRequest {
  inventory_item_id: number;
}

export interface Recommendation {
  id?: number | null;
  inventory_item_id: number;
  product_name?: string | null;
  action_type: string;
  action_message: string;
  urgency: string;
  created_at?: string | null;
}

export async function recommendAction(payload: RecommendationRequest) {
  const response = await apiClient.post<Recommendation>("/actions/recommend", payload);
  return response.data;
}
