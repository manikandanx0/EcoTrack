import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import EcoTrackLogo from './EcoTrackLogo';
import { Calculator, User, Trophy, LogOut, Menu, X } from 'lucide-react';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
    setMobileMenuOpen(false);
  };

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

          {/* Desktop Navigation */}
          {user && (
            <nav className="hidden md:flex items-center space-x-6">
              <Link 
                to="/" 
                className={`flex items-center space-x-2 transition-colors ${
                  isActive('/') ? 'text-green-600' : 'text-gray-600 hover:text-green-600'
                }`}
              >
                <Calculator className="w-4 h-4" />
                <span>Calculate</span>
              </Link>
              <Link 
                to="/leaderboard" 
                className={`flex items-center space-x-2 transition-colors ${
                  isActive('/leaderboard') ? 'text-green-600' : 'text-gray-600 hover:text-green-600'
                }`}
              >
                <Trophy className="w-4 h-4" />
                <span>Leaderboard</span>
              </Link>
              <Link 
                to="/profile" 
                className={`flex items-center space-x-2 transition-colors ${
                  isActive('/profile') ? 'text-green-600' : 'text-gray-600 hover:text-green-600'
                }`}
              >
                <User className="w-4 h-4" />
                <span>Profile</span>
              </Link>
            </nav>
          )}

          {/* User Menu / Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  Welcome, <span className="font-medium">{user.name}</span>
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 text-gray-600 hover:text-red-600 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-sm text-gray-600 hover:text-green-600 transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button 
            className="md:hidden p-2 text-gray-600 hover:text-green-600"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pb-4 border-t border-gray-200">
            <nav className="flex flex-col space-y-3 pt-4">
              {user ? (
                <>
                  <Link 
                    to="/" 
                    className={`flex items-center space-x-2 py-2 transition-colors ${
                      isActive('/') ? 'text-green-600' : 'text-gray-600'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <Calculator className="w-4 h-4" />
                    <span>Calculate</span>
                  </Link>
                  <Link 
                    to="/leaderboard" 
                    className={`flex items-center space-x-2 py-2 transition-colors ${
                      isActive('/leaderboard') ? 'text-green-600' : 'text-gray-600'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <Trophy className="w-4 h-4" />
                    <span>Leaderboard</span>
                  </Link>
                  <Link 
                    to="/profile" 
                    className={`flex items-center space-x-2 py-2 transition-colors ${
                      isActive('/profile') ? 'text-green-600' : 'text-gray-600'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <User className="w-4 h-4" />
                    <span>Profile</span>
                  </Link>
                  <div className="pt-3 border-t border-gray-200">
                    <div className="text-sm text-gray-600 mb-2">
                      Welcome, <span className="font-medium">{user.name}</span>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="flex items-center space-x-2 text-gray-600 hover:text-red-600 transition-colors"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="flex items-center space-x-2 py-2 text-gray-600"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <span>Login</span>
                  </Link>
                  <Link
                    to="/register"
                    className="flex items-center space-x-2 py-2 text-green-600 font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <span>Sign Up</span>
                  </Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
