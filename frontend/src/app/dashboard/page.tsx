"use client";

import { useAppContext } from "@/store/AppContext";
import Heatmap from "@/components/Heatmap";
import QueueList from "@/components/QueueList";
import RecommendationCard from "@/components/RecommendationCard";
import { RefreshCw } from "lucide-react";

export default function Dashboard() {
  const { isLoading } = useAppContext();

  return (
    <div className="h-full p-8 flex flex-col gap-8 max-w-7xl mx-auto animate-in fade-in duration-500">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Stadium Overview</h1>
          <p className="text-muted-foreground mt-1">Real-time crowd and queue intelligence</p>
        </div>
        <div className="flex items-center gap-2 bg-secondary/50 text-secondary-foreground px-4 py-2 rounded-lg">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
          <span className="text-sm font-medium">Live Connection</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        <div className="lg:col-span-2 flex flex-col gap-6 h-full">
          <div className="flex-none">
            <RecommendationCard />
          </div>
          <div className="flex-1 min-h-[300px]">
            <Heatmap />
          </div>
        </div>
        
        <div className="flex flex-col h-full">
          <div className="flex-1 min-h-[400px]">
            <QueueList />
          </div>
        </div>
      </div>
    </div>
  );
}