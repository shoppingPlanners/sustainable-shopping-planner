"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Navigation } from "@/components/navigation"
import { login as loginAPI } from "@/lib/auth"
import { useAuth } from "@/lib/auth-context"
import { useState } from "react"

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuth()
  
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = e.currentTarget as HTMLFormElement
    const email = (form.querySelector('#email') as HTMLInputElement)?.value
    const password = (form.querySelector('#password') as HTMLInputElement)?.value
    
    // Basic validation
    if (!email || !password) {
      setError('Please fill in all fields')
      return
    }
    
    setLoading(true)
    setError(null)
    try {
      const response = await loginAPI(email, password)
      // Extract user info from token
      const payload = JSON.parse(atob(response.access_token.split('.')[1]))
      const userId = payload.sub
      const userName = payload.name || email.split('@')[0]
      
      // Use AuthContext login to update global state
      login(response.access_token, userId, email, userName)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid credentials')
      setLoading(false)
    }
  }
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Navigation */}
      <Navigation />

      {/* Login Form */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Welcome Back</h1>
            <p className="text-muted-foreground">Continue your sustainable journey</p>
          </div>

          <Card className="border-border shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl text-foreground">Sign In</CardTitle>
              <CardDescription className="text-muted-foreground">Access your account</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {error ? <p className="text-sm text-red-500">{error}</p> : null}
              <form className="space-y-4" onSubmit={onSubmit}>
              <div className="space-y-2">
                <Label htmlFor="email" className="text-foreground">
                  Email
                </Label>
                <Input id="email" type="email" placeholder="you@example.com" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-foreground">
                  Password
                </Label>
                <Input id="password" type="password" placeholder="••••••••" />
              </div>

              <div className="flex items-center justify-between text-sm">
                <Link href="/forgot-password" className="text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>

              <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" size="lg" type="submit" disabled={loading}>
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>

              <div className="text-center text-sm text-muted-foreground">
                New here?{" "}
                <Link href="/register" className="text-primary hover:underline font-medium">
                  Create account
                </Link>
              </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
