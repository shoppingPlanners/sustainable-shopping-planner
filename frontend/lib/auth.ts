"use client";

import { BACKEND_URL } from "./config";

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type RegisterResponse = {
  message: string;
  user: {
    id: string;
    email: string;
    name: string;
    role: string;
  };
};

export async function login(email: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${BACKEND_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Login failed");
  }
  
  const data = (await res.json()) as LoginResponse;
  
  // Store token in localStorage
  localStorage.setItem("ssp_token", data.access_token);
  
  // Extract user_id from JWT token (basic implementation)
  try {
    const payload = JSON.parse(atob(data.access_token.split('.')[1]));
    localStorage.setItem("ssp_user_id", payload.sub); // sub contains the email
    localStorage.setItem("ssp_user_email", payload.sub);
  } catch (e) {
    console.warn("Could not extract user info from token");
  }
  
  return data;
}

export async function registerAccount(args: { 
  email: string; 
  password: string; 
  name: string;
}): Promise<RegisterResponse> {
  const res = await fetch(`${BACKEND_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Registration failed");
  }
  
  const data = (await res.json()) as RegisterResponse;
  
  // Store user info in localStorage
  localStorage.setItem("ssp_user_id", data.user.id);
  localStorage.setItem("ssp_user_email", data.user.email);
  localStorage.setItem("ssp_user_name", data.user.name);
  
  return data;
}

export function getAuthToken(): string | null {
  return typeof window === "undefined" ? null : localStorage.getItem("ssp_token");
}

export function getUserInfo(): { id: string; email: string; name: string } | null {
  if (typeof window === "undefined") return null;
  
  const id = localStorage.getItem("ssp_user_id");
  const email = localStorage.getItem("ssp_user_email");
  const name = localStorage.getItem("ssp_user_name");
  
  if (!id || !email) return null;
  
  return { id, email, name: name || "" };
}

export function logout(): void {
  if (typeof window === "undefined") return;
  
  localStorage.removeItem("ssp_token");
  localStorage.removeItem("ssp_user_id");
  localStorage.removeItem("ssp_user_email");
  localStorage.removeItem("ssp_user_name");
}



