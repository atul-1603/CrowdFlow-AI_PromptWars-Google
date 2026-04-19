"use client";

import { useAppContext } from "@/store/AppContext";
import { Loader2, AlertCircle, Map } from "lucide-react";

export default function Heatmap() {
  const { heatmapData, isLoading, error } = useAppContext();

  if (isLoading && !heatmapData) {
    return (
      <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden flex flex-col h-full min-h-[300px] animate-in fade-in duration-500">
        <div className="p-5 border-b border-border flex justify-between bg-secondary/30">
          <div className="h-6 w-48 bg-secondary rounded animate-pulse"></div>
          <div className="h-4 w-32 bg-secondary rounded animate-pulse"></div>
        </div>
        <div className="p-5 flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="rounded-lg border border-border bg-background p-4 animate-pulse">
              <div className="flex justify-between mb-4">
                <div className="h-4 w-24 bg-secondary rounded"></div>
                <div className="h-4 w-12 bg-secondary rounded-full"></div>
              </div>
              <div className="h-8 w-16 bg-secondary rounded mb-2 mt-6"></div>
              <div className="h-1.5 w-full bg-secondary rounded-full mt-3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error && !heatmapData) {
    return (
      <div className="h-64 flex flex-col items-center justify-center bg-card rounded-xl border border-destructive shadow-sm text-destructive p-6 text-center animate-in fade-in zoom-in-95 duration-300">
        <AlertCircle className="w-10 h-10 mb-4 opacity-80" />
        <p className="text-base font-semibold">Error loading heatmap data</p>
        <p className="text-sm opacity-80 mt-1 max-w-xs">{error}</p>
      </div>
    );
  }

  const locations = heatmapData?.locations || {};
  const locationEntries = Object.entries(locations);

  return (
    <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden flex flex-col h-full animate-in fade-in duration-500">
      <div className="p-5 border-b border-border flex justify-between items-center bg-secondary/30 transition-colors duration-500">
        <div>
          <h2 className="text-lg font-semibold text-card-foreground flex items-center gap-2">
            <Map className="w-5 h-5 text-primary" />
            Live Crowd Heatmap
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Last updated: {heatmapData?.timestamp ? new Date(heatmapData.timestamp).toLocaleTimeString() : "Just now"}
          </p>
        </div>
        <div className="flex gap-3 text-[10px] font-bold uppercase tracking-wider">
          <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full bg-success shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>Low</div>
          <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full bg-warning shadow-[0_0_8px_rgba(245,158,11,0.5)]"></div>Mod</div>
          <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full bg-destructive shadow-[0_0_8px_rgba(239,68,68,0.5)]"></div>High</div>
        </div>
      </div>

      <div className="p-5 flex-1 overflow-y-auto">
        {locationEntries.length === 0 ? (
          <div className="h-full min-h-[200px] flex flex-col items-center justify-center text-muted-foreground animate-in fade-in">
            <Map className="w-12 h-12 mb-3 opacity-10" />
            <p className="text-sm font-medium">No active zones tracked currently.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {locationEntries.map(([id, data]) => {
              const formatId = id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
              
              let colorClass = "bg-success text-success-foreground border-success/30 shadow-[0_0_15px_rgba(16,185,129,0.1)]";
              let barColor = "bg-success";
              
              if (data.status_label === "MODERATE") {
                colorClass = "bg-warning text-warning-foreground border-warning/30 shadow-[0_0_15px_rgba(245,158,11,0.1)]";
                barColor = "bg-warning";
              } else if (data.status_label === "HIGH" || data.status_label === "CRITICAL") {
                colorClass = "bg-destructive text-destructive-foreground border-destructive/30 shadow-[0_0_15px_rgba(239,68,68,0.15)]";
                barColor = "bg-destructive";
              }

              return (
                <div key={id} className="relative overflow-hidden group rounded-xl border border-border bg-background p-4 hover:border-primary/40 hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)] hover:-translate-y-1 transition-all duration-300 ease-out cursor-default">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-semibold text-sm text-foreground truncate pr-2 group-hover:text-primary transition-colors">{formatId}</h3>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold tracking-wide transition-all duration-500 ${colorClass}`}>
                      {data.status_label}
                    </span>
                  </div>
                  
                  <div className="flex items-end justify-between mt-auto">
                    <span className="text-3xl font-black font-mono tracking-tighter text-foreground group-hover:scale-105 origin-bottom-left transition-transform duration-300">
                      {data.density_percentage}%
                    </span>
                    <span className="text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wider">capacity</span>
                  </div>
                  
                  {/* Progress Bar */}
                  <div className="h-1.5 w-full bg-secondary rounded-full mt-4 overflow-hidden shadow-inner">
                    <div 
                      className={`h-full rounded-full ${barColor} transition-all duration-1000 ease-out`} 
                      style={{ width: `${data.density_percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
