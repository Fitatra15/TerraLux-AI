import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { MapPin, Search, ArrowRight, ShieldCheck, Globe, Sparkles, Navigation, PlusCircle } from 'lucide-react';
import { apiClient } from '../api/client';
import { getNasaGibsTileUrl, NASA_GIBS_ATTRIBUTION } from '../utils/nasaGibs';

// Custom marker icon
const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Exploitations de référence
const REFERENCE_LOCATIONS = [
  { name: 'Exploitation Luxembourg-Centre', country: 'LUX', region: 'Gutland', lat: 49.6116, lng: 6.1319, type: 'Plateau tempéré céréalier (Cambisol)' },
  { name: 'Domaine Esch-sur-Alzette', country: 'LUX', region: 'Minett', lat: 49.4958, lng: 5.9806, type: 'Bassin sédimentaire (Luvisol)' },
  { name: 'Exploitation Antsiranana (Diana)', country: 'MDG', region: 'Diana', lat: -12.2794, lng: 49.2914, type: 'Tropical volcanique (Ferralsol)' },
  { name: 'Domaine Nosy Be', country: 'MDG', region: 'Diana', lat: -13.3167, lng: 48.2667, type: 'Insulaire agroforestier' },
  { name: 'Exploitation Sambirano (Ambanja)', country: 'MDG', region: 'Diana', lat: -13.6786, lng: 48.4522, type: 'Cacaoyères alluviales (Fluvisol)' },
  { name: 'Domaine Ambilobe', country: 'MDG', region: 'Diana', lat: -13.2000, lng: 49.0500, type: 'Plaine vertique (Vertisol)' }
];

function LocationMarker({ position, setPosition }) {
  useMapEvents({
    click(e) {
      setPosition([e.latlng.lat, e.latlng.lng]);
    },
  });

  return position === null ? null : (
    <Marker position={position} icon={customIcon}>
      <Popup>
        <span className="font-semibold text-xs text-forest">
          Parcelle sélectionnée : [{position[0].toFixed(4)}, {position[1].toFixed(4)}]
        </span>
      </Popup>
    </Marker>
  );
}

export default function Home() {
  const navigate = useNavigate();
  const [position, setPosition] = useState([49.6116, 6.1319]); // Luxembourg par défaut
  const [parcelName, setParcelName] = useState('Exploitation Luxembourg-Centre');
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSelectLocation = (p) => {
    setPosition([p.lat, p.lng]);
    setParcelName(p.name);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await apiClient.post('/parcels', {
        name: parcelName,
        latitude: position[0],
        longitude: position[1],
        area_ha: 2.5
      });
      navigate(`/parcel/${res.data.id}`);
    } catch (err) {
      console.error(err);
      navigate('/parcels');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Hero Banner */}
      <div className="bg-gradient-to-r from-forest to-forest-light rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 opacity-10 pointer-events-none flex items-center pr-10">
          <Globe className="w-96 h-96 text-sand" />
        </div>
        
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 bg-sand/20 border border-sand/30 rounded-full px-3 py-1 text-xs text-sand font-medium backdrop-blur-xs">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            <span>Moteur agronomique multimodal Luxembourg & Diana (Madagascar)</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight">
            Décision agronomique explicable, appuyée par la science.
          </h1>

          <p className="text-sm sm:text-base text-sand/90 font-light leading-relaxed">
            TerraLux AI croise les données satellitaires <strong>NASA POWER (30 ans)</strong>, les cartes mondiales <strong>SoilGrids (ISRIC)</strong> et les exigences <strong>FAO ECOCROP</strong> pour guider le choix des cultures et sécuriser vos rendements.
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => {
                const el = document.getElementById('parcel-name-input');
                if (el) el.focus();
              }}
              className="px-5 py-2.5 rounded-full bg-accent hover:bg-emerald-400 text-forest font-bold text-xs shadow-lg transition-all flex items-center gap-2"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Créer ma parcelle</span>
            </button>
            <button
              onClick={() => navigate('/parcels')}
              className="px-5 py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white font-medium text-xs backdrop-blur-xs border border-white/20 transition-all flex items-center gap-2"
            >
              <span>Voir le portfolio d'exploitations</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid : Controls + Map */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column: Preset Points & Action */}
        <div className="space-y-4">
          
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-200 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-forest uppercase tracking-wider flex items-center gap-2">
                <Navigation className="w-4 h-4 text-accent" />
                <span>1. Choisissez ou pointez une parcelle</span>
              </h2>
            </div>

            {/* Quick Location Buttons */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-500">Exploitations de référence vérifiées :</label>
              <div className="grid grid-cols-1 gap-2">
                {REFERENCE_LOCATIONS.map((p, i) => (
                  <button
                    key={i}
                    onClick={() => handleSelectLocation(p)}
                    className={`w-full text-left p-3 rounded-xl border text-xs transition-all flex items-center justify-between ${
                      Math.abs(position[0] - p.lat) < 0.001 && Math.abs(position[1] - p.lng) < 0.001
                        ? 'border-forest bg-forest/5 font-semibold text-forest shadow-xs'
                        : 'border-gray-200 hover:border-forest/40 hover:bg-gray-50 text-gray-700'
                    }`}
                  >
                    <div>
                      <div className="font-bold flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-accent"></span>
                        {p.name}
                        <span className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.2 rounded font-mono">
                          {p.country}
                        </span>
                      </div>
                      <span className="text-[11px] text-gray-500">{p.type}</span>
                    </div>
                    <MapPin className="w-4 h-4 text-forest/40 shrink-0" />
                  </button>
                ))}
              </div>
            </div>

            {/* Selected Coordinates */}
            <div className="p-3 bg-sand/30 rounded-xl border border-sand-dark/30 space-y-1">
              <span className="text-[11px] font-semibold text-forest uppercase tracking-wider block">
                Coordonnées GPS de l'épingle :
              </span>
              <div className="font-mono text-xs text-gray-800 flex justify-between">
                <span>Lat: {position[0].toFixed(4)}°</span>
                <span>Lng: {position[1].toFixed(4)}°</span>
              </div>
            </div>

            {/* Name Input */}
            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-600">Nom de la parcelle / exploitation :</label>
              <input
                id="parcel-name-input"
                type="text"
                value={parcelName}
                onChange={(e) => setParcelName(e.target.value)}
                placeholder="ex. Domaine de Grevenmacher"
                className="w-full bg-gray-50 border border-gray-300 rounded-xl px-3 py-2 text-xs focus:ring-2 focus:ring-forest focus:outline-none"
              />
            </div>

            {/* Action Button */}
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full py-3.5 bg-forest hover:bg-forest-light text-sand font-bold text-sm rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 transform active:scale-98 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-sand border-t-transparent rounded-full animate-spin" />
                  <span>Analyse du sol (SoilGrids) & climat (NASA)...</span>
                </>
              ) : (
                <>
                  <PlusCircle className="w-4 h-4 text-accent" />
                  <span>Créer & Analyser ma parcelle</span>
                  <ArrowRight className="w-4 h-4 text-accent" />
                </>
              )}
            </button>

          </div>

        </div>

        {/* Right Column: Interactive Map */}
        <div className="lg:col-span-2 bg-white rounded-2xl p-4 shadow-sm border border-gray-200 flex flex-col h-[580px]">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-accent" />
              <span className="text-xs font-bold text-gray-800">
                Pointez une parcelle sur l'imagerie satellite NASA EOSDIS GIBS
              </span>
            </div>
            <span className="text-[11px] text-gray-400">NASA GIBS MODIS TrueColor</span>
          </div>

          <div className="flex-1 mt-3 rounded-xl overflow-hidden relative shadow-inner">
            <MapContainer
              center={position}
              zoom={5}
              scrollWheelZoom={true}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution={NASA_GIBS_ATTRIBUTION}
                url={getNasaGibsTileUrl()}
                maxNativeZoom={9}
                maxZoom={18}
              />
              <LocationMarker position={position} setPosition={setPosition} />
            </MapContainer>
          </div>
        </div>

      </div>

    </div>
  );
}
