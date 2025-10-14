"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, Cookie, Eye, BarChart3 } from "lucide-react";
import { tracker } from "@/lib/tracking";

export function ConsentBanner() {
  const [showBanner, setShowBanner] = useState(false);
  const [consentGiven, setConsentGiven] = useState(false);

  useEffect(() => {
    // Check if consent has been given
    const hasConsent = tracker.getConsent();
    setConsentGiven(hasConsent);
    
    // Show banner if no consent decision has been made
    if (!hasConsent && typeof window !== "undefined") {
      const consentDecision = localStorage.getItem("tracking_consent");
      if (!consentDecision) {
        setShowBanner(true);
      }
    }
  }, []);

  const handleAccept = async () => {
    await tracker.setConsent(true);
    setConsentGiven(true);
    setShowBanner(false);
  };

  const handleDecline = async () => {
    await tracker.setConsent(false);
    setConsentGiven(false);
    setShowBanner(false);
  };

  const handleManagePreferences = () => {
    // Open a modal or navigate to preferences page
    console.log("Opening privacy preferences...");
  };

  if (!showBanner) {
    return null;
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 p-4 bg-background/95 backdrop-blur-sm border-t border-border">
      <div className="max-w-4xl mx-auto">
        <Card className="border-border shadow-lg">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-2 mb-2">
              <Shield className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg">Privacy & Analytics</CardTitle>
            </div>
            <CardDescription>
              We use analytics to improve your shopping experience and provide personalized recommendations.
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center gap-2 text-sm">
                <Eye className="h-4 w-4 text-muted-foreground" />
                <span>Page views & navigation</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <BarChart3 className="h-4 w-4 text-muted-foreground" />
                <span>Product interactions</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Cookie className="h-4 w-4 text-muted-foreground" />
                <span>Preference tracking</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <Button onClick={handleAccept} className="flex-1">
                Accept All
              </Button>
              <Button onClick={handleDecline} variant="outline" className="flex-1">
                Decline
              </Button>
              <Button onClick={handleManagePreferences} variant="ghost" size="sm">
                Manage Preferences
              </Button>
            </div>

            <div className="text-xs text-muted-foreground">
              <p>
                By accepting, you agree to our use of cookies and analytics. 
                You can change your preferences at any time in your account settings.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}