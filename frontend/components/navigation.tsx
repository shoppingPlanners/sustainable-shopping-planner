"use client";

import { Leaf } from "lucide-react"
import Link from "next/link"
import { useTracking } from "@/hooks/use-tracking"

export function Navigation() {
  const { trackClick } = useTracking();

  const handleNavClick = (page: string) => {
    trackClick("navigation_link", undefined, { page });
  };

  return (
    <nav className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link 
            href="/" 
            className="flex items-center gap-2"
            onClick={() => handleNavClick("home")}
          >
            <Leaf className="h-6 w-6 text-primary" />
            <span className="font-semibold text-lg text-foreground">StyleSustain</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link 
              href="/" 
              className="text-muted-foreground hover:text-primary transition-colors"
              onClick={() => handleNavClick("home")}
            >
              Home
            </Link>
            <Link 
              href="/suggestions" 
              className="text-muted-foreground hover:text-primary transition-colors"
              onClick={() => handleNavClick("suggestions")}
            >
              Discover
            </Link>
            <Link 
              href="/about" 
              className="text-muted-foreground hover:text-primary transition-colors"
              onClick={() => handleNavClick("about")}
            >
              About
            </Link>
            <Link 
              href="/login" 
              className="text-muted-foreground hover:text-primary transition-colors"
              onClick={() => handleNavClick("login")}
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
