import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Analytics } from '@vercel/analytics/next'
import { ConsentBanner } from '@/components/consent-banner'
import { tracker } from '@/lib/tracking'
import './globals.css'

export const metadata: Metadata = {
  title: 'Sustainable Shopping Planner App',
  description: 'A sustainable shopping planner app',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  if (typeof window !== 'undefined') {
    tracker.init()
  }
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        {children}
        <ConsentBanner />
        <Analytics />
      </body>
    </html>
  )
}
