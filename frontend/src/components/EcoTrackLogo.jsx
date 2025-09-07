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
