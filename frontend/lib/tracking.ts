"use client";

import { BACKEND_URL } from "./config";

type EventPayload = {
  event_type: string;
  session_id: string;
  anonymous_id: string;
  user_id?: string | null;
  page?: string | null;
  element?: string | null;
  item_id?: string | null;
  brand_id?: string | null;
  tags?: string[] | null;
  keywords?: string[] | null;
  value?: number | null;
  metadata?: Record<string, unknown> | null;
};

const STORAGE_KEYS = {
  anon: "ssp_anonymous_id",
  consent: "ssp_consent",
  session: "ssp_session_id",
};

function generateId(prefix: string) {
  return `${prefix}_${crypto.randomUUID()}`;
}

function getAnonymousId(): string {
  let id = localStorage.getItem(STORAGE_KEYS.anon);
  if (!id) {
    id = generateId("anon");
    localStorage.setItem(STORAGE_KEYS.anon, id);
  }
  return id;
}

function getConsent(): boolean {
  return localStorage.getItem(STORAGE_KEYS.consent) === "granted";
}

async function setConsent(granted: boolean) {
  localStorage.setItem(STORAGE_KEYS.consent, granted ? "granted" : "denied");
  const anonymous_id = getAnonymousId();
  await fetch(`${BACKEND_URL}/consent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ anonymous_id, granted }),
    keepalive: true,
  });
}

async function startSession() {
  const anonymous_id = getAnonymousId();
  const res = await fetch(`${BACKEND_URL}/session/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      anonymous_id,
      user_agent: navigator.userAgent,
      referrer: document.referrer || null,
      page: location.pathname,
    }),
  });
  const data = await res.json();
  localStorage.setItem(STORAGE_KEYS.session, data.session_id);
}

function getSessionId(): string | null {
  return localStorage.getItem(STORAGE_KEYS.session);
}

async function endSession(reason: "navigation" | "timeout" | "manual" | "unload") {
  const session_id = getSessionId();
  if (!session_id) return;
  await fetch(`${BACKEND_URL}/session/end`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, end_reason: reason }),
    keepalive: true,
  });
  localStorage.removeItem(STORAGE_KEYS.session);
}

async function sendEvent(payload: Omit<EventPayload, "anonymous_id" | "session_id">) {
  if (!getConsent()) return;
  let session_id = getSessionId();
  if (!session_id) await startSession();
  session_id = getSessionId();
  if (!session_id) return;
  const body: EventPayload = {
    anonymous_id: getAnonymousId(),
    session_id,
    ...payload,
  } as EventPayload;
  await fetch(`${BACKEND_URL}/event`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    keepalive: payload.event_type === "page_view" || payload.event_type === "time_spent",
  });
}

function init() {
  // start session lazily on first event; send a page view immediately if consent already granted
  if (getConsent()) {
    void sendEvent({ event_type: "page_view", page: location.pathname });
  }
  // end session on unload
  addEventListener("beforeunload", () => {
    void endSession("unload");
  });
}

export const tracker = {
  init,
  getConsent,
  setConsent,
  startSession,
  endSession,
  sendEvent,
};


