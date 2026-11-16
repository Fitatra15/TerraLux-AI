import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ParcelPortfolio from './pages/ParcelPortfolio';
import PastEventsScreen from './pages/PastEventsScreen';
import ReforestationPlanScreen from './pages/ReforestationPlanScreen';
import ResiliencePassportScreen from './pages/ResiliencePassportScreen';
import Home from './pages/Home';
import ParcelDetail from './pages/ParcelDetail';
import Dashboard from './pages/Dashboard';
import ChatWidget from './components/ChatWidget';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#06120D] text-slate-100 font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
        <Navbar />
        
        <main className="flex-1">
          <Routes>
            {/* Screen 1 : Luxury Bento Grid Agronomic Portfolio */}
            <Route path="/" element={<ParcelPortfolio />} />
            <Route path="/portfolio" element={<ParcelPortfolio />} />

            {/* Screen 2 : Past Events & Paleoclimatic Stress Analysis */}
            <Route path="/events/:id" element={<PastEventsScreen />} />
            <Route path="/events" element={<PastEventsScreen />} />

            {/* Screen 3 : Reforestation & Agroforestry Strategy */}
            <Route path="/reforestation" element={<ReforestationPlanScreen />} />

            {/* Screen 4 : Resilience Passport (Innovation I1 Bankable Certificate) */}
            <Route path="/passport/:id" element={<ResiliencePassportScreen />} />
            <Route path="/passport" element={<ResiliencePassportScreen />} />

            {/* Global Interactive Map & Agronomic Explorer */}
            <Route path="/map" element={<Home />} />
            <Route path="/parcel/:id" element={<ParcelDetail />} />

            {/* Macro Institutional Dashboard */}
            <Route path="/dashboard" element={<Dashboard />} />

            {/* Catch-all redirect to portfolio */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        
        {/* Sovereign Floating Chatbot */}
        <ChatWidget />

        {/* Luxury AgriTech Footer */}
        <footer className="bg-[#030805] text-slate-400 text-xs py-8 border-t border-white/[0.08]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="space-y-1 text-center sm:text-left">
              <p className="font-serif text-white font-bold tracking-wide">
                TerraLux <span className="text-emerald-400 italic">AI</span> — Luxury AgriTech & Sovereign Intelligence
              </p>
              <p className="text-[11px] text-slate-500 font-mono">
                Conforme RGPD Art. 30 • Immunité Cloud Act 100% UE • Validé EIP-Agri Luxembourg
              </p>
            </div>
            <p className="text-[11px] text-slate-400 font-mono text-center sm:text-right">
              Données Certifiées : NASA POWER • ISRIC SoilGrids v2 • FAO ECOCROP • NOAA IBTrACS
            </p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
