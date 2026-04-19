"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { ChatMessage, HeatmapResponse, QueueResponse, CrowdData } from "@/types";
import { collection, onSnapshot, query } from "firebase/firestore";
import { db } from "@/lib/firebase";

interface AppState {
  chatHistory: ChatMessage[];
  addMessage: (msg: ChatMessage) => void;
  heatmapData: HeatmapResponse | null;
  queueData: QueueResponse | null;
  isLoading: boolean;
  isRefreshing: boolean; // Retained for recommendation polling
  error: string | null;
}

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [heatmapData, setHeatmapData] = useState<HeatmapResponse | null>(null);
  const [queueData, setQueueData] = useState<QueueResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addMessage = (msg: ChatMessage) => {
    setChatHistory((prev) => [...prev, msg]);
  };

  useEffect(() => {
    try {
      if (!process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID) {
        throw new Error("Missing Firebase Config! Please set NEXT_PUBLIC_FIREBASE_PROJECT_ID in .env.local.");
      }

      // 1. Listen to Crowd Heatmap
      const unsubCrowd = onSnapshot(collection(db, "crowd"), (snapshot) => {
        if (snapshot.empty) {
          // Robust Fallback if DB is completely empty
          setHeatmapData({
            locations: {
              "entrance_gate_a": { density_percentage: 85, location_id: "entrance_gate_a", status_label: "CRITICAL" },
              "food_court_1": { density_percentage: 62, location_id: "food_court_1", status_label: "MODERATE" },
              "restroom_north": { density_percentage: 15, location_id: "restroom_north", status_label: "LOW" },
              "merchandise_shop": { density_percentage: 40, location_id: "merchandise_shop", status_label: "MODERATE" }
            },
            timestamp: new Date().toISOString()
          });
        } else {
          const locations: Record<string, CrowdData> = {};
          let total = 0;
          
          snapshot.forEach(doc => {
            const val = doc.data().density || 0;
            let status: "LOW" | "MODERATE" | "HIGH" | "CRITICAL" = "LOW";
            if (val > 80) status = "CRITICAL";
            else if (val > 60) status = "HIGH";
            else if (val > 30) status = "MODERATE";
            locations[doc.id] = { density_percentage: val, location_id: doc.id, status_label: status };
            total += val;
          });
          
          setHeatmapData({
            locations,
            timestamp: new Date().toISOString()
          });
        }
        setIsLoading(false); // Only unset loading after first paint
      }, (err) => {
        console.error("Firebase Crowd Listener Error:", err);
        setError("Disconnected from Live Crowd Data.");
      });

      // 2. Listen to Queue List
      const unsubQueue = onSnapshot(collection(db, "queue"), (snapshot) => {
        if (snapshot.empty) {
          setQueueData({
            queues: [
              { name: "Burger Stall", people_waiting: 25, service_rate: 2.0, wait_time_minutes: Math.ceil(25/2.0) },
              { name: "Entrance Gate A", people_waiting: 120, service_rate: 4.0, wait_time_minutes: Math.ceil(120/4.0) }
            ]
          });
        } else {
          const queues = snapshot.docs.map(doc => {
            const data = doc.data();
            const name = doc.id.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
            const people = data.people || 0;
            const rate = data.service_rate || 1.0;
            return {
              name,
              people_waiting: people,
              service_rate: rate,
              wait_time_minutes: Math.ceil(people / rate)
            };
          });
          setQueueData({ queues });
        }
      }, (err) => {
        console.error("Firebase Queue Listener Error:", err);
      });

      // Cleanup listeners on unmount
      return () => {
        unsubCrowd();
        unsubQueue();
      };
      
    } catch (err: any) {
      console.error(err);
      setError(err.message);
      setIsLoading(false);
    }
  }, []);

  return (
    <AppContext.Provider
      value={{
        chatHistory,
        addMessage,
        heatmapData,
        queueData,
        isLoading,
        isRefreshing,
        error
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
};
