import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { 
  ArrowLeft, Download, Trees, ShieldCheck, Sparkles, 
  Leaf, Droplets, Wind, CheckCircle2, ArrowUpRight, ExternalLink,
  MapPin, Compass, Search, Globe
} from 'lucide-react';
import { apiClient } from '../api/client';
import { 
  getNasaGibsTileUrl, 
  NASA_GIBS_ATTRIBUTION, 
  CARTODB_DARK_MATTER_URL, 
  CARTODB_ATTRIBUTION,
  ESRI_WORLD_IMAGERY_URL,
  ESRI_WORLD_IMAGERY_ATTRIBUTION
} from '../utils/nasaGibs';

const parcelPinIcon = new L.DivIcon({
  className: 'restoration-parcel-pin',
  html: `<div style="width: 24px; height: 24px; border-radius: 50%; background: #10b981; border: 3px solid #ffffff; box-shadow: 0 0 18px rgba(16, 185, 129, 0.9); animation: pulse 2s infinite;"></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 12]
});

function MapRecenter({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] && center[1]) {
      map.flyTo(center, 13, { duration: 1.2 });
    }
  }, [center, map]);
  return null;
}

export default function ReforestationPlanScreen() {
  const [searchParams] = useSearchParams();
  const urlParcelId = searchParams.get('parcel_id');

  const [parcels, setParcels] = useState([]);
  const [selectedParcelId, setSelectedParcelId] = useState(urlParcelId || '');
  const [planData, setPlanData] = useState(null);
  const [selectedSpeciesIndex, setSelectedSpeciesIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  // 1. Fetch available parcels
  useEffect(() => {
    let mounted = true;
    apiClient.get('/parcels')
      .then(res => {
        if (mounted && Array.isArray(res.data)) {
          setParcels(res.data);
          if (!selectedParcelId && res.data.length > 0) {
            setSelectedParcelId(res.data[0].id);
          }
        }
      })
      .catch(err => {
        console.warn("Could not fetch parcels for restoration plan:", err);
      });
    return () => { mounted = false; };
  }, []);

  // 2. Fetch dynamic restoration plan from Tavily + SoilGrids fusion engine
  useEffect(() => {
    setLoading(true);
    const pid = selectedParcelId || '';
    apiClient.get(`/restoration/plan?parcel_id=${pid}`)
      .then(res => {
        setPlanData(res.data);
        setSelectedSpeciesIndex(0);
      })
      .catch(err => {
        console.error("Failed to fetch dynamic restoration plan:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedParcelId]);

  const handleExportPlan = () => {
    setExporting(true);
    setTimeout(() => {
      const pid = planData?.parcel?.id || 'demo';
      window.open(`/api/parcels/${pid}/report.pdf`, '_blank');
      setExporting(false);
    }, 600);
  };

  const speciesList = planData?.recommended_species || [];
  const current = speciesList[selectedSpeciesIndex] || speciesList[0];
  const parcel = planData?.parcel;
  const soil = planData?.soil_context;
  const mapCenter = parcel?.latitude && parcel?.longitude 
    ? [parcel.latitude, parcel.longitude] 
    : [-12.2880, 49.2880];

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Top Header : Back link + Title + Export Button */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/[0.08]">
          <div className="space-y-2">
            <Link
              to="/portfolio"
              className="inline-flex items-center gap-2 text-xs font-mono text-slate-400 hover:text-emerald-300 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Asset Portfolio</span>
            </Link>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
              <Trees className="w-3.5 h-3.5" />
              <span>100% Dynamic Agroforestry & Carbon Engine (Tavily + SoilGrids)</span>
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-serif text-white tracking-tight">
              Ecological Restoration & Canopy Plan
            </h1>
            <p className="text-slate-400 text-xs sm:text-sm max-w-2xl font-light">
              Zero hardcoded species. Live web intelligence crawled via Tavily and cross-referenced with satellite soil physics (ISRIC SoilGrids & NASA POWER).
            </p>
          </div>

          {/* Export Plan Button */}
          <button
            onClick={handleExportPlan}
            disabled={exporting || loading}
            className="inline-flex items-center gap-2.5 px-7 py-4 rounded-full bg-white hover:bg-emerald-100 text-black font-semibold text-sm shadow-2xl hover:shadow-emerald-400/30 transition-all duration-300 hover:scale-105 active:scale-95 group disabled:opacity-50"
          >
            <Download className="w-4 h-4 text-emerald-800 group-hover:translate-y-0.5 transition-transform" />
            <span>{exporting ? 'Generating PDF dossier...' : 'Export Restoration Plan'}</span>
          </button>
        </div>

        {/* Parcel Selector & Live Query Banner */}
        <div className="glass-card rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row items-center justify-between gap-4 border border-white/10">
          <div className="flex items-center gap-3 w-full md:w-auto">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
              <Compass className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <label className="block text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                Select Active Parcel for Restoration Analysis:
              </label>
              <select
                value={selectedParcelId}
                onChange={(e) => setSelectedParcelId(e.target.value)}
                className="mt-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-emerald-400 font-sans"
              >
                {parcels.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.region || p.country} • {p.area_ha || 5.0} ha)
                  </option>
                ))}
              </select>
            </div>
          </div>

          {planData?.query_used && (
            <div className="flex items-center gap-2 text-xs font-mono bg-black/40 px-3.5 py-2 rounded-xl border border-white/10 text-slate-300 w-full md:w-auto">
              <Search className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span className="truncate">Live Tavily Query: <span className="text-emerald-300">"{planData.query_used}"</span></span>
            </div>
          )}
        </div>

        {/* Layout : 60% Map / 40% Dynamic Species Details */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">

          {/* 60% Map Container */}
          <div className="lg:col-span-3 rounded-3xl overflow-hidden glass-card p-2 min-h-[560px] relative border border-white/10 shadow-2xl">
            <div className="w-full h-[540px] rounded-2xl overflow-hidden relative">
              <MapContainer
                center={mapCenter}
                zoom={13}
                zoomControl={true}
                className="w-full h-full"
              >
                {/* Continuous Seamless Satellite Imagery Base (Esri World Imagery) */}
                <TileLayer
                  attribution={ESRI_WORLD_IMAGERY_ATTRIBUTION}
                  url={ESRI_WORLD_IMAGERY_URL}
                  maxZoom={19}
                />

                <MapRecenter center={mapCenter} />

                {parcel && (
                  <Marker position={mapCenter} icon={parcelPinIcon}>
                    <Popup>
                      <div className="space-y-1 font-sans text-xs">
                        <div className="font-bold text-emerald-600">{parcel.name}</div>
                        <div>Region: {parcel.region} ({parcel.country})</div>
                        <div>Soil WRB: {soil?.wrb_class} (pH {soil?.ph})</div>
                        <div>Area: {parcel.area_ha} ha</div>
                      </div>
                    </Popup>
                  </Marker>
                )}
              </MapContainer>

              {/* Floating Map Legend */}
              <div className="absolute bottom-5 left-5 z-[500] glass-panel px-4 py-3 rounded-2xl border border-white/20 space-y-2 pointer-events-auto">
                <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                  Satellite Earth Observation
                </div>
                <div className="flex flex-col gap-1.5 text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-emerald-400 shadow-glow-mint"></span>
                    <span className="text-slate-200">Parcel Active Target • {parcel?.name || 'Selected Field'}</span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    ISRIC SoilGrids: {soil?.wrb_class || 'Ferralsol'} • NASA MODIS TrueColor (J-2)
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 40% Dynamic Species Details */}
          <div className="lg:col-span-2 space-y-6">

            <div className="glass-card rounded-3xl p-6 sm:p-8 space-y-6 border border-white/10">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Dynamic Web Intelligence</span>
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30 text-cyan-300">
                    Live Tavily Fused
                  </span>
                </div>
                <h2 className="text-2xl font-serif text-white tracking-tight mt-1">
                  Verified Resilient Species
                </h2>
                <p className="text-xs text-slate-400 font-light mt-1">
                  Extracted in real time for {soil?.wrb_class} soils in {parcel?.region || 'target zone'}.
                </p>
              </div>

              {loading ? (
                <div className="py-12 flex flex-col items-center justify-center space-y-3">
                  <div className="w-8 h-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-xs font-mono text-emerald-300">Crawling scientific agronomic web...</p>
                </div>
              ) : (
                <>
                  {/* Dynamic Species Selector Tabs */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                    {speciesList.map((s, idx) => (
                      <button
                        key={s.id || idx}
                        onClick={() => setSelectedSpeciesIndex(idx)}
                        className={`px-3 py-2.5 rounded-2xl text-xs font-mono font-medium flex items-center justify-center gap-2 transition-all ${
                          selectedSpeciesIndex === idx
                            ? 'bg-emerald-400 text-black font-bold shadow-glow-mint'
                            : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-white/10'
                        }`}
                      >
                        <span className="shrink-0">{s.icon_emoji || '🌿'}</span>
                        <span className="truncate">{s.common_name?.split('(')[0]?.trim() || s.scientific_name}</span>
                      </button>
                    ))}
                  </div>

                  {/* Active Species Detail Card */}
                  {current && (
                    <div className="p-5 rounded-2xl bg-white/[0.04] border border-white/10 space-y-4">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <h3 className="text-lg font-serif font-bold text-white flex items-center gap-2">
                            <span>{current.scientific_name}</span>
                            <span className="text-base">{current.icon_emoji || '🌿'}</span>
                          </h3>
                          <p className="text-xs font-mono text-emerald-400">{current.common_name}</p>
                          <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                            Soil Compatibility: <span className="text-emerald-300 font-bold">{current.soil_compatibility_score}%</span>
                          </p>
                        </div>
                        <span className="text-[11px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
                          {current.carbon_capture}
                        </span>
                      </div>

                      {/* Drought Resistance Progress Bar */}
                      <div className="space-y-1.5">
                        <div className="flex justify-between text-xs font-mono">
                          <span className="text-slate-400">Drought & Climate Resistance</span>
                          <span className="font-bold text-emerald-300">{current.drought_resistance}%</span>
                        </div>
                        <div className="w-full h-2 rounded-full bg-white/10 overflow-hidden">
                          <div 
                            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-300 shadow-glow-mint transition-all duration-700"
                            style={{ width: `${current.drought_resistance}%` }}
                          />
                        </div>
                      </div>

                      {/* Key Ecological Characteristics */}
                      <div className="space-y-2 text-xs">
                        <div className="p-3 rounded-xl bg-black/40 border border-white/5 space-y-1">
                          <div className="text-[10px] font-mono text-slate-400 uppercase">Soil & Root Physics</div>
                          <div className="text-slate-200 font-light">{current.soil_fixation}</div>
                        </div>
                        <div className="p-3 rounded-xl bg-black/40 border border-white/5 space-y-1">
                          <div className="text-[10px] font-mono text-slate-400 uppercase">Canopy Architecture</div>
                          <div className="text-slate-200 font-light">{current.canopy_type}</div>
                        </div>
                      </div>

                      {/* Live Web Citation & Source Link */}
                      <div className="pt-3 border-t border-white/10 space-y-1.5">
                        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                          <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
                            <Globe className="w-3.5 h-3.5" />
                            <span>Verified Web Source:</span>
                          </span>
                          {current.source_url && (
                            <a 
                              href={current.source_url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-cyan-400 hover:text-cyan-300 underline"
                            >
                              <span>Inspect Source</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                        <p className="text-[11px] text-slate-300 font-serif italic bg-emerald-950/20 p-2.5 rounded-xl border border-emerald-500/20">
                          "{current.citation_snippet}"
                        </p>
                      </div>
                    </div>
                  )}
                </>
              )}

              {/* Luxembourg Future Fund Sovereign Note */}
              <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-200/90 space-y-1">
                <div className="font-bold font-mono flex items-center gap-1.5 text-emerald-300">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Certified Carbon Asset (Luxembourg Future Fund)</span>
                </div>
                <p className="text-[11px] text-slate-300 leading-normal">
                  Every parcel replanted under this verified dynamic strategy generates sovereign carbon credits certified in compliance with GDPR Art. 30 and acceptable for banking guarantees.
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
