import React, { useState, useEffect } from 'react';
import { Leaf, ExternalLink, Download, CheckCircle } from 'lucide-react';

const OffsetRecommender = ({ footprint }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [purchased, setPurchased] = useState(false);

  useEffect(() => {
    if (footprint > 0) {
      fetchRecommendations();
    }
  }, [footprint]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/offset', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ footprint_kg: footprint }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch offset recommendations');
      }

      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (project) => {
    setSelectedProject(project);
    // Simulate purchase process
    setTimeout(() => {
      setPurchased(true);
    }, 2000);
  };

  const getProjectIcon = (type) => {
    switch (type) {
      case 'Reforestation':
        return '🌳';
      case 'Renewable Energy':
        return '⚡';
      case 'Energy Efficiency':
        return '💡';
      default:
        return '🌱';
    }
  };

  const getProjectColor = (type) => {
    switch (type) {
      case 'Reforestation':
        return 'bg-green-100 border-green-200 text-green-800';
      case 'Renewable Energy':
        return 'bg-blue-100 border-blue-200 text-blue-800';
      case 'Energy Efficiency':
        return 'bg-yellow-100 border-yellow-200 text-yellow-800';
      default:
        return 'bg-gray-100 border-gray-200 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-eco-light mx-auto mb-4"></div>
          <p className="text-gray-600">Finding the best offset options for you...</p>
        </div>
      </div>
    );
  }

  if (purchased && selectedProject) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Offset Purchase Successful!</h3>
          <p className="text-gray-600 mb-6">
            You've successfully offset {(typeof footprint === 'number' ? footprint.toFixed(1) : footprint)} kg of CO₂ emissions through the{' '}
            <strong>{selectedProject.project_name}</strong> project.
          </p>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <h4 className="font-semibold text-green-800 mb-2">Transaction Details</h4>
            <div className="text-sm text-green-700 space-y-1">
              <p><strong>Project:</strong> {selectedProject.project_name}</p>
              <p><strong>Type:</strong> {selectedProject.project_type}</p>
              <p><strong>Amount:</strong> ${selectedProject.total_cost.toFixed(2)}</p>
              <p><strong>Transaction ID:</strong> {selectedProject.transaction_id}</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => window.open(selectedProject.certificate_url, '_blank')}
              className="btn-primary flex items-center justify-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Download Certificate
            </button>
            <button
              onClick={() => {
                setPurchased(false);
                setSelectedProject(null);
              }}
              className="btn-secondary"
            >
              View Other Options
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center mb-6">
        <Leaf className="w-6 h-6 text-eco-dark mr-2" />
        <h3 className="text-xl font-semibold text-gray-900">Carbon Offset Recommendations</h3>
      </div>

      <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-blue-800 text-sm">
          <strong>Offset your {(typeof footprint === 'number' ? footprint.toFixed(1) : footprint)} kg CO₂ footprint</strong> by supporting verified 
          carbon reduction projects. Each project is blockchain-verified and provides transparent 
          impact tracking.
        </p>
      </div>

      <div className="space-y-4">
        {recommendations.map((project, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start">
                <div className="text-2xl mr-3">{getProjectIcon(project.project_type)}</div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-1">
                    {project.project_name}
                  </h4>
                  <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium border ${getProjectColor(project.project_type)}`}>
                    {project.project_type}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900">
                  ${project.total_cost.toFixed(2)}
                </div>
                <div className="text-sm text-gray-600">
                  ${project.cost_per_ton}/ton CO₂
                </div>
              </div>
            </div>

            <p className="text-gray-600 mb-4">
              {project.impact_description}
            </p>

            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                <span className="font-medium">Transaction ID:</span> {project.transaction_id}
              </div>
              <button
                onClick={() => handlePurchase(project)}
                className="btn-primary"
              >
                Purchase Offset
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-semibold text-gray-900 mb-2">How Carbon Offsets Work</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Each offset represents 1 kg of CO₂ removed from or prevented from entering the atmosphere</li>
          <li>• Projects are verified by third-party standards and blockchain technology</li>
          <li>• You receive a certificate proving your environmental impact</li>
          <li>• Offsets are additional to, not a replacement for, reducing your own emissions</li>
        </ul>
      </div>
    </div>
  );
};

export default OffsetRecommender;
