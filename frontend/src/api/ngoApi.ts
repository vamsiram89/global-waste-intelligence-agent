import { apiClient } from "./apiClient";

export interface NgoPartner {
  id: number;
  name: string;
  location: string;
  accepted_categories: string;
  capacity: number;
  contact: string;
}

export interface RedistributionRequest {
  inventory_item_id: number;
  quantity: number;
}

export interface RedistributionResponse {
  request_id?: number | null;
  inventory_item_id: number;
  product_name: string;
  ngo_id?: number | null;
  ngo_name?: string | null;
  quantity: number;
  status: string;
  message: string;
}

export async function getNgos() {
  const response = await apiClient.get<NgoPartner[]>("/ngos");
  return response.data;
}

export async function redistributeFood(payload: RedistributionRequest) {
  const response = await apiClient.post<RedistributionResponse>("/redistribute", payload);
  return response.data;
}
