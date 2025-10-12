"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Leaf, Recycle, Heart, Star, ExternalLink, Loader2 } from "lucide-react"
import { Navigation } from "@/components/navigation"
import { tracker } from "@/lib/tracking"
import { useState } from "react"

interface Recommendation {
  id: string;
  name: string;
  brand: string;
  rating: number;
  sustainabilityScore: number;
  price: string;
  image: string;
  buyUrl: string;
  features: string[];
  category: string;
  match_score: number;
  reason: string;
}

export default function HomePage() {
  const [formData, setFormData] = useState({
    category: "",
    budget: "",
    style: "",
    sustainability_priorities: "",
    size: ""
  });
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRecommendations, setShowRecommendations] = useState(false);

  if (typeof window !== 'undefined') {
    void tracker.sendEvent({ event_type: 'page_view', page: '/' })
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Save preferences
      const saveResponse = await fetch('http://localhost:8000/api/preferences/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!saveResponse.ok) {
        throw new Error('Failed to save preferences');
      }

      // Get recommendations
      const params = new URLSearchParams();
      Object.entries(formData).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const recommendationsResponse = await fetch(`http://localhost:8000/api/preferences/recommendations?${params.toString()}`);
      
      if (!recommendationsResponse.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await recommendationsResponse.json();
      setRecommendations(data);
      setShowRecommendations(true);
      
      // Track the form submission
      void tracker.sendEvent({ 
        event_type: 'form_submit', 
        page: '/'
      });

    } catch (err) {
      console.error('Error:', err);
      setError('Failed to get recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <Navigation />

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="flex items-center gap-2 bg-accent/10 px-4 py-2 rounded-full">
              <Recycle className="h-5 w-5 text-accent" />
              <span className="text-sm font-medium text-accent">Conscious Fashion</span>
            </div>
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold text-foreground mb-6 text-balance">
            Elegant
            <span className="text-primary"> Sustainability</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 text-pretty max-w-2xl mx-auto">
            Discover premium sustainable fashion that aligns with your values and style.
          </p>
        </div>
      </section>

      {/* Requirements Input Form */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mx-auto">
          <Card className="border-border shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-foreground">Your Preferences</CardTitle>
              <CardDescription className="text-muted-foreground">Tell us what matters to you</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="clothing-type" className="text-foreground">
                      Category
                    </Label>
                    <Select value={formData.category} onValueChange={(value) => handleInputChange("category", value)}>
                      <SelectTrigger id="clothing-type">
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="tops">Tops</SelectItem>
                        <SelectItem value="bottoms">Bottoms</SelectItem>
                        <SelectItem value="dresses">Dresses</SelectItem>
                        <SelectItem value="outerwear">Outerwear</SelectItem>
                        <SelectItem value="activewear">Activewear</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="budget" className="text-foreground">
                      Budget
                    </Label>
                    <Select value={formData.budget} onValueChange={(value) => handleInputChange("budget", value)}>
                      <SelectTrigger id="budget">
                        <SelectValue placeholder="Price range" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="under-50">Under $50</SelectItem>
                        <SelectItem value="50-100">$50 - $100</SelectItem>
                        <SelectItem value="100-200">$100 - $200</SelectItem>
                        <SelectItem value="200-plus">$200+</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="style" className="text-foreground">
                    Style
                  </Label>
                  <Select value={formData.style} onValueChange={(value) => handleInputChange("style", value)}>
                    <SelectTrigger id="style">
                      <SelectValue placeholder="Your aesthetic" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="casual">Casual</SelectItem>
                      <SelectItem value="professional">Professional</SelectItem>
                      <SelectItem value="trendy">Contemporary</SelectItem>
                      <SelectItem value="minimalist">Minimalist</SelectItem>
                      <SelectItem value="bohemian">Bohemian</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sustainability" className="text-foreground">
                    Priorities
                  </Label>
                  <Textarea
                    id="sustainability"
                    placeholder="Organic materials, fair trade, carbon neutral..."
                    className="min-h-[80px] resize-none"
                    value={formData.sustainability_priorities}
                    onChange={(e) => handleInputChange("sustainability_priorities", e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="size" className="text-foreground">
                    Size
                  </Label>
                  <Input 
                    id="size" 
                    placeholder="e.g., M, L, 32" 
                    value={formData.size}
                    onChange={(e) => handleInputChange("size", e.target.value)}
                  />
                </div>

                {error && (
                  <div className="text-destructive text-sm text-center">
                    {error}
                  </div>
                )}

                <Button 
                  type="submit" 
                  className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" 
                  size="lg"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Finding Matches...
                    </>
                  ) : (
                    <>
                      <Heart className="h-4 w-4 mr-2" />
                      Find My Matches
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Recommendations Section */}
      {showRecommendations && (
        <section className="py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-foreground mb-4">Your Personalized Recommendations</h2>
              <p className="text-muted-foreground">Based on your preferences, here are our top picks for you</p>
            </div>

            {recommendations.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((item) => (
                  <Card key={item.id} className="group hover:shadow-xl transition-all duration-300 border-border overflow-hidden">
                    <div className="aspect-[4/5] overflow-hidden">
                      <img
                        src={item.image || "/placeholder.svg"}
                        alt={item.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>

                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <CardTitle className="text-lg text-foreground line-clamp-2">{item.name}</CardTitle>
                          <CardDescription className="text-muted-foreground font-medium">{item.brand}</CardDescription>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-foreground">{item.price}</div>
                        </div>
                      </div>
                    </CardHeader>

                    <CardContent className="pt-0 space-y-4">
                      {/* Match Score */}
                      <div className="flex items-center justify-between">
                        <Badge variant="secondary" className="bg-primary/10 text-primary">
                          {item.match_score}% Match
                        </Badge>
                        <div className="text-xs text-muted-foreground text-right max-w-[200px]">
                          {item.reason}
                        </div>
                      </div>

                      {/* Ratings */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 fill-accent text-accent" />
                          <span className="text-sm font-medium text-foreground">{item.rating}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Leaf className="h-4 w-4 text-primary" />
                          <span className="text-sm font-medium text-primary">{item.sustainabilityScore}%</span>
                        </div>
                      </div>

                      {/* Features */}
                      <div className="flex flex-wrap gap-1">
                        {item.features.slice(0, 3).map((feature, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="text-xs bg-secondary/50 text-secondary-foreground"
                          >
                            {feature}
                          </Badge>
                        ))}
                      </div>

                      {/* Buy Button */}
                      <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground group/btn" asChild>
                        <a href={item.buyUrl} target="_blank" rel="noopener noreferrer">
                          Shop Now
                          <ExternalLink className="h-4 w-4 ml-2 group-hover/btn:translate-x-0.5 transition-transform" />
                        </a>
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-muted-foreground mb-4">No recommendations found. Try adjusting your preferences.</p>
                <Button onClick={() => setShowRecommendations(false)} variant="outline">
                  Adjust Preferences
                </Button>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">Why Sustainable?</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Leaf className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Eco Materials</h3>
                <p className="text-muted-foreground text-sm">Organic, recycled, and innovative sustainable fabrics</p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Heart className="h-6 w-6 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Fair Production</h3>
                <p className="text-muted-foreground text-sm">Ethical wages and transparent supply chains</p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Recycle className="h-6 w-6 text-secondary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Circular Design</h3>
                <p className="text-muted-foreground text-sm">Built for longevity and end-of-life recycling</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  )
}
