import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Leaf, Recycle, Heart } from "lucide-react"
import { Navigation } from "@/components/navigation"
import { tracker } from "@/lib/tracking"

export default function HomePage() {
  if (typeof window !== 'undefined') {
    void tracker.sendEvent({ event_type: 'page_view', page: '/' })
  }
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <Navigation />

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="flex items-center gap-2 bg-accent/10 px-4 py-2 rounded-full">
              <Recycle className="h-5 w-5 text-accent" />
              <span className="text-sm font-medium text-accent">Conscious Fashion</span>
            </div>
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold text-foreground mb-6 text-balance">
            Elegant
            <span className="text-primary"> Sustainability</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 text-pretty max-w-2xl mx-auto">
            Discover premium sustainable fashion that aligns with your values and style.
          </p>
        </div>
      </section>

      {/* Requirements Input Form */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mx-auto">
          <Card className="border-border shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-foreground">Your Preferences</CardTitle>
              <CardDescription className="text-muted-foreground">Tell us what matters to you</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="clothing-type" className="text-foreground">
                    Category
                  </Label>
                  <Select>
                    <SelectTrigger id="clothing-type">
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tops">Tops</SelectItem>
                      <SelectItem value="bottoms">Bottoms</SelectItem>
                      <SelectItem value="dresses">Dresses</SelectItem>
                      <SelectItem value="outerwear">Outerwear</SelectItem>
                      <SelectItem value="activewear">Activewear</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="budget" className="text-foreground">
                    Budget
                  </Label>
                  <Select>
                    <SelectTrigger id="budget">
                      <SelectValue placeholder="Price range" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="under-50">Under $50</SelectItem>
                      <SelectItem value="50-100">$50 - $100</SelectItem>
                      <SelectItem value="100-200">$100 - $200</SelectItem>
                      <SelectItem value="200-plus">$200+</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="style" className="text-foreground">
                  Style
                </Label>
                <Select>
                  <SelectTrigger id="style">
                    <SelectValue placeholder="Your aesthetic" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="casual">Casual</SelectItem>
                    <SelectItem value="professional">Professional</SelectItem>
                    <SelectItem value="trendy">Contemporary</SelectItem>
                    <SelectItem value="minimalist">Minimalist</SelectItem>
                    <SelectItem value="bohemian">Bohemian</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="sustainability" className="text-foreground">
                  Priorities
                </Label>
                <Textarea
                  id="sustainability"
                  placeholder="Organic materials, fair trade, carbon neutral..."
                  className="min-h-[80px] resize-none"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="size" className="text-foreground">
                  Size
                </Label>
                <Input id="size" placeholder="e.g., M, L, 32" />
              </div>

              <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" size="lg">
                <Heart className="h-4 w-4 mr-2" />
                Find My Matches
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">Why Sustainable?</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Leaf className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Eco Materials</h3>
                <p className="text-muted-foreground text-sm">Organic, recycled, and innovative sustainable fabrics</p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Heart className="h-6 w-6 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Fair Production</h3>
                <p className="text-muted-foreground text-sm">Ethical wages and transparent supply chains</p>
              </CardContent>
            </Card>

            <Card className="text-center border-border">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Recycle className="h-6 w-6 text-secondary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Circular Design</h3>
                <p className="text-muted-foreground text-sm">Built for longevity and end-of-life recycling</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  )
}
