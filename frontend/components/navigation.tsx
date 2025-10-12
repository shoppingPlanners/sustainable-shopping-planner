import { Leaf } from "lucide-react"
import Link from "next/link"

export function Navigation() {
  return (
    <nav className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center gap-2">
            <Leaf className="h-6 w-6 text-primary" />
            <span className="font-semibold text-lg text-foreground">StyleSustain</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/" className="text-muted-foreground hover:text-primary transition-colors">
              Home
            </Link>
            <Link href="/suggestions" className="text-muted-foreground hover:text-primary transition-colors">
              Discover
            </Link>
            <Link href="/about" className="text-muted-foreground hover:text-primary transition-colors">
              About
            </Link>
            <Link href="/login" className="text-muted-foreground hover:text-primary transition-colors">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
