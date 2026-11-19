import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Polygon, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { MapPin, Navigation, Compass, Layers, RotateCcw, Check, Sparkles } from 'lucide-react';
import { getNasaGibsTileUrl, NASA_GIBS_ATTRIBUTION } from '../utils/nasaGibs';
import { apiClient } from '../api/client';

// Custom Map Marker Icon
const fieldPinIcon = new L.DivIcon({
  className: 'custom-field-pin',
  html: `<div style="width: 22px; height: 22px; border-radius: 50%; background: #10b981; border: 3px solid #ffffff; box-shadow: 0 0 15px rgba(16, 185, 129, 0.8); animation: pulse 2s infinite;"></div>`,
  iconSize: [22, 22],
  iconAnchor: [11, 11]
});

// Helper: Geodesic area calculation on Earth sphere (Haversine/Spherical Shoelace)
export function calculatePolygonAreaHa(coords) {
  if (!coords || coords.length < 3) return 0;
  const R = 6378137; // Rayon moyen terrestre en mètres
  let area = 0;
  for (let i = 0; i < coords.length; i++) {
    const p1 = coords[i];
    const p2 = coords[(i + 1) % coords.length];
    const lat1 = (p1[0] * Math.PI) / 180;
    const lat2 = (p2[0] * Math.PI) / 180;
    const lon1 = (p1[1] * Math.PI) / 180;
    const lon2 = (p2[1] * Math.PI) / 180;
    area += (lon2 - lon1) * (2 + Math.sin(lat1) + Math.sin(lat2));
  }
  area = Math.abs((area * R * R) / 2.0);
  return parseFloat((area / 10000.0).toFixed(2));
}

// Controller to pan/zoom map programmatically
function MapController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] && center[1]) {
      map.flyTo(center, zoom || 14, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

// Map event listener for clicking & drawing
function MapClickHandler({ isDrawing, onAddPoint, onSetMarker }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      if (isDrawing) {
        onAddPoint([parseFloat(lat.toFixed(6)), parseFloat(lng.toFixed(6))]);
      } else {
        onSetMarker(parseFloat(lat.toFixed(6)), parseFloat(lng.toFixed(6)));
      }
    }
  });
  return null;
}

export default function ParcelMapDrawer({
  latitude,
  longitude,
  areaHa,
  onChange,
  country
}) {
  const [locations, setLocations] = useState([]);
  const [selectedLocId, setSelectedLocId] = useState('');
  const [gpsLoading, setGpsLoading] = useState(false);
  const [gpsError, setGpsError] = useState(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [polygonCoords, setPolygonCoords] = useState([]);

  // Fetch geographic hierarchy for dropdown
  useEffect(() => {
    let mounted = true;
    apiClient.get('/locations')
      .then(res => {
        if (mounted && res.data && res.data.locations) {
          setLocations(res.data.locations);
        }
      })
      .catch(err => {
        console.warn("Could not fetch locations hierarchy:", err);
      });
    return () => { mounted = false; };
  }, []);

  // Handle location dropdown select
  const handleLocationSelect = (locId) => {
    setSelectedLocId(locId);
    const loc = locations.find(l => l.id === locId);
    if (loc && loc.latitude && loc.longitude) {
      onChange({
        latitude: loc.latitude,
        longitude: loc.longitude,
        country: loc.country || country,
        nameHint: loc.name
      });
      setPolygonCoords([]);
    }
  };

  // HTML5 Geolocation API: Use current GPS location
  const handleUseCurrentGPS = () => {
    if (!navigator.geolocation) {
      setGpsError("La géolocalisation n'est pas supportée par votre navigateur.");
      return;
    }
    setGpsLoading(true);
    setGpsError(null);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = parseFloat(pos.coords.latitude.toFixed(6));
        const lon = parseFloat(pos.coords.longitude.toFixed(6));
        setGpsLoading(false);
        // Automatically infer country from latitude (Luxembourg ~49-50, Madagascar ~ -12 to -25)
        const inferredCountry = lat > 45 ? "LUX" : "MDG";
        onChange({
          latitude: lat,
          longitude: lon,
          country: inferredCountry
        });
      },
      (err) => {
        setGpsLoading(false);
        setGpsError("Impossible de récupérer votre position GPS (autorisation refusée ou signal indisponible).");
        console.warn("GPS error:", err);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  };

  // Add a point to the field polygon
  const handleAddPolygonPoint = (pt) => {
    const updated = [...polygonCoords, pt];
    setPolygonCoords(updated);
    if (updated.length >= 3) {
      const calculatedArea = calculatePolygonAreaHa(updated);
      onChange({
        area_ha: calculatedArea > 0 ? calculatedArea : areaHa,
        latitude: pt[0],
        longitude: pt[1]
      });
    }
  };

  // Clear polygon drawing
  const handleResetPolygon = () => {
    setPolygonCoords([]);
    setIsDrawing(false);
  };

  const centerCoords = [latitude || 49.6116, longitude || 6.1319];

  return (
    <div className="space-y-4">
      {/* Top Bar: Dropdown Location Selector + GPS Button */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {/* Dropdown Menu of official communes */}
        <div>
          <label className="block text-[11px] font-mono text-slate-300 mb-1 flex items-center gap-1.5">
            <Compass className="w-3.5 h-3.5 text-emerald-400" />
            <span>Sélectionner une commune (Menu déroulant)</span>
          </label>
          <select
            value={selectedLocId}
            onChange={(e) => handleLocationSelect(e.target.value)}
            className="w-full bg-[#0a1d15] border border-white/20 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-400 font-sans"
          >
            <option value="">-- Choisir une commune ou ville --</option>
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>
                {loc.label}
              </option>
            ))}
          </select>
        </div>

        {/* GPS Button */}
        <div>
          <label className="block text-[11px] font-mono text-slate-300 mb-1 flex items-center gap-1.5">
            <Navigation className="w-3.5 h-3.5 text-cyan-400" />
            <span>Positionnement temps réel</span>
          </label>
          <button
            type="button"
            onClick={handleUseCurrentGPS}
            disabled={gpsLoading}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-xl text-xs font-mono transition-all"
          >
            <Navigation className={`w-3.5 h-3.5 ${gpsLoading ? 'animate-spin' : ''}`} />
            <span>{gpsLoading ? 'Acquisition GPS en cours...' : 'Utiliser ma position GPS actuelle'}</span>
          </button>
        </div>
      </div>

      {gpsError && (
        <p className="text-[11px] text-amber-400 font-mono bg-amber-950/40 border border-amber-800/40 p-2 rounded-lg">
          {gpsError}
        </p>
      )}

      {/* Polygon Drawing Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 rounded-xl bg-white/5 border border-white/10 text-xs font-mono">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          <span className="text-slate-300 font-semibold">Outil Polygone (Calcul surface) :</span>
          {polygonCoords.length > 0 && (
            <span className="text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-500/30 font-bold">
              {polygonCoords.length} sommets • {calculatePolygonAreaHa(polygonCoords)} ha
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {!isDrawing ? (
            <button
              type="button"
              onClick={() => setIsDrawing(true)}
              className="px-3 py-1 bg-emerald-400 hover:bg-emerald-300 text-black font-semibold rounded-lg text-[11px] transition-all flex items-center gap-1"
            >
              <Sparkles className="w-3 h-3" />
              <span>Dessiner mon champ</span>
            </button>
          ) : (
            <>
              <span className="text-[11px] text-amber-300 animate-pulse">
                Cliquez sur la carte pour délimiter le champ
              </span>
              <button
                type="button"
                onClick={() => setIsDrawing(false)}
                className="px-2.5 py-1 bg-emerald-500 text-black font-bold rounded-lg text-[11px] flex items-center gap-1"
              >
                <Check className="w-3 h-3" />
                <span>Terminer</span>
              </button>
            </>
          )}

          {polygonCoords.length > 0 && (
            <button
              type="button"
              onClick={handleResetPolygon}
              className="p-1 text-slate-400 hover:text-white rounded-lg hover:bg-white/10"
              title="Effacer le tracé"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Interactive Map */}
      <div className="relative w-full h-64 sm:h-72 rounded-2xl overflow-hidden border border-white/20 shadow-2xl">
        <MapContainer
          center={centerCoords}
          zoom={13}
          style={{ height: '100%', width: '100%', background: '#071610' }}
          attributionControl={false}
        >
          {/* NASA GIBS MODIS TrueColor Satellite Layer (2 days ago) */}
          <TileLayer
            url={getNasaGibsTileUrl()}
            maxZoom={9}
            attribution={NASA_GIBS_ATTRIBUTION}
          />
          {/* Detailed OpenStreetMap vector hybrid overlay for parcel precision */}
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{y}/{x}.png"
            opacity={0.45}
            maxZoom={19}
          />

          <MapController center={centerCoords} zoom={isDrawing ? 15 : 13} />
          
          <MapClickHandler
            isDrawing={isDrawing}
            onAddPoint={handleAddPolygonPoint}
            onSetMarker={(lat, lon) => onChange({ latitude: lat, longitude: lon })}
          />

          {/* Marker at current coordinates */}
          {latitude && longitude && (
            <Marker position={[latitude, longitude]} icon={fieldPinIcon} />
          )}

          {/* Drawn Polygon Boundary */}
          {polygonCoords.length >= 3 && (
            <Polygon
              positions={polygonCoords}
              pathOptions={{
                color: '#10b981',
                weight: 3,
                fillColor: '#10b981',
                fillOpacity: 0.35,
                dashArray: isDrawing ? '4, 4' : null
              }}
            />
          )}
        </MapContainer>

        {/* Legend Badge */}
        <div className="absolute bottom-2 left-2 z-[400] bg-black/75 backdrop-blur-md px-2.5 py-1 rounded-lg border border-white/10 text-[10px] font-mono text-emerald-300 flex items-center gap-1.5">
          <MapPin className="w-3 h-3 text-emerald-400" />
          <span>NASA GIBS Satellite (J-2) • Lat: {latitude?.toFixed(4)}, Lon: {longitude?.toFixed(4)}</span>
        </div>
      </div>
    </div>
  );
}
