'use client'

import { useEffect, useState } from 'react'

interface Product {
  product_id: string
  product_name: string
  brand_name: string
  sustainability_score: number
  price: string
  recommendation_score: number
  reasons: string[]
  category: string
  url: string
}

export default function SuggestionsPage() {
  const [userId, setUserId] = useState('demo_user')
  const [suggestions, setSuggestions] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchSuggestions = async () => {
    setLoading(true)
    setError('')
    
    try {
      const response = await fetch(`http://localhost:5004/suggestions/${userId}?limit=10`)
      const data = await response.json()
      
      if (data.status === 'success') {
        setSuggestions(data.suggestions)
      } else {
        setError('Failed to fetch suggestions')
      }
    } catch (err) {
      setError('Could not connect to suggestion service')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = async (productId: string, feedbackType: string) => {
    try {
      await fetch('http://localhost:5004/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          product_id: productId,
          feedback_type: feedbackType
        })
      })
      
      // Track the event
      await fetch('http://localhost:5003/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          event_type: feedbackType,
          product_id: productId,
          timestamp: Date.now() / 1000
        })
      })
    } catch (err) {
      console.error('Failed to submit feedback:', err)
    }
  }

  useEffect(() => {
    fetchSuggestions()
  }, [])

  const getScoreBadge = (score: number) => {
    if (score >= 80) return 'badge-green'
    if (score >= 60) return 'badge-yellow'
    return 'badge-red'
  }

  const getGrade = (score: number) => {
    if (score >= 90) return 'A+'
    if (score >= 85) return 'A'
    if (score >= 80) return 'A-'
    if (score >= 75) return 'B+'
    if (score >= 70) return 'B'
    if (score >= 65) return 'B-'
    if (score >= 60) return 'C+'
    return 'C'
  }

  return (
    <main className="container mx-auto px-4 py-12">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 text-gray-800">
            Personalized Suggestions
          </h1>
          <p className="text-gray-600 mb-4">
            Products recommended just for you based on your preferences and sustainability values
          </p>
          
          <div className="flex items-center space-x-4">
            <input
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter User ID"
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
            <button
              onClick={fetchSuggestions}
              disabled={loading}
              className="btn-primary disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Get Suggestions'}
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {suggestions.length === 0 && !loading && !error && (
          <div className="card text-center py-12">
            <div className="text-6xl mb-4">🌱</div>
            <h3 className="text-xl font-semibold mb-2">No suggestions yet</h3>
            <p className="text-gray-600 mb-4">
              Start browsing to get personalized recommendations
            </p>
            <button onClick={fetchSuggestions} className="btn-primary">
              Generate Suggestions
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {suggestions.map((product) => (
            <div key={product.product_id} className="card hover:scale-[1.02] transition-transform">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-1">
                    {product.product_name}
                  </h3>
                  <p className="text-gray-600">{product.brand_name}</p>
                </div>
                <div className="text-right">
                  <div className={`badge ${getScoreBadge(product.sustainability_score)}`}>
                    {getGrade(product.sustainability_score)}
                  </div>
                  <div className="text-sm text-gray-500 mt-1">
                    {product.sustainability_score}/100
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <div className="inline-block bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                  {product.category}
                </div>
                <div className="text-2xl font-bold text-green-600 mt-2">
                  {product.price}
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-semibold text-gray-700 mb-2">Why we recommend this:</h4>
                <ul className="space-y-1">
                  {product.reasons.map((reason, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      {reason}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex space-x-2 pt-4 border-t">
                <button
                  onClick={() => handleFeedback(product.product_id, 'liked')}
                  className="flex-1 py-2 px-4 bg-green-50 hover:bg-green-100 text-green-700 rounded-lg transition"
                >
                  👍 Like
                </button>
                <button
                  onClick={() => handleFeedback(product.product_id, 'clicked')}
                  className="flex-1 py-2 px-4 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition"
                >
                  🔗 View
                </button>
                <button
                  onClick={() => handleFeedback(product.product_id, 'dismissed')}
                  className="flex-1 py-2 px-4 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded-lg transition"
                >
                  ✕ Pass
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}

