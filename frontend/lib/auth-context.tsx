"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (token: string, userId: string, userEmail: string, userName: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('ssp_token');
      const userId = localStorage.getItem('ssp_user_id');
      const userEmail = localStorage.getItem('ssp_user_email');
      const userName = localStorage.getItem('ssp_user_name');
      
      if (token && userId && userEmail && userName) {
        setUser({ id: userId, email: userEmail, name: userName });
        setIsAuthenticated(true);
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
      setLoading(false);
    };
    
    checkAuth();
  }, []);

  const loginUser = (token: string, userId: string, userEmail: string, userName: string) => {
    localStorage.setItem("ssp_token", token);
    localStorage.setItem("ssp_user_id", userId);
    localStorage.setItem("ssp_user_email", userEmail);
    localStorage.setItem("ssp_user_name", userName);
    setUser({ id: userId, email: userEmail, name: userName });
    setIsAuthenticated(true);
    router.push('/dashboard');
  };

  const logoutUser = () => {
    localStorage.removeItem("ssp_token");
    localStorage.removeItem("ssp_user_id");
    localStorage.removeItem("ssp_user_email");
    localStorage.removeItem("ssp_user_name");
    setUser(null);
    setIsAuthenticated(false);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, loading, login: loginUser, logout: logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
