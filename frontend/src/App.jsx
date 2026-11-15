import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ParcelDetail from './pages/ParcelDetail';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-gray-50/60 font-sans text-gray-900">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/parcel/:id" element={<ParcelDetail />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
        
        {/* Footer */}
        <footer className="bg-forest text-sand/80 text-xs py-6 border-t border-forest-dark">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
            <p>© 2026 TerraLux AI — Système agronomique multimodal Luxembourg & Madagascar (Diana).</p>
            <p className="text-[11px] text-sand/60">
              Données scientifiques : NASA POWER • ISRIC SoilGrids • FAO ECOCROP • NOAA IBTrACS
            </p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
