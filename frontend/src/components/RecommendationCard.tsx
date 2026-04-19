"use client";

import { useRecommendation } from "@/lib/hooks";
import { Sparkles, Loader2, AlertCircle, Clock } from "lucide-react";

export default function RecommendationCard() {
  const { recommendation, isLoading, isRefreshing, error } = useRecommendation();

  if (isLoading && !recommendation) {
    return (
      <div className="relative overflow-hidden bg-card rounded-xl border border-border p-6 shadow-sm min-h-[160px] animate-in fade-in duration-500">
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-primary/5 rounded-full blur-3xl"></div>
        <div className="relative z-10 flex items-start gap-5">
          <div className="w-12 h-12 rounded-xl bg-secondary animate-pulse shrink-0"></div>
          <div className="w-full flex flex-col gap-3 pt-1">
            <div className="h-4 w-32 bg-secondary rounded animate-pulse"></div>
            <div className="h-7 w-2/3 bg-secondary rounded animate-pulse mt-1"></div>
            <div className="h-4 w-full bg-secondary rounded animate-pulse mt-2"></div>
            <div className="h-6 w-32 bg-secondary rounded-full animate-pulse mt-3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error && !recommendation) {
    return (
      <div className="bg-destructive/10 rounded-xl border border-destructive/20 p-6 flex flex-col items-center justify-center min-h-[160px] text-destructive text-center animate-in fade-in zoom-in-95 duration-300">
        <AlertCircle size={28} className="mb-3 opacity-80" />
        <p className="text-base font-semibold">Unable to connect to AI</p>
        <p className="text-xs mt-1 max-w-xs opacity-75">Please check your network connection or API key.</p>
      </div>
    );
  }

  if (!recommendation) return null;

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-card to-background rounded-xl border border-primary/30 p-6 shadow-[0_0_20px_rgba(59,130,246,0.08)] group hover:border-primary/60 transition-all duration-500 hover:shadow-[0_8px_30px_rgba(59,130,246,0.15)] animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Background glow effect */}
      <div className="absolute -top-24 -right-24 w-56 h-56 bg-primary/20 rounded-full blur-3xl opacity-40 group-hover:opacity-70 group-hover:scale-110 transition-all duration-700"></div>
      <div className="absolute -bottom-24 -left-24 w-56 h-56 bg-accent/20 rounded-full blur-3xl opacity-40 group-hover:opacity-70 group-hover:scale-110 transition-all duration-700"></div>

      <div className="relative z-10 flex items-start gap-5">
        <div className={`w-12 h-12 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(59,130,246,0.2)] transition-transform duration-500 ${isRefreshing ? 'scale-110 shadow-[0_0_25px_rgba(59,130,246,0.4)] bg-primary/20' : 'group-hover:scale-105 group-hover:rotate-3'}`}>
          <Sparkles className={`w-6 h-6 text-primary transition-all duration-500 ${isRefreshing ? 'animate-pulse scale-110' : ''}`} />
        </div>
        
        <div className="flex-1">
          <div className="flex items-center justify-between mb-1.5">
            <h3 className="text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-2">
              Vertex AI Recommendation
            </h3>
            {isRefreshing && (
              <span className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-primary bg-primary/10 px-2 py-0.5 rounded-full animate-in fade-in duration-300">
                <Loader2 size={10} className="animate-spin" /> Analyzing
              </span>
            )}
          </div>
          <p className="text-xl font-bold text-foreground mb-2 leading-tight group-hover:text-primary transition-colors duration-300">
            {recommendation.action}
          </p>
          <p className="text-sm text-muted-foreground leading-relaxed mb-4 max-w-3xl">
            {recommendation.reason}
          </p>
          
          <div className="inline-flex items-center gap-2 bg-secondary/80 backdrop-blur-sm border border-border px-3 py-1.5 rounded-full text-xs font-medium text-foreground group-hover:bg-secondary transition-colors duration-300">
            <Clock size={12} className="text-primary" />
            Estimated Time: <span className="font-bold text-primary">{recommendation.estimated_time}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
