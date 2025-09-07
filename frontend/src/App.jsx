import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import EcoTrackLogo from './components/EcoTrackLogo';
import Header from './components/Header';
import InputForm from './components/InputForm';
import Dashboard from './components/Dashboard';
import OffsetRecommender from './components/OffsetRecommender';
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';
import Leaderboard from './components/Leaderboard';
import Suggestions from './components/Suggestions';
import axios from 'axios';
import toast from 'react-hot-toast';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

// Main App Component
const AppContent = () => {
  const [footprintData, setFootprintData] = useState(null);
  const [loading, setLoading] = useState(false);

  const { token } = useAuth();

  const handleCalculate = async (formData) => {
    setLoading(true);
    try {
      // Calculate baseline footprint
      const response = await axios.post('http://localhost:8000/api/calc', formData, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      const baselineData = response.data;

      setFootprintData({
        baseline: baselineData,
        formData: formData
      });
      
      toast.success('Carbon footprint calculated successfully!');
    } catch (error) {
      console.error('Error calculating footprint:', error);
      toast.error('Error calculating footprint. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <Header />
        
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <div className="max-w-4xl mx-auto">
                    <div className="text-center mb-8">
                      <EcoTrackLogo size="xl" className="mx-auto mb-4" />
                      <h1 className="text-4xl font-bold text-gray-900 mb-2">
                        Hybrid Carbon Footprint Tracker
                      </h1>
                      <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                        Calculate your personal carbon footprint using our hybrid approach: 
                        rule-based baseline calculations combined with AI refinements for 
                        accurate and personalized results.
                      </p>
                    </div>
                    
                    <InputForm 
                      onSubmit={handleCalculate} 
                      loading={loading}
                    />
                    
                    {footprintData && footprintData.baseline && footprintData.baseline.breakdown && (
                      <div className="mt-8 space-y-6">
                        <Dashboard data={footprintData} />
                        <Suggestions breakdown={footprintData.baseline.breakdown} />
                        <OffsetRecommender footprint={footprintData.baseline.baseline_total} />
                      </div>
                    )}
                  </div>
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Navigate to="/" />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/leaderboard" 
              element={
                <ProtectedRoute>
                  <Leaderboard />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </main>
        
        <footer className="bg-white border-t border-gray-200 py-6 mt-12">
          <div className="container mx-auto px-4 text-center text-gray-600">
            <div className="flex items-center justify-center mb-2">
              <EcoTrackLogo size="sm" className="mr-2" />
              <span className="font-semibold">EcoTrack</span>
            </div>
            <p className="text-sm">
              Hybrid Carbon Footprint Tracker - Making sustainability measurable and actionable
            </p>
          </div>
        </footer>
        
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#4ade80',
                secondary: '#fff',
              },
            },
            error: {
              duration: 4000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

// Main App with Auth Provider
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
