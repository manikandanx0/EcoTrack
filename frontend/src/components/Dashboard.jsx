import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Leaf, Zap, Car, Utensils, Trash2, ShoppingBag } from 'lucide-react';

const Dashboard = ({ data }) => {
  const { baseline, refined } = data;

  // Prepare data for pie chart
  const pieData = Object.entries(baseline.breakdown).map(([category, value]) => ({
    name: category.charAt(0).toUpperCase() + category.slice(1),
    value: Math.abs(value),
    color: getCategoryColor(category)
  }));

  // Prepare data for comparison chart
  const comparisonData = Object.entries(baseline.breakdown).map(([category, value]) => ({
    category: category.charAt(0).toUpperCase() + category.slice(1),
    baseline: Math.abs(value),
    refined: refined ? Math.abs(refined.breakdown[category] || 0) : 0
  }));

  const categoryIcons = {
    transport: Car,
    food: Utensils,
    energy: Zap,
    waste: Trash2,
    consumption: ShoppingBag
  };

  const categoryColors = {
    transport: '#3B82F6',
    food: '#EF4444',
    energy: '#F59E0B',
    waste: '#8B5CF6',
    consumption: '#10B981'
  };

  function getCategoryColor(category) {
    return categoryColors[category] || '#6B7280';
  }

  const totalBaseline = baseline.baseline_total;
  const totalRefined = refined ? refined.refined_total : null;
  const improvement = totalRefined ? ((totalBaseline - totalRefined) / totalBaseline * 100) : 0;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="flex items-center justify-center mb-2">
            <Leaf className="w-6 h-6 text-eco-dark mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Baseline Footprint</h3>
          </div>
          <div className="text-3xl font-bold text-gray-900 mb-1">
            {totalBaseline.toFixed(1)}
          </div>
          <div className="text-sm text-gray-600">kg CO₂</div>
        </div>

        {totalRefined && (
          <div className="card text-center">
            <div className="flex items-center justify-center mb-2">
              <TrendingUp className="w-6 h-6 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">AI Refined</h3>
            </div>
            <div className="text-3xl font-bold text-blue-600 mb-1">
              {totalRefined.toFixed(1)}
            </div>
            <div className="text-sm text-gray-600">kg CO₂</div>
          </div>
        )}

        {totalRefined && (
          <div className="card text-center">
            <div className="flex items-center justify-center mb-2">
              <TrendingUp className="w-6 h-6 text-green-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Improvement</h3>
            </div>
            <div className="text-3xl font-bold text-green-600 mb-1">
              {improvement.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">reduction</div>
          </div>
        )}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Emissions Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value.toFixed(1)} kg CO₂`, 'Emissions']} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Comparison Chart */}
        {totalRefined && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Baseline vs AI Refined</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={comparisonData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip formatter={(value) => [`${value.toFixed(1)} kg CO₂`, 'Emissions']} />
                <Legend />
                <Bar dataKey="baseline" fill="#6B7280" name="Baseline" />
                <Bar dataKey="refined" fill="#3B82F6" name="AI Refined" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Detailed Breakdown */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Breakdown</h3>
        <div className="space-y-4">
          {Object.entries(baseline.breakdown).map(([category, value]) => {
            const Icon = categoryIcons[category];
            const color = categoryColors[category];
            const refinedValue = refined ? refined.breakdown[category] : null;
            
            return (
              <div key={category} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className="p-2 rounded-full mr-3" style={{ backgroundColor: `${color}20` }}>
                    <Icon className="w-5 h-5" style={{ color }} />
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 capitalize">{category}</h4>
                    <p className="text-sm text-gray-600">
                      {baseline.details[category] && Object.keys(baseline.details[category]).length > 0
                        ? Object.entries(baseline.details[category])
                            .map(([key, val]) => `${key}: ${val.toFixed(1)} kg CO₂`)
                            .join(', ')
                        : 'No details available'
                      }
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-semibold text-gray-900">
                    {Math.abs(value).toFixed(1)} kg CO₂
                  </div>
                  {refinedValue && (
                    <div className="text-sm text-blue-600">
                      Refined: {Math.abs(refinedValue).toFixed(1)} kg CO₂
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights & Recommendations</h3>
        <div className="space-y-3">
          {Object.entries(baseline.breakdown).map(([category, value]) => {
            const percentage = (Math.abs(value) / totalBaseline) * 100;
            if (percentage > 20) {
              return (
                <div key={category} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-800">
                    <strong>{category.charAt(0).toUpperCase() + category.slice(1)}</strong> accounts for {percentage.toFixed(1)}% of your footprint. 
                    Consider reducing this category for maximum impact.
                  </p>
                </div>
              );
            }
            return null;
          })}
          
          {totalRefined && improvement > 0 && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800">
                <strong>Great news!</strong> Our AI model refined your footprint by {improvement.toFixed(1)}%, 
                providing a more accurate assessment based on your specific circumstances.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
