"use client";

import { useRouting } from "@/lib/hooks";
import { useState } from "react";
import { MapPin, Navigation, ArrowRight, Loader2, AlertTriangle } from "lucide-react";

export default function RoutePlanner() {
  const [start, setStart] = useState("");
  const [destination, setDestination] = useState("");
  const { route, calculateRoute, isLoading, error } = useRouting();

  const handleRoute = (e: React.FormEvent) => {
    e.preventDefault();
    if (!start.trim() || !destination.trim()) return;
    calculateRoute(start, destination);
  };

  return (
    <div className="bg-card rounded-xl border border-border shadow-sm flex flex-col">
      <div className="p-5 border-b border-border bg-secondary/30 flex items-center gap-2">
        <Navigation className="w-5 h-5 text-accent" />
        <h2 className="text-lg font-semibold text-card-foreground">Smart Route Planner</h2>
      </div>

      <div className="p-5">
        <form onSubmit={handleRoute} className="space-y-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <MapPin size={16} className="text-muted-foreground" />
            </div>
            <input
              type="text"
              value={start}
              onChange={(e) => setStart(e.target.value)}
              placeholder="Start Location (e.g., entrance)"
              className="w-full bg-input border border-border rounded-lg pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-accent transition-all"
            />
          </div>
          
          <div className="flex justify-center -my-2 relative z-10">
            <div className="bg-background border border-border rounded-full p-1 text-muted-foreground">
              <ArrowRight size={14} className="rotate-90" />
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <MapPin size={16} className="text-accent" />
            </div>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="Destination (e.g., gate_5)"
              className="w-full bg-input border border-border rounded-lg pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-accent transition-all"
            />
          </div>

          <button 
            type="submit"
            disabled={isLoading || !start.trim() || !destination.trim()}
            className="w-full bg-accent hover:bg-accent/90 text-accent-foreground font-medium rounded-lg py-2.5 text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_20px_rgba(139,92,246,0.5)]"
          >
            {isLoading ? <Loader2 size={16} className="animate-spin" /> : "Calculate Route"}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-sm text-destructive flex items-start gap-2">
            <AlertTriangle size={16} className="shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}

        {route && !isLoading && (
          <div className="mt-6 p-4 bg-secondary/50 border border-border rounded-lg animate-in fade-in slide-in-from-bottom-2">
            <div className="flex justify-between items-start mb-3">
              <h3 className="font-semibold text-sm">Suggested Path</h3>
              <span className="text-xs font-bold bg-primary/20 text-primary px-2 py-1 rounded-md">
                ~{route.estimated_time_minutes} min
              </span>
            </div>
            
            <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
              {route.route_description}
            </p>
            
            <div className="space-y-3">
              {route.path.map((step, idx) => (
                <div key={idx} className="flex gap-3 relative">
                  {idx !== route.path.length - 1 && (
                    <div className="absolute left-[7px] top-5 bottom-[-15px] w-0.5 bg-border z-0"></div>
                  )}
                  <div className="w-4 h-4 rounded-full bg-background border-2 border-accent z-10 mt-0.5"></div>
                  <p className="text-sm font-medium">{step.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
