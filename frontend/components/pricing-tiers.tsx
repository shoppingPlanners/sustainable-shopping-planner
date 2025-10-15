"use client"

import { Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

const tiers = [
  {
    name: "Free",
    price: "$0",
    description: "Perfect for getting started with sustainable shopping",
    features: [
      "Browse 300+ sustainable products",
      "Basic sustainability scores",
      "Product recommendations",
      "Save up to 10 favorites",
      "Basic analytics dashboard",
    ],
    cta: "Get Started Free",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "$9.99",
    period: "/month",
    description: "For conscious shoppers who want more",
    features: [
      "Everything in Free, plus:",
      "Unlimited favorites",
      "Advanced sustainability insights",
      "Price drop alerts",
      "Carbon footprint tracking",
      "Priority customer support",
      "Early access to new brands",
    ],
    cta: "Start Pro Trial",
    highlighted: true,
    badge: "Most Popular",
  },
  {
    name: "Premium",
    price: "$19.99",
    period: "/month",
    description: "For sustainability enthusiasts",
    features: [
      "Everything in Pro, plus:",
      "Personalized shopping consultant",
      "Exclusive brand partnerships",
      "Impact reports & certifications",
      "Custom sustainability goals",
      "Brand transparency deep dives",
      "Monthly sustainability workshops",
    ],
    cta: "Go Premium",
    highlighted: false,
  },
]

interface PricingTiersProps {
  onSelectTier?: (tier: string) => void
  selectedTier?: string
}

export function PricingTiers({ onSelectTier, selectedTier = "Free" }: PricingTiersProps) {
  return (
    <div className="py-12">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4">Choose Your Plan</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Start free and upgrade anytime. All plans include access to our curated sustainable brands.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
        {tiers.map((tier) => (
          <Card
            key={tier.name}
            className={`relative ${
              tier.highlighted
                ? "border-primary shadow-lg scale-105"
                : selectedTier === tier.name
                ? "border-primary"
                : ""
            }`}
          >
            {tier.badge && (
              <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                {tier.badge}
              </Badge>
            )}
            
            <CardHeader>
              <CardTitle className="text-2xl">{tier.name}</CardTitle>
              <CardDescription>{tier.description}</CardDescription>
              <div className="mt-4">
                <span className="text-4xl font-bold">{tier.price}</span>
                {tier.period && (
                  <span className="text-muted-foreground">{tier.period}</span>
                )}
              </div>
            </CardHeader>

            <CardContent>
              <ul className="space-y-3">
                {tier.features.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Check className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                    <span className={feature.includes("Everything in") ? "font-semibold" : ""}>
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>
            </CardContent>

            <CardFooter>
              <Button
                className="w-full"
                variant={tier.highlighted ? "default" : "outline"}
                onClick={() => onSelectTier?.(tier.name)}
              >
                {tier.cta}
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      <div className="text-center mt-8 text-sm text-muted-foreground">
        <p>All plans are currently free during beta. Premium features coming soon!</p>
      </div>
    </div>
  )
}

