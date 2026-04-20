"use client";

import { useState } from "react";
import { useAppContext } from "@/store/AppContext";
import { Loader2, AlertCircle, Map as MapIcon, LayoutGrid } from "lucide-react";
import StadiumMap from "./StadiumMap";

export default function Heatmap() {
  const { heatmapData, isLoading, error } = useAppContext();
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map');

  if (isLoading && !heatmapData) {
    return (
      <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden flex flex-col h-full min-h-[400px] animate-in fade-in duration-500">
        <div className="p-5 border-b border-border flex justify-between bg-secondary/30">
          <div className="h-6 w-48 bg-secondary rounded animate-pulse"></div>
          <div className="h-4 w-32 bg-secondary rounded animate-pulse"></div>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-primary opacity-50" />
        </div>
      </div>
    );
  }

  if (error && !heatmapData) {
    return (
      <div className="h-full min-h-[400px] flex flex-col items-center justify-center bg-card rounded-xl border border-destructive shadow-sm text-destructive p-6 text-center">
        <AlertCircle className="w-10 h-10 mb-4 opacity-80" />
        <p className="text-base font-semibold">Error loading heatmap data</p>
        <p className="text-sm opacity-80 mt-1 max-w-xs">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden flex flex-col h-full animate-in fade-in duration-500">
      <div className="p-5 border-b border-border flex justify-between items-center bg-secondary/30 transition-colors duration-500">
        <div>
          <h2 className="text-lg font-semibold text-card-foreground flex items-center gap-2">
            <MapIcon className="w-5 h-5 text-primary" />
            Live Stadium Flow
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time tracking of {Object.keys(heatmapData?.locations || {}).length} zones
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="bg-background/50 p-1 rounded-lg border border-border flex">
            <button 
              onClick={() => setViewMode('map')}
              className={`p-1.5 rounded-md transition-all ${viewMode === 'map' ? 'bg-primary text-primary-foreground shadow-sm' : 'hover:bg-secondary text-muted-foreground'}`}
              title="Map View"
            >
              <MapIcon size={16} />
            </button>
            <button 
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-md transition-all ${viewMode === 'list' ? 'bg-primary text-primary-foreground shadow-sm' : 'hover:bg-secondary text-muted-foreground'}`}
              title="List View"
            >
              <LayoutGrid size={16} />
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 relative overflow-hidden">
        {viewMode === 'map' ? (
          <div className="absolute inset-0 p-4">
            <StadiumMap />
          </div>
        ) : (
          <div className="p-5 h-full overflow-y-auto">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(heatmapData?.locations || {}).map(([id, data]) => {
                const formatId = id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                let colorClass = data.status_label === 'CRITICAL' || data.status_label === 'HIGH' ? 'bg-destructive/10 text-destructive' : data.status_label === 'MODERATE' ? 'bg-warning/10 text-warning' : 'bg-success/10 text-success';
                
                return (
                  <div key={id} className="p-4 rounded-xl border border-border bg-background/50 hover:border-primary/50 transition-all">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="font-semibold text-sm">{formatId}</h3>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${colorClass}`}>
                        {data.status_label}
                      </span>
                    </div>
                    <div className="flex items-end justify-between">
                      <span className="text-2xl font-black font-mono">{data.density_percentage}%</span>
                      <span className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1">capacity</span>
                    </div>
                    <div className="h-1 w-full bg-secondary rounded-full mt-3 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${data.status_label === 'CRITICAL' || data.status_label === 'HIGH' ? 'bg-destructive' : data.status_label === 'MODERATE' ? 'bg-warning' : 'bg-success'}`}
                        style={{ width: `${data.density_percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      <div className="px-5 py-3 border-t border-border bg-secondary/10 flex justify-between items-center text-[10px] text-muted-foreground">
        <div className="flex gap-3">
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-success"></div> Low</div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-warning"></div> Moderate</div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-destructive"></div> High</div>
        </div>
        <div>Last Update: {new Date().toLocaleTimeString()}</div>
      </div>
    </div>
  );
}
