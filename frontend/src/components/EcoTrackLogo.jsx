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
