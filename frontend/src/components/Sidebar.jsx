import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  BarChart3, Sprout, Award, BookOpen, 
  Settings, Info, Map, X, ShieldCheck 
} from 'lucide-react';
import Logo from './Logo';

export default function Sidebar({ isOpen, onClose }) {
  const { t } = useTranslation();

  const navItems = [
    { to: '/dashboard', label: t('nav.dashboard'), icon: BarChart3 },
    { to: '/', label: t('nav.parcels'), icon: Sprout },
    { to: '/passport', label: t('nav.passport'), icon: Award },
    { to: '/guides', label: t('nav.guides'), icon: BookOpen },
    { to: '/settings', label: t('nav.settings'), icon: Settings },
    { to: '/about', label: t('nav.about'), icon: Info },
  ];

  const content = (
    <div className="h-full flex flex-col justify-between p-6">
      {/* Brand & Logo */}
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <Logo variant="dark" size="md" />
          {/* Close button for mobile drawer */}
          {onClose && (
            <button
              onClick={onClose}
              className="md:hidden p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Navigation List */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                end={item.to === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-mono font-medium transition-all duration-200 group ${
                    isActive
                      ? 'bg-emerald-400 text-black font-bold shadow-glow-mint'
                      : 'text-slate-300 hover:text-white hover:bg-white/[0.06]'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon className={`w-4 h-4 transition-transform group-hover:scale-110 ${isActive ? 'text-black' : 'text-emerald-400'}`} />
                    <span className="tracking-wide">{item.label}</span>
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Sovereign Trust Box in Bottom of Sidebar */}
      <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 space-y-2">
        <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono font-bold">
          <ShieldCheck className="w-4 h-4 text-emerald-300" />
          <span>{t('brand.tier')}</span>
        </div>
        <p className="text-[10px] text-slate-400 font-mono leading-tight">
          {t('brand.eu_status')}
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Fixed Sidebar */}
      <aside className="hidden md:flex flex-col w-64 shrink-0 bg-[#06120D] border-r border-white/10 fixed inset-y-0 left-0 z-40">
        {content}
      </aside>

      {/* Mobile Drawer Backdrop & Sidebar */}
      {isOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          <div 
            onClick={onClose}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm transition-opacity" 
          />
          <aside className="relative w-72 max-w-[85vw] bg-[#06120D] border-r border-white/15 h-full z-10 shadow-2xl">
            {content}
          </aside>
        </div>
      )}
    </>
  );
}
