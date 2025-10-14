"use client";

import { useEffect, useCallback, useRef } from "react";
import { tracker, TrackingEvent } from "@/lib/tracking";

// Enhanced tracking hook for comprehensive event tracking
export function useTracking() {
  const pageViewSent = useRef(false);

  // Track page view on mount
  useEffect(() => {
    if (typeof window !== "undefined" && !pageViewSent.current) {
      const currentPage = window.location.pathname;
      tracker.trackPageView(currentPage);
      pageViewSent.current = true;
    }
  }, []);

  // Track item view
  const trackItemView = useCallback((itemId: string, page?: string, tags?: string[]) => {
    tracker.trackItemView(itemId, page, tags);
  }, []);

  // Track click events
  const trackClick = useCallback((element: string, itemId?: string, metadata?: Record<string, any>) => {
    tracker.sendEvent({
      event_type: "click",
      element,
      item_id: itemId,
      metadata,
    });
  }, []);

  // Track search events
  const trackSearch = useCallback((keywords: string[], filters?: Record<string, any>) => {
    tracker.sendEvent({
      event_type: "search",
      keywords,
      metadata: { filters },
    });
  }, []);

  // Track add to cart events
  const trackAddToCart = useCallback((itemId: string, price?: string, quantity?: number) => {
    tracker.sendEvent({
      event_type: "add_to_cart",
      item_id: itemId,
      metadata: {
        price,
        quantity: quantity || 1,
      },
    });
  }, []);

  // Track filter changes
  const trackFilterChange = useCallback((filterType: string, value: string, page?: string) => {
    tracker.trackFilterSelect(filterType, value);
    tracker.sendEvent({
      event_type: "filter_change",
      metadata: {
        filter_type: filterType,
        filter_value: value,
        page,
      },
    });
  }, []);

  // Track form interactions
  const trackFormInteraction = useCallback((formType: string, action: string, metadata?: Record<string, any>) => {
    tracker.sendEvent({
      event_type: "form_interaction",
      metadata: {
        form_type: formType,
        action,
        ...metadata,
      },
    });
  }, []);

  // Track purchase events
  const trackPurchase = useCallback((itemId: string, price?: string, metadata?: Record<string, any>) => {
    tracker.trackPurchase(itemId, price);
    tracker.sendEvent({
      event_type: "purchase",
      item_id: itemId,
      metadata: {
        price,
        ...metadata,
      },
    });
  }, []);

  // Track scroll depth
  const trackScrollDepth = useCallback((depth: number, page?: string) => {
    tracker.sendEvent({
      event_type: "scroll_depth",
      metadata: {
        depth_percentage: depth,
        page,
      },
    });
  }, []);

  // Track time on page
  const trackTimeOnPage = useCallback((timeInSeconds: number, page?: string) => {
    tracker.sendEvent({
      event_type: "time_on_page",
      metadata: {
        time_seconds: timeInSeconds,
        page,
      },
    });
  }, []);

  return {
    trackItemView,
    trackClick,
    trackSearch,
    trackAddToCart,
    trackFilterChange,
    trackFormInteraction,
    trackPurchase,
    trackScrollDepth,
    trackTimeOnPage,
  };
}

// Hook for tracking item interactions
export function useItemTracking(itemId: string, page?: string) {
  const { trackItemView, trackClick, trackAddToCart } = useTracking();

  const handleItemView = useCallback(() => {
    trackItemView(itemId, page);
  }, [itemId, page, trackItemView]);

  const handleItemClick = useCallback((element: string) => {
    trackClick(element, itemId);
  }, [itemId, trackClick]);

  const handleAddToCart = useCallback((price?: string, quantity?: number) => {
    trackAddToCart(itemId, price, quantity);
  }, [itemId, trackAddToCart]);

  return {
    handleItemView,
    handleItemClick,
    handleAddToCart,
  };
}

// Hook for tracking search interactions
export function useSearchTracking() {
  const { trackSearch, trackFilterChange } = useTracking();

  const handleSearch = useCallback((query: string, filters?: Record<string, any>) => {
    const keywords = query.trim().split(/\s+/).filter(Boolean);
    trackSearch(keywords, filters);
  }, [trackSearch]);

  const handleFilterChange = useCallback((filterType: string, value: string) => {
    trackFilterChange(filterType, value);
  }, [trackFilterChange]);

  return {
    handleSearch,
    handleFilterChange,
  };
}

// Hook for tracking scroll behavior
export function useScrollTracking(page?: string) {
  const { trackScrollDepth } = useTracking();
  const lastTrackedDepth = useRef(0);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercentage = Math.round((scrollTop / scrollHeight) * 100);

      // Track at 25%, 50%, 75%, and 100%
      if (scrollPercentage >= 25 && lastTrackedDepth.current < 25) {
        trackScrollDepth(25, page);
        lastTrackedDepth.current = 25;
      } else if (scrollPercentage >= 50 && lastTrackedDepth.current < 50) {
        trackScrollDepth(50, page);
        lastTrackedDepth.current = 50;
      } else if (scrollPercentage >= 75 && lastTrackedDepth.current < 75) {
        trackScrollDepth(75, page);
        lastTrackedDepth.current = 75;
      } else if (scrollPercentage >= 100 && lastTrackedDepth.current < 100) {
        trackScrollDepth(100, page);
        lastTrackedDepth.current = 100;
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [page, trackScrollDepth]);
}

// Hook for tracking time on page
export function useTimeTracking(page?: string) {
  const { trackTimeOnPage } = useTracking();
  const startTime = useRef<number>(Date.now());

  useEffect(() => {
    const handleBeforeUnload = () => {
      const timeSpent = Math.round((Date.now() - startTime.current) / 1000);
      if (timeSpent > 5) { // Only track if user spent more than 5 seconds
        trackTimeOnPage(timeSpent, page);
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [page, trackTimeOnPage]);
}
