import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sprout, BarChart3, Map, ShieldCheck, Bell } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="bg-forest text-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-forest-light border border-forest-dark flex items-center justify-center text-sand shadow-inner group-hover:scale-105 transition-transform">
            <Sprout className="w-6 h-6 text-sand" />
          </div>
          <div>
            <div className="font-bold text-lg tracking-tight flex items-center gap-2">
              TerraLux AI
              <span className="text-[10px] bg-accent px-2 py-0.5 rounded-full font-semibold uppercase tracking-wider text-white">
                Multi-pays
              </span>
            </div>
            <p className="text-xs text-sand/80 font-medium">Système d'aide agronomique explicable</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex items-center space-x-1 sm:space-x-3">
          <Link
            to="/"
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              location.pathname === '/' 
                ? 'bg-forest-dark text-sand' 
                : 'text-white/80 hover:bg-forest-light hover:text-white'
            }`}
          >
            <Map className="w-4 h-4" />
            <span>Carte & Parcelles</span>
          </Link>

          <Link
            to="/dashboard"
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              location.pathname === '/dashboard' 
                ? 'bg-forest-dark text-sand' 
                : 'text-white/80 hover:bg-forest-light hover:text-white'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Dashboard Institutions</span>
          </Link>
        </nav>

        {/* Status indicator */}
        <div className="hidden md:flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-2.5 py-1 bg-white/10 rounded-full text-xs text-sand/90 border border-white/10">
            <ShieldCheck className="w-3.5 h-3.5 text-sand" />
            <span>NASA POWER & SoilGrids v2</span>
          </div>
        </div>

      </div>
    </header>
  );
}
