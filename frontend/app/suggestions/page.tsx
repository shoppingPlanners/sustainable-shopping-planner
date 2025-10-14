"use client";

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Leaf, Star, ExternalLink, Filter, Search, Loader2, Heart, ShoppingCart, TrendingUp, Sparkles } from "lucide-react"
import { Navigation } from "@/components/navigation"
import { ItemCard } from "@/components/item-card"
import { SearchFilters } from "@/components/search-filters"
import { useTracking, useScrollTracking, useTimeTracking } from "@/hooks/use-tracking"
import { useAuth } from "@/lib/auth-context"
import { userBehaviorTracker } from "@/lib/user-behavior"
import { useState, useEffect } from "react"

interface ProductSuggestion {
  product_id: string;
  product_name: string;
  brand_name: string;
  sustainability_score: number;
  price: string;
  recommendation_score: number;
  reasons: string[];
  category: string;
  url: string;
}

interface TrendingProduct {
  product_id: string;
  product_name: string;
  brand_name: string;
  sustainability_score: number;
  price: string;
  category: string;
  url: string;
}

export default function SuggestionsPage() {
  const { user, isAuthenticated } = useAuth();
  const [personalizedSuggestions, setPersonalizedSuggestions] = useState<ProductSuggestion[]>([]);
  const [trendingProducts, setTrendingProducts] = useState<TrendingProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [activeTab, setActiveTab] = useState<'personalized' | 'trending'>('personalized');
  const [minSustainabilityScore, setMinSustainabilityScore] = useState<number>(70);

  const { trackFormInteraction } = useTracking();
  
  // Track scroll and time on page
  useScrollTracking("/suggestions");
  useTimeTracking("/suggestions");

  useEffect(() => {
    if (user) {
      userBehaviorTracker.trackPageView('/suggestions');
    }
    fetchSuggestions();
  }, [selectedCategory, filters, minSustainabilityScore, user]);

  const fetchSuggestions = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (isAuthenticated && user) {
        // Get personalized AI recommendations
        const personalizedResponse = await fetch(
          `http://localhost:5004/suggestions/${user.id}?limit=12&category=${selectedCategory !== "all" ? selectedCategory : ""}&min_sustainability_score=${minSustainabilityScore}`
        );
        
        if (personalizedResponse.ok) {
          const personalizedData = await personalizedResponse.json();
          setPersonalizedSuggestions(personalizedData.suggestions || []);
        }
        
        // Get trending products
        const trendingResponse = await fetch(
          `http://localhost:5004/trending?limit=12&min_sustainability_score=${minSustainabilityScore}`
        );
        
        if (trendingResponse.ok) {
          const trendingData = await trendingResponse.json();
          setTrendingProducts(trendingData.trending_products || []);
        }
        
        // Track the recommendation request
        await userBehaviorTracker.trackEvent(user.id, 'recommendation_request', undefined, {
          category: selectedCategory,
          min_sustainability_score: minSustainabilityScore
        });
        
      } else {
        // For non-authenticated users, get trending products only
        const trendingResponse = await fetch(
          `http://localhost:5004/trending?limit=12&min_sustainability_score=${minSustainabilityScore}`
        );
        
        if (trendingResponse.ok) {
          const trendingData = await trendingResponse.json();
          setTrendingProducts(trendingData.trending_products || []);
        }
      }
      
    } catch (err) {
      console.error("Failed to fetch suggestions:", err);
      setError("Failed to load suggestions. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query: string, searchFilters: Record<string, any>) => {
    setSearchQuery(query);
    setFilters(searchFilters);
    trackFormInteraction("search", "submit", { query, filters: searchFilters });
  };

  const handleFilterChange = (filterType: string, value: string) => {
    setFilters(prev => ({ ...prev, [filterType]: value }));
    trackFormInteraction("filter", "change", { filterType, value });
  };

  const handleAddToCart = async (itemId: string, price: string) => {
    trackFormInteraction("cart", "add", { itemId, price });
    
    if (user) {
      await userBehaviorTracker.trackEvent(user.id, 'add_to_cart', itemId, { price });
    }
    
    console.log(`Added item ${itemId} to cart for ${price}`);
  };

  const handleAddToWishlist = async (itemId: string) => {
    trackFormInteraction("wishlist", "add", { itemId });
    
    if (user) {
      await userBehaviorTracker.trackEvent(user.id, 'liked', itemId);
    }
    
    console.log(`Added item ${itemId} to wishlist`);
  };

  const handleProductView = async (itemId: string) => {
    if (user) {
      await userBehaviorTracker.trackEvent(user.id, 'viewed', itemId);
    }
  };

  const handleProductClick = async (itemId: string) => {
    if (user) {
      await userBehaviorTracker.trackEvent(user.id, 'clicked', itemId);
    }
  };

  const handleLoadMore = () => {
    trackFormInteraction("pagination", "load_more", { page: 2, pageSize: 50 });
    console.log("Loading more items...");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <Navigation />

      {/* Header Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-4">
              {isAuthenticated ? "AI-Powered Recommendations" : "Sustainable Products"}
            </h1>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              {isAuthenticated 
                ? "Personalized sustainable fashion recommendations powered by AI and your behavior patterns"
                : "Discover trending sustainable products"
              }
            </p>
            {isAuthenticated && (
              <Badge variant="secondary" className="mt-2 flex items-center gap-1 w-fit mx-auto">
                <Sparkles className="h-3 w-3" />
                Powered by AI & User Behavior
              </Badge>
            )}
          </div>

          {/* Tab Navigation */}
          {isAuthenticated && (
            <div className="flex justify-center mb-8">
              <div className="flex bg-muted rounded-lg p-1">
                <Button
                  variant={activeTab === 'personalized' ? 'default' : 'ghost'}
                  onClick={() => setActiveTab('personalized')}
                  className="flex items-center gap-2"
                >
                  <Heart className="h-4 w-4" />
                  Personalized
                </Button>
                <Button
                  variant={activeTab === 'trending' ? 'default' : 'ghost'}
                  onClick={() => setActiveTab('trending')}
                  className="flex items-center gap-2"
                >
                  <TrendingUp className="h-4 w-4" />
                  Trending
                </Button>
              </div>
            </div>
          )}

          {/* Search and Filters */}
          <SearchFilters 
            onSearch={handleSearch}
            onFilterChange={handleFilterChange}
            page="/suggestions"
          />
        </div>
      </section>

      {/* Suggestions Grid */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <div className="text-center">
                <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
                <p className="text-muted-foreground">
                  {isAuthenticated ? "Generating AI recommendations..." : "Loading products..."}
                </p>
              </div>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-destructive mb-4">{error}</p>
              <Button onClick={fetchSuggestions} variant="outline">
                Try Again
              </Button>
            </div>
          ) : (
            <>
              {/* Personalized Suggestions */}
              {isAuthenticated && activeTab === 'personalized' && (
                <>
                  {personalizedSuggestions.length === 0 ? (
                    <div className="text-center py-12">
                      <p className="text-muted-foreground mb-4">No personalized recommendations found.</p>
                      <Button onClick={() => setActiveTab('trending')} variant="outline">
                        View Trending Products
                      </Button>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {personalizedSuggestions.map((suggestion) => (
                        <Card key={suggestion.product_id} className="group hover:shadow-lg transition-shadow">
                          <CardHeader className="pb-2">
                            <div className="flex items-start justify-between">
                              <CardTitle className="text-lg line-clamp-2">{suggestion.product_name}</CardTitle>
                              <Badge variant="secondary" className="ml-2">
                                {Math.round(suggestion.recommendation_score * 100)}% match
                              </Badge>
                            </div>
                            <CardDescription className="text-sm text-muted-foreground">
                              {suggestion.brand_name}
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-3">
                              <div className="flex items-center justify-between">
                                <span className="text-2xl font-bold">{suggestion.price}</span>
                                <div className="flex items-center gap-1">
                                  <Leaf className="h-4 w-4 text-green-600" />
                                  <span className="text-sm font-medium">{suggestion.sustainability_score}/100</span>
                                </div>
                              </div>
                              
                              <div className="space-y-2">
                                <p className="text-sm text-muted-foreground">Why we recommend:</p>
                                <ul className="text-xs space-y-1">
                                  {suggestion.reasons.slice(0, 2).map((reason, index) => (
                                    <li key={index} className="flex items-start gap-1">
                                      <Star className="h-3 w-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                                      <span>{reason}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              
                              <div className="flex gap-2">
                                <Button 
                                  size="sm" 
                                  className="flex-1"
                                  onClick={() => handleProductClick(suggestion.product_id)}
                                >
                                  <ExternalLink className="h-4 w-4 mr-1" />
                                  View
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleAddToWishlist(suggestion.product_id)}
                                >
                                  <Heart className="h-4 w-4" />
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleAddToCart(suggestion.product_id, suggestion.price)}
                                >
                                  <ShoppingCart className="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  )}
                </>
              )}

              {/* Trending Products */}
              {(activeTab === 'trending' || !isAuthenticated) && (
                <>
                  {trendingProducts.length === 0 ? (
                    <div className="text-center py-12">
                      <p className="text-muted-foreground mb-4">No trending products found.</p>
                      <Button onClick={fetchSuggestions} variant="outline">
                        Refresh
                      </Button>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {trendingProducts.map((product) => (
                        <Card key={product.product_id} className="group hover:shadow-lg transition-shadow">
                          <CardHeader className="pb-2">
                            <div className="flex items-start justify-between">
                              <CardTitle className="text-lg line-clamp-2">{product.product_name}</CardTitle>
                              <Badge variant="outline" className="ml-2">
                                <TrendingUp className="h-3 w-3 mr-1" />
                                Trending
                              </Badge>
                            </div>
                            <CardDescription className="text-sm text-muted-foreground">
                              {product.brand_name}
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-3">
                              <div className="flex items-center justify-between">
                                <span className="text-2xl font-bold">{product.price}</span>
                                <div className="flex items-center gap-1">
                                  <Leaf className="h-4 w-4 text-green-600" />
                                  <span className="text-sm font-medium">{product.sustainability_score}/100</span>
                                </div>
                              </div>
                              
                              <div className="flex gap-2">
                                <Button 
                                  size="sm" 
                                  className="flex-1"
                                  onClick={() => handleProductClick(product.product_id)}
                                >
                                  <ExternalLink className="h-4 w-4 mr-1" />
                                  View
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleAddToWishlist(product.product_id)}
                                >
                                  <Heart className="h-4 w-4" />
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="outline"
                                  onClick={() => handleAddToCart(product.product_id, product.price)}
                                >
                                  <ShoppingCart className="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  )}
                </>
              )}
            </>
          )}

          {/* Load More */}
          <div className="text-center mt-12">
            <Button 
              variant="outline" 
              size="lg" 
              className="border-border hover:bg-muted bg-transparent"
              onClick={handleLoadMore}
            >
              View More
            </Button>
          </div>
        </div>
      </section>

      {/* Sustainability Info */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-foreground mb-4">
            {isAuthenticated ? "AI-Powered Sustainability Analysis" : "Sustainability Ratings"}
          </h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            {isAuthenticated 
              ? "Our AI analyzes materials, production methods, and environmental impact to provide personalized sustainability scores"
              : "Based on materials, production, and environmental impact"
            }
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="flex items-center gap-2 mb-2">
                <div className="text-primary font-semibold">90-100%</div>
                {isAuthenticated && <Sparkles className="h-4 w-4 text-primary" />}
              </div>
              <div className="text-sm text-muted-foreground">
                {isAuthenticated ? "AI-identified exceptional practices" : "Exceptional practices"}
              </div>
            </div>
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="flex items-center gap-2 mb-2">
                <div className="text-accent font-semibold">75-89%</div>
                {isAuthenticated && <Leaf className="h-4 w-4 text-accent" />}
              </div>
              <div className="text-sm text-muted-foreground">
                {isAuthenticated ? "AI-detected strong commitment" : "Strong commitment"}
              </div>
            </div>
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="flex items-center gap-2 mb-2">
                <div className="text-secondary-foreground font-semibold">60-74%</div>
                {isAuthenticated && <Star className="h-4 w-4 text-secondary-foreground" />}
              </div>
              <div className="text-sm text-muted-foreground">
                {isAuthenticated ? "AI-recognized good efforts" : "Good efforts"}
              </div>
            </div>
          </div>
          
          {isAuthenticated && (
            <div className="mt-8 p-4 bg-primary/10 rounded-lg border border-primary/20">
              <p className="text-sm text-primary">
                <strong>AI Learning:</strong> Your interactions help our AI improve sustainability recommendations over time.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
