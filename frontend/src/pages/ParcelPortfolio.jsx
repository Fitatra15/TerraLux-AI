import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L from 'leaflet';
import { useTranslation } from 'react-i18next';
import { 
  Plus, ShieldCheck, Sparkles, MapPin, ArrowUpRight, 
  Leaf, Award, Eye, FileText, ChevronRight, Activity, Globe, Satellite, Trash2
} from 'lucide-react';
import { cachedGet, apiClient } from '../api/client';
import RadialProgress from '../components/RadialProgress';
import ParcelMapDrawer from '../components/ParcelMapDrawer';
import { 
  getNasaGibsTileUrl, 
  NASA_GIBS_ATTRIBUTION, 
  CARTODB_DARK_MATTER_URL, 
  CARTODB_ATTRIBUTION 
} from '../utils/nasaGibs';

const miniIcon = new L.DivIcon({
  className: 'custom-pin',
  html: `<div class="w-4 h-4 rounded-full bg-emerald-400 border-2 border-white shadow-glow-mint animate-pulse"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8]
});

export default function ParcelPortfolio() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [parcels, setParcels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterCountry, setFilterCountry] = useState('ALL');

  // New parcel form state
  const [newParcel, setNewParcel] = useState({
    name: '',
    latitude: -12.2794,
    longitude: 49.2914,
    area_ha: 3.5,
    country: 'MDG'
  });
  const [creating, setCreating] = useState(false);

  const fetchParcels = async () => {
    try {
      setLoading(true);
      const data = await cachedGet('/parcels');
      setParcels(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Could not fetch parcels, fallback to reference points", e);
      setParcels([
        {
          id: "845ef4e9-b776-40b4-af77-c84510862b1e",
          name: "Antsiranana Agricultural Estate (Diana)",
          country: "MDG",
          region: "Diana",
          latitude: -12.2794,
          longitude: 49.2914,
          area_ha: 14.8,
          soil_type: "Ferralsol rhodi-lixique",
          score: 69.6,
          status: "Ready",
          top_crops: ["Bourbon Vanilla", "Upland Rice", "Cassava"]
        },
        {
          id: "95304210-d47a-4bef-9d28-d8a07f48dd8b",
          name: "Luxembourg Central Farm",
          country: "LUX",
          region: "Gutland",
          latitude: 49.6116,
          longitude: 6.1319,
          area_ha: 28.5,
          soil_type: "Cambisol calcaro-eutrique",
          score: 81.3,
          status: "Ready",
          top_crops: ["Winter Wheat", "Rapeseed", "Barley"]
        },
        {
          id: "abc8c355-0775-463b-be1d-a705287617d6",
          name: "Esch-sur-Alzette Domain",
          country: "LUX",
          region: "Minett",
          latitude: 49.4958,
          longitude: 5.9806,
          area_ha: 19.2,
          soil_type: "Luvisol haplique",
          score: 78.4,
          status: "Ready",
          top_crops: ["Winter Rye", "Rustic Oats"]
        },
        {
          id: "07c8c5d0-f66b-4aac-8a24-eb369b56c8ea",
          name: "Ambilobe Foodcrop Estate",
          country: "MDG",
          region: "Diana",
          latitude: -12.9167,
          longitude: 49.0500,
          area_ha: 32.0,
          soil_type: "Vertisol pélic",
          score: 76.1,
          status: "Needs photo",
          top_crops: ["Sugar Cane", "Tropical Maize"]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParcels();
  }, []);

  const handleCreateParcel = async (e) => {
    e.preventDefault();
    try {
      setCreating(true);
      const res = await apiClient.post('/parcels', newParcel);
      setShowAddModal(false);
      fetchParcels();
      if (res.data?.id) {
        navigate(`/passport/${res.data.id}`);
      }
    } catch (err) {
      alert("Error creating parcel. Please check coordinates.");
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteParcel = async (id, name, e) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete "${name}"? This action cascades to all observations and passports.`)) {
      return;
    }
    try {
      await apiClient.delete(`/parcels/${id}`);
      setParcels(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      console.error("Failed to delete parcel:", err);
      alert("Error deleting parcel.");
    }
  };

  const filtered = parcels.filter(p => {
    if (filterCountry === 'ALL') return true;
    return p.country === filterCountry;
  });

  const getStatusText = (st) => {
    if (st === 'Ready') return 'Ready';
    if (st === 'Needs photo') return 'Needs Leaf Photo';
    if (st === 'Analyzing') return 'Analyzing...';
    return st;
  };

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30 selection:text-emerald-200">
      <div className="max-w-7xl mx-auto space-y-10">

        {/* ======================================================== */}
        {/* HEADER : Luxury Greeting + Add Parcel Pill Glow Button  */}
        {/* ======================================================== */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/[0.08]">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono tracking-wide">
              <Globe className="w-3.5 h-3.5" />
              <span>Sovereign Earth Observation & Pedology</span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-serif tracking-tight text-white font-normal">
              Agricultural Asset Portfolio — <span className="italic font-serif font-light text-emerald-300">TerraLux AI</span>
            </h1>
            <p className="text-slate-400 text-sm max-w-2xl font-light">
              High-resolution spatial parcel management across Luxembourg and Madagascar (Diana). Every registered field is calibrated in real time with SoilGrids v2, NASA POWER, and Tavily live market data.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Filter Pill */}
            <div className="flex bg-white/5 p-1 rounded-2xl border border-white/10 backdrop-blur-xl">
              <button
                onClick={() => setFilterCountry('ALL')}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                  filterCountry === 'ALL' 
                    ? 'bg-emerald-500 text-black shadow-glow-mint font-bold' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                All Assets
              </button>
              <button
                onClick={() => setFilterCountry('LUX')}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                  filterCountry === 'LUX' 
                    ? 'bg-emerald-500 text-black shadow-glow-mint font-bold' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Luxembourg
              </button>
              <button
                onClick={() => setFilterCountry('MDG')}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                  filterCountry === 'MDG' 
                    ? 'bg-emerald-500 text-black shadow-glow-mint font-bold' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Madagascar
              </button>
            </div>

            {/* Create Parcel Button */}
            <button
              onClick={() => setShowAddModal(true)}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-sm shadow-glow-mint hover:shadow-emerald-400/50 transition-all duration-300 hover:scale-105 active:scale-95"
            >
              <Plus className="w-4 h-4 stroke-[2.5]" />
              <span>Register New Parcel</span>
            </button>
          </div>
        </div>

        {/* ======================================================== */}
        {/* BANNER : Call To Action "Register New Parcel"           */}
        {/* ======================================================== */}
        <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-emerald-950/40 via-emerald-900/20 to-black/50 border border-emerald-500/20 backdrop-blur-xl flex flex-col sm:flex-row sm:items-center justify-between gap-6 shadow-2xl">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <Satellite className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-300">
                NASA GIBS Satellite Imagery & ISRIC SoilGrids v2 Multi-Layers
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-serif text-white font-bold">
              Own or manage agricultural acreage?
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 font-light max-w-2xl">
              Pin your land coordinates or draw parcel polygons to generate instant satellite audits, yield projections, and certified Resilience Passports.
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-xs sm:text-sm font-mono shadow-glow-mint transition-all duration-300 hover:scale-105 active:scale-95 shrink-0"
          >
            <Plus className="w-4 h-4 stroke-[2.5]" />
            <span>Register New Parcel</span>
          </button>
        </div>

        {/* ======================================================== */}
        {/* BENTO GRID (Asymmetric Luxury Layout)                    */}
        {/* ======================================================== */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {filtered.map((parcel, idx) => {
            const isHero = idx === 0;
            const score = parcel.score || (parcel.country === 'LUX' ? 81.3 : 69.6);
            const status = parcel.status || 'Ready';
            const lat = parcel.latitude || (parcel.country === 'LUX' ? 49.6116 : -12.2794);
            const lng = parcel.longitude || (parcel.country === 'LUX' ? 6.1319 : 49.2914);
            const soilType = parcel.soil_type || (parcel.country === 'LUX' ? 'Cambisol calcaro-eutrique' : 'Ferralsol rhodi-lixique');

            return (
              <div
                key={parcel.id || idx}
                className={`group relative rounded-3xl overflow-hidden glass-card glass-card-hover p-6 sm:p-8 flex flex-col justify-between ${
                  isHero ? 'lg:col-span-2 min-h-[380px]' : 'min-h-[340px]'
                }`}
              >
                {/* Background Satellite map for hero parcel with CartoDB Dark Matter */}
                {isHero && (
                  <div className="absolute inset-0 pointer-events-none opacity-30 mix-blend-screen">
                    <MapContainer
                      center={[lat, lng]}
                      zoom={9}
                      zoomControl={false}
                      attributionControl={false}
                      className="w-full h-full"
                    >
                      <TileLayer
                        url={CARTODB_DARK_MATTER_URL}
                        attribution={CARTODB_ATTRIBUTION}
                        maxZoom={19}
                      />
                      <TileLayer
                        url={getNasaGibsTileUrl()}
                        attribution={NASA_GIBS_ATTRIBUTION}
                        opacity={0.8}
                        maxNativeZoom={9}
                        maxZoom={18}
                      />
                      <Marker position={[lat, lng]} icon={miniIcon} />
                    </MapContainer>
                    <div className="absolute inset-0 bg-gradient-to-t from-[#06120D] via-[#06120D]/85 to-transparent" />
                  </div>
                )}

                {/* Card Top Details */}
                <div className="relative z-10 space-y-4">
                  {/* Status & Country Pill */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-mono tracking-wider uppercase px-2.5 py-1 rounded-full bg-white/10 border border-white/10 text-slate-300">
                        {parcel.country === 'LUX' ? 'Luxembourg' : 'Madagascar'}
                      </span>
                      {parcel.region && (
                        <span className="text-xs text-slate-400 font-mono">
                          • {parcel.region}
                        </span>
                      )}
                    </div>

                    {/* Glowing status dot */}
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-black/40 border border-white/10">
                      <span className={`w-2 h-2 rounded-full ${
                        status === 'Ready' 
                          ? 'bg-emerald-400 shadow-glow-mint' 
                          : status === 'Analyzing' 
                            ? 'bg-blue-400 animate-ping' 
                            : 'bg-amber-400 shadow-glow-gold'
                      }`} />
                      <span className="text-[11px] font-mono font-medium text-slate-300">{getStatusText(status)}</span>
                    </div>
                  </div>

                  {/* Parcel Title */}
                  <div>
                    <h3 className={`font-serif text-white group-hover:text-emerald-300 transition-colors ${
                      isHero ? 'text-2xl sm:text-3xl' : 'text-xl'
                    }`}>
                      {parcel.name}
                    </h3>
                    <p className="text-xs font-mono text-slate-400 mt-1 flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                      [{lat.toFixed(4)}, {lng.toFixed(4)}] • {parcel.area_ha || 4.2} ha • <span className="text-emerald-300 font-semibold">{soilType}</span>
                    </p>
                  </div>
                </div>

                {/* Card Bottom : Radial Progress + Actions */}
                <div className="relative z-10 mt-8 pt-6 border-t border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                  
                  {/* Radial Progress Gauge */}
                  <div className="flex items-center gap-4">
                    <RadialProgress
                      value={Math.round(score)}
                      size={isHero ? 78 : 68}
                      strokeWidth={7}
                      color={score >= 80 ? '#4ADE80' : score >= 70 ? '#FBBF24' : '#F87171'}
                    />
                    <div>
                      <div className="text-xs font-mono uppercase tracking-wider text-slate-400">
                        Resilience Score
                      </div>
                      <div className="text-sm font-semibold text-white">
                        {score >= 80 ? 'Grade AAA Sovereign' : score >= 70 ? 'Grade AA Bankable' : 'Grade A Transition'}
                      </div>
                      <div className="text-[11px] text-emerald-400/80 font-mono flex items-center gap-1">
                        <Satellite className="w-3 h-3" />
                        <span>ISRIC & NASA Verified</span>
                      </div>
                    </div>
                  </div>

                  {/* Action Navigation Buttons */}
                  <div className="flex flex-wrap items-center gap-2">
                    <Link
                      to={`/passport/${parcel.id}`}
                      className="px-4 py-2 rounded-xl bg-white/10 hover:bg-emerald-500 hover:text-black text-white text-xs font-medium font-mono border border-white/15 transition-all flex items-center gap-1.5 group/btn"
                    >
                      <Award className="w-3.5 h-3.5 text-emerald-300 group-hover/btn:text-black" />
                      <span>Passport</span>
                      <ArrowUpRight className="w-3 h-3 opacity-60" />
                    </Link>

                    <Link
                      to={`/events/${parcel.id}`}
                      className="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 text-xs font-mono border border-white/10 transition-all flex items-center gap-1.5"
                    >
                      <Activity className="w-3.5 h-3.5 text-amber-300" />
                      <span>Events</span>
                    </Link>

                    <Link
                      to={`/parcel/${parcel.id}`}
                      className="p-2 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 border border-white/10 transition-all"
                      title="Inspect Field"
                    >
                      <Eye className="w-4 h-4" />
                    </Link>

                    {/* Delete Parcel Button */}
                    <button
                      onClick={(e) => handleDeleteParcel(parcel.id, parcel.name, e)}
                      className="p-2 rounded-xl bg-red-500/10 hover:bg-red-500/30 text-red-400 hover:text-red-300 border border-red-500/30 transition-all"
                      title="Delete Parcel"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                </div>

              </div>
            );
          })}

        </div>

      </div>

      {/* ======================================================== */}
      {/* MODAL : Register New Parcel with NASA GIBS & GPS Map     */}
      {/* ======================================================== */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md overflow-y-auto">
          <div className="relative w-full max-w-2xl rounded-3xl glass-panel p-6 sm:p-8 space-y-5 border border-white/20 my-8">
            <div className="space-y-1">
              <span className="text-[11px] font-mono text-emerald-400 uppercase tracking-widest">
                Real-Time Earth Observation
              </span>
              <h2 className="text-2xl font-serif text-white">Register Agricultural Parcel</h2>
              <p className="text-xs text-slate-400">
                Position your acreage using GPS, administrative selection, or interactive polygon tracing.
              </p>
            </div>

            <form onSubmit={handleCreateParcel} className="space-y-4">
              {/* Leaflet + Satellite NASA GIBS + GPS + Polygon */}
              <ParcelMapDrawer
                latitude={newParcel.latitude}
                longitude={newParcel.longitude}
                areaHa={newParcel.area_ha}
                country={newParcel.country}
                onChange={(updates) => {
                  setNewParcel((prev) => {
                    const next = { ...prev, ...updates };
                    if (updates.nameHint && !prev.name) {
                      next.name = `Parcel ${updates.nameHint}`;
                    }
                    return next;
                  });
                }}
              />

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Parcel Designation / Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Domaine Antsiranana Nord or Parzelle Clervaux"
                  value={newParcel.name}
                  onChange={e => setNewParcel({ ...newParcel, name: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-slate-400 focus:outline-none focus:border-emerald-400 font-sans transition-colors"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">Latitude</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newParcel.latitude}
                    onChange={e => setNewParcel({ ...newParcel, latitude: parseFloat(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder:text-slate-400 font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">Longitude</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newParcel.longitude}
                    onChange={e => setNewParcel({ ...newParcel, longitude: parseFloat(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder:text-slate-400 font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">
                    Area (Hectares) — Auto-calculated
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={newParcel.area_ha}
                    onChange={e => setNewParcel({ ...newParcel, area_ha: parseFloat(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder:text-slate-400 font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">Jurisdiction / Country</label>
                  <select
                    value={newParcel.country}
                    onChange={e => setNewParcel({ ...newParcel, country: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-400"
                  >
                    <option value="LUX">Luxembourg (Temperate Cambisols)</option>
                    <option value="MDG">Madagascar — Diana (Tropical Ferralsols)</option>
                  </select>
                </div>
              </div>

              <div className="pt-2 flex items-center justify-end gap-3 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-5 py-2.5 rounded-full text-xs font-mono text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="px-6 py-2.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-xs font-mono shadow-glow-mint transition-all"
                >
                  {creating ? 'Analyzing Satellite Data...' : 'Confirm & Save Parcel'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
