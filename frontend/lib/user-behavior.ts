import { USER_BEHAVIOR_TRACKER_URL } from './config';

class UserBehaviorTracker {
  private userId: string | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this.userId = localStorage.getItem('ssp_user_id');
      window.addEventListener('storage', this.handleStorageChange);
    }
  }

  private handleStorageChange = (event: StorageEvent) => {
    if (event.key === 'ssp_user_id') {
      this.userId = event.newValue;
    }
  };

  public setUserId(id: string) {
    this.userId = id;
    localStorage.setItem('ssp_user_id', id);
  }

  public async trackEvent(
    userId: string,
    eventType: string,
    productId?: string,
    metadata?: Record<string, any>
  ) {
    if (!userId) {
      console.warn("Cannot track event: User ID is not set.");
      return;
    }

    const eventData = {
      user_id: userId,
      event_type: eventType,
      product_id: productId,
      timestamp: Date.now() / 1000, // Unix timestamp in seconds
      metadata: {
        page: window.location.pathname,
        ...metadata,
      },
    };

    try {
      const response = await fetch(`${USER_BEHAVIOR_TRACKER_URL}/track`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
      });

      if (!response.ok) {
        console.error(`Failed to track event: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error sending tracking event:", error);
    }
  }

  public trackPageView(page: string) {
    if (this.userId) {
      this.trackEvent(this.userId, 'page_view', undefined, { page });
    }
  }

  public async trackPreferences(preferences: Record<string, any>) {
    if (this.userId) {
      await this.trackEvent(this.userId, 'preferences_submitted', undefined, { preferences });
    }
  }
}

export const userBehaviorTracker = new UserBehaviorTracker();
