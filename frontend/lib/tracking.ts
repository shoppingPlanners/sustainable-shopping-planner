"use client";

import { TRACKER_URL } from "./config";

export interface TrackingEvent {
  event_type: string;
  user_id?: string;
  session_id?: string;
  item_id?: string;
  brand_id?: string;
  page?: string;
  keywords?: string[];
  element?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  timestamp?: number;
}

export interface UserProfile {
  user_id: string;
  age?: number;
  gender?: string;
  location?: string;
  preferences?: Record<string, any>;
}

class TrackingService {
  private sessionId: string;
  private userId: string | null = null;
  private consent: boolean = false;
  private eventQueue: TrackingEvent[] = [];
  private isInitialized = false;

  constructor() {
    this.sessionId = this.generateSessionId();
    this.loadUserData();
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private loadUserData(): void {
    if (typeof window === "undefined") return;
    
    this.userId = localStorage.getItem("ssp_user_id");
    this.consent = localStorage.getItem("tracking_consent") === "true";
  }

  public init(): void {
    if (this.isInitialized) return;
    this.isInitialized = true;
    
    // Track session start
    this.sendEvent({
      event_type: "session_start",
      session_id: this.sessionId,
      user_id: this.userId || undefined,
    });

    // Process queued events if consent was given
    if (this.consent) {
      this.processEventQueue();
    }
  }

  public setConsent(consent: boolean): Promise<void> {
    this.consent = consent;
    if (typeof window !== "undefined") {
      localStorage.setItem("tracking_consent", consent.toString());
    }

    if (consent) {
      this.processEventQueue();
      return this.sendEvent({
        event_type: "consent_given",
        session_id: this.sessionId,
        user_id: this.userId || undefined,
      });
    } else {
      return this.sendEvent({
        event_type: "consent_declined",
        session_id: this.sessionId,
        user_id: this.userId || undefined,
      });
    }
  }

  public getConsent(): boolean {
    return this.consent;
  }

  public setUserId(userId: string): void {
    this.userId = userId;
    if (typeof window !== "undefined") {
      localStorage.setItem("ssp_user_id", userId);
    }
  }

  public async sendEvent(event: TrackingEvent): Promise<void> {
    if (!this.consent) {
      this.eventQueue.push(event);
      return;
    }

    try {
      const payload = {
        ...event,
        session_id: this.sessionId,
        user_id: this.userId || event.user_id,
        timestamp: event.timestamp || Date.now() / 1000,
      };

      await fetch(`${TRACKER_URL}/track`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
    } catch (error) {
      console.warn("Failed to send tracking event:", error);
      // Queue the event for retry
      this.eventQueue.push(event);
    }
  }

  public async updateProfile(profile: UserProfile): Promise<void> {
    if (!this.consent) return;

    try {
      await fetch(`${TRACKER_URL}/bio`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profile),
      });
    } catch (error) {
      console.warn("Failed to update user profile:", error);
    }
  }

  private async processEventQueue(): Promise<void> {
    if (this.eventQueue.length === 0) return;

    const events = [...this.eventQueue];
    this.eventQueue = [];

    for (const event of events) {
      await this.sendEvent(event);
    }
  }

  // Utility methods for common tracking scenarios
  public trackPageView(page: string): void {
    this.sendEvent({
      event_type: "page_view",
      page,
    });
  }

  public trackSearch(keywords: string[]): void {
    this.sendEvent({
      event_type: "search",
      keywords,
    });
  }

  public trackItemView(itemId: string, page?: string, tags?: string[]): void {
    this.sendEvent({
      event_type: "view_item",
      item_id: itemId,
      page,
      tags,
    });
  }

  public trackClick(element: string, itemId?: string): void {
    this.sendEvent({
      event_type: "click",
      element,
      item_id: itemId,
    });
  }

  public trackFilterSelect(filterType: string, value: string): void {
    this.sendEvent({
      event_type: "filter_select",
      metadata: {
        filter_type: filterType,
        filter_value: value,
      },
    });
  }

  public trackPurchase(itemId: string, price?: string): void {
    this.sendEvent({
      event_type: "purchase",
      item_id: itemId,
      metadata: {
        price,
      },
    });
  }
}

export const tracker = new TrackingService();





