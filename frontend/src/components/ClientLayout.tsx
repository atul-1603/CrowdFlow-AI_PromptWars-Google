"use client";

import { usePathname } from "next/navigation";
import { AppProvider } from "@/store/AppContext";
import { AuthProvider } from "@/context/AuthContext";
import ProtectedRoute from "@/components/Auth/ProtectedRoute";
import Sidebar from "@/components/Sidebar";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLandingPage = pathname === "/";
  const isAuthPage = pathname === "/login" || pathname === "/signup";

  return (
    <AuthProvider>
      <AppProvider>
        {isLandingPage || isAuthPage ? (
          <main className="flex-1 overflow-y-auto">
            {children}
          </main>
        ) : (
          <ProtectedRoute>
            <Sidebar />
            <main className="flex-1 overflow-y-auto bg-background/50">
              {children}
            </main>
          </ProtectedRoute>
        )}
      </AppProvider>
    </AuthProvider>
  );
}
