import React from 'react';

const sizes = {
  sm: 24,
  md: 36,
  lg: 48,
  xl: 64,
};

const EcoTrackLogo = ({ size = 'md', className = '' }) => {
  const px = sizes[size] || sizes.md;
  return (
    <div className={`inline-flex items-center ${className}`}>
      <svg width={px} height={px} viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="32" cy="32" r="30" stroke="#16A34A" strokeWidth="4" fill="#ECFDF5" />
        <path d="M18 38c10-2 16-8 18-18 6 8 6 18-2 26-6 6-14 8-22 6 4-4 6-8 6-14z" fill="#16A34A" />
      </svg>
      <span className="ml-2 font-semibold text-eco-dark">EcoTrack</span>
    </div>
  );
};

export default EcoTrackLogo;

import React from 'react';

const EcoTrackLogo = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-20 h-20'
  };

  return (
    <div className={`${sizeClasses[size]} ${className} relative`}>
      {/* Logo Container */}
      <div className="w-full h-full rounded-full overflow-hidden border-2 border-white shadow-lg">
        {/* Top half - Light green */}
        <div className="h-1/2 bg-gradient-to-b from-green-400 to-green-500 relative">
          {/* Top leaf */}
          <svg
            className="absolute top-2 left-1/2 transform -translate-x-1/2 w-4 h-4 text-white"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 2C8 2 4 6 4 10c0 4 4 8 8 8s8-4 8-8c0-4-4-8-8-8z" />
            <path d="M12 6v8" />
            <path d="M8 10h8" />
          </svg>
        </div>
        
        {/* Bottom half - Dark green */}
        <div className="h-1/2 bg-gradient-to-b from-green-600 to-green-700 relative">
          {/* Bottom leaf */}
          <svg
            className="absolute bottom-2 right-3 w-3 h-3 text-white transform rotate-12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 2C8 2 4 6 4 10c0 4 4 8 8 8s8-4 8-8c0-4-4-8-8-8z" />
            <path d="M12 6v8" />
            <path d="M8 10h8" />
          </svg>
        </div>
        
        {/* ECOTRACK Text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-white font-bold text-xs leading-none tracking-tight">
            ECOTRACK
          </span>
        </div>
      </div>
    </div>
  );
};

export default EcoTrackLogo;
