import React from 'react';
import { useTranslation } from 'react-i18next';
import { 
  Info, Users, Satellite, Database, Sprout, 
  ShieldCheck, Globe, Award, Sparkles 
} from 'lucide-react';
import Logo from '../components/Logo';

export default function AboutPage() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto space-y-12">

        {/* Brand Header */}
        <div className="space-y-4 pb-8 border-b border-white/10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <Info className="w-3.5 h-3.5" />
            <span>Sovereign Agronomic Mission</span>
          </div>
          <div className="pt-2">
            <Logo variant="dark" size="lg" />
          </div>
          <h1 className="text-3xl sm:text-5xl font-serif text-white tracking-tight pt-2">
            {t('about.title')}
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl font-light">
            {t('about.subtitle')}
          </p>
        </div>

        {/* Mission Statement Card */}
        <div className="p-8 sm:p-10 rounded-3xl glass-card border border-white/10 space-y-4 relative overflow-hidden">
          <div className="absolute right-0 top-0 translate-x-12 -translate-y-8 w-64 h-64 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />

          <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest">
            {t('about.mission_title')}
          </span>
          <h2 className="text-2xl sm:text-3xl font-serif text-white font-bold tracking-tight">
            {t('about.subtitle')}
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed font-light">
            {t('about.mission_text')}
          </p>
        </div>

        {/* The TerraLux Team */}
        <div className="p-8 sm:p-10 rounded-3xl glass-card border border-white/10 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-300">
              <Users className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-serif font-bold text-white">{t('about.team_title')}</h2>
              <p className="text-xs font-mono text-emerald-400">Founders & Sovereign Agronomy Engineers</p>
            </div>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed font-light">
            {t('about.team_text')}
          </p>
        </div>

        {/* Scientific Sources */}
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-serif text-white">{t('about.science_title')}</h2>
            <p className="text-xs font-mono text-slate-400 mt-1">
              Mathematical validation and verified scientific calibration
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-3xl glass-card border border-white/10 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-300">
                <Satellite className="w-5 h-5" />
              </div>
              <h3 className="font-serif font-bold text-white">NASA POWER</h3>
              <p className="text-xs text-slate-300 leading-relaxed font-light">
                {t('about.science_nasa')}
              </p>
            </div>

            <div className="p-6 rounded-3xl glass-card border border-white/10 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-300">
                <Database className="w-5 h-5" />
              </div>
              <h3 className="font-serif font-bold text-white">ISRIC SoilGrids v2</h3>
              <p className="text-xs text-slate-300 leading-relaxed font-light">
                {t('about.science_soil')}
              </p>
            </div>

            <div className="p-6 rounded-3xl glass-card border border-white/10 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-300">
                <Sprout className="w-5 h-5" />
              </div>
              <h3 className="font-serif font-bold text-white">FAO ECOCROP</h3>
              <p className="text-xs text-slate-300 leading-relaxed font-light">
                {t('about.science_fao')}
              </p>
            </div>
          </div>
        </div>

        {/* Legal & Sovereign Commitment */}
        <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs font-mono text-slate-400">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>100% Sovereign Infrastructure • GDPR Art. 30 Compliant Registry</span>
          </div>
          <span className="text-emerald-400">Grand Duchy of Luxembourg & Madagascar</span>
        </div>

      </div>
    </div>
  );
}
