import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Sprout, Award, Activity, Trees, Map, 
  BarChart3, ShieldCheck, Sparkles 
} from 'lucide-react';

export default function Navbar() {
  const location = useLocation();

  const navLinks = [
    { to: '/', label: 'Asset Portfolio', icon: Sprout, match: ['/', '/portfolio'] },
    { to: '/passport/845ef4e9-b776-40b4-af77-c84510862b1e', label: 'Passport I1', icon: Award, match: ['/passport'] },
    { to: '/events/845ef4e9-b776-40b4-af77-c84510862b1e', label: 'Past Events', icon: Activity, match: ['/events'] },
    { to: '/reforestation', label: 'Restoration Plan', icon: Trees, match: ['/reforestation'] },
    { to: '/map', label: 'Global Map', icon: Map, match: ['/map'] },
    { to: '/dashboard', label: 'Macro Dashboard', icon: BarChart3, match: ['/dashboard'] },
  ];

  const isActive = (link) => {
    return link.match.some(m => location.pathname === m || (m !== '/' && location.pathname.startsWith(m)));
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur-2xl bg-[#06120D]/85 border-b border-white/[0.08] transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Brand : Luxury Serif Logo */}
        <Link to="/" className="flex items-center space-x-3.5 group">
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-700 flex items-center justify-center text-black shadow-glow-mint group-hover:scale-105 transition-transform">
            <Sprout className="w-6 h-6 stroke-[2.2]" />
          </div>
          <div>
            <div className="font-serif font-bold text-xl tracking-tight text-white flex items-center gap-2">
              TerraLux <span className="text-emerald-400 italic font-serif">AI</span>
              <span className="text-[10px] bg-emerald-500/15 border border-emerald-400/30 px-2 py-0.5 rounded-full font-mono uppercase tracking-wider text-emerald-300 font-semibold">
                Sovereign Tier 1
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-mono">Sovereign Agronomic Decision Infrastructure</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center space-x-1 bg-white/[0.03] p-1.5 rounded-2xl border border-white/[0.06]">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link);
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-mono transition-all duration-200 ${
                  active
                    ? 'bg-emerald-400 text-black font-bold shadow-glow-mint'
                    : 'text-slate-300 hover:text-white hover:bg-white/[0.06]'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${active ? 'text-black' : 'text-emerald-400'}`} />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Sovereign EU Trust Badge */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 bg-emerald-500/10 rounded-full text-xs font-mono text-emerald-300 border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-glow-mint animate-pulse" />
            <span>EU Sovereign • Cloud Act Immune</span>
          </div>
        </div>

      </div>

      {/* Mobile navigation scrollable row */}
      <div className="lg:hidden flex items-center space-x-2 px-4 py-2 overflow-x-auto border-t border-white/[0.06] bg-[#030805]">
        {navLinks.map((link) => {
          const Icon = link.icon;
          const active = isActive(link);
          return (
            <Link
              key={link.to}
              to={link.to}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[11px] font-mono shrink-0 ${
                active
                  ? 'bg-emerald-400 text-black font-bold shadow-glow-mint'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Icon className="w-3 h-3" />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </div>
    </header>
  );
}
