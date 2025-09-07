import React from 'react';
import { Link } from 'react-router-dom';
import EcoTrackLogo from './EcoTrackLogo';
import { Leaf, BarChart3, Calculator } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <EcoTrackLogo size="md" />
            <div>
              <h1 className="text-xl font-bold text-gray-900">EcoTrack</h1>
              <p className="text-sm text-gray-600">Carbon Footprint Tracker</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link 
              to="/" 
              className="flex items-center space-x-2 text-gray-600 hover:text-eco-dark transition-colors"
            >
              <Calculator className="w-4 h-4" />
              <span>Calculate</span>
            </Link>
            <Link 
              to="/dashboard" 
              className="flex items-center space-x-2 text-gray-600 hover:text-eco-dark transition-colors"
            >
              <BarChart3 className="w-4 h-4" />
              <span>Dashboard</span>
            </Link>
            <Link 
              to="/about" 
              className="flex items-center space-x-2 text-gray-600 hover:text-eco-dark transition-colors"
            >
              <Leaf className="w-4 h-4" />
              <span>About</span>
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden p-2 text-gray-600 hover:text-eco-dark">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
