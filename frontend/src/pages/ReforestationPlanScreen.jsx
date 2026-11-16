import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MapContainer, TileLayer, Polygon, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { 
  ArrowLeft, Download, Trees, ShieldCheck, Sparkles, 
  Leaf, Droplets, Wind, CheckCircle2, ArrowUpRight, Share2 
} from 'lucide-react';
import { cachedGet } from '../api/client';

const zoneMarkerIcon = new L.DivIcon({
  className: 'zone-pin',
  html: `<div class="w-5 h-5 rounded-full bg-emerald-400 border-2 border-white shadow-glow-mint flex items-center justify-center text-[10px] font-bold text-black">R1</div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10]
});

export default function ReforestationPlanScreen() {
  const [selectedSpecies, setSelectedSpecies] = useState('moringa');
  const [exporting, setExporting] = useState(false);

  // Polygon coordinates for Priority Zones (Antsiranana Montagne des Français / Ambilobe watershed)
  const zone1Polygon = [
    [-12.2850, 49.2800],
    [-12.2700, 49.3000],
    [-12.2820, 49.3150],
    [-12.2980, 49.2950]
  ];

  const zone2Polygon = [
    [-12.3000, 49.2600],
    [-12.3150, 49.2800],
    [-12.3250, 49.2700],
    [-12.3100, 49.2450]
  ];

  const speciesList = [
    {
      id: 'moringa',
      name: 'Moringa Oleifera',
      vernacular: 'Ananambo (Arbre Miracle)',
      droughtResistance: 95,
      carbonCapture: '12.4 tCO₂ / ha / an',
      soilFixation: 'Fixation symbiotique d’azote & phosphore',
      canopyType: 'Ombrage filtrant optimal pour vanille & cacao',
      iconEmoji: '🌿',
      origin: 'Diana — Madagascar',
      reason: 'Croissance ultra-rapide (3m/an), survit avec moins de 300mm de pluie et régénère les micro-organismes des sols ferrallitiques lessivés.'
    },
    {
      id: 'baobab',
      name: 'Adansonia Madagascariensis',
      vernacular: 'Reniala (Baobab de Diana)',
      droughtResistance: 98,
      carbonCapture: '8.1 tCO₂ / ha / an',
      soilFixation: 'Rétention d’eau souterraine (jusqu’à 100 000 L/tronc)',
      canopyType: 'Brise-vent structurel contre cyclones catégorie 4',
      iconEmoji: '🌳',
      origin: 'Nord Madagascar',
      reason: 'Pilier hydraulique naturel, freine le ravinement des collines et crée un microclimat hygrométrique protecteur pour les cultures vivrières.'
    },
    {
      id: 'oak',
      name: 'Quercus Petraea',
      vernacular: 'Chêne Sessile Luxembourgeois',
      droughtResistance: 90,
      carbonCapture: '14.2 tCO₂ / ha / an',
      soilFixation: 'Système racinaire pivotant jusqu’à 5m de profondeur',
      canopyType: 'Canopée dense régulatrice des écarts thermiques',
      iconEmoji: '🍃',
      origin: 'Grand-Duché de Luxembourg',
      reason: 'Stabilisation des versants ardennais, résistance aux sécheresses estivales tempérées et préservation de la biodiversité entomologique.'
    },
    {
      id: 'teak',
      name: 'Tectona Grandis & Vanille',
      vernacular: 'Teck Protecteur & Liane Vanille',
      droughtResistance: 88,
      carbonCapture: '16.8 tCO₂ / ha / an',
      soilFixation: 'Couverture de litière anti-érosion',
      canopyType: 'Tuteur vivant d’agroforesterie de haute rente',
      iconEmoji: '🪵',
      origin: 'Sava & Diana',
      reason: 'Combine valorisation financière bancable (marché export vanille bourbon) et rempart physique robuste face aux cyclones saisonniers.'
    }
  ];

  const handleExportPlan = () => {
    setExporting(true);
    setTimeout(() => {
      // Trigger download of strategic PDF
      window.open('/api/passport/p-antsiranana/pdf', '_blank');
      setExporting(false);
    }, 800);
  };

  const current = speciesList.find(s => s.id === selectedSpecies) || speciesList[0];

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Top Header : Back link + Title + Apple-style Export Plan Button */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/[0.08]">
          <div className="space-y-2">
            <Link
              to="/portfolio"
              className="inline-flex items-center gap-2 text-xs font-mono text-slate-400 hover:text-emerald-300 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Retour au Portfolio des Actifs</span>
            </Link>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
              <Trees className="w-3.5 h-3.5" />
              <span>Ecological Restoration & Carbon Asset Engineering</span>
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-serif text-white tracking-tight">
              Reforestation & Canopy Strategy
            </h1>
            <p className="text-slate-400 text-xs sm:text-sm max-w-2xl font-light">
              Modélisation spatiale des corridors écologiques prioritaires, remparts brise-vent cycloniques et certification de crédits carbone souverains.
            </p>
          </div>

          {/* Apple-style Export Plan Button */}
          <button
            onClick={handleExportPlan}
            disabled={exporting}
            className="inline-flex items-center gap-2.5 px-7 py-4 rounded-full bg-white hover:bg-emerald-100 text-black font-semibold text-sm shadow-2xl hover:shadow-emerald-400/30 transition-all duration-300 hover:scale-105 active:scale-95 group"
          >
            <Download className="w-4 h-4 text-emerald-800 group-hover:translate-y-0.5 transition-transform" />
            <span>{exporting ? 'Génération du dossier...' : 'Export Restoration Plan'}</span>
          </button>
        </div>

        {/* ======================================================== */}
        {/* ASYMMETRIC LAYOUT : 60% Map / 40% Restoration Details   */}
        {/* ======================================================== */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">

          {/* 60% Map Container (3 cols out of 5) */}
          <div className="lg:col-span-3 rounded-3xl overflow-hidden glass-card p-2 min-h-[560px] relative border border-white/10 shadow-2xl">
            <div className="w-full h-[540px] rounded-2xl overflow-hidden relative">
              <MapContainer
                center={[-12.2880, 49.2880]}
                zoom={13}
                zoomControl={true}
                className="w-full h-full leaflet-dark"
              >
                <TileLayer
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  attribution='&copy; CARTO &copy; TerraLux AI'
                />

                {/* Priority Zone 1 : High Erosion Risk (Red/Amber) */}
                <Polygon
                  positions={zone1Polygon}
                  pathOptions={{
                    color: '#EF4444',
                    fillColor: '#EF4444',
                    fillOpacity: 0.28,
                    weight: 2,
                    dashArray: '6, 6'
                  }}
                >
                  <Popup>
                    <div className="space-y-1">
                      <div className="text-xs font-mono font-bold text-red-400 uppercase">Zone 1 : Alerte Rupture</div>
                      <div className="text-xs font-semibold text-white">Versant Nord Montagne des Français</div>
                      <div className="text-[11px] text-slate-300">Surface : 142 ha • Pente : 18% • Érosion critique</div>
                      <div className="text-[11px] text-emerald-400 font-mono font-bold">Arbre prescrit : Moringa & Baobab</div>
                    </div>
                  </Popup>
                </Polygon>

                {/* Priority Zone 2 : Agroforestry Corridor (Orange) */}
                <Polygon
                  positions={zone2Polygon}
                  pathOptions={{
                    color: '#F97316',
                    fillColor: '#F97316',
                    fillOpacity: 0.24,
                    weight: 2
                  }}
                >
                  <Popup>
                    <div className="space-y-1">
                      <div className="text-xs font-mono font-bold text-orange-400 uppercase">Zone 2 : Corridor de Rente</div>
                      <div className="text-xs font-semibold text-white">Bassin Alluvionnaire Mahavavy</div>
                      <div className="text-[11px] text-slate-300">Surface : 285 ha • Pente : 6% • Brise-vent cyclonique</div>
                      <div className="text-[11px] text-emerald-400 font-mono font-bold">Arbre prescrit : Teck & Vanille Bourbon</div>
                    </div>
                  </Popup>
                </Polygon>

                <Marker position={[-12.2850, 49.2800]} icon={zoneMarkerIcon}>
                  <Popup>
                    <span className="text-xs font-mono font-bold text-emerald-300">Pylône de Restauration R1</span>
                  </Popup>
                </Marker>
              </MapContainer>

              {/* Floating Map Legend */}
              <div className="absolute bottom-5 left-5 z-[500] glass-panel px-4 py-3 rounded-2xl border border-white/20 space-y-2 pointer-events-auto">
                <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Polygones de Restauration</div>
                <div className="flex flex-col gap-1.5 text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded bg-red-500/50 border border-red-500"></span>
                    <span className="text-slate-200">Zone 1 — Priorité Haute (Érosion active)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded bg-orange-500/50 border border-orange-500"></span>
                    <span className="text-slate-200">Zone 2 — Corridor Agroforestier (Brise-vent)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 40% Details Container (2 cols out of 5) */}
          <div className="lg:col-span-2 space-y-6">

            <div className="glass-card rounded-3xl p-6 sm:p-8 space-y-6">
              <div>
                <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest">
                  Species Engineering
                </span>
                <h2 className="text-2xl font-serif text-white tracking-tight">
                  Restoration Strategy
                </h2>
                <p className="text-xs text-slate-400 font-light mt-1">
                  Sélection d'arbres à haut rendement éco-systémique validés pour l'ancrage hydrique.
                </p>
              </div>

              {/* Species selector pills */}
              <div className="grid grid-cols-2 gap-2">
                {speciesList.map(s => (
                  <button
                    key={s.id}
                    onClick={() => setSelectedSpecies(s.id)}
                    className={`px-3 py-2.5 rounded-2xl text-xs font-mono font-medium flex items-center gap-2 transition-all ${
                      selectedSpecies === s.id
                        ? 'bg-emerald-500 text-black font-bold shadow-glow-mint'
                        : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-white/10'
                    }`}
                  >
                    <span>{s.iconEmoji}</span>
                    <span className="truncate">{s.name.split(' ')[0]}</span>
                  </button>
                ))}
              </div>

              {/* Active Species Detail Card */}
              <div className="p-5 rounded-2xl bg-white/[0.04] border border-white/10 space-y-4">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-lg font-serif font-bold text-white flex items-center gap-2">
                      <span>{current.name}</span>
                      <span className="text-base">{current.iconEmoji}</span>
                    </h3>
                    <p className="text-xs font-mono text-emerald-400">{current.vernacular}</p>
                    <p className="text-[11px] text-slate-400 font-mono mt-0.5">{current.origin}</p>
                  </div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
                    Souverain
                  </span>
                </div>

                {/* Drought Resistance Progress Bar */}
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs font-mono">
                    <span className="text-slate-400">Résistance Sécheresse</span>
                    <span className="font-bold text-emerald-300">{current.droughtResistance}%</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-white/10 overflow-hidden">
                    <div 
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-300 shadow-glow-mint transition-all duration-700"
                      style={{ width: `${current.droughtResistance}%` }}
                    />
                  </div>
                </div>

                {/* Key Metrics Grid */}
                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 rounded-xl bg-black/40 border border-white/5 space-y-0.5">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Captation Carbone</div>
                    <div className="text-xs font-bold text-emerald-300 font-mono">{current.carbonCapture}</div>
                  </div>
                  <div className="p-3 rounded-xl bg-black/40 border border-white/5 space-y-0.5">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Impact Microclimat</div>
                    <div className="text-xs font-bold text-cyan-300 font-mono">{current.canopyType.split(' ')[0]}</div>
                  </div>
                </div>

                {/* Why Selected Note */}
                <div className="pt-2 text-xs text-slate-300 leading-relaxed font-light border-t border-white/10">
                  <span className="font-semibold text-emerald-400 font-mono">Pourquoi ce choix ? </span>
                  {current.reason}
                </div>
              </div>

              {/* Financing & Carbon Asset Note */}
              <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-200/90 space-y-1">
                <div className="font-bold font-mono flex items-center gap-1.5 text-emerald-300">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Actif Carbone Éligible Luxembourg Future Fund</span>
                </div>
                <p className="text-[11px] text-slate-300 leading-normal">
                  Chaque hectare replanté selon ce plan génère des crédits carbone certifiés traçables dans le registre Art. 30 RGPD et valorisables auprès des banques partenaires.
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
