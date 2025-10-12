"use client";

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Leaf, Heart, Shield, Users, Globe, Recycle, Award, CheckCircle } from "lucide-react"
import Link from "next/link"
import { Navigation } from "@/components/navigation"
import { tracker } from "@/lib/tracking"

export default function AboutPage() {
  if (typeof window !== 'undefined') {
    void tracker.sendEvent({ event_type: 'page_view', page: '/about' })
  }
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <Navigation />

      {/* Hero Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full">
              <Globe className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium text-primary">Fashion Forward</span>
            </div>
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-6 text-balance">
            About <span className="text-primary">StyleSustain</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 text-pretty max-w-3xl mx-auto">
            We connect conscious consumers with premium sustainable brands that prioritize both style and environmental
            responsibility.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">Our Mission</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Making sustainable fashion accessible and elegant
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Leaf className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground mb-3 text-lg">Environmental Care</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Eco-friendly materials and sustainable production methods that minimize environmental impact.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Heart className="h-8 w-8 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-3 text-lg">Ethical Standards</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Fair wages, safe conditions, and transparent supply chains that respect human rights.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-16 h-16 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-8 w-8 text-secondary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-3 text-lg">Verified Quality</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Rigorous verification ensures sustainability claims are backed by certifications.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">How It Works</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Smart recommendations based on sustainability and style
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-primary-foreground font-semibold text-sm">1</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">Data Collection</h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    We analyze materials, certifications, and production practices from premium sustainable brands.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-accent-foreground font-semibold text-sm">2</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">Smart Scoring</h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    Our algorithm calculates sustainability ratings based on environmental and ethical metrics.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-secondary-foreground font-semibold text-sm">3</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">Personal Curation</h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    We match your style and values with the most suitable sustainable options.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-foreground">What We Evaluate</CardTitle>
                <CardDescription>Key sustainability factors</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Organic & recycled materials</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Energy & water conservation</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Fair labor practices</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Supply chain transparency</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Carbon footprint reduction</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">Why Trust Us?</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Verified certifications and community-driven insights
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="border-border">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Award className="h-6 w-6 text-primary" />
                  <CardTitle className="text-foreground">Verified Certifications</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-sm mb-4">
                  Only brands with legitimate third-party certifications.
                </p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary" className="bg-secondary/50">
                    GOTS
                  </Badge>
                  <Badge variant="secondary" className="bg-secondary/50">
                    Fair Trade
                  </Badge>
                  <Badge variant="secondary" className="bg-secondary/50">
                    B-Corp
                  </Badge>
                  <Badge variant="secondary" className="bg-secondary/50">
                    Cradle to Cradle
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Users className="h-6 w-6 text-accent" />
                  <CardTitle className="text-foreground">Community Driven</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-sm mb-4">
                  Enhanced by real user reviews and community feedback.
                </p>
                <div className="flex items-center gap-4 text-sm">
                  <div className="text-foreground">
                    <span className="font-semibold">50K+</span> Users
                  </div>
                  <div className="text-foreground">
                    <span className="font-semibold">200+</span> Brands
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-card border border-border rounded-2xl p-8 md:p-12">
            <Recycle className="h-12 w-12 text-primary mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-foreground mb-4">Ready to Start?</h2>
            <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
              Join conscious consumers making a positive impact through fashion.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground" asChild>
                <Link href="/">
                  <Heart className="h-4 w-4 mr-2" />
                  Start Shopping
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="border-border hover:bg-muted bg-transparent" asChild>
                <Link href="/suggestions">View Collection</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
