export interface StandardResponse<T> {
  status: "success" | "error";
  data?: T;
  message?: string;
}

export interface ChatResponse {
  response: string;
  action_taken: string;
}

export interface CrowdData {
  location_id: string;
  density_percentage: number;
  status_label: "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
}

export interface HeatmapResponse {
  locations: Record<string, CrowdData>;
  timestamp: string;
}

export interface QueueItem {
  name: string;
  wait_time_minutes: number;
  people_waiting?: number;
  service_rate?: number;
}

export interface QueueResponse {
  queues: QueueItem[];
}

export interface RouteResponse {
  start: string;
  destination: string;
  path: string[];
  estimated_time_minutes: number;
  route_description: string;
}

export interface RecommendationResponse {
  action: string;
  reason: string;
  estimated_time: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "ai";
  content: string;
  timestamp: number;
}
