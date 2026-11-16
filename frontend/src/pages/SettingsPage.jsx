import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  Settings, Globe, Moon, Bell, ShieldCheck, 
  User, CheckCircle2, Lock 
} from 'lucide-react';

export default function SettingsPage() {
  const { i18n, t } = useTranslation();
  const [role, setRole] = useState('farmer');
  const [jurisdiction, setJurisdiction] = useState('MDG');
  const [cycloneAlerts, setCycloneAlerts] = useState(true);
  const [droughtAlerts, setDroughtAlerts] = useState(true);
  const [savedNotice, setSavedNotice] = useState(false);

  const languages = [
    { code: 'fr', label: 'Français (FR)' },
    { code: 'en', label: 'English (EN)' },
    { code: 'mg', label: 'Malagasy (MG)' },
  ];

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
            {t('settings.title')}
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl font-light">
            {t('settings.subtitle')}
          </p>
        </div>

        {/* Settings Sections */}
        <div className="space-y-6">

          {/* 1. Language Preference */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <Globe className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">{t('settings.lang_section')}</h2>
                <p className="text-xs text-slate-400 font-mono">{t('settings.lang_desc')}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
              {languages.map((l) => {
                const isSelected = i18n.language === l.code;
                return (
                  <button
                    key={l.code}
                    onClick={() => i18n.changeLanguage(l.code)}
                    className={`p-4 rounded-2xl text-xs font-mono font-bold flex items-center justify-between transition-all ${
                      isSelected
                        ? 'bg-emerald-400 text-black shadow-glow-mint'
                        : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-white/10'
                    }`}
                  >
                    <span>{l.label}</span>
                    {isSelected && <CheckCircle2 className="w-4 h-4 text-black" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* 2. Visual Theme */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <Moon className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">{t('settings.theme_section')}</h2>
                <p className="text-xs text-slate-400 font-mono">Palette sombre optimisée pour la cartographie spatiale</p>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-white/[0.04] border border-emerald-500/30 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded-full bg-emerald-400 shadow-glow-mint" />
                <span className="text-xs font-mono font-bold text-emerald-300">{t('settings.theme_dark')}</span>
              </div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/5">
                Actif
              </span>
            </div>
          </div>

          {/* 3. Climate Feeds & Alerts */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">{t('settings.notif_section')}</h2>
                <p className="text-xs text-slate-400 font-mono">Flux satellitaires en temps réel</p>
              </div>
            </div>

            <div className="space-y-3 pt-2">
              <label className="flex items-center justify-between p-4 rounded-2xl bg-white/[0.03] border border-white/10 cursor-pointer hover:bg-white/[0.06] transition-colors">
                <span className="text-xs font-mono text-slate-200">{t('settings.notif_cyclone')}</span>
                <input
                  type="checkbox"
                  checked={cycloneAlerts}
                  onChange={e => setCycloneAlerts(e.target.checked)}
                  className="w-4 h-4 accent-emerald-400 rounded cursor-pointer"
                />
              </label>

              <label className="flex items-center justify-between p-4 rounded-2xl bg-white/[0.03] border border-white/10 cursor-pointer hover:bg-white/[0.06] transition-colors">
                <span className="text-xs font-mono text-slate-200">{t('settings.notif_drought')}</span>
                <input
                  type="checkbox"
                  checked={droughtAlerts}
                  onChange={e => setDroughtAlerts(e.target.checked)}
                  className="w-4 h-4 accent-emerald-400 rounded cursor-pointer"
                />
              </label>
            </div>
          </div>

          {/* 4. Data Sovereignty & GDPR Art. 30 */}
          <div className="p-6 sm:p-8 rounded-3xl glass-card space-y-4 border border-white/10">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <div>
                <h2 className="text-lg font-serif font-bold text-white">{t('settings.sovereignty_section')}</h2>
                <span className="inline-block mt-0.5 text-[10px] font-mono text-emerald-300 font-bold bg-emerald-500/15 border border-emerald-500/30 px-2 py-0.5 rounded-full">
                  {t('settings.sovereignty_badge')}
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-300 font-light leading-relaxed pt-1">
              {t('settings.sovereignty_desc')}
            </p>

            <div className="p-3.5 rounded-2xl bg-black/40 border border-white/5 flex items-center justify-between text-xs font-mono text-slate-400">
              <span className="flex items-center gap-2">
                <Lock className="w-3.5 h-3.5 text-emerald-400" />
                <span>Registre d'Inférence LLM Souverain</span>
              </span>
              <a
                href="/api/compliance/registre"
                target="_blank"
                rel="noreferrer"
                className="text-emerald-400 hover:underline"
              >
                Consulter l'Art. 30 →
              </a>
            </div>
          </div>

        </div>

        {/* Action Button */}
        <div className="flex items-center justify-between pt-4">
          <div className="text-xs font-mono text-emerald-400">
            {savedNotice && <span>✓ {t('actions.save')} avec succès !</span>}
          </div>
          <button
            onClick={handleSave}
            className="px-8 py-3.5 rounded-full bg-emerald-400 hover:bg-emerald-300 text-black font-semibold text-xs font-mono shadow-glow-mint transition-all"
          >
            {t('actions.save')}
          </button>
        </div>

      </div>
    </div>
  );
}
