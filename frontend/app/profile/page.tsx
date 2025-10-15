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

export default function ProfilePage() {
  const { user } = useAuth()
  const router = useRouter()
  const [isEditing, setIsEditing] = useState(false)
  const [userTier, setUserTier] = useState("Free")

  useEffect(() => {
    if (!user) {
      router.push('/login')
    }
  }, [user, router])

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
                <CardTitle>Shopping Preferences</CardTitle>
                <CardDescription>Customize your recommendations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Favorite Categories</Label>
                  <div className="flex flex-wrap gap-2">
                    {["Tops & Shirts", "Dresses", "Jackets & Outerwear", "Bottoms & Jeans"].map((cat) => (
                      <Badge key={cat} variant="secondary" className="cursor-pointer hover:bg-primary hover:text-primary-foreground">
                        {cat}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Budget Range</Label>
                  <div className="flex gap-2">
                    <Input placeholder="Min" type="number" defaultValue="50" className="w-24" />
                    <span className="self-center">—</span>
                    <Input placeholder="Max" type="number" defaultValue="200" className="w-24" />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Sustainability Priorities</Label>
                  <div className="flex flex-wrap gap-2">
                    {["Organic Materials", "Fair Trade", "Recycled", "Vegan"].map((priority) => (
                      <Badge key={priority} variant="outline" className="cursor-pointer hover:bg-primary hover:text-primary-foreground">
                        {priority}
                      </Badge>
                    ))}
                  </div>
                </div>

                <Button>Save Preferences</Button>
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

