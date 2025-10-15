export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
export const USER_BEHAVIOR_TRACKER_URL = process.env.NEXT_PUBLIC_USER_BEHAVIOR_TRACKER_URL || "http://localhost:5003";
export const TRACKER_URL = USER_BEHAVIOR_TRACKER_URL; // Alias for tracking service
export const SUGGESTION_AGENT_URL = process.env.NEXT_PUBLIC_SUGGESTION_AGENT_URL || "http://localhost:5004";