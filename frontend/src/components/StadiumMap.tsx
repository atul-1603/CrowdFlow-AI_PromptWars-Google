"use client";

import React, { useState, useEffect } from 'react';
import {
  APIProvider,
  Map,
  AdvancedMarker,
  Pin,
  InfoWindow,
  useMap,
  useMapsLibrary
} from '@vis.gl/react-google-maps';
import { useAppContext } from '@/store/AppContext';
import { LocateFixed, Navigation, Info } from 'lucide-react';

const STADIUM_CENTER = { lat: 37.4033, lng: -121.9702 };

const ZONE_COORDS: Record<string, { lat: number; lng: number; label: string }> = {
  "entrance_gate_a": { lat: 37.4045, lng: -121.9705, label: "Entrance Gate A" },
  "food_court_1": { lat: 37.4035, lng: -121.9715, label: "Food Court 1" },
  "restroom_north": { lat: 37.4050, lng: -121.9695, label: "Restroom North" },
  "merchandise_shop": { lat: 37.4025, lng: -121.9710, label: "Merchandise Shop" },
  "gate_b": { lat: 37.4040, lng: -121.9690, label: "Gate B" },
  "vip_lounge": { lat: 37.4030, lng: -121.9700, label: "VIP Lounge" },
};

export default function StadiumMap() {
  const { heatmapData } = useAppContext();
  const [selectedMarker, setSelectedMarker] = useState<string | null>(null);
  const [userLocation, setUserLocation] = useState<google.maps.LatLngLiteral | null>(null);
  const [destinationMarker, setDestinationMarker] = useState<string | null>(null);
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

  const handleLocate = () => {
    // For demo purposes, we simulate the user's location near the stadium entrance.
    // Real geolocation would likely place the user thousands of miles away from the stadium.
    const mockLocation = { lat: 37.4042, lng: -121.9700 };
    setUserLocation(mockLocation);
  };

  if (!apiKey) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-secondary/20 rounded-xl border border-dashed border-border p-8 text-center">
        <div>
          <p className="text-destructive font-bold mb-2">Google Maps API Key Missing</p>
          <p className="text-sm text-muted-foreground">Please add NEXT_PUBLIC_GOOGLE_MAPS_API_KEY to your .env.local file to see the interactive map.</p>
        </div>
      </div>
    );
  }

  return (
    <APIProvider apiKey={apiKey}>
      <div className="h-full w-full relative group rounded-xl overflow-hidden border border-border shadow-inner">
        <Map
          defaultCenter={STADIUM_CENTER}
          defaultZoom={17}
          mapId="STADIUM_MAP_ID"
          disableDefaultUI={true}
          gestureHandling={'greedy'}
          colorScheme='DARK'
        >
          {Object.entries(heatmapData?.locations || {}).map(([id, data]) => {
            const coords = ZONE_COORDS[id];
            if (!coords) return null;
            const color = getStatusColor(data.status_label);

            return (
              <React.Fragment key={id}>
                <AdvancedMarker
                  position={coords}
                  onClick={() => setSelectedMarker(id)}
                >
                  <Pin 
                    background={color} 
                    glyphColor={'#fff'} 
                    borderColor={'rgba(255,255,255,0.5)'}
                    scale={1.1}
                  />
                </AdvancedMarker>

                {selectedMarker === id && (
                  <InfoWindow
                    position={coords}
                    onCloseClick={() => setSelectedMarker(null)}
                  >
                    <div className="p-3 min-w-[150px] text-foreground bg-card">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-sm">{coords.label}</h3>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${getStatusBg(data.status_label)}`}>
                          {data.status_label}
                        </span>
                      </div>
                      <div className="space-y-1.5">
                        <div className="flex justify-between items-center text-xs">
                          <span className="text-muted-foreground">Capacity</span>
                          <span className="font-mono font-bold">{data.density_percentage}%</span>
                        </div>
                        <div className="h-1 w-full bg-secondary rounded-full overflow-hidden mb-2">
                          <div 
                            className="h-full transition-all duration-500" 
                            style={{ width: `${data.density_percentage}%`, backgroundColor: color }}
                          />
                        </div>
                        <button
                          onClick={() => {
                            setDestinationMarker(id);
                            setSelectedMarker(null);
                          }}
                          className="w-full py-1.5 bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground text-xs font-bold rounded-lg transition-colors flex items-center justify-center gap-1"
                        >
                          <Navigation size={12} /> Navigate Here
                        </button>
                      </div>
                    </div>
                  </InfoWindow>
                )}
              </React.Fragment>
            );
          })}

          {userLocation && (
            <AdvancedMarker position={userLocation}>
              <div className="w-4 h-4 bg-blue-500 rounded-full border-2 border-white shadow-[0_0_15px_rgba(59,130,246,1)] animate-pulse"></div>
            </AdvancedMarker>
          )}

          {destinationMarker && (
            <SmartRoute 
              start={userLocation || STADIUM_CENTER} 
              end={ZONE_COORDS[destinationMarker]} 
              heatmapData={heatmapData}
            />
          )}
          <MapUpdater location={userLocation} />
        </Map>

        {/* Map Controls */}
        <div className="absolute top-4 right-4 flex flex-col gap-2">
          <button 
            onClick={handleLocate}
            className="p-3 bg-card/80 backdrop-blur-md border border-border rounded-xl shadow-lg hover:bg-card transition-all active:scale-95"
            title="Locate Me"
          >
            <LocateFixed size={18} className="text-primary" />
          </button>
          {destinationMarker && (
            <button 
              onClick={() => setDestinationMarker(null)}
              className="p-3 bg-destructive text-destructive-foreground rounded-xl shadow-lg transition-all active:scale-95"
              title="Clear Route"
            >
              <Navigation size={18} className="rotate-45" />
            </button>
          )}
        </div>

        {/* Legend */}
        <div className="absolute bottom-4 left-4 p-3 bg-card/80 backdrop-blur-md border border-border rounded-xl shadow-xl hidden md:flex gap-4">
          <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider">
            <div className="w-2 h-2 rounded-full bg-success"></div> Low
          </div>
          <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider">
            <div className="w-2 h-2 rounded-full bg-warning"></div> Mod
          </div>
          <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider">
            <div className="w-2 h-2 rounded-full bg-destructive"></div> High
          </div>
        </div>
      </div>
    </APIProvider>
  );
}

function SmartRoute({ start, end, heatmapData }: { start: any, end: any, heatmapData: any }) {
  const map = useMap();
  const routesLibrary = useMapsLibrary('routes');
  const geometryLibrary = useMapsLibrary('geometry');
  const [directionsService, setDirectionsService] = useState<google.maps.DirectionsService>();

  useEffect(() => {
    if (!routesLibrary || !map || !geometryLibrary) return;
    setDirectionsService(new routesLibrary.DirectionsService());
  }, [routesLibrary, map, geometryLibrary]);

  useEffect(() => {
    if (!directionsService || !geometryLibrary || !map) return;
    
    let currentPolylines: google.maps.Polyline[] = [];
    let timeouts: NodeJS.Timeout[] = [];

    directionsService.route({
      origin: start,
      destination: end,
      travelMode: google.maps.TravelMode.WALKING
    }).then(res => {
      const path = res.routes[0].overview_path;
      
      for (let i = 0; i < path.length - 1; i++) {
        const p1 = path[i];
        const p2 = path[i+1];
        
        let nearestZoneId = '';
        let minDistance = Infinity;
        
        Object.entries(ZONE_COORDS).forEach(([id, coords]) => {
          const zoneLatLng = new google.maps.LatLng(coords.lat, coords.lng);
          const dist = geometryLibrary.spherical.computeDistanceBetween(p1, zoneLatLng);
          if (dist < minDistance) {
            minDistance = dist;
            nearestZoneId = id;
          }
        });
        
        const density = heatmapData?.locations?.[nearestZoneId]?.density_percentage || 0;
        let color = '#10b981';
        if (density > 70) color = '#ef4444';
        else if (density > 40) color = '#f59e0b';
        
        const polyline = new google.maps.Polyline({
          path: [p1, p2],
          strokeColor: color,
          strokeWeight: 6,
          strokeOpacity: 0.8,
        });
        
        currentPolylines.push(polyline);
        
        const t = setTimeout(() => {
          polyline.setMap(map);
        }, i * 30);
        timeouts.push(t);
      }
    }).catch(err => console.error("Routing error:", err));
    
    return () => {
      timeouts.forEach(clearTimeout);
      currentPolylines.forEach(p => p.setMap(null));
    };
  }, [directionsService, start, end, heatmapData, geometryLibrary, map]);

  return null;
}

function MapUpdater({ location }: { location: any }) {
  const map = useMap();
  useEffect(() => {
    if (map && location) {
      map.panTo(location);
      map.setZoom(18);
    }
  }, [map, location]);
  return null;
}

function getStatusColor(status: string) {
  switch (status) {
    case 'CRITICAL':
    case 'HIGH': return '#ef4444';
    case 'MODERATE': return '#f59e0b';
    case 'LOW': default: return '#10b981';
  }
}

function getStatusBg(status: string) {
  switch (status) {
    case 'CRITICAL':
    case 'HIGH': return 'bg-destructive/20 text-destructive';
    case 'MODERATE': return 'bg-warning/20 text-warning';
    case 'LOW': default: return 'bg-success/20 text-success';
  }
}
