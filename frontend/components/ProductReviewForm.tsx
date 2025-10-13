'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Star, Send, Loader2 } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

interface ProductReviewFormProps {
  productId: string;
  onReviewSubmitted?: () => void;
  className?: string;
}

export default function ProductReviewForm({ 
  productId, 
  onReviewSubmitted,
  className 
}: ProductReviewFormProps) {
  const [rating, setRating] = useState<number>(0);
  const [reviewText, setReviewText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (rating === 0) {
      toast({
        title: "Rating Required",
        description: "Please select a rating before submitting your review.",
        variant: "destructive",
      });
      return;
    }

    if (reviewText.trim().length < 10) {
      toast({
        title: "Review Too Short",
        description: "Please write at least 10 characters for your review.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:3000/api/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: productId,
          user_id: 'current-user', // In a real app, get from auth context
          rating: rating,
          text: reviewText.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit review');
      }

      const data = await response.json();
      
      toast({
        title: "Review Submitted!",
        description: "Your review has been submitted and AI rating calculation has been triggered.",
      });

      // Reset form
      setRating(0);
      setReviewText('');
      
      // Notify parent component
      if (onReviewSubmitted) {
        onReviewSubmitted();
      }

    } catch (error) {
      console.error('Error submitting review:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your review. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Star className="h-5 w-5 text-yellow-500" />
          Write a Review
        </CardTitle>
        <p className="text-sm text-gray-600">
          Share your experience and help others make sustainable choices
        </p>
      </CardHeader>
      
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Rating Selection */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Rating *</Label>
            <RadioGroup
              value={rating.toString()}
              onValueChange={(value) => setRating(parseInt(value))}
              className="flex gap-4"
            >
              {[1, 2, 3, 4, 5].map((star) => (
                <div key={star} className="flex items-center space-x-2">
                  <RadioGroupItem value={star.toString()} id={`rating-${star}`} />
                  <Label htmlFor={`rating-${star}`} className="flex items-center gap-1 cursor-pointer">
                    <span className="text-sm">{star}</span>
                    <Star className="h-4 w-4 text-yellow-500" />
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </div>

          {/* Review Text */}
          <div className="space-y-3">
            <Label htmlFor="review-text" className="text-sm font-medium">
              Review Text *
            </Label>
            <Textarea
              id="review-text"
              placeholder="Tell us about your experience with this product. Mention any sustainability features you noticed, quality, fit, etc."
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              className="min-h-[120px]"
              maxLength={1000}
            />
            <div className="text-xs text-gray-500 text-right">
              {reviewText.length}/1000 characters
            </div>
          </div>

          {/* Submit Button */}
          <Button 
            type="submit" 
            className="w-full" 
            disabled={isSubmitting || rating === 0 || reviewText.trim().length < 10}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Submitting Review...
              </>
            ) : (
              <>
                <Send className="h-4 w-4 mr-2" />
                Submit Review
              </>
            )}
          </Button>

          <p className="text-xs text-gray-500 text-center">
            Your review will trigger an AI analysis to update the product's sustainability rating
          </p>
        </form>
      </CardContent>
    </Card>
  );
}
