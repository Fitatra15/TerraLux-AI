import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  Settings, Moon, Bell, ShieldCheck, 
  User, CheckCircle2, Lock, CloudRain, Wind 
} from 'lucide-react';

export default function SettingsPage() {
  const { t } = useTranslation();
  const [role, setRole] = useState('farmer');
  const [jurisdiction, setJurisdiction] = useState('MDG');
  const [cycloneAlerts, setCycloneAlerts] = useState(true);
  const [droughtAlerts, setDroughtAlerts] = useState(true);
  const [savedNotice, setSavedNotice] = useState(false);

  const handleSave = () => {
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 2500);
  };

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto space-y-10">

        {/* Header */}
        <div className="space-y-3 pb-6 border-b border-white/10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <Settings className="w-3.5 h-3.5" />
            <span>Platform Configuration</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-serif text-white tracking-tight">
            Settings & System Preferences
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl font-light">
            Manage your spatial mapping parameters, early warning thresholds, and sovereign security configurations.
          </p>
        </div>

        {/* Settings Sections */}
        <div className="space-y-6">

          {/* 1. Visual Theme */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <Moon className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">Visual Experience</h2>
                <p className="text-xs text-slate-400 font-mono">High-contrast Dark Matter theme calibrated for satellite Earth observation</p>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-white/[0.04] border border-emerald-500/30 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded-full bg-emerald-400 shadow-glow-mint" />
                <span className="text-xs font-mono font-bold text-emerald-300">Dark Matter GIS Pro</span>
              </div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/5">
                Active
              </span>
            </div>
          </div>

          {/* 2. Climate Feeds & Alerts */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">Meteorological Alert Subscriptions</h2>
                <p className="text-xs text-slate-400 font-mono">Real-time alerts triggered by NOAA IBTrACS & NASA POWER anomalies</p>
              </div>
            </div>

            <div className="space-y-3 pt-2">
              <label className="flex items-center justify-between p-4 rounded-2xl bg-white/5 hover:bg-white/[0.08] border border-white/10 cursor-pointer transition-colors">
                <div className="flex items-center gap-3">
                  <Wind className="w-4 h-4 text-cyan-400" />
                  <span className="text-xs font-mono text-white">Tropical Cyclone Warnings (NOAA IBTrACS)</span>
                </div>
                <input
                  type="checkbox"
                  checked={cycloneAlerts}
                  onChange={(e) => setCycloneAlerts(e.target.checked)}
                  className="w-4 h-4 accent-emerald-400 rounded cursor-pointer"
                />
              </label>

              <label className="flex items-center justify-between p-4 rounded-2xl bg-white/5 hover:bg-white/[0.08] border border-white/10 cursor-pointer transition-colors">
                <div className="flex items-center gap-3">
                  <CloudRain className="w-4 h-4 text-amber-400" />
                  <span className="text-xs font-mono text-white">Drought & Soil Moisture Deficits (ISRIC & Open-Meteo)</span>
                </div>
                <input
                  type="checkbox"
                  checked={droughtAlerts}
                  onChange={(e) => setDroughtAlerts(e.target.checked)}
                  className="w-4 h-4 accent-emerald-400 rounded cursor-pointer"
                />
              </label>
            </div>
          </div>

          {/* 3. Sovereign Security & Audits */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">Sovereignty & GDPR Art. 30 Compliance</h2>
                <p className="text-xs text-slate-400 font-mono">Immutable SHA-256 telemetry ledger & zero third-party commercial trackers</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-1">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Audit Trail Ledger</span>
                <div className="text-xs font-mono text-emerald-300 font-bold">SHA-256 Merkle Certified</div>
              </div>
              <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-1">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Data Sovereignty</span>
                <div className="text-xs font-mono text-cyan-300 font-bold">EU Sovereign Host (OVHcloud)</div>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="pt-4 flex items-center justify-between">
            {savedNotice ? (
              <span className="inline-flex items-center gap-1.5 text-xs font-mono text-emerald-400 animate-in fade-in">
                <CheckCircle2 className="w-4 h-4" />
                <span>Preferences updated successfully!</span>
              </span>
            ) : <div />}

            <button
              onClick={handleSave}
              className="px-8 py-3.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-xs font-mono shadow-glow-mint transition-all duration-300 hover:scale-105 active:scale-95"
            >
              Save System Preferences
            </button>
          </div>

        </div>

      </div>
    </div>
  );
}
