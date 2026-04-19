import Link from "next/link";
import { LayoutDashboard, MessageSquare, Map as MapIcon, Navigation } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-card border-r border-border h-full flex flex-col shadow-lg z-10">
      <div className="p-6">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
          CrowdFlow AI
        </h1>
        <p className="text-xs text-muted-foreground mt-1">Intelligent Stadium Management</p>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        <Link href="/" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-sm font-medium">
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

      <div className="p-6 border-t border-border mt-auto">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-accent flex items-center justify-center text-primary-foreground font-bold text-sm">
            CF
          </div>
          <div className="text-sm font-medium">Admin User</div>
        </div>
      </div>
    </aside>
  );
}
