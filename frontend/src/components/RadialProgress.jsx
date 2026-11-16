import React from 'react';

export default function RadialProgress({ 
  value = 85, 
  size = 72, 
  strokeWidth = 6, 
  color = '#4ADE80', 
  label = '', 
  subtitle = '',
  showPercent = true 
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg className="w-full h-full -rotate-90" viewBox={`0 0 ${size} ${size}`}>
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            className="text-white/10"
          />
          {/* Progress Arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            style={{
              transition: 'stroke-dashoffset 1s ease-in-out',
              filter: `drop-shadow(0 0 6px ${color}88)`
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="font-mono font-bold text-white tracking-tighter" style={{ fontSize: size * 0.28 }}>
            {value}
            {showPercent && <span className="text-[10px] text-white/50 font-normal">%</span>}
          </span>
        </div>
      </div>
      {label && <span className="text-xs font-semibold text-slate-200 mt-2 text-center">{label}</span>}
      {subtitle && <span className="text-[10px] text-slate-400 font-mono text-center">{subtitle}</span>}
    </div>
  );
}
