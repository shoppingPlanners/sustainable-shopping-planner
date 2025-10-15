"use client";

import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Analytics } from '@vercel/analytics/next'
import { ConsentBanner } from '@/components/consent-banner'
import { Footer } from '@/components/footer'
import { AuthProvider } from '@/lib/auth-context'
import { tracker } from '@/lib/tracking'
import { useEffect } from 'react'
import './globals.css'

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  useEffect(() => {
    tracker.init();
  }, []);

  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <AuthProvider>
          <div className="flex flex-col min-h-screen">
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
          <ConsentBanner />
          <Analytics />
        </AuthProvider>
      </body>
    </html>
  )
}
