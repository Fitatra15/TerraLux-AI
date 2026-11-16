import React from 'react';

export default function Logo({ 
  variant = 'dark', 
  className = '', 
  size = 'md', 
  withText = true,
  useImage = false 
}) {
  const isDark = variant === 'dark';

  // Dimension presets
  const sizeMap = {
    sm: { icon: 'w-7 h-7', text: 'text-lg', badge: 'text-[9px]' },
    md: { icon: 'w-9 h-9', text: 'text-xl', badge: 'text-[10px]' },
    lg: { icon: 'w-12 h-12', text: 'text-2xl', badge: 'text-xs' },
  };
  const dims = sizeMap[size] || sizeMap.md;

  if (useImage) {
    return (
      <div className={`flex items-center gap-3 ${className}`}>
        <img 
          src="/logo.jpg" 
          alt="TerraLux Logo" 
          className={`${dims.icon} rounded-xl object-contain shadow-glow-mint`} 
        />
        {withText && (
          <div className="flex flex-col">
            <span className={`font-serif font-black tracking-tight leading-none ${dims.text}`}>
              <span className={isDark ? 'text-white' : 'text-slate-900'}>Terra</span>
              <span className="text-emerald-400">Lux</span>
            </span>
            <span className="text-[10px] font-mono tracking-widest uppercase text-emerald-400/80">
              AI Infrastructure
            </span>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      {/* Precision Vector Emblem matching the uploaded logo */}
      <div className={`relative ${dims.icon} shrink-0`}>
        <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
          {/* Outer circle */}
          <circle 
            cx="50" 
            cy="50" 
            r="46" 
            fill={isDark ? "#081b13" : "#F8FAFC"} 
            stroke={isDark ? "#10B981" : "#0F172A"} 
            strokeWidth="5" 
          />
          
          {/* Satellite Orbit Line & Nodes */}
          <path
            d="M 22,35 Q 50,55 78,35"
            fill="none"
            stroke="#4ADE80"
            strokeWidth="3.5"
            strokeDasharray="1, 0"
          />
          <circle cx="36" cy="43" r="3.5" fill="#FFFFFF" />
          <circle cx="64" cy="43" r="3.5" fill="#4ADE80" />

          {/* Satellite Symbol in Top Area */}
          <g transform="translate(42, 16) rotate(30)">
            <rect x="5" y="5" width="14" height="10" rx="2" fill="#4ADE80" />
            <line x1="0" y1="10" x2="5" y2="10" stroke="#FFFFFF" strokeWidth="2.5" />
            <line x1="19" y1="10" x2="24" y2="10" stroke="#FFFFFF" strokeWidth="2.5" />
            <rect x="-3" y="6" width="3" height="8" rx="1" fill="#FFFFFF" />
            <rect x="24" y="6" width="3" height="8" rx="1" fill="#FFFFFF" />
          </g>

          {/* Agricultural Waves / Leaf Strands in Bottom Area */}
          <path
            d="M 20,62 C 32,54 44,70 52,58 C 42,76 30,80 20,62 Z"
            fill="#10B981"
          />
          <path
            d="M 24,76 C 36,68 48,82 58,68 C 48,86 34,90 24,76 Z"
            fill="#4ADE80"
          />
          <path
            d="M 32,84 C 44,78 54,88 66,76 C 54,92 40,94 32,84 Z"
            fill="#059669"
          />
        </svg>
      </div>

      {/* Wordmark */}
      {withText && (
        <div className="flex flex-col">
          <div className="flex items-center gap-1.5 leading-none">
            <span className={`font-serif font-black tracking-tight ${dims.text}`}>
              <span className={isDark ? 'text-white' : 'text-slate-900'}>Terra</span>
              <span className="text-emerald-400">Lux</span>
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold uppercase tracking-wider">
              AI
            </span>
          </div>
          <span className="text-[10px] font-mono tracking-wider text-slate-400 mt-0.5">
            AgriTech Sovereign
          </span>
        </div>
      )}
    </div>
  );
}
