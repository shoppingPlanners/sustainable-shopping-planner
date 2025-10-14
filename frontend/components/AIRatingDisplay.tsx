'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { Star, Leaf, TrendingUp, Shield, Clock } from 'lucide-react';

interface AIRating {
  id: string;
  product_id: string;
  ai_rating: number;
  sentiment_score: number;
  sustainability_score: number;
  confidence: number;
  breakdown: {
    sentiment_analysis: {
      average_sentiment: number;
      total_reviews: number;
      positive_reviews: number;
      negative_reviews: number;
    };
    sustainability_analysis: {
      product_sustainability: number;
      sustainability_mentions: string[];
      mention_count: number;
    };
  };
  timestamp: string;
}

interface AIRatingDisplayProps {
  productId: string;
  className?: string;
}

export default function AIRatingDisplay({ productId, className }: AIRatingDisplayProps) {
  const [rating, setRating] = useState<AIRating | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAIRating();
  }, [productId]);

  const fetchAIRating = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3000/api/ratings/product/${productId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('No AI rating available for this product yet');
          return;
        }
        throw new Error('Failed to fetch AI rating');
      }
      
      const data = await response.json();
      setRating(data.data);
      setError(null);
    } catch (err) {
      setError('Failed to load AI rating');
      console.error('Error fetching AI rating:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRatingColor = (rating: number) => {
    if (rating >= 4.5) return 'text-green-600';
    if (rating >= 3.5) return 'text-yellow-600';
    if (rating >= 2.5) return 'text-orange-600';
    return 'text-red-600';
  };

  const getRatingBadgeVariant = (rating: number) => {
    if (rating >= 4.5) return 'default';
    if (rating >= 3.5) return 'secondary';
    return 'destructive';
  };

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-blue-600" />
            AI Verified Rating
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">Calculating AI rating...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-gray-400" />
            AI Verified Rating
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <p className="text-gray-500 mb-2">{error}</p>
            <button 
              onClick={fetchAIRating}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              Try again
            </button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!rating) return null;

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Shield className="h-5 w-5 text-blue-600" />
          AI Verified Rating
          <Badge variant={getRatingBadgeVariant(rating.ai_rating)}>
            {rating.ai_rating}/5.0
          </Badge>
        </CardTitle>
        <p className="text-sm text-gray-600">
          Last updated: {formatDate(rating.timestamp)}
        </p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Overall Rating */}
        <div className="text-center">
          <div className={`text-4xl font-bold ${getRatingColor(rating.ai_rating)}`}>
            {rating.ai_rating}
          </div>
          <div className="flex justify-center mt-2">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`h-5 w-5 ${
                  i < Math.floor(rating.ai_rating)
                    ? 'text-yellow-400 fill-current'
                    : 'text-gray-300'
                }`}
              />
            ))}
          </div>
          <p className="text-sm text-gray-600 mt-1">
            Confidence: {Math.round(rating.confidence * 100)}%
          </p>
        </div>

        <Separator />

        {/* Breakdown */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900">Rating Breakdown</h4>
          
          {/* Sentiment Analysis */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium">Sentiment Score</span>
              </div>
              <span className="text-sm font-semibold">
                {rating.sentiment_score > 0 ? '+' : ''}{rating.sentiment_score.toFixed(2)}
              </span>
            </div>
            <Progress 
              value={((rating.sentiment_score + 1) / 2) * 100} 
              className="h-2"
            />
            <div className="text-xs text-gray-600">
              Based on {rating.breakdown.sentiment_analysis.total_reviews} reviews
              ({rating.breakdown.sentiment_analysis.positive_reviews} positive, 
              {rating.breakdown.sentiment_analysis.negative_reviews} negative)
            </div>
          </div>

          {/* Sustainability Analysis */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Leaf className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium">Sustainability Score</span>
              </div>
              <span className="text-sm font-semibold">
                {Math.round(rating.sustainability_score * 100)}%
              </span>
            </div>
            <Progress 
              value={rating.sustainability_score * 100} 
              className="h-2"
            />
            <div className="text-xs text-gray-600">
              {rating.breakdown.sustainability_analysis.mention_count} sustainability mentions
            </div>
          </div>
        </div>

        {/* Sustainability Features */}
        {rating.breakdown.sustainability_analysis.sustainability_mentions.length > 0 && (
          <>
            <Separator />
            <div className="space-y-2">
              <h4 className="font-semibold text-gray-900">Sustainability Features</h4>
              <div className="flex flex-wrap gap-1">
                {rating.breakdown.sustainability_analysis.sustainability_mentions.map((feature, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    {feature.replace('-', ' ')}
                  </Badge>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Last Updated */}
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <Clock className="h-3 w-3" />
          <span>AI analysis completed {formatDate(rating.timestamp)}</span>
        </div>
      </CardContent>
    </Card>
  );
}
