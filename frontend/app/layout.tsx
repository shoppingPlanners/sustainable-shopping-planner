"use client";

import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Analytics } from '@vercel/analytics/next'
import { ConsentBanner } from '@/components/consent-banner'
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
          {children}
          <ConsentBanner />
          <Analytics />
        </AuthProvider>
      </body>
    </html>
  )
}
