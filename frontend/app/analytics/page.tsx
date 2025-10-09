"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BACKEND_URL } from "@/lib/config";

type Metrics = {
  average_session_ms: number;
  eco_product_view_rate: number;
  top_keywords: { keyword: string; count: number }[];
  top_tags: { tag: string; count: number }[];
};

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/analytics/metrics`).then(r => r.json()).then(setMetrics).catch(() => {});
  }, []);

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-foreground">Average Session Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">
              {metrics ? `${Math.round(metrics.average_session_ms / 1000)}s` : "--"}
            </div>
          </CardContent>
        </Card>

        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-foreground">Eco Product View Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">
              {metrics ? `${Math.round(metrics.eco_product_view_rate * 100)}%` : "--"}
            </div>
          </CardContent>
        </Card>

        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-foreground">Top Keywords</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="text-sm text-muted-foreground space-y-1">
              {metrics?.top_keywords?.map(k => (
                <li key={k.keyword} className="flex justify-between"><span className="text-foreground">{k.keyword}</span><span>{k.count}</span></li>
              )) || null}
            </ul>
          </CardContent>
        </Card>

        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-foreground">Top Sustainability Tags</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="text-sm text-muted-foreground space-y-1">
              {metrics?.top_tags?.map(t => (
                <li key={t.tag} className="flex justify-between"><span className="text-foreground">{t.tag}</span><span>{t.count}</span></li>
              )) || null}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


