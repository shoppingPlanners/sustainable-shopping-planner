'use client'

import { useEffect, useState } from 'react'

interface TrendingProduct {
  product_id: string
  product_name: string
  brand_name: string
  sustainability_score: number
  price: string
  category: string
  url: string
}

export default function TrendingPage() {
  const [products, setProducts] = useState<TrendingProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [minScore, setMinScore] = useState(70)

  const fetchTrending = async () => {
    setLoading(true)
    try {
      const response = await fetch(
        `http://localhost:5004/trending?limit=20&min_sustainability_score=${minScore}`
      )
      const data = await response.json()
      
      if (data.status === 'success') {
        setProducts(data.trending_products)
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTrending()
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
    return 'C'
  }

  return (
    <main className="container mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4 text-gray-800">
          🔥 Trending Sustainable Products
        </h1>
        <p className="text-gray-600 mb-4">
          Popular sustainable products with high environmental and social ratings
        </p>

        <div className="flex items-center space-x-4">
          <label className="text-gray-700">
            Minimum Sustainability Score:
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            className="w-48"
          />
          <span className="font-semibold text-green-600">{minScore}</span>
          <button
            onClick={fetchTrending}
            className="btn-primary"
          >
            Update
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">Loading trending products...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-xl font-semibold mb-2">No trending products found</h3>
          <p className="text-gray-600">
            Try lowering the minimum sustainability score
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product, index) => (
            <div key={index} className="card hover:scale-[1.02] transition-transform">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-800 mb-1">
                    {product.product_name}
                  </h3>
                  <p className="text-sm text-gray-600">{product.brand_name}</p>
                </div>
                <div className="text-center ml-2">
                  <div className={`badge ${getScoreBadge(product.sustainability_score)}`}>
                    {getGrade(product.sustainability_score)}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {product.sustainability_score}/100
                  </div>
                </div>
              </div>

              <div className="mb-3">
                <span className="inline-block bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                  {product.category}
                </span>
              </div>

              <div className="text-2xl font-bold text-green-600 mb-3">
                {product.price}
              </div>

              <div className="pt-3 border-t">
                <div className="text-sm text-gray-600">
                  <div className="flex items-center mb-1">
                    <span className="text-green-500 mr-2">🌱</span>
                    <span>Highly sustainable choice</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-blue-500 mr-2">🔥</span>
                    <span>Popular among conscious shoppers</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-12 card bg-green-50 text-center">
        <h3 className="text-xl font-semibold mb-2">💡 Did you know?</h3>
        <p className="text-gray-700">
          These products are trending because they combine excellent sustainability
          scores with positive user engagement. Every purchase makes a difference!
        </p>
      </div>
    </main>
  )
}

