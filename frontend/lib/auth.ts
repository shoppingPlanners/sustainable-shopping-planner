"use client";

import { BACKEND_URL } from "./config";

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user_id: string;
};

export async function login(email: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${BACKEND_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Login failed");
  const data = (await res.json()) as LoginResponse;
  localStorage.setItem("ssp_token", data.access_token);
  localStorage.setItem("ssp_user_id", data.user_id);
  return data;
}

export type RegisterResponse = LoginResponse;

export async function registerAccount(args: { email: string; password: string; name?: string | null; age?: number | null; gender?: string | null; }): Promise<RegisterResponse> {
  const res = await fetch(`${BACKEND_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  if (!res.ok) throw new Error("Register failed");
  const data = (await res.json()) as RegisterResponse;
  localStorage.setItem("ssp_token", data.access_token);
  localStorage.setItem("ssp_user_id", data.user_id);
  return data;
}

export function getAuthToken(): string | null {
  return typeof window === "undefined" ? null : localStorage.getItem("ssp_token");
}


