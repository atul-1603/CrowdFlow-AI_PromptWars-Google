import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { LogOut, User as UserIcon, LayoutDashboard, MessageSquare, Map as MapIcon } from "lucide-react";

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="w-64 bg-card border-r border-border h-full flex flex-col shadow-lg z-10">
      <div className="p-6">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
          CrowdFlow AI
        </h1>
        <p className="text-xs text-muted-foreground mt-1">Intelligent Stadium Management</p>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        <Link href="/dashboard" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-sm font-medium">
          <LayoutDashboard size={18} className="text-primary" />
          Dashboard
        </Link>
        <Link href="/chat" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-sm font-medium">
          <MessageSquare size={18} className="text-accent" />
          AI Assistant
        </Link>
        <Link href="/map" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-sm font-medium">
          <MapIcon size={18} className="text-success" />
          Live Map
        </Link>
      </nav>

      <div className="p-4 border-t border-border mt-auto">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {user?.photoURL ? (
              <img src={user.photoURL} alt="Avatar" className="w-8 h-8 rounded-full border border-border" />
            ) : (
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-sm">
                {user?.displayName?.[0] || <UserIcon size={14} />}
              </div>
            )}
            <div className="text-xs">
              <p className="font-bold truncate max-w-[100px]">{user?.displayName || "User"}</p>
              <p className="text-muted-foreground truncate max-w-[100px]">{user?.email}</p>
            </div>
          </div>
          <button 
            onClick={() => logout()}
            className="p-2 hover:bg-destructive/10 hover:text-destructive rounded-lg transition-colors"
            title="Log out"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </aside>
  );
}
