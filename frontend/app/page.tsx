'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Home() {
  const [stats, setStats] = useState({
    brands: 0,
    ratings: 0,
    users: 0
  })

  useEffect(() => {
    // Fetch stats from all agents
    Promise.all([
      fetch('http://localhost:5001/brands').then(r => r.json()),
      fetch('http://localhost:5002/ratings').then(r => r.json()),
      fetch('http://localhost:5003/users').then(r => r.json()),
    ]).then(([brands, ratings, users]) => {
      setStats({
        brands: brands.count || 0,
        ratings: ratings.count || 0,
        users: users.count || 0
      })
    }).catch(console.error)
  }, [])

  return (
    <main className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4 text-gray-800">
          Shop Sustainably, Live Consciously
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered recommendations for sustainable shopping
        </p>
        <div className="flex justify-center space-x-4">
          <Link href="/suggestions" className="btn-primary">
            Get Personalized Suggestions
          </Link>
          <Link href="/trending" className="btn-secondary">
            See Trending Products
          </Link>
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div className="card text-center">
          <div className="text-4xl mb-2">🏢</div>
          <div className="text-3xl font-bold text-green-600">{stats.brands}</div>
          <div className="text-gray-600">Sustainable Brands</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-2">⭐</div>
          <div className="text-3xl font-bold text-green-600">{stats.ratings}</div>
          <div className="text-gray-600">Sustainability Ratings</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-2">👥</div>
          <div className="text-3xl font-bold text-green-600">{stats.users}</div>
          <div className="text-gray-600">Active Users</div>
        </div>
      </div>

      {/* Features Section */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card text-center">
            <div className="text-5xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-2">Discover Brands</h3>
            <p className="text-gray-600">
              We analyze thousands of brands for sustainability practices
            </p>
          </div>
          <div className="card text-center">
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Get Ratings</h3>
            <p className="text-gray-600">
              AI-powered sustainability scores from 0-100
            </p>
          </div>
          <div className="card text-center">
            <div className="text-5xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold mb-2">Personalized</h3>
            <p className="text-gray-600">
              Recommendations tailored to your preferences
            </p>
          </div>
          <div className="card text-center">
            <div className="text-5xl mb-4">🌍</div>
            <h3 className="text-xl font-semibold mb-2">Make Impact</h3>
            <p className="text-gray-600">
              Every purchase supports sustainable practices
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="card bg-gradient-to-r from-green-50 to-emerald-50 text-center">
        <h2 className="text-3xl font-bold mb-4 text-gray-800">
          Ready to Shop Sustainably?
        </h2>
        <p className="text-gray-600 mb-6">
          Get personalized recommendations based on your preferences
        </p>
        <Link href="/suggestions" className="btn-primary inline-block">
          Get Started
        </Link>
      </div>
    </main>
  )
}

