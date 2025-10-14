'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Star, Heart, ShoppingCart, Leaf, Shield } from 'lucide-react';
import AIRatingDisplay from '@/components/AIRatingDisplay';
import ProductReviewForm from '@/components/ProductReviewForm';

interface Product {
  id: string;
  name: string;
  brand: string;
  category: string;
  price: number;
  description: string;
  sustainability_features: string[];
  image: string;
}

interface Review {
  id: string;
  product_id: string;
  user_id: string;
  rating: number;
  text: string;
  date: string;
}

export default function ProductPage() {
  const params = useParams();
  const productId = params.id as string;
  
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    fetchProduct();
    fetchReviews();
  }, [productId]);

  const fetchProduct = async () => {
    try {
      const response = await fetch(`http://localhost:3000/api/products/${productId}`);
      if (!response.ok) throw new Error('Failed to fetch product');
      
      const data = await response.json();
      setProduct(data.data);
    } catch (err) {
      setError('Failed to load product');
      console.error('Error fetching product:', err);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await fetch(`http://localhost:3000/api/reviews?product_id=${productId}`);
      if (!response.ok) throw new Error('Failed to fetch reviews');
      
      const data = await response.json();
      setReviews(data.data);
    } catch (err) {
      console.error('Error fetching reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSubmitted = () => {
    // Refresh reviews and AI rating
    fetchReviews();
    setRefreshKey(prev => prev + 1);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getAverageRating = () => {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + review.rating, 0);
    return sum / reviews.length;
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2">Loading product...</span>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <p className="text-gray-600 mb-6">{error || 'The product you\'re looking for doesn\'t exist.'}</p>
          <Button onClick={() => window.history.back()}>
            Go Back
          </Button>
        </div>
      </div>
    );
  }

  const averageRating = getAverageRating();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Product Image */}
        <div className="space-y-4">
          <div className="aspect-square relative overflow-hidden rounded-lg border">
            <Image
              src={product.image}
              alt={product.name}
              fill
              className="object-cover"
            />
          </div>
        </div>

        {/* Product Details */}
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
            <p className="text-lg text-gray-600 mb-4">by {product.brand}</p>
            
            <div className="flex items-center gap-4 mb-4">
              <div className="flex items-center gap-2">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-5 w-5 ${
                        i < Math.floor(averageRating)
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600">
                  {averageRating > 0 ? averageRating.toFixed(1) : 'No ratings yet'}
                </span>
                <span className="text-sm text-gray-500">
                  ({reviews.length} review{reviews.length !== 1 ? 's' : ''})
                </span>
              </div>
            </div>

            <div className="text-3xl font-bold text-gray-900 mb-6">
              {formatPrice(product.price)}
            </div>
          </div>

          {/* Sustainability Features */}
          {product.sustainability_features.length > 0 && (
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Leaf className="h-5 w-5 text-green-600" />
                Sustainability Features
              </h3>
              <div className="flex flex-wrap gap-2">
                {product.sustainability_features.map((feature, index) => (
                  <Badge key={index} variant="outline" className="text-green-700 border-green-200">
                    {feature.replace('-', ' ')}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Description */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">Description</h3>
            <p className="text-gray-700 leading-relaxed">{product.description}</p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <Button size="lg" className="flex-1">
              <ShoppingCart className="h-5 w-5 mr-2" />
              Add to Cart
            </Button>
            <Button size="lg" variant="outline">
              <Heart className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>

      <Separator className="my-8" />

      {/* AI Rating Display */}
      <div className="mb-8">
        <AIRatingDisplay 
          key={refreshKey}
          productId={productId} 
          className="max-w-2xl mx-auto"
        />
      </div>

      <Separator className="my-8" />

      {/* Reviews Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Review Form */}
        <div>
          <ProductReviewForm
            productId={productId}
            onReviewSubmitted={handleReviewSubmitted}
          />
        </div>

        {/* Reviews List */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900">Customer Reviews</h2>
          
          {reviews.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Star className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No reviews yet. Be the first to review this product!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <Card key={review.id}>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div className="flex">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`h-4 w-4 ${
                                i < review.rating
                                  ? 'text-yellow-400 fill-current'
                                  : 'text-gray-300'
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm font-medium">User {review.user_id}</span>
                      </div>
                      <span className="text-sm text-gray-500">
                        {formatDate(review.date)}
                      </span>
                    </div>
                    <p className="text-gray-700">{review.text}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
