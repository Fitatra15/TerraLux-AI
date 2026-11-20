import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  BookOpen, MapPin, Activity, Sprout, Award, 
  ChevronDown, ChevronUp, CheckCircle2, ArrowRight 
} from 'lucide-react';
import { Link } from 'react-router-dom';

export default function GuidesPage() {
  const { t } = useTranslation();
  const [openStep, setOpenStep] = useState(1);

  const steps = [
    {
      step: 1,
      title: t('guides.step1_title'),
      desc: t('guides.step1_desc'),
      icon: MapPin,
      badge: "Cadastre & NASA GPS",
      color: "text-emerald-400",
      cta: { text: t('actions.add_parcel'), to: '/' }
    },
    {
      step: 2,
      title: t('guides.step2_title'),
      desc: t('guides.step2_desc'),
      icon: Activity,
      badge: "SoilGrids & Climate",
      color: "text-cyan-400",
      cta: { text: t('actions.view_history'), to: '/events' }
    },
    {
      step: 3,
      title: t('guides.step3_title'),
      desc: t('guides.step3_desc'),
      icon: Sprout,
      badge: "FAO ECOCROP & Margins",
      color: "text-amber-400",
      cta: { text: t('actions.view_details'), to: '/parcel/845ef4e9-b776-40b4-af77-c84510862b1e' }
    },
    {
      step: 4,
      title: t('guides.step4_title'),
      desc: t('guides.step4_desc'),
      icon: Award,
      badge: "SHA-256 Certification",
      color: "text-emerald-300",
      cta: { text: t('actions.view_passport'), to: '/passport' }
    }
  ];

  return (
    <div className="min-h-screen bg-[#06120D] text-slate-100 py-10 px-4 sm:px-6 lg:px-12 selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto space-y-10">

        {/* Header */}
        <div className="space-y-3 pb-6 border-b border-white/10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Interactive Operational Guides</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-serif text-white tracking-tight">
            {t('guides.title')}
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl font-light">
            {t('guides.subtitle')}
          </p>
        </div>

        {/* Stepper / Accordion List */}
        <div className="space-y-4">
          {steps.map((item) => {
            const Icon = item.icon;
            const isOpen = openStep === item.step;

            return (
              <div 
                key={item.step}
                className="rounded-3xl glass-card overflow-hidden transition-all duration-300 border border-white/10"
              >
                {/* Accordion Header */}
                <button
                  onClick={() => setOpenStep(isOpen ? 0 : item.step)}
                  className="w-full p-6 sm:p-8 flex items-center justify-between text-left hover:bg-white/[0.02] transition-colors"
                >
                  <div className="flex items-center gap-4 sm:gap-6">
                    <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0 shadow-inner">
                      <Icon className={`w-6 h-6 ${item.color}`} />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 font-bold">
                          {item.badge}
                        </span>
                      </div>
                      <h2 className="text-lg sm:text-xl font-serif font-bold text-white mt-1">
                        {item.title}
                      </h2>
                    </div>
                  </div>

                  <div className="p-2 rounded-xl bg-white/5 text-slate-400">
                    {isOpen ? <ChevronUp className="w-5 h-5 text-emerald-400" /> : <ChevronDown className="w-5 h-5" />}
                  </div>
                </button>

                {/* Accordion Content */}
                {isOpen && (
                  <div className="px-6 sm:px-8 pb-8 pt-2 border-t border-white/5 space-y-4">
                    <p className="text-sm text-slate-300 leading-relaxed font-light">
                      {item.desc}
                    </p>

                    <div className="flex items-center justify-between pt-2">
                      <div className="flex items-center gap-2 text-xs font-mono text-emerald-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Sovereign real-time audited process</span>
                      </div>

                      <Link
                        to={item.cta.to}
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-400 text-black text-xs font-mono font-bold shadow-glow-mint hover:bg-emerald-300 transition-colors"
                      >
                        <span>{item.cta.text}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}
