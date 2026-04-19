"use client";

import { useAppContext } from "@/store/AppContext";
import { Clock, TrendingDown, Users } from "lucide-react";

export default function QueueList() {
  const { queueData, isLoading } = useAppContext();

  const queues = queueData?.queues || [];
  
  // Sort by wait time ascending
  const sortedQueues = [...queues].sort((a, b) => a.wait_time_minutes - b.wait_time_minutes);
  const fastest = sortedQueues[0];

  return (
    <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden flex flex-col h-full animate-in fade-in duration-500">
      <div className="p-5 border-b border-border bg-secondary/30">
        <h2 className="text-lg font-semibold text-card-foreground flex items-center gap-2">
          <Clock className="w-5 h-5 text-primary" />
          Live Queue Estimates
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading && !queueData ? (
          <ul className="divide-y divide-border">
            {[1, 2, 3, 4, 5].map((i) => (
              <li key={i} className="p-4 flex items-center justify-between animate-pulse">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-secondary"></div>
                  <div className="h-4 w-32 bg-secondary rounded"></div>
                </div>
                <div className="h-6 w-12 bg-secondary rounded"></div>
              </li>
            ))}
          </ul>
        ) : sortedQueues.length === 0 ? (
          <div className="h-full min-h-[250px] flex flex-col items-center justify-center text-muted-foreground animate-in fade-in">
            <Users className="w-12 h-12 mb-3 opacity-10" />
            <p className="text-sm font-medium">No queue data available.</p>
          </div>
        ) : (
          <ul className="divide-y divide-border">
            {sortedQueues.map((q, idx) => {
              const isFastest = fastest && q.name === fastest.name;
              
              return (
                <li 
                  key={q.name} 
                  className={`p-4 flex items-center justify-between group hover:bg-secondary/40 transition-all duration-300 ease-in-out cursor-default ${isFastest ? 'bg-primary/5 border-l-2 border-l-primary' : 'border-l-2 border-l-transparent'}`}
                >
                  <div className="flex items-center gap-4 transform group-hover:translate-x-2 transition-transform duration-300">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs transition-colors duration-500 ${isFastest ? 'bg-primary text-primary-foreground shadow-[0_0_12px_rgba(59,130,246,0.4)] scale-110' : 'bg-secondary text-secondary-foreground group-hover:bg-primary/20 group-hover:text-primary'}`}>
                      {idx + 1}
                    </div>
                    <div>
                      <p className="text-sm font-bold text-foreground">{q.name}</p>
                      {isFastest ? (
                        <p className="text-[10px] text-primary font-bold tracking-wide uppercase flex items-center gap-1 mt-0.5 animate-in fade-in slide-in-from-left-2">
                          <TrendingDown size={12} /> Fastest Option
                        </p>
                      ) : (
                        <p className="text-[10px] text-muted-foreground font-medium flex items-center gap-1 mt-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                          <Users size={10} /> {q.people_waiting} in line
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="text-right pr-2">
                    <p className={`text-xl font-black font-mono tracking-tight transition-colors duration-500 ${isFastest ? 'text-primary' : 'text-foreground'}`}>
                      {q.wait_time_minutes} <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">min</span>
                    </p>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
