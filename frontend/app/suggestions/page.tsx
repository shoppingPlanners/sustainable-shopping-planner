"use client";

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Leaf, Star, ExternalLink, Filter, Search } from "lucide-react"
import { Navigation } from "@/components/navigation"
import { tracker } from "@/lib/tracking"

// Mock data for clothing suggestions
const suggestions = [
  {
    id: 1,
    name: "Organic Cotton Classic Tee",
    brand: "Patagonia",
    rating: 4.8,
    sustainabilityScore: 95,
    price: "$35",
    image: "/organic-cotton-t-shirt-sustainable-fashion.png",
    buyUrl: "https://patagonia.com",
    features: ["Organic Cotton", "Fair Trade", "Carbon Neutral"],
    category: "tops",
  },
  {
    id: 2,
    name: "Recycled Denim Jeans",
    brand: "Everlane",
    rating: 4.6,
    sustainabilityScore: 88,
    price: "$78",
    image: "/recycled-denim-jeans-sustainable-fashion.png",
    buyUrl: "https://everlane.com",
    features: ["Recycled Materials", "Water-Saving Process", "Ethical Production"],
    category: "bottoms",
  },
  {
    id: 3,
    name: "Hemp Blend Hoodie",
    brand: "Tentree",
    rating: 4.7,
    sustainabilityScore: 92,
    price: "$89",
    image: "/hemp-hoodie-sustainable-fashion.jpg",
    buyUrl: "https://tentree.com",
    features: ["Hemp Blend", "Tree Planting Program", "Plastic-Free Packaging"],
    category: "outerwear",
  },
  {
    id: 4,
    name: "Bamboo Fiber Dress",
    brand: "Reformation",
    rating: 4.5,
    sustainabilityScore: 90,
    price: "$128",
    image: "/bamboo-dress-sustainable-fashion.jpg",
    buyUrl: "https://reformation.com",
    features: ["Bamboo Fiber", "Biodegradable", "Low Water Usage"],
    category: "dresses",
  },
  {
    id: 5,
    name: "Recycled Polyester Jacket",
    brand: "Girlfriend Collective",
    rating: 4.4,
    sustainabilityScore: 85,
    price: "$98",
    image: "/recycled-polyester-jacket-sustainable-fashion.jpg",
    buyUrl: "https://girlfriend.com",
    features: ["Recycled Polyester", "Inclusive Sizing", "Transparent Pricing"],
    category: "outerwear",
  },
  {
    id: 6,
    name: "Organic Linen Shirt",
    brand: "Eileen Fisher",
    rating: 4.9,
    sustainabilityScore: 96,
    price: "$158",
    image: "/organic-linen-shirt-sustainable-fashion.jpg",
    buyUrl: "https://eileenfisher.com",
    features: ["Organic Linen", "Timeless Design", "Take-Back Program"],
    category: "tops",
  },
]

export default function SuggestionsPage() {
  if (typeof window !== "undefined") {
    // send page view
    void tracker.sendEvent({ event_type: "page_view", page: "/suggestions" })
  }
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <Navigation />

      {/* Header Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-4">Your Curated Collection</h1>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Premium sustainable pieces selected for you
            </p>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Filter className="h-4 w-4" />
              <span>Filter:</span>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
              <Select>
                <SelectTrigger className="w-full sm:w-[140px]">
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Items</SelectItem>
                  <SelectItem value="tops">Tops</SelectItem>
                  <SelectItem value="bottoms">Bottoms</SelectItem>
                  <SelectItem value="dresses">Dresses</SelectItem>
                  <SelectItem value="outerwear">Outerwear</SelectItem>
                </SelectContent>
              </Select>

              <Select>
                <SelectTrigger className="w-full sm:w-[140px]">
                  <SelectValue placeholder="Price Range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Prices</SelectItem>
                  <SelectItem value="under-50">Under $50</SelectItem>
                  <SelectItem value="50-100">$50 - $100</SelectItem>
                  <SelectItem value="100-200">$100 - $200</SelectItem>
                  <SelectItem value="200-plus">$200+</SelectItem>
                </SelectContent>
              </Select>

              <div className="relative w-full sm:w-[200px]">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search brands..." className="pl-9" onBlur={(e)=>{
                  const q = e.currentTarget.value?.trim()
                  if(q) void tracker.sendEvent({ event_type: "search", keywords: q.split(/\s+/) })
                }} />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Suggestions Grid */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {suggestions.map((item) => (
              <Card
                key={item.id}
                className="group hover:shadow-xl transition-all duration-300 border-border overflow-hidden"
              >
                <div className="aspect-[4/5] overflow-hidden">
                  <img
                    src={item.image || "/placeholder.svg"}
                    alt={item.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onLoad={()=>{ void tracker.sendEvent({ event_type: "view_item", item_id: String(item.id), page: "/suggestions", tags: item.features }) }}
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
                  {/* Ratings */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1">
                      <Star className="h-4 w-4 fill-accent text-accent" />
                      <span className="text-sm font-medium text-foreground">{item.rating}</span>
                      <span className="text-sm text-muted-foreground">(124 reviews)</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Leaf className="h-4 w-4 text-primary" />
                      <span className="text-sm font-medium text-primary">{item.sustainabilityScore}%</span>
                    </div>
                  </div>

                  {/* Features */}
                  <div className="flex flex-wrap gap-1">
                    {item.features.map((feature, index) => (
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
                  <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground group/btn" asChild onClick={()=>{ void tracker.sendEvent({ event_type: "click", element: "shop_now", item_id: String(item.id) }) }}>
                    <a href={item.buyUrl} target="_blank" rel="noopener noreferrer">
                      Shop Now
                      <ExternalLink className="h-4 w-4 ml-2 group-hover/btn:translate-x-0.5 transition-transform" />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Load More */}
          <div className="text-center mt-12">
            <Button variant="outline" size="lg" className="border-border hover:bg-muted bg-transparent">
              View More
            </Button>
          </div>
        </div>
      </section>

      {/* Sustainability Info */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-foreground mb-4">Sustainability Ratings</h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Based on materials, production, and environmental impact
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="text-primary font-semibold mb-2">90-100%</div>
              <div className="text-sm text-muted-foreground">Exceptional practices</div>
            </div>
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="text-accent font-semibold mb-2">75-89%</div>
              <div className="text-sm text-muted-foreground">Strong commitment</div>
            </div>
            <div className="bg-card rounded-lg p-4 border border-border">
              <div className="text-secondary-foreground font-semibold mb-2">60-74%</div>
              <div className="text-sm text-muted-foreground">Good efforts</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
