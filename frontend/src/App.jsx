import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import EcoTrackLogo from './components/EcoTrackLogo';
import Header from './components/Header';
import InputForm from './components/InputForm';
import Dashboard from './components/Dashboard';
import OffsetRecommender from './components/OffsetRecommender';

function App() {
  const [footprintData, setFootprintData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async (formData) => {
    setLoading(true);
    try {
      // Calculate baseline footprint
      const baselineResponse = await fetch('/api/calc', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!baselineResponse.ok) {
        throw new Error('Failed to calculate baseline footprint');
      }

      const baselineData = await baselineResponse.json();

      // Refine with ML (placeholder)
      const refinedResponse = await fetch('/api/refine', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!refinedResponse.ok) {
        throw new Error('Failed to refine footprint');
      }

      const refinedData = await refinedResponse.json();

      setFootprintData({
        baseline: baselineData,
        refined: refinedData,
        formData: formData
      });
    } catch (error) {
      console.error('Error calculating footprint:', error);
      alert('Error calculating footprint. Please try again.');
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
            <Route 
              path="/" 
              element={
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
                  
                  {footprintData && (
                    <div className="mt-8 space-y-6">
                      <Dashboard data={footprintData} />
                      <OffsetRecommender footprint={footprintData.refined.baseline_total} />
                    </div>
                  )}
                </div>
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
      </div>
    </Router>
  );
}

export default App;
