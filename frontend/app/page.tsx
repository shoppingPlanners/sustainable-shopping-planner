"use client";

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Leaf, Recycle, Heart, Sparkles, ArrowRight, ShieldCheck } from "lucide-react"
import Link from "next/link"
import { Navigation } from "@/components/navigation"
import { useEffect, useState } from "react"
import { getUserInfo } from "@/lib/auth"
import { useRouter } from "next/navigation"

export default function WelcomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const user = getUserInfo()
    if (user) {
      setIsAuthenticated(true)
      // Redirect authenticated users to home
      router.push('/home')
    }
  }, [router])

  // Don't render welcome page if authenticated
  if (isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-muted/20">
      {/* Navigation */}
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <div className="flex justify-center mb-6">
            <div className="flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full border border-primary/20">
              <Sparkles className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium text-primary">AI-Powered Sustainable Shopping</span>
            </div>
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-foreground mb-6 text-balance">
            Shop Sustainably,
            <br />
            <span className="text-primary">Live Consciously</span>
          </h1>
          
          <p className="text-xl text-muted-foreground mb-10 text-pretty max-w-3xl mx-auto leading-relaxed">
            Discover personalized sustainable fashion recommendations powered by AI. 
            Make eco-friendly choices without compromising on style or quality.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/register">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground text-lg px-8 py-6 h-auto">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6 h-auto">
                Sign In
              </Button>
            </Link>
          </div>

          <p className="mt-6 text-sm text-muted-foreground">
            Join thousands making a difference, one purchase at a time
          </p>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Why Choose Sustainable Shopping?
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Your choices matter. Every purchase is an opportunity to support ethical practices.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mb-4">
                  <Sparkles className="h-7 w-7 text-primary" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">AI-Powered Recommendations</h3>
                <p className="text-muted-foreground">
                  Get personalized sustainable product suggestions tailored to your style, budget, and values.
                </p>
              </CardContent>
            </Card>

            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-accent/10 rounded-2xl flex items-center justify-center mb-4">
                  <Leaf className="h-7 w-7 text-accent" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">Eco-Friendly Materials</h3>
                <p className="text-muted-foreground">
                  Discover products made from organic cotton, recycled materials, and innovative sustainable fabrics.
                </p>
              </CardContent>
            </Card>

            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-green-500/10 rounded-2xl flex items-center justify-center mb-4">
                  <ShieldCheck className="h-7 w-7 text-green-600" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">Verified Brands</h3>
                <p className="text-muted-foreground">
                  Shop from trusted brands committed to ethical production and environmental responsibility.
                </p>
              </CardContent>
            </Card>

            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-pink-500/10 rounded-2xl flex items-center justify-center mb-4">
                  <Heart className="h-7 w-7 text-pink-600" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">Fair Trade Certified</h3>
                <p className="text-muted-foreground">
                  Support fair wages and transparent supply chains that put people before profits.
                </p>
              </CardContent>
            </Card>

            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-blue-500/10 rounded-2xl flex items-center justify-center mb-4">
                  <Recycle className="h-7 w-7 text-blue-600" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">Circular Fashion</h3>
                <p className="text-muted-foreground">
                  Products designed for longevity, repairability, and end-of-life recycling.
                </p>
              </CardContent>
            </Card>

            <Card className="border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="w-14 h-14 bg-purple-500/10 rounded-2xl flex items-center justify-center mb-4">
                  <Sparkles className="h-7 w-7 text-purple-600" />
                </div>
                <h3 className="font-semibold text-xl text-foreground mb-3">Track Your Impact</h3>
                <p className="text-muted-foreground">
                  See the positive environmental impact of your sustainable shopping choices over time.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-primary/5">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-6">
            Ready to Make a Difference?
          </h2>
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Join our community of conscious consumers and start your sustainable fashion journey today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground text-lg px-10 py-6 h-auto">
                Create Free Account
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
          <p className="mt-6 text-sm text-muted-foreground">
            No credit card required • Get started in minutes
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary mb-2">10K+</div>
              <div className="text-muted-foreground">Sustainable Products</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">500+</div>
              <div className="text-muted-foreground">Verified Brands</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">98%</div>
              <div className="text-muted-foreground">Customer Satisfaction</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
