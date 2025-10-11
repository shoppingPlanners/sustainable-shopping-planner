"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { tracker } from "@/lib/tracking";

export function ConsentBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(!tracker.getConsent());
  }, []);

  const accept = async () => {
    await tracker.setConsent(true);
    setVisible(false);
    // record initial page view
    await tracker.sendEvent({ event_type: "page_view", page: location.pathname });
  };

  const decline = async () => {
    await tracker.setConsent(false);
    setVisible(false);
  };

  if (!visible) return null;
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 p-4">
      <Card className="mx-auto max-w-3xl p-4 border-border bg-card">
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <p className="text-sm text-muted-foreground text-center sm:text-left">
            We use anonymized analytics to improve sustainable shopping features. Do you consent to usage tracking?
          </p>
          <div className="flex gap-2">
            <Button variant="outline" className="border-border" onClick={decline}>
              Decline
            </Button>
            <Button className="bg-primary text-primary-foreground" onClick={accept}>
              Accept
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}




