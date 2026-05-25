import axios, { AxiosError } from "axios";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface ApiError {
  message: string;
  status?: number;
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 9000,
  headers: {
    "Content-Type": "application/json",
  },
});

export function getFriendlyApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string }>;
    if (axiosError.response) {
      return {
        message: axiosError.response.data?.detail ?? "The server returned an unexpected response.",
        status: axiosError.response.status,
      };
    }
    if (axiosError.code === "ECONNABORTED") {
      return { message: "The backend took too long to respond. Please try again." };
    }
    return { message: "Backend is offline or unreachable. Start FastAPI on port 8000 and refresh." };
  }
  return { message: "Something went wrong. Please try again." };
}

export async function getHealth() {
  const response = await apiClient.get<{ status: string; service: string }>("/health");
  return response.data;
}
