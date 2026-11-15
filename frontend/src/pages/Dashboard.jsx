import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import {
  BarChart3, Download, ShieldCheck, Layers, AlertTriangle,
  FileSpreadsheet, Users, TreePine, MapPin
} from 'lucide-react';
import { cachedGet } from '../api/client';

const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const statsData = await cachedGet('/stats/overview');
        setStats(statsData);
        const zonesData = await cachedGet('/reforestation/zones');
        setZones(zonesData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  const handleExportCSV = () => {
    if (!stats || !stats.regions) return;

    const headers = ["Région", "Pays", "Parcelles suivies", "Score de richesse sol (0-100)", "Culture principale", "Risque Cyclonique", "Risque Sécheresse"];
    const rows = stats.regions.map(r => [
      `"${r.region}"`,
      `"${r.country}"`,
      r.parcels_count,
      r.avg_soil_richness,
      `"${r.top_recommended_crop}"`,
      `"${r.cyclone_risk}"`,
      `"${r.drought_risk}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `terralux_rapport_agronomique_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-gray-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase bg-forest/10 text-forest px-2.5 py-0.5 rounded-full">
              Ministères & Institutions
            </span>
          </div>
          <h1 className="text-2xl font-black text-forest mt-1 tracking-tight">
            Tableau de Bord Institutionnel & Territorial
          </h1>
          <p className="text-xs text-gray-500">
            Évaluation territoriale des risques agro-climatiques, santé des terres et planification de résilience
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="px-5 py-2.5 bg-forest hover:bg-forest-light text-sand rounded-2xl font-bold text-xs flex items-center gap-2 shadow-md transition-all shrink-0"
        >
          <FileSpreadsheet className="w-4 h-4 text-accent" />
          <span>Exporter rapport CSV</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-3xl border border-gray-200 shadow-sm">
          <span className="text-xs text-gray-500 font-semibold block">Parcelles Numérisées</span>
          <div className="text-3xl font-black text-forest font-mono mt-1">
            {stats?.total_parcels || 48}
          </div>
          <span className="text-[11px] text-emerald-600 font-medium">Cadastre & GPS vérifié</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-gray-200 shadow-sm">
          <span className="text-xs text-gray-500 font-semibold block">Superficie Sous Suivi</span>
          <div className="text-3xl font-black text-forest font-mono mt-1">
            {stats?.total_area_ha || 142.5} <span className="text-base text-gray-400">ha</span>
          </div>
          <span className="text-[11px] text-gray-400">Céréales, tubercules, agroforesterie</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-gray-200 shadow-sm">
          <span className="text-xs text-gray-500 font-semibold block">Exploitants Connectés</span>
          <div className="text-3xl font-black text-forest font-mono mt-1">
            {stats?.active_farmers || 34}
          </div>
          <span className="text-[11px] text-accent font-medium">Diana & Luxembourg</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-gray-200 shadow-sm">
          <span className="text-xs text-gray-500 font-semibold block">Santé Moyenne des Sols</span>
          <div className="text-3xl font-black text-forest font-mono mt-1">
            78.1 <span className="text-base text-gray-400">/100</span>
          </div>
          <span className="text-[11px] text-forest font-medium">Indice utilisable banques & assurances</span>
        </div>
      </div>

      {/* Aggregated Map */}
      <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-forest">Cartographie Territoriale des Pôles Agricoles</h2>
            <p className="text-xs text-gray-500">Luxembourg (tempéré) et Madagascar (tropical Diana)</p>
          </div>
          <span className="text-xs text-gray-400 font-mono">Multi-pays</span>
        </div>

        <div className="h-[380px] rounded-2xl overflow-hidden shadow-inner border border-gray-100">
          <MapContainer center={[15.0, 30.0]} zoom={2} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            
            {/* Diana Madagascar Cluster */}
            <Marker position={[-12.2794, 49.2914]} icon={customIcon}>
              <Popup>
                <div className="font-sans">
                  <strong>Pôle Régional Diana (Madagascar)</strong>
                  <p className="text-xs text-gray-600">32 parcelles • Richesse 74.2/100 • Risque cyclone</p>
                </div>
              </Popup>
            </Marker>
            <Circle center={[-12.2794, 49.2914]} radius={150000} pathOptions={{ color: '#e67e22', fillColor: '#e67e22', fillOpacity: 0.15 }} />

            {/* Luxembourg Cluster */}
            <Marker position={[49.6116, 6.1319]} icon={customIcon}>
              <Popup>
                <div className="font-sans">
                  <strong>Pôle Luxembourg & Gutland</strong>
                  <p className="text-xs text-gray-600">16 parcelles • Richesse 82.0/100 • Risque sécheresse</p>
                </div>
              </Popup>
            </Marker>
            <Circle center={[49.6116, 6.1319]} radius={50000} pathOptions={{ color: '#1a4d2e', fillColor: '#1a4d2e', fillOpacity: 0.2 }} />
          </MapContainer>
        </div>
      </div>

      {/* Regions Breakdown Table */}
      <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-sm space-y-4">
        <h2 className="text-base font-bold text-forest">Synthèse par Région Agricole</h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-gray-700">
            <thead className="bg-sand/40 text-forest uppercase font-bold text-[10px] tracking-wider border-b border-sand-dark/30">
              <tr>
                <th className="py-3 px-4 rounded-l-xl">Région</th>
                <th className="py-3 px-4">Pays</th>
                <th className="py-3 px-4">Parcelles</th>
                <th className="py-3 px-4">Score Sol</th>
                <th className="py-3 px-4">Culture Recommandée</th>
                <th className="py-3 px-4">Risque Cyclonique</th>
                <th className="py-3 px-4 rounded-r-xl">Risque Sécheresse</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {stats?.regions?.map((reg, idx) => (
                <tr key={idx} className="hover:bg-gray-50/80 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-gray-900">{reg.region}</td>
                  <td className="py-3.5 px-4">
                    <span className="font-semibold text-gray-600">{reg.country}</span>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-semibold">{reg.parcels_count}</td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-1.5 font-bold font-mono text-forest">
                      <span>{reg.avg_soil_richness}</span>
                      <span className="text-[10px] text-gray-400">/100</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 font-medium text-emerald-800">{reg.top_recommended_crop}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      reg.cyclone_risk.includes('Élevé') ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'
                    }`}>
                      {reg.cyclone_risk}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      reg.drought_risk.includes('Élevé') ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-600'
                    }`}>
                      {reg.drought_risk}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Priority Reforestation Zones (Section 5) */}
      <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-forest">
          <TreePine className="w-5 h-5 text-emerald-700" />
          <h2 className="text-base font-bold">Zones Prioritaires de Reboisement & Lutte contre l'Érosion</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {zones.map((z, idx) => (
            <div key={idx} className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-100 space-y-2">
              <div className="flex justify-between items-start">
                <h4 className="font-bold text-sm text-emerald-950">{z.name}</h4>
                <span className="text-[10px] bg-emerald-200/70 text-emerald-900 px-2 py-0.5 rounded-full font-bold">
                  {z.area_ha} ha
                </span>
              </div>
              <p className="text-xs text-emerald-800">
                <strong>Objectif :</strong> {z.risk_type}
              </p>
              <div>
                <span className="text-[11px] font-semibold text-emerald-900 block">Essences recommandées :</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {z.species_proposed?.map((sp, sIdx) => (
                    <span key={sIdx} className="text-[10px] bg-white border border-emerald-200 text-emerald-700 px-2 py-0.5 rounded-md">
                      {sp}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
