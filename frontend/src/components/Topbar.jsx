import React from 'react';
import { useTranslation } from 'react-i18next';
import { Menu, Globe, Map, Trees, Activity, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import Logo from './Logo';

export default function Topbar({ onOpenSidebar }) {
  const { t } = useTranslation();

  return (
    <header className="sticky top-0 z-30 h-20 backdrop-blur-xl bg-[#06120D]/85 border-b border-white/10 px-4 sm:px-8 flex items-center justify-between">
      {/* Left : Hamburger for mobile + Logo */}
      <div className="flex items-center gap-4">
        <button
          onClick={onOpenSidebar}
          className="md:hidden p-2.5 rounded-xl bg-white/5 border border-white/10 text-white hover:bg-white/10 transition-colors"
          aria-label="Open Navigation Menu"
        >
          <Menu className="w-5 h-5 text-emerald-400" />
        </button>

        {/* Logo shown on mobile when sidebar is hidden */}
        <div className="md:hidden">
          <Logo variant="dark" size="sm" />
        </div>

        {/* Quick shortcut pills for desktop */}
        <div className="hidden sm:flex items-center gap-2">
          <Link
            to="/map"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-xs font-mono text-slate-300 border border-white/10 transition-colors"
          >
            <Map className="w-3.5 h-3.5 text-emerald-400" />
            <span>Map</span>
          </Link>
          <Link
            to="/reforestation"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-xs font-mono text-slate-300 border border-white/10 transition-colors"
          >
            <Trees className="w-3.5 h-3.5 text-emerald-300" />
            <span>Restoration Plan</span>
          </Link>
          <Link
            to="/portfolio"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-xs font-mono text-slate-300 border border-white/10 transition-colors"
          >
            <Activity className="w-3.5 h-3.5 text-amber-300" />
            <span>Parcels</span>
          </Link>
        </div>
      </div>

      {/* Right : Platform Status Badge (Forced English, no language selector) */}
      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.04] border border-white/10 text-[11px] font-mono text-slate-300">
          <Globe className="w-3.5 h-3.5 text-emerald-400" />
          <span>English (Global)</span>
        </div>

        {/* Sovereign Status */}
        <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-300">
          <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-glow-mint animate-pulse" />
          <span>EU Sovereign Active</span>
        </div>
      </div>
    </header>
  );
}
