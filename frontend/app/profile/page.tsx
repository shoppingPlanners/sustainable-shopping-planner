"use client"

import { useState, useEffect } from "react"
import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { useAuth } from "@/lib/auth-context"
import { User, Crown, Settings, Bell, Shield, CreditCard, Star } from "lucide-react"
import { useRouter } from "next/navigation"
import { BACKEND_URL } from "@/lib/config"

export default function ProfilePage() {
  const { user } = useAuth()
  const router = useRouter()
  const [isEditing, setIsEditing] = useState(false)
  const [userTier, setUserTier] = useState("Free")
  const [prefsLoading, setPrefsLoading] = useState(true)
  const [prefsAnalysis, setPrefsAnalysis] = useState<{
    total_submissions?: number,
    top_category?: { value: string, count: number } | null,
    top_budget?: { value: string, count: number } | null,
    top_style?: { value: string, count: number } | null,
    top_sustainability_priorities?: { value: string, count: number } | null,
    top_size?: { value: string, count: number } | null,
    last_preference?: Record<string, any>
  } | null>(null)

  useEffect(() => {
    if (!user) {
      router.push('/login')
    }
  }, [user, router])

  // Load overall preferences analysis (from user_preferences)
  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setPrefsLoading(true)
        const res = await fetch(`${BACKEND_URL}/api/preferences/analysis`)
        if (res.ok) {
          const data = await res.json()
          setPrefsAnalysis(data?.analysis || null)
        } else {
          setPrefsAnalysis(null)
        }
      } catch {
        setPrefsAnalysis(null)
      } finally {
        setPrefsLoading(false)
      }
    }
    fetchAnalysis()
  }, [])

  if (!user) return null

  const userInitials = user.name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'U'

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Profile Header */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
              <Avatar className="h-24 w-24">
                <AvatarFallback className="text-2xl bg-primary text-primary-foreground">
                  {userInitials}
                </AvatarFallback>
              </Avatar>

              <div className="flex-1 text-center md:text-left">
                <div className="flex flex-col md:flex-row md:items-center gap-3 mb-2">
                  <h1 className="text-3xl font-bold">{user.name}</h1>
                  <Badge variant="secondary" className="w-fit mx-auto md:mx-0">
                    <Crown className="h-3 w-3 mr-1" />
                    {userTier} Member
                  </Badge>
                </div>
                <p className="text-muted-foreground">{user.email}</p>
                <p className="text-sm text-muted-foreground mt-2">
                  Member since {new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                </p>
              </div>

              <Button variant="outline" onClick={() => setIsEditing(!isEditing)}>
                <Settings className="h-4 w-4 mr-2" />
                {isEditing ? 'Cancel' : 'Edit Profile'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs defaultValue="account" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="account">Account</TabsTrigger>
            <TabsTrigger value="plan">Plan & Billing</TabsTrigger>
            <TabsTrigger value="preferences">Preferences</TabsTrigger>
            <TabsTrigger value="security">Security</TabsTrigger>
          </TabsList>

          {/* Account Tab */}
          <TabsContent value="account" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>Update your account details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input id="name" defaultValue={user.name} disabled={!isEditing} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" defaultValue={user.email} disabled={!isEditing} />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea 
                    id="bio" 
                    placeholder="Tell us a bit about your sustainable fashion journey..." 
                    disabled={!isEditing}
                    rows={4}
                  />
                </div>

                {isEditing && (
                  <div className="flex gap-2">
                    <Button>Save Changes</Button>
                    <Button variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Sustainability Stats</CardTitle>
                <CardDescription>Your impact at a glance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-3xl font-bold text-primary mb-1">24</div>
                    <div className="text-sm text-muted-foreground">Products Viewed</div>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-3xl font-bold text-primary mb-1">8</div>
                    <div className="text-sm text-muted-foreground">Favorites</div>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-3xl font-bold text-primary mb-1">85</div>
                    <div className="text-sm text-muted-foreground">Eco Score</div>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-3xl font-bold text-primary mb-1">12</div>
                    <div className="text-sm text-muted-foreground">Days Active</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Plan & Billing Tab */}
          <TabsContent value="plan" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Current Plan</CardTitle>
                <CardDescription>Manage your subscription</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-start justify-between p-4 border rounded-lg">
                  <div className="flex items-start gap-4">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <Crown className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">{userTier} Plan</h3>
                      <p className="text-sm text-muted-foreground mt-1">
                        {userTier === "Free" 
                          ? "Access to basic features and 10 saved products" 
                          : "Full access to all premium features"
                        }
                      </p>
                      <Badge variant="secondary" className="mt-2">
                        {userTier === "Free" ? "$0/month" : "$9.99/month"}
                      </Badge>
                    </div>
                  </div>
                  <Button>Upgrade Plan</Button>
                </div>

                <Separator />

                <div>
                  <h4 className="font-semibold mb-3">Plan Features</h4>
                  <div className="space-y-2">
                    {[
                      { feature: "Browse 300+ sustainable products", included: true },
                      { feature: "Basic sustainability scores", included: true },
                      { feature: "Save up to 10 favorites", included: userTier === "Free" },
                      { feature: "Unlimited favorites", included: userTier !== "Free" },
                      { feature: "Advanced analytics", included: userTier !== "Free" },
                      { feature: "Price drop alerts", included: userTier !== "Free" },
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <Star className={`h-4 w-4 ${item.included ? 'text-primary fill-primary' : 'text-muted-foreground'}`} />
                        <span className={item.included ? '' : 'text-muted-foreground'}>
                          {item.feature}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {userTier !== "Free" && (
                  <>
                    <Separator />
                    <div>
                      <h4 className="font-semibold mb-3">Billing Information</h4>
                      <div className="flex items-center gap-3 p-3 border rounded-lg">
                        <CreditCard className="h-5 w-5 text-muted-foreground" />
                        <div className="flex-1">
                          <p className="text-sm">•••• •••• •••• 4242</p>
                          <p className="text-xs text-muted-foreground">Expires 12/25</p>
                        </div>
                        <Button variant="outline" size="sm">Update</Button>
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Preferences Tab */}
          <TabsContent value="preferences" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Preferences Overview</CardTitle>
                <CardDescription>Overall analysis from saved user preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {prefsLoading ? (
                  <p className="text-sm text-muted-foreground">Loading…</p>
                ) : prefsAnalysis ? (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Total Submissions</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.total_submissions || 0}</p>
                      </div>
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Top Category</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.top_category?.value || '—'}</p>
                      </div>
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Top Budget</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.top_budget?.value || '—'}</p>
                      </div>
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Top Style</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.top_style?.value || '—'}</p>
                      </div>
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Top Sustainability Priority</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.top_sustainability_priorities?.value || '—'}</p>
                      </div>
                      <div className="p-3 border rounded-lg">
                        <p className="text-xs text-muted-foreground">Top Size</p>
                        <p className="text-lg font-semibold">{prefsAnalysis.top_size?.value || '—'}</p>
                      </div>
                    </div>

                    <Separator />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-xs text-muted-foreground">Last Category</p>
                        <p className="font-medium">{prefsAnalysis.last_preference?.category || '—'}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Last Budget</p>
                        <p className="font-medium">{prefsAnalysis.last_preference?.budget || '—'}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Last Style</p>
                        <p className="font-medium">{prefsAnalysis.last_preference?.style || '—'}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Last Sustainability Priorities</p>
                        <p className="font-medium">{prefsAnalysis.last_preference?.sustainability_priorities || '—'}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Last Size</p>
                        <p className="font-medium">{prefsAnalysis.last_preference?.size || '—'}</p>
                      </div>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No preferences found.</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Shopping Preferences</CardTitle>
                <CardDescription>Your latest saved preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {prefsLoading ? (
                  <p className="text-sm text-muted-foreground">Loading…</p>
                ) : prefsAnalysis ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-1">
                      <Label>Category</Label>
                      <Input value={prefsAnalysis.last_preference?.category || ''} disabled />
                    </div>
                    <div className="space-y-1">
                      <Label>Budget</Label>
                      <Input value={prefsAnalysis.last_preference?.budget || ''} disabled />
                    </div>
                    <div className="space-y-1">
                      <Label>Style</Label>
                      <Input value={prefsAnalysis.last_preference?.style || ''} disabled />
                    </div>
                    <div className="space-y-1">
                      <Label>Sustainability Priorities</Label>
                      <Input value={prefsAnalysis.last_preference?.sustainability_priorities || ''} disabled />
                    </div>
                    <div className="space-y-1">
                      <Label>Size</Label>
                      <Input value={prefsAnalysis.last_preference?.size || ''} disabled />
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No saved preferences yet.</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>Manage how we communicate with you</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  { label: "Email notifications", desc: "Receive updates about new products and deals" },
                  { label: "Price drop alerts", desc: "Get notified when items on your wishlist go on sale" },
                  { label: "Sustainability tips", desc: "Weekly tips for sustainable shopping" },
                  { label: "New brand announcements", desc: "Be the first to know about new sustainable brands" },
                ].map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{item.label}</p>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Bell className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Tab */}
          <TabsContent value="security" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Security Settings</CardTitle>
                <CardDescription>Keep your account secure</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="current-password">Current Password</Label>
                  <Input id="current-password" type="password" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="new-password">New Password</Label>
                  <Input id="new-password" type="password" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirm-password">Confirm New Password</Label>
                  <Input id="confirm-password" type="password" />
                </div>

                <Button>Update Password</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Account Actions</CardTitle>
                <CardDescription>Manage your account status</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Shield className="h-4 w-4 mr-2" />
                  Download My Data
                </Button>
                <Button variant="destructive" className="w-full justify-start">
                  Delete Account
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

