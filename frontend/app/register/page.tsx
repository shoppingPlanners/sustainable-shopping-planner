"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Navigation } from "@/components/navigation"
import { registerAccount, login as loginAPI } from "@/lib/auth"
import { useAuth } from "@/lib/auth-context"
import { useState } from "react"
import { PricingTiers } from "@/components/pricing-tiers"

export default function RegisterPage() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedTier, setSelectedTier] = useState("Free")
  const [step, setStep] = useState<'pricing' | 'register'>('pricing')
  const { login } = useAuth()
  
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = e.currentTarget
    const name = (form.querySelector('#name') as HTMLInputElement)?.value
    const email = (form.querySelector('#email') as HTMLInputElement)?.value
    const password = (form.querySelector('#password') as HTMLInputElement)?.value
    const confirmPassword = (form.querySelector('#confirm-password') as HTMLInputElement)?.value
    
    // Validate password confirmation
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }
    
    // Basic validation
    if (!name || !email || !password) {
      setError('Please fill in all fields')
      return
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }
    
    setLoading(true)
    setError(null)
    try {
      const registerResponse = await registerAccount({ email, password, name })
      // Auto-login after registration
      const loginResponse = await loginAPI(email, password)
      login(loginResponse.access_token, registerResponse.user.id, email, name)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
      setLoading(false)
    }
  }
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Navigation */}
      <Navigation />

      {/* Content */}
      <div className="flex-1 px-4 sm:px-6 lg:px-8 py-12">
        {step === 'pricing' ? (
          // Step 1: Pricing Tiers
          <div className="max-w-7xl mx-auto">
            <PricingTiers 
              onSelectTier={(tier) => {
                setSelectedTier(tier)
                setStep('register')
              }}
              selectedTier={selectedTier}
            />
          </div>
        ) : (
          // Step 2: Register Form
          <div className="flex items-center justify-center">
            <div className="w-full max-w-md">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-foreground mb-2">Join StyleSustain</h1>
                <p className="text-muted-foreground">
                  Create your account for the <span className="font-semibold text-primary">{selectedTier}</span> plan
                </p>
                <Button 
                  variant="ghost" 
                  onClick={() => setStep('pricing')}
                  className="mt-2 text-sm"
                >
                  ← Change plan
                </Button>
              </div>

              <Card className="border-border shadow-lg">
                <CardHeader>
                  <CardTitle className="text-xl text-foreground">Create Account</CardTitle>
                  <CardDescription className="text-muted-foreground">Get personalized recommendations</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {error ? <p className="text-sm text-red-500">{error}</p> : null}
                  <form className="space-y-4" onSubmit={onSubmit}>
                  <div className="space-y-2">
                    <Label htmlFor="name" className="text-foreground">
                      Full Name
                    </Label>
                    <Input id="name" type="text" placeholder="Jane Doe" />
                  </div>

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

                  <div className="space-y-2">
                    <Label htmlFor="confirm-password" className="text-foreground">
                      Confirm Password
                    </Label>
                    <Input id="confirm-password" type="password" placeholder="••••••••" />
                  </div>

                  <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" size="lg" type="submit" disabled={loading}>
                    {loading ? 'Creating...' : `Create ${selectedTier} Account`}
                  </Button>

                  <div className="text-center text-sm text-muted-foreground">
                    Already have an account?{" "}
                    <Link href="/login" className="text-primary hover:underline font-medium">
                      Sign in
                    </Link>
                  </div>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
