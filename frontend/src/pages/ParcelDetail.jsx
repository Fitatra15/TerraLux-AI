import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import {
  Sprout, Droplets, Thermometer, ShieldAlert, Award,
  ChevronDown, ChevronUp, Camera, RefreshCw, Calendar,
  ArrowLeft, FileText, CheckCircle2, AlertTriangle, Layers
} from 'lucide-react';

import { cachedGet, apiClient } from '../api/client';
import ChatWidget from '../components/ChatWidget';
import LeafDiagnoseModal from '../components/LeafDiagnoseModal';
import { getNasaGibsTileUrl, NASA_GIBS_ATTRIBUTION } from '../utils/nasaGibs';

const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function ParcelDetail() {
  const { id } = useParams();

  const [parcel, setParcel] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [soil, setSoil] = useState(null);
  const [events, setEvents] = useState([]);
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Accordion state for "Pourquoi ?"
  const [expandedCrop, setExpandedCrop] = useState(0); // first expanded by default
  const [showDiagnoseModal, setShowDiagnoseModal] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Parcel details
      let pData;
      try {
        pData = await cachedGet(`/parcels/${id}`);
      } catch {
        pData = {
          id: id,
          name: 'Parcelle Antsiranana (Diana)',
          latitude: -12.2794,
          longitude: 49.2914,
          country: 'MDG',
          region: 'Diana',
          area_ha: 3.5
        };
      }
      setParcel(pData);

      // 2. Recommendations
      const recData = await cachedGet(`/parcels/${id}/recommendation`);
      setRecommendations(recData.top3);

      // 3. Soil Profile
      const soilData = await cachedGet(`/parcels/${id}/soil`);
      setSoil(soilData);

      // 4. Events
      const eventData = await cachedGet(`/parcels/${id}/events`);
      setEvents(Array.isArray(eventData) ? eventData : []);

      // 5. Diseases
      const disData = await cachedGet(`/parcels/${id}/diseases`);
      setDiseases(Array.isArray(disData) ? disData : []);

    } catch (err) {
      console.error(err);
      setError("Impossible de charger l'intégralité des données de la parcelle.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 space-y-6 animate-pulse">
        <div className="h-24 bg-gray-200 rounded-3xl" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="h-64 bg-gray-200 rounded-2xl" />
          <div className="h-64 bg-gray-200 rounded-2xl" />
          <div className="h-64 bg-gray-200 rounded-2xl" />
        </div>
      </div>
    );
  }

  if (error && !parcel) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-accent mx-auto" />
        <h2 className="text-xl font-bold text-gray-800">Erreur de chargement</h2>
        <p className="text-sm text-gray-600">{error}</p>
        <button
          onClick={fetchData}
          className="px-5 py-2.5 bg-forest text-sand rounded-xl font-semibold text-xs inline-flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" /> Réessayer
        </button>
      </div>
    );
  }

  const lat = parcel?.latitude || -12.2794;
  const lng = parcel?.longitude || 49.2914;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      {/* Top Bar : Back + Parcel Header + Photo Diagnosis Action */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-gray-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Link to="/" className="text-xs text-forest hover:underline flex items-center gap-1 font-semibold">
              <ArrowLeft className="w-3.5 h-3.5" /> Retour carte
            </Link>
            <span className="text-gray-300">•</span>
            <span className="text-[11px] font-mono uppercase bg-sand text-forest-dark px-2 py-0.5 rounded font-bold">
              {parcel?.country || 'MDG'} - {parcel?.region || 'Diana'}
            </span>
          </div>
          <h1 className="text-2xl font-black text-forest tracking-tight">
            {parcel?.name || 'Fiche Diagnostic Parcelle'}
          </h1>
          <p className="text-xs text-gray-500 font-mono">
            GPS: [{lat.toFixed(4)}, {lng.toFixed(4)}] • Surface: {parcel?.area_ha || 2.5} ha
          </p>
        </div>

        {/* Diagnosis Trigger Button & PDF Export */}
        <div className="flex flex-wrap items-center gap-2">
          <a
            href={`/api/parcels/${id}/report.pdf`}
            target="_blank"
            rel="noreferrer"
            className="px-4 py-3 bg-forest-light hover:bg-forest text-sand rounded-2xl font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm border border-forest transition-colors"
          >
            <FileText className="w-4 h-4 text-accent" />
            <span>Rapport PDF</span>
          </a>

          <button
            onClick={() => setShowDiagnoseModal(true)}
            className="px-5 py-3 bg-accent hover:bg-accent-dark text-white rounded-2xl font-bold text-xs flex items-center justify-center gap-2 shadow-md transition-transform hover:scale-102"
          >
            <Camera className="w-4 h-4" />
            <span>Uploader une photo de feuille</span>
          </button>
        </div>
      </div>

      {/* Two Column Layout: Main Diagnostics + Side Map & Events */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* LEFT COLUMN (2 Cols): Richesse Sol & Top 3 Recommandations */}
        <div className="lg:col-span-2 space-y-8">

          {/* 1. Bloc Richesse du sol (Prompt 4) */}
          {soil && (
            <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-sm space-y-5">
              <div className="flex items-center justify-between border-b border-gray-100 pb-4">
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-forest/10 flex items-center justify-center text-forest">
                    <Layers className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-base font-bold text-forest">Profil & Richesse du Sol</h2>
                    <p className="text-xs text-gray-500">Classification WRB & Indices multi-profondeurs (SoilGrids v2.0)</p>
                  </div>
                </div>

                <div className="text-right">
                  <div className="flex items-baseline gap-1 justify-end">
                    <span className="text-3xl font-black text-forest font-mono">
                      {soil.richness_index}
                    </span>
                    <span className="text-xs text-gray-400 font-semibold">/100</span>
                  </div>
                  <span className="text-[11px] font-semibold text-accent uppercase">
                    Indice : {soil.richness_label}
                  </span>
                </div>
              </div>

              {/* WRB Class Badge & Properties */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-[10px] text-gray-500 font-medium block">Type de Sol (WRB)</span>
                  <span className="text-xs font-bold text-gray-800 block mt-0.5 truncate" title={soil.wrb_class}>
                    {soil.wrb_class}
                  </span>
                </div>
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-[10px] text-gray-500 font-medium block">pH H2O (0-5cm)</span>
                  <span className="text-xs font-bold text-gray-800 block mt-0.5">
                    {soil.properties?.ph?.value} ({soil.properties?.ph?.status})
                  </span>
                </div>
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-[10px] text-gray-500 font-medium block">Carbone SOC</span>
                  <span className="text-xs font-bold text-gray-800 block mt-0.5">
                    {soil.properties?.soc?.value} g/kg
                  </span>
                </div>
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-[10px] text-gray-500 font-medium block">Azote Total</span>
                  <span className="text-xs font-bold text-gray-800 block mt-0.5">
                    {soil.properties?.nitrogen?.value} g/kg
                  </span>
                </div>
              </div>

              {/* Deficiencies */}
              {soil.deficiencies && soil.deficiencies.length > 0 && (
                <div className="p-3 bg-amber-50/70 border border-amber-200/80 rounded-2xl flex items-start gap-2.5">
                  <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-xs font-bold text-amber-800">Carences & points de vigilance identifiés :</span>
                    <ul className="text-xs text-amber-700 list-disc list-inside mt-0.5 space-y-0.5">
                      {soil.deficiencies.map((d, idx) => (
                        <li key={idx}>{d}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Agronomic Interpretation */}
              <div className="p-4 bg-sand/30 border border-sand-dark/20 rounded-2xl text-xs text-forest leading-relaxed">
                📖 <strong>Interprétation agronomique :</strong> {soil.interpretation}
              </div>
            </div>
          )}

          {/* 2. Bloc Top 3 cultures & Explicabilité radicale (Prompt 3) */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-forest flex items-center gap-2">
                  <Sprout className="w-5 h-5 text-accent" />
                  <span>Top 3 Cultures Recommandées</span>
                </h2>
                <p className="text-xs text-gray-500">Scoring agro-climatique & Explicabilité radicale (FAO ECOCROP)</p>
              </div>
              <span className="text-[11px] font-mono text-gray-400">rules-v1</span>
            </div>

            <div className="space-y-4">
              {recommendations && recommendations.map((crop, idx) => (
                <div
                  key={idx}
                  className={`bg-white rounded-3xl p-6 border transition-all shadow-sm ${
                    idx === 0 ? 'border-forest/40 ring-1 ring-forest/10' : 'border-gray-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-2xl bg-forest/5 flex items-center justify-center font-bold font-mono text-forest">
                        #{idx + 1}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="font-bold text-base text-gray-900">{crop.name}</h3>
                          {idx === 0 && (
                            <span className="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold uppercase">
                              Choix optimal
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 italic">{crop.scientific_name}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <span className="text-2xl font-black text-forest font-mono">{crop.score}</span>
                        <span className="text-xs text-gray-400">/100</span>
                      </div>
                      
                      <button
                        onClick={() => setExpandedCrop(expandedCrop === idx ? -1 : idx)}
                        className="px-3.5 py-1.5 bg-gray-100 hover:bg-forest hover:text-sand text-gray-700 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors"
                      >
                        <span>Pourquoi ?</span>
                        {expandedCrop === idx ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>

                  {/* Accordion Content : Scientifically cited reasons */}
                  {expandedCrop === idx && (
                    <div className="mt-5 pt-4 border-t border-gray-100 space-y-3 animate-in fade-in duration-150">
                      
                      {/* Positive reasons */}
                      <div className="space-y-1">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Facteurs favorables (Climat & Sol vérifiés) :</span>
                        </span>
                        <ul className="text-xs text-gray-700 space-y-1 pl-4 list-disc">
                          {crop.reasons?.positive?.map((pos, pIdx) => (
                            <li key={pIdx} className="leading-relaxed">{pos}</li>
                          ))}
                        </ul>
                      </div>

                      {/* Negative reasons */}
                      {crop.reasons?.negative?.length > 0 && (
                        <div className="space-y-1 pt-1">
                          <span className="text-[11px] font-bold uppercase tracking-wider text-amber-700 flex items-center gap-1">
                            <AlertTriangle className="w-3.5 h-3.5" />
                            <span>Contraintes & Limites :</span>
                          </span>
                          <ul className="text-xs text-gray-700 space-y-1 pl-4 list-disc">
                            {crop.reasons?.negative?.map((neg, nIdx) => (
                              <li key={nIdx} className="leading-relaxed">{neg}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Rotation explanation */}
                      {crop.reasons?.rotation && (
                        <div className="pt-2 text-xs bg-gray-50 p-3 rounded-xl border border-gray-200/60 text-gray-600">
                          🔄 <strong>Rotation culturale :</strong> {crop.reasons.rotation}
                        </div>
                      )}

                    </div>
                  )}

                </div>
              ))}
            </div>
          </div>

        </div>

        {/* RIGHT COLUMN (1 Col): Map, Historical Events, Disease Risks */}
        <div className="space-y-6">

          {/* Mini Leaflet Map with pin */}
          <div className="bg-white rounded-3xl p-4 border border-gray-200 shadow-sm overflow-hidden h-[280px] flex flex-col">
            <span className="text-xs font-bold text-forest mb-2 block">Localisation satellite</span>
            <div className="flex-1 rounded-2xl overflow-hidden shadow-inner">
              <MapContainer
                center={[lat, lng]}
                zoom={10}
                scrollWheelZoom={false}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  attribution={NASA_GIBS_ATTRIBUTION}
                  url={getNasaGibsTileUrl()}
                  maxNativeZoom={9}
                  maxZoom={18}
                />
                <Marker position={[lat, lng]} icon={customIcon}>
                  <Popup>{parcel?.name}</Popup>
                </Marker>
              </MapContainer>
            </div>
          </div>

          {/* 3. Bloc Risques Maladies (Prompt 2.3 & 7) */}
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm space-y-3">
            <h3 className="text-sm font-bold text-forest uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-accent" />
              <span>Risques Sanitaires & Pathogènes</span>
            </h3>

            <div className="space-y-2">
              {diseases.map((d, idx) => (
                <div key={idx} className="p-3 bg-gray-50 rounded-2xl border border-gray-100 flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-gray-800 block">{d.disease}</span>
                    <span className="text-[10px] text-gray-500">Confiance modèle : {Math.round(d.confidence * 100)}%</span>
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                    d.risk_level === 'high' ? 'bg-red-100 text-red-700' :
                    d.risk_level === 'medium' ? 'bg-amber-100 text-amber-700' :
                    'bg-emerald-100 text-emerald-700'
                  }`}>
                    {d.risk_level === 'high' ? 'Élevé' : d.risk_level === 'medium' ? 'Moyen' : 'Faible'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* 4. Bloc Événements Passés (Timeline Sécheresses & Cyclones) */}
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm space-y-3">
            <h3 className="text-sm font-bold text-forest uppercase tracking-wider flex items-center gap-2">
              <Calendar className="w-4 h-4 text-accent" />
              <span>Historique Climatique Extrême</span>
            </h3>

            <div className="space-y-3 relative pl-4 before:absolute before:left-1.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-200">
              {events.map((ev, idx) => (
                <div key={idx} className="relative space-y-0.5">
                  <span className="absolute -left-4 top-1 w-2.5 h-2.5 rounded-full bg-accent border-2 border-white"></span>
                  <div className="text-xs font-bold text-gray-800">{ev.type}</div>
                  <div className="text-[10px] text-gray-500">
                    {ev.start} {ev.end ? `au ${ev.end}` : ''} • Source: {ev.source}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

      {/* Floating Chatbot Widget (Prompt 7) */}
      <ChatWidget parcelId={id} />

      {/* Modal Leaf Diagnosis (Prompt 5 & 6) */}
      {showDiagnoseModal && (
        <LeafDiagnoseModal
          parcelId={id}
          onClose={() => setShowDiagnoseModal(false)}
        />
      )}

    </div>
  );
}
