import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Sustainable Shopping Planner',
  description: 'AI-powered sustainable shopping recommendations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-green-600 text-white shadow-lg">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">🌱</span>
                <h1 className="text-xl font-bold">Sustainable Shopping</h1>
              </div>
              <div className="flex space-x-6">
                <a href="/" className="hover:text-green-200 transition">Home</a>
                <a href="/brands" className="hover:text-green-200 transition">Brands</a>
                <a href="/suggestions" className="hover:text-green-200 transition">For You</a>
                <a href="/trending" className="hover:text-green-200 transition">Trending</a>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  )
}

