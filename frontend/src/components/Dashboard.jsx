import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Leaf, Zap, Car, Utensils, Trash2, ShoppingBag, Download } from 'lucide-react';
import jsPDF from 'jspdf';

const Dashboard = ({ data }) => {
  const { baseline, refined } = data;

  // Category metadata defined before use
  const categoryColors = {
    transport: '#3B82F6',
    food: '#EF4444',
    energy: '#F59E0B',
    waste: '#8B5CF6',
    consumption: '#10B981'
  };

  const categoryIcons = {
    transport: Car,
    food: Utensils,
    energy: Zap,
    waste: Trash2,
    consumption: ShoppingBag
  };

  function getCategoryColor(category) {
    return categoryColors[category] || '#6B7280';
  }

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

  

  const totalBaseline = baseline.baseline_total;
  const totalRefined = refined ? refined.refined_total : null;
  const improvement = totalRefined ? ((totalBaseline - totalRefined) / totalBaseline * 100) : 0;

  const exportToPDF = () => {
    const doc = new jsPDF({ unit: 'pt', format: 'a4' });
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    // Header band
    doc.setFillColor(22, 163, 74); // eco green
    doc.rect(0, 0, pageWidth, 70, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.text('EcoTrack — Carbon Footprint Report', 40, 42);
    doc.setFontSize(11);
    doc.text(`Generated on ${new Date().toLocaleString()}`, 40, 58);

    // Reset text color
    doc.setTextColor(0, 0, 0);

    let y = 95;

    // Summary cards
    const card = (x, title, value, subtitle, color) => {
      doc.setDrawColor(229, 231, 235);
      doc.setFillColor(249, 250, 251);
      doc.roundedRect(x, y, 180, 90, 8, 8, 'FD');
      doc.setFontSize(12);
      doc.setTextColor(75, 85, 99);
      doc.text(title, x + 14, y + 24);
      doc.setTextColor(color[0], color[1], color[2]);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(24);
      doc.text(value, x + 14, y + 56);
      doc.setTextColor(107, 114, 128);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(11);
      doc.text(subtitle, x + 14, y + 76);
      doc.setTextColor(0, 0, 0);
    };

    card(40, 'Baseline Footprint', `${totalBaseline.toFixed(1)} kg CO₂`, 'Total emissions', [16, 163, 74]);
    if (totalRefined) {
      card(240, 'AI Refined', `${totalRefined.toFixed(1)} kg CO₂`, 'Model-adjusted', [59, 130, 246]);
      card(440, 'Improvement', `${improvement.toFixed(1)}%`, 'Reduction vs baseline', [34, 197, 94]);
    }

    y += 120;

    // Breakdown section
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('Emissions Breakdown', 40, y);
    y += 18;

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    const lineHeight = 18;
    Object.entries(baseline.breakdown).forEach(([category, value]) => {
      const pct = (Math.abs(value) / totalBaseline) * 100;
      const text = `${category.charAt(0).toUpperCase() + category.slice(1)} — ${Math.abs(value).toFixed(1)} kg CO₂ (${pct.toFixed(1)}%)`;
      doc.text(text, 48, y);
      // bar visualization
      const barWidth = Math.min(400, (pct / 100) * 400);
      doc.setFillColor(16, 185, 129);
      doc.roundedRect(350, y - 10, barWidth, 8, 3, 3, 'F');
      y += lineHeight;
      if (y > pageHeight - 100) {
        doc.addPage();
        y = 60;
      }
    });

    // Recommendations section
    if (y > pageHeight - 160) {
      doc.addPage();
      y = 60;
    }
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('Recommendations', 40, y);
    y += 16;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    Object.entries(baseline.breakdown).forEach(([category, value]) => {
      const pct = (Math.abs(value) / totalBaseline) * 100;
      if (pct > 20) {
        doc.text(`• Focus on reducing ${category} (currently ${pct.toFixed(1)}% of footprint)`, 48, y);
        y += 16;
      }
    });
    if (totalRefined && improvement !== 0) {
      const msg = improvement > 0 ? 'reduction' : 'increase';
      doc.text(`• AI refinement indicates a ${Math.abs(improvement).toFixed(1)}% ${msg}`, 48, y);
      y += 16;
    }

    // Footer
    doc.setFontSize(10);
    doc.setTextColor(107, 114, 128);
    doc.text('EcoTrack — Hybrid Carbon Footprint Tracker', pageWidth / 2, pageHeight - 24, { align: 'center' });

    doc.save('carbon-footprint-report.pdf');
  };

  return (
    <div className="space-y-6">
      {/* Export Button */}
      <div className="flex justify-end">
        <button
          onClick={exportToPDF}
          className="btn-secondary flex items-center"
        >
          <Download className="w-4 h-4 mr-2" />
          Export PDF Report
        </button>
      </div>

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
            const Icon = categoryIcons[category] || Leaf;
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
                            .map(([key, val]) => {
                              const isNumber = typeof val === 'number' && isFinite(val);
                              return isNumber ? `${key}: ${Math.abs(val).toFixed(1)} kg CO₂` : `${key}: ${String(val)}`;
                            })
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

      {/* ML Insights */}
      {refined && refined.details && refined.details.ml_insights && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-center mb-4">
            <div className="w-6 h-6 text-blue-600 mr-2">🤖</div>
            <h3 className="text-lg font-semibold text-gray-900">AI Insights</h3>
          </div>
          <div className="space-y-3">
            {refined.details.ml_insights.map((insight, index) => (
              <div key={index} className="p-3 bg-white border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>AI Analysis:</strong> {insight}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Insights & Recommendations */}
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

          {totalRefined && improvement < 0 && (
            <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
              <p className="text-sm text-orange-800">
                <strong>AI Adjustment:</strong> Our model adjusted your footprint by {Math.abs(improvement).toFixed(1)}% 
                based on your specific circumstances and patterns.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
