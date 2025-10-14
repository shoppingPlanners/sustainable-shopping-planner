"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Leaf, Star, ExternalLink, Heart, ShoppingCart } from "lucide-react";
import { useItemTracking } from "@/hooks/use-tracking";
import { useState } from "react";

interface Item {
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
  match_score?: number;
  reason?: string;
}

interface ItemCardProps {
  item: Item;
  page?: string;
  showMatchScore?: boolean;
  onAddToCart?: (itemId: string, price: string) => void;
  onAddToWishlist?: (itemId: string) => void;
}

export function ItemCard({ 
  item, 
  page = "/suggestions", 
  showMatchScore = false,
  onAddToCart,
  onAddToWishlist 
}: ItemCardProps) {
  const { handleItemView, handleItemClick, handleAddToCart } = useItemTracking(item.id, page);
  const [isInCart, setIsInCart] = useState(false);
  const [isInWishlist, setIsInWishlist] = useState(false);

  const handleImageLoad = () => {
    handleItemView();
  };

  const handleShopNowClick = () => {
    handleItemClick("shop_now_button");
  };

  const handleAddToCartClick = () => {
    if (onAddToCart) {
      onAddToCart(item.id, item.price);
    }
    handleAddToCart(item.price);
    setIsInCart(true);
    
    // Reset after animation
    setTimeout(() => setIsInCart(false), 2000);
  };

  const handleWishlistClick = () => {
    if (onAddToWishlist) {
      onAddToWishlist(item.id);
    }
    handleItemClick("wishlist_button");
    setIsInWishlist(!isInWishlist);
  };

  const handleCardClick = () => {
    handleItemClick("item_card");
  };

  const handleFeatureClick = (feature: string) => {
    handleItemClick("feature_badge");
  };

  return (
    <Card 
      className="group hover:shadow-xl transition-all duration-300 border-border overflow-hidden cursor-pointer"
      onClick={handleCardClick}
    >
      <div className="aspect-[4/5] overflow-hidden relative">
        <img
          src={item.image || "/placeholder.svg"}
          alt={item.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onLoad={handleImageLoad}
        />
        
        {/* Wishlist Button */}
        <Button
          variant="ghost"
          size="sm"
          className="absolute top-2 right-2 bg-background/80 hover:bg-background/90 backdrop-blur-sm"
          onClick={(e) => {
            e.stopPropagation();
            handleWishlistClick();
          }}
        >
          <Heart 
            className={`h-4 w-4 ${isInWishlist ? 'fill-red-500 text-red-500' : 'text-muted-foreground hover:text-red-500'}`} 
          />
        </Button>

        {/* Add to Cart Button */}
        <Button
          variant="secondary"
          size="sm"
          className="absolute top-2 left-2 bg-background/80 hover:bg-background/90 backdrop-blur-sm"
          onClick={(e) => {
            e.stopPropagation();
            handleAddToCartClick();
          }}
        >
          <ShoppingCart className={`h-4 w-4 ${isInCart ? 'text-green-500' : 'text-muted-foreground'}`} />
        </Button>
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
        {/* Match Score (if available) */}
        {showMatchScore && item.match_score && (
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="bg-primary/10 text-primary">
              {item.match_score}% Match
            </Badge>
            <div className="text-xs text-muted-foreground text-right max-w-[200px]">
              {item.reason}
            </div>
          </div>
        )}

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
          {item.features.slice(0, 3).map((feature, index) => (
            <Badge
              key={index}
              variant="secondary"
              className="text-xs bg-secondary/50 text-secondary-foreground cursor-pointer hover:bg-secondary/70"
              onClick={(e) => {
                e.stopPropagation();
                handleFeatureClick(feature);
              }}
            >
              {feature}
            </Badge>
          ))}
          {item.features.length > 3 && (
            <Badge variant="outline" className="text-xs">
              +{item.features.length - 3} more
            </Badge>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button 
            className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground group/btn" 
            asChild
            onClick={(e) => {
              e.stopPropagation();
              handleShopNowClick();
            }}
          >
            <a href={item.buyUrl} target="_blank" rel="noopener noreferrer">
              Shop Now
              <ExternalLink className="h-4 w-4 ml-2 group-hover/btn:translate-x-0.5 transition-transform" />
            </a>
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleAddToCartClick();
            }}
            className={isInCart ? "bg-green-50 border-green-200 text-green-700" : ""}
          >
            <ShoppingCart className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
