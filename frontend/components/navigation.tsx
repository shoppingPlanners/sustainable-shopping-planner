"use client";

import { Leaf, LogOut, User, ChevronDown } from "lucide-react"
import Link from "next/link"
import { useTracking } from "@/hooks/use-tracking"
import { useAuth } from "@/lib/auth-context"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function Navigation() {
  const { trackClick } = useTracking();
  const { user, isAuthenticated, logout } = useAuth();
  const pathname = usePathname();

  const handleNavClick = (page: string) => {
    trackClick("navigation_link", undefined, { page });
  };

  const handleLogout = () => {
    logout();
    trackClick("logout_button");
  };

  const isActivePath = (path: string) => pathname === path;

  const getUserInitial = () => {
    if (user?.name) return user.name.charAt(0).toUpperCase();
    if (user?.email) return user.email.charAt(0).toUpperCase();
    return "U";
  };

  return (
    <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link 
            href={isAuthenticated ? "/home" : "/"} 
            className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            onClick={() => handleNavClick("home")}
          >
            <div className="p-1.5 rounded-lg bg-green-100 dark:bg-green-900">
              <Leaf className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            <span className="font-bold text-lg">StyleSustain</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-6">
            {isAuthenticated ? (
              <>
                <Link 
                  href="/home" 
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    isActivePath("/home") ? "text-primary" : "text-muted-foreground"
                  }`}
                  onClick={() => handleNavClick("home")}
                >
                  Home
                </Link>
                <Link 
                  href="/discover" 
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    isActivePath("/discover") ? "text-primary" : "text-muted-foreground"
                  }`}
                  onClick={() => handleNavClick("discover")}
                >
                  Discover
                </Link>
                <Link 
                  href="/about" 
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    isActivePath("/about") ? "text-primary" : "text-muted-foreground"
                  }`}
                  onClick={() => handleNavClick("about")}
                >
                  About
                </Link>

                {/* User Dropdown Menu */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <button 
                      className="flex items-center gap-2 h-10 px-3 rounded-md hover:bg-accent transition-all duration-200 cursor-pointer group border border-transparent hover:border-border"
                    >
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 text-white font-semibold text-sm shadow-sm group-hover:shadow-md transition-shadow">
                        {getUserInitial()}
                      </div>
                      <span className="text-sm font-medium hidden sm:block">{user?.name || "User"}</span>
                      <ChevronDown className="h-4 w-4 text-muted-foreground group-hover:text-foreground transition-colors" />
                    </button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-56 mt-2">
                    <DropdownMenuLabel>
                      <div className="flex flex-col space-y-1">
                        <p className="text-sm font-medium">{user?.name || "User"}</p>
                        <p className="text-xs text-muted-foreground truncate">
                          {user?.email}
                        </p>
                      </div>
                    </DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem asChild>
                      <Link href="/profile" className="cursor-pointer flex items-center">
                        <User className="mr-2 h-4 w-4" />
                        <span>Profile</span>
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem 
                      onClick={handleLogout}
                      className="cursor-pointer text-red-600 focus:text-red-600 focus:bg-red-50 dark:focus:bg-red-950"
                    >
                      <LogOut className="mr-2 h-4 w-4" />
                      <span>Log out</span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <>
                <Link 
                  href="/#features" 
                  className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  onClick={() => handleNavClick("features")}
                >
                  Features
                </Link>
                <Link 
                  href="/about" 
                  className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  onClick={() => handleNavClick("about")}
                >
                  About
                </Link>
                <Link 
                  href="/login" 
                  className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  onClick={() => handleNavClick("login")}
                >
                  Sign In
                </Link>
                <Button asChild size="sm" className="bg-primary hover:bg-primary/90">
                  <Link 
                    href="/register" 
                    onClick={() => handleNavClick("register")}
                  >
                    Get Started
                  </Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
