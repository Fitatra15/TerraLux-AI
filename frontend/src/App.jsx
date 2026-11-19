import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import ParcelPortfolio from './pages/ParcelPortfolio';
import PastEventsScreen from './pages/PastEventsScreen';
import ReforestationPlanScreen from './pages/ReforestationPlanScreen';
import ResiliencePassportScreen from './pages/ResiliencePassportScreen';
import GuidesPage from './pages/GuidesPage';
import SettingsPage from './pages/SettingsPage';
import AboutPage from './pages/AboutPage';
import Home from './pages/Home';
import ParcelDetail from './pages/ParcelDetail';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#06120D] text-slate-100 flex flex-col font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
        
        {/* Desktop Fixed Sidebar & Mobile Drawer */}
        <Sidebar 
          isOpen={mobileSidebarOpen} 
          onClose={() => setMobileSidebarOpen(false)} 
        />

        {/* Main Application Container (Offset by sidebar width on desktop) */}
        <div className="flex-1 flex flex-col md:pl-64 transition-all duration-300">
          
          {/* Topbar with Language Selector and Navigation */}
          <Topbar onOpenSidebar={() => setMobileSidebarOpen(true)} />

          {/* Page Content */}
          <main className="flex-1 p-2 sm:p-4">
            <Routes>
              {/* Core SaaS Routes */}
              <Route path="/" element={<ParcelPortfolio />} />
              <Route path="/portfolio" element={<ParcelPortfolio />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/passport/:id" element={<ResiliencePassportScreen />} />
              <Route path="/passport" element={<ResiliencePassportScreen />} />
              <Route path="/guides" element={<GuidesPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/about" element={<AboutPage />} />

              {/* Agronomic & Scientific Feature Routes */}
              <Route path="/events/:id" element={<PastEventsScreen />} />
              <Route path="/events" element={<PastEventsScreen />} />
              <Route path="/reforestation" element={<ReforestationPlanScreen />} />
              <Route path="/map" element={<Home />} />
              <Route path="/parcel/:id" element={<ParcelDetail />} />

              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>

          {/* Luxury AgriTech Footer */}
          <footer className="bg-[#030805] text-slate-400 text-xs py-8 px-6 sm:px-12 border-t border-white/[0.08]">
            <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="space-y-1 text-center sm:text-left">
                <p className="font-serif text-white font-bold tracking-wide">
                  TerraLux <span className="text-emerald-400 italic">AI</span> — Luxury AgriTech & Sovereign Intelligence
                </p>
                <p className="text-[11px] text-slate-500 font-mono">
                  The TerraLux Team • Conforme RGPD Art. 30 • Immunité Cloud Act 100% UE
                </p>
              </div>
              <p className="text-[11px] text-slate-400 font-mono text-center sm:text-right">
                NASA POWER • ISRIC SoilGrids v2 • FAO ECOCROP • NOAA IBTrACS
              </p>
            </div>
          </footer>

        </div>

      </div>
    </BrowserRouter>
  );
}
