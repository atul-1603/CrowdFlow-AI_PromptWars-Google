"use client";

import Heatmap from "@/components/Heatmap";
import RoutePlanner from "@/components/RoutePlanner";

export default function MapPage() {
  return (
    <div className="h-full p-8 flex flex-col gap-6 max-w-7xl mx-auto animate-in fade-in duration-500">
      <header>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Live Map & Routing</h1>
        <p className="text-muted-foreground mt-1">Navigate the stadium efficiently while avoiding crowds</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        <div className="lg:col-span-2 flex flex-col min-h-[500px]">
          <Heatmap />
        </div>
        
        <div className="flex flex-col min-h-[400px]">
          <RoutePlanner />
        </div>
      </div>
    </div>
  );
}
