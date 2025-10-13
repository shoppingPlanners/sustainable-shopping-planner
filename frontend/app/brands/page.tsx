'use client'

import { useEffect, useState } from 'react'

interface Brand {
  brand_name: string
  url: string
  product_count: number
  sustainability_commitments: string[]
  certifications: string[]
  scraped_at: string
}

interface Rating {
  brand_name: string
  overall_score: number
  environmental_score: number
  social_score: number
  economic_score: number
  grade: string
}

export default function BrandsPage() {
  const [brands, setBrands] = useState<Brand[]>([])
  const [ratings, setRatings] = useState<{ [key: string]: Rating }>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:5001/brands').then(r => r.json()),
      fetch('http://localhost:5002/ratings').then(r => r.json())
    ]).then(([brandsData, ratingsData]) => {
      setBrands(brandsData.brands || [])
      
      const ratingsMap: { [key: string]: Rating } = {}
      ;(ratingsData.ratings || []).forEach((rating: Rating) => {
        ratingsMap[rating.brand_name] = rating
      })
      setRatings(ratingsMap)
      setLoading(false)
    }).catch(err => {
      console.error(err)
      setLoading(false)
    })
  }, [])

  const getScoreBadge = (score: number) => {
    if (score >= 80) return 'badge-green'
    if (score >= 60) return 'badge-yellow'
    return 'badge-red'
  }

  if (loading) {
    return (
      <main className="container mx-auto px-4 py-12">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">Loading brands...</p>
        </div>
      </main>
    )
  }

  return (
    <main className="container mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4 text-gray-800">
          Sustainable Brands
        </h1>
        <p className="text-gray-600">
          Browse our collection of brands rated for sustainability
        </p>
      </div>

      {brands.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">🏢</div>
          <h3 className="text-xl font-semibold mb-2">No brands yet</h3>
          <p className="text-gray-600">
            Brands will appear here once they are scraped and rated
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {brands.map((brand, index) => {
            const rating = ratings[brand.brand_name]
            
            return (
              <div key={index} className="card">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800 mb-1">
                      {brand.brand_name}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {brand.product_count} products
                    </p>
                  </div>
                  {rating && (
                    <div className="text-center">
                      <div className={`badge ${getScoreBadge(rating.overall_score)}`}>
                        {rating.grade}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {Math.round(rating.overall_score)}/100
                      </div>
                    </div>
                  )}
                </div>

                {brand.certifications && brand.certifications.length > 0 && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">
                      Certifications:
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {brand.certifications.map((cert, i) => (
                        <span
                          key={i}
                          className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded"
                        >
                          {cert}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {brand.sustainability_commitments && brand.sustainability_commitments.length > 0 && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">
                      Commitments:
                    </h4>
                    <ul className="space-y-1">
                      {brand.sustainability_commitments.slice(0, 2).map((commitment, i) => (
                        <li key={i} className="text-xs text-gray-600 flex items-start">
                          <span className="text-green-500 mr-1">•</span>
                          {commitment.substring(0, 100)}...
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {rating && (
                  <div className="pt-3 border-t mt-3">
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div>
                        <div className="text-xs text-gray-500">Environmental</div>
                        <div className="font-semibold text-sm">
                          {Math.round(rating.environmental_score)}
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500">Social</div>
                        <div className="font-semibold text-sm">
                          {Math.round(rating.social_score)}
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500">Economic</div>
                        <div className="font-semibold text-sm">
                          {Math.round(rating.economic_score)}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </main>
  )
}

