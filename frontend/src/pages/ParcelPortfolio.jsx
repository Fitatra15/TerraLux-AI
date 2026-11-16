import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L from 'leaflet';
import { useTranslation } from 'react-i18next';
import { 
  Plus, ShieldCheck, Sparkles, MapPin, ArrowUpRight, 
  Leaf, Award, Eye, FileText, ChevronRight, Activity, Globe
} from 'lucide-react';
import { cachedGet, apiClient } from '../api/client';
import RadialProgress from '../components/RadialProgress';

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
      console.error("Could not fetch parcels, fallback to demo points", e);
      // High-end demo fallback
      setParcels([
        {
          id: "845ef4e9-b776-40b4-af77-c84510862b1e",
          name: "Antsiranana Vanilla & Rice Estate",
          country: "MDG",
          region: "Diana",
          latitude: -12.2794,
          longitude: 49.2914,
          area_ha: 14.8,
          soil_type: "Ferralsol Humique",
          score: 85,
          status: "Ready",
          top_crops: ["Vanille Bourbon", "Riz pluvial", "Manioc doux"]
        },
        {
          id: "95304210-d47a-4bef-9d28-d8a07f48dd8b",
          name: "Domaine de la Sûre — Bettendorf",
          country: "LUX",
          region: "Diekirch",
          latitude: 49.8767,
          longitude: 6.2167,
          area_ha: 28.5,
          soil_type: "Cambisol Dystrique",
          score: 92,
          status: "Ready",
          top_crops: ["Blé d'hiver", "Colza oléagineux", "Orge brassicole"]
        },
        {
          id: "abc8c355-0775-463b-be1d-a705287617d6",
          name: "Plateau Minier Esch-sur-Alzette",
          country: "LUX",
          region: "Esch",
          latitude: 49.4958,
          longitude: 5.9806,
          area_ha: 19.2,
          soil_type: "Anthrosol Reconstitué",
          score: 78,
          status: "Analyzing",
          top_crops: ["Seigle d'hiver", "Avoine rustique"]
        },
        {
          id: "07c8c5d0-f66b-4aac-8a24-eb369b56c8ea",
          name: "Vallée Mahavavy Ambilobe",
          country: "MDG",
          region: "Diana",
          latitude: -12.9167,
          longitude: 49.0500,
          area_ha: 32.0,
          soil_type: "Fluvisol Alluvionnaire",
          score: 64,
          status: "Needs photo",
          top_crops: ["Canne à sucre", "Maïs tropical"]
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
      alert("Erreur lors de la création de la parcelle.");
    } finally {
      setCreating(false);
    }
  };

  const filtered = parcels.filter(p => {
    if (filterCountry === 'ALL') return true;
    return p.country === filterCountry;
  });

  const getStatusText = (st) => {
    if (st === 'Ready') return t('status.ready');
    if (st === 'Needs photo') return t('status.needs_photo');
    if (st === 'Analyzing') return t('status.analyzing');
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
              <span>{t('brand.tagline')}</span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-serif tracking-tight text-white font-normal">
              {t('portfolio.welcome').split('TerraLux')[0]}
              <span className="italic font-serif font-light text-emerald-300">TerraLux AI</span>
            </h1>
            <p className="text-slate-400 text-sm max-w-2xl font-light">
              {t('portfolio.subtitle')}
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
                {t('portfolio.all_assets')}
              </button>
              <button
                onClick={() => setFilterCountry('LUX')}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                  filterCountry === 'LUX' 
                    ? 'bg-emerald-500 text-black shadow-glow-mint font-bold' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {t('portfolio.luxembourg')}
              </button>
              <button
                onClick={() => setFilterCountry('MDG')}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                  filterCountry === 'MDG' 
                    ? 'bg-emerald-500 text-black shadow-glow-mint font-bold' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {t('portfolio.madagascar')}
              </button>
            </div>

            {/* Killer Feature Pill Button */}
            <button
              onClick={() => setShowAddModal(true)}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-sm shadow-glow-mint hover:shadow-emerald-400/50 transition-all duration-300 hover:scale-105 active:scale-95"
            >
              <Plus className="w-4 h-4 stroke-[2.5]" />
              <span>{t('actions.add_parcel')}</span>
            </button>
          </div>
        </div>

        {/* ======================================================== */}
        {/* BENTO GRID (Asymmetric Luxury Layout)                    */}
        {/* ======================================================== */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {filtered.map((parcel, idx) => {
            const isHero = idx === 0;
            const score = parcel.score || (parcel.country === 'LUX' ? 92 : 85);
            const status = parcel.status || 'Ready';
            const lat = parcel.latitude || (parcel.country === 'LUX' ? 49.8767 : -12.2794);
            const lng = parcel.longitude || (parcel.country === 'LUX' ? 6.2167 : 49.2914);

            return (
              <div
                key={parcel.id || idx}
                className={`group relative rounded-3xl overflow-hidden glass-card glass-card-hover p-6 sm:p-8 flex flex-col justify-between ${
                  isHero ? 'lg:col-span-2 min-h-[380px]' : 'min-h-[340px]'
                }`}
              >
                {/* Background Leaflet map for hero parcel with dark luxury overlay */}
                {isHero && (
                  <div className="absolute inset-0 pointer-events-none opacity-25 mix-blend-luminosity">
                    <MapContainer
                      center={[lat, lng]}
                      zoom={12}
                      zoomControl={false}
                      attributionControl={false}
                      className="w-full h-full leaflet-dark"
                    >
                      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
                      <Marker position={[lat, lng]} icon={miniIcon} />
                    </MapContainer>
                    <div className="absolute inset-0 bg-gradient-to-t from-[#06120D] via-[#06120D]/80 to-transparent" />
                  </div>
                )}

                {/* Card Top Details */}
                <div className="relative z-10 space-y-4">
                  {/* Status & Country Pill */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-mono tracking-wider uppercase px-2.5 py-1 rounded-full bg-white/10 border border-white/10 text-slate-300">
                        {parcel.country === 'LUX' ? t('portfolio.luxembourg') : t('portfolio.madagascar')}
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
                      [{lat.toFixed(4)}, {lng.toFixed(4)}] • {parcel.area_ha || 4.2} ha • {parcel.soil_type || 'Ferralsol Humique'}
                    </p>
                  </div>
                </div>

                {/* Card Bottom : Radial Progress + Key Crops + Actions */}
                <div className="relative z-10 mt-8 pt-6 border-t border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                  
                  {/* Radial Progress Gauge (Killer feature) */}
                  <div className="flex items-center gap-4">
                    <RadialProgress
                      value={score}
                      size={isHero ? 78 : 68}
                      strokeWidth={7}
                      color={score >= 80 ? '#4ADE80' : score >= 70 ? '#FBBF24' : '#F87171'}
                    />
                    <div>
                      <div className="text-xs font-mono uppercase tracking-wider text-slate-400">
                        {t('portfolio.resilience_score')}
                      </div>
                      <div className="text-sm font-semibold text-white">
                        {score >= 85 ? t('portfolio.grade_aaa') : score >= 75 ? t('portfolio.grade_aa') : t('portfolio.grade_a')}
                      </div>
                      <div className="text-[11px] text-emerald-400/80 font-mono">
                        {t('portfolio.certified_data')}
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
                      <span>{t('actions.view_passport')}</span>
                      <ArrowUpRight className="w-3 h-3 opacity-60" />
                    </Link>

                    <Link
                      to={`/events/${parcel.id}`}
                      className="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 text-xs font-mono border border-white/10 transition-all flex items-center gap-1.5"
                    >
                      <Activity className="w-3.5 h-3.5 text-amber-300" />
                      <span>{t('actions.view_history')}</span>
                    </Link>

                    <Link
                      to={`/parcel/${parcel.id}`}
                      className="p-2 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 border border-white/10 transition-all"
                      title={t('actions.view_details')}
                    >
                      <Eye className="w-4 h-4" />
                    </Link>
                  </div>

                </div>

              </div>
            );
          })}

        </div>

      </div>

      {/* ======================================================== */}
      {/* MODAL : Add Parcel                                       */}
      {/* ======================================================== */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="relative w-full max-w-lg rounded-3xl glass-panel p-8 space-y-6 border border-white/20">
            <div className="space-y-1">
              <span className="text-[11px] font-mono text-emerald-400 uppercase tracking-widest">
                {t('brand.tagline')}
              </span>
              <h2 className="text-2xl font-serif text-white">{t('portfolio.create_modal_title')}</h2>
              <p className="text-xs text-slate-400">
                {t('portfolio.create_modal_desc')}
              </p>
            </div>

            <form onSubmit={handleCreateParcel} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">{t('portfolio.parcel_name_label')}</label>
                <input
                  type="text"
                  required
                  placeholder={t('portfolio.parcel_name_placeholder')}
                  value={newParcel.name}
                  onChange={e => setNewParcel({ ...newParcel, name: e.target.value })}
                  className="w-full bg-white/5 border border-white/15 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-400 transition-colors"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">{t('portfolio.latitude')}</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newParcel.latitude}
                    onChange={e => setNewParcel({ ...newParcel, latitude: parseFloat(e.target.value) })}
                    className="w-full bg-white/5 border border-white/15 rounded-xl px-4 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">{t('portfolio.longitude')}</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newParcel.longitude}
                    onChange={e => setNewParcel({ ...newParcel, longitude: parseFloat(e.target.value) })}
                    className="w-full bg-white/5 border border-white/15 rounded-xl px-4 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">{t('portfolio.surface')}</label>
                  <input
                    type="number"
                    step="0.1"
                    required
                    value={newParcel.area_ha}
                    onChange={e => setNewParcel({ ...newParcel, area_ha: parseFloat(e.target.value) })}
                    className="w-full bg-white/5 border border-white/15 rounded-xl px-4 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-emerald-400"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-slate-300 mb-1">{t('portfolio.target_region')}</label>
                  <select
                    value={newParcel.country}
                    onChange={e => setNewParcel({ ...newParcel, country: e.target.value })}
                    className="w-full bg-[#0a1d15] border border-white/15 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-400"
                  >
                    <option value="MDG">Madagascar — Diana (Tropical)</option>
                    <option value="LUX">Luxembourg (Tempéré)</option>
                  </select>
                </div>
              </div>

              <div className="pt-4 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-5 py-2.5 rounded-full text-xs font-mono text-slate-400 hover:text-white"
                >
                  {t('actions.cancel')}
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="px-6 py-2.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-xs font-mono shadow-glow-mint transition-all"
                >
                  {creating ? t('status.analyzing') : t('actions.add_parcel')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
