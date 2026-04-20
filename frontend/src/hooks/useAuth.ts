"use client";

import { useAuthContext } from "@/context/AuthContext";

export function useAuth() {
  const { user, loading, logout, signInWithGoogle } = useAuthContext();
  
  return {
    user,
    loading,
    isAuthenticated: !!user,
    logout,
    signInWithGoogle
  };
}
