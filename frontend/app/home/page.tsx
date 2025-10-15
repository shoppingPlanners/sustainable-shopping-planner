"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Leaf, Recycle, Heart, Star, ExternalLink, Loader2, AlertCircle, Package, Sparkles } from "lucide-react"
import { Navigation } from "@/components/navigation"
import { ItemCard } from "@/components/item-card"
import { useTracking, useScrollTracking, useTimeTracking } from "@/hooks/use-tracking"
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
  sustainability_focus?: string[];
  is_bestseller?: boolean;
  description?: string;
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

  const { trackFormInteraction, trackClick } = useTracking();
  
  // Track scroll and time on page
  useScrollTracking("/home");
  useTimeTracking("/home");

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    trackFormInteraction("preferences_form", "field_change", { field, value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // First, save preferences to the database
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

      const saveResult = await saveResponse.json();
      console.log('Preferences saved:', saveResult);

      // Then get personalized recommendations
      const params = new URLSearchParams();
      Object.entries(formData).forEach(([key, value]) => {
        if (value && value !== "all") {
          params.append(key, value);
        }
      });

      const recommendationsResponse = await fetch(`http://localhost:8000/api/preferences/recommendations?${params.toString()}`);
      
      if (!recommendationsResponse.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await recommendationsResponse.json();
      
      // The backend already returns recommendations in the correct format
      setRecommendations(data);
      setShowRecommendations(true);
      
      // Track the form submission
      trackFormInteraction("preferences_form", "submit", { 
        preferences: formData,
        recommendation_count: data.length 
      });

    } catch (err) {
      console.error('Error:', err);
      setError('Failed to get recommendations. Please try again.');
      trackFormInteraction("preferences_form", "error", { error: err instanceof Error ? err.message : 'Unknown error' });
    } finally {
      setLoading(false);
    }
  };

  // Helper function to generate match reasons
  const generateMatchReason = (preferences: any, item: any) => {
    const reasons = [];
    
    // Match by product name keywords
    if (preferences.category && preferences.category !== "all") {
      const productName = item.name.toLowerCase();
      if (preferences.category === "dresses" && productName.includes("dress")) {
        reasons.push("Perfect dress match");
      } else if (preferences.category === "tops" && (productName.includes("blouse") || productName.includes("top"))) {
        reasons.push("Great top option");
      } else if (preferences.category === "t-shirts" && productName.includes("t-shirt")) {
        reasons.push("Classic t-shirt style");
      } else if (preferences.category === "summer" && productName.includes("summer")) {
        reasons.push("Summer collection item");
      }
    }
    
    if (preferences.budget) {
      const price = parseFloat(item.price.replace(/[^0-9.]/g, ''));
      if (preferences.budget === 'under-20' && price < 20) {
        reasons.push('Great value under $20');
      } else if (preferences.budget === '20-30' && price >= 20 && price <= 30) {
        reasons.push('Perfect mid-range price');
      } else if (preferences.budget === '30-50' && price >= 30 && price <= 50) {
        reasons.push('Premium quality range');
      } else if (preferences.budget === '50-plus' && price > 50) {
        reasons.push('High-end option');
      }
    }
    
    if (preferences.sustainability_priorities && item.sustainabilityScore > 0) {
      reasons.push('Sustainable materials');
    }
    
    // Match by style preferences
    if (preferences.style) {
      const productName = item.name.toLowerCase();
      if (preferences.style === "printed" && productName.includes("printed")) {
        reasons.push("Beautiful printed design");
      } else if (preferences.style === "summer" && productName.includes("summer")) {
        reasons.push("Perfect summer style");
      } else if (preferences.style === "chiffon" && productName.includes("chiffon")) {
        reasons.push("Elegant chiffon material");
      } else if (preferences.style === "basic" && productName.includes("faded")) {
        reasons.push("Classic basic style");
      }
    }
    
    // Check available sizes
    if (preferences.size && item.features.includes(preferences.size.toUpperCase())) {
      reasons.push(`Available in size ${preferences.size.toUpperCase()}`);
    }
    
    if (reasons.length === 0) {
      reasons.push('Great sustainable option');
    }
    
    return reasons.join(', ');
  };

  const handleAddToCart = (itemId: string, price: string) => {
    trackFormInteraction("cart", "add", { itemId, price });
    // Here you would typically add to cart state/context
    console.log(`Added item ${itemId} to cart for ${price}`);
  };

  const handleAddToWishlist = (itemId: string) => {
    trackFormInteraction("wishlist", "add", { itemId });
    // Here you would typically add to wishlist state/context
    console.log(`Added item ${itemId} to wishlist`);
  };

  const handleAdjustPreferences = () => {
    setShowRecommendations(false);
    trackClick("adjust_preferences_button");
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
                        <SelectItem value="all">All Items</SelectItem>
                        <SelectItem value="dresses">Dresses</SelectItem>
                        <SelectItem value="tops">Tops & Shirts</SelectItem>
                        <SelectItem value="t-shirts">T-Shirts</SelectItem>
                        <SelectItem value="bottoms">Bottoms & Jeans</SelectItem>
                        <SelectItem value="outerwear">Jackets & Outerwear</SelectItem>
                        <SelectItem value="activewear">Activewear</SelectItem>
                        <SelectItem value="footwear">Footwear</SelectItem>
                        <SelectItem value="accessories">Accessories</SelectItem>
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
                        <SelectItem value="under-20">Under $20</SelectItem>
                        <SelectItem value="20-30">$20 - $30</SelectItem>
                        <SelectItem value="30-50">$30 - $50</SelectItem>
                        <SelectItem value="50-plus">$50+</SelectItem>
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
                      <SelectItem value="printed">Printed & Patterned</SelectItem>
                      <SelectItem value="summer">Summer Style</SelectItem>
                      <SelectItem value="basic">Basic & Simple</SelectItem>
                      <SelectItem value="chiffon">Elegant Chiffon</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sustainability" className="text-foreground">
                    Priorities
                  </Label>
                  <Textarea
                    id="sustainability"
                    placeholder="Organic cotton, recycled materials, fair trade, eco-friendly dyes..."
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
                    placeholder="e.g., S, M, L" 
                    value={formData.size}
                    onChange={(e) => handleInputChange("size", e.target.value)}
                  />
                </div>

                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      {error}
                    </AlertDescription>
                  </Alert>
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
                      Finding Your Perfect Matches...
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4 mr-2" />
                      Find My Matches
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Loading State */}
      {loading && (
        <section className="py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-8">
              <Skeleton className="h-8 w-96 mx-auto mb-4" />
              <Skeleton className="h-4 w-64 mx-auto" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, index) => (
                <Card key={index} className="overflow-hidden">
                  <Skeleton className="aspect-[4/5] w-full" />
                  <CardHeader>
                    <Skeleton className="h-6 w-3/4 mb-2" />
                    <Skeleton className="h-4 w-1/2" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-4 w-full mb-2" />
                    <Skeleton className="h-4 w-2/3" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Recommendations Section */}
      {showRecommendations && !loading && (
        <section className="py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-8">
              <Badge variant="secondary" className="mb-4">
                <Sparkles className="h-3 w-3 mr-1" />
                {recommendations.length} Perfect Matches
              </Badge>
              <h2 className="text-3xl font-bold text-foreground mb-4">Your Personalized Recommendations</h2>
              <p className="text-muted-foreground">Curated sustainable fashion based on your unique preferences</p>
            </div>

            {recommendations.length > 0 ? (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {recommendations.map((item) => (
                    <ItemCard
                      key={item.id}
                      item={item}
                      page="/home"
                      showMatchScore={true}
                      onAddToCart={handleAddToCart}
                      onAddToWishlist={handleAddToWishlist}
                    />
                  ))}
                </div>
                <div className="text-center">
                  <Button onClick={handleAdjustPreferences} variant="outline" size="lg">
                    <Leaf className="h-4 w-4 mr-2" />
                    Refine Preferences
                  </Button>
                </div>
              </>
            ) : (
              <Card className="border-dashed">
                <CardContent className="text-center py-16">
                  <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                    <Package className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">No Matches Found</h3>
                  <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                    We couldn't find items matching your exact criteria. Try broadening your preferences or exploring different categories.
                  </p>
                  <div className="flex gap-3 justify-center">
                    <Button onClick={handleAdjustPreferences} variant="default">
                      <Leaf className="h-4 w-4 mr-2" />
                      Adjust Preferences
                    </Button>
                    <Button onClick={() => handleInputChange("category", "all")} variant="outline">
                      View All Items
                    </Button>
                  </div>
                </CardContent>
              </Card>
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