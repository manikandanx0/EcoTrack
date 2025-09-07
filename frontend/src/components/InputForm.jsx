import React, { useState } from 'react';
import { Car, Utensils, Zap, Trash2, ShoppingBag } from 'lucide-react';

const InputForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    // Transport
    commute_km: 0,
    transport_mode: 'car_petrol',
    
    // Food (kg per week)
    beef_kg: 0,
    chicken_kg: 0,
    pork_kg: 0,
    fish_kg: 0,
    dairy_kg: 0,
    vegetables_kg: 0,
    fruits_kg: 0,
    
    // Energy
    electricity_kwh: 0,
    natural_gas_kwh: 0,
    
    // Waste
    waste_kg: 0,
    recycled_kg: 0,
    
    // Consumption
    clothing_kg: 0,
    electronics_items: 0,
    
    // Optional ML features
    house_size: null,
    occupants: null,
    ac_hours: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? 0 : parseFloat(value) || 0
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const transportModes = [
    { value: 'car_petrol', label: 'Car (Petrol)' },
    { value: 'car_diesel', label: 'Car (Diesel)' },
    { value: 'car_hybrid', label: 'Car (Hybrid)' },
    { value: 'car_ev', label: 'Car (Electric)' },
    { value: 'bus_diesel', label: 'Bus' },
    { value: 'train_electric', label: 'Train' },
    { value: 'bicycle', label: 'Bicycle' },
    { value: 'walking', label: 'Walking' },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Transport Section */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Car className="w-5 h-5 text-eco-dark mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Transportation</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Daily Commute Distance (km)
            </label>
            <input
              type="number"
              name="commute_km"
              value={formData.commute_km}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Transport Mode
            </label>
            <select
              name="transport_mode"
              value={formData.transport_mode}
              onChange={handleInputChange}
              className="input-field"
            >
              {transportModes.map(mode => (
                <option key={mode.value} value={mode.value}>
                  {mode.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Food Section */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Utensils className="w-5 h-5 text-eco-dark mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Food Consumption (per week)</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Beef (kg)
            </label>
            <input
              type="number"
              name="beef_kg"
              value={formData.beef_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Chicken (kg)
            </label>
            <input
              type="number"
              name="chicken_kg"
              value={formData.chicken_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Pork (kg)
            </label>
            <input
              type="number"
              name="pork_kg"
              value={formData.pork_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fish (kg)
            </label>
            <input
              type="number"
              name="fish_kg"
              value={formData.fish_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dairy (kg)
            </label>
            <input
              type="number"
              name="dairy_kg"
              value={formData.dairy_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Vegetables (kg)
            </label>
            <input
              type="number"
              name="vegetables_kg"
              value={formData.vegetables_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fruits (kg)
            </label>
            <input
              type="number"
              name="fruits_kg"
              value={formData.fruits_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
        </div>
      </div>

      {/* Energy Section */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Zap className="w-5 h-5 text-eco-dark mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Energy Usage (per month)</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Electricity (kWh)
            </label>
            <input
              type="number"
              name="electricity_kwh"
              value={formData.electricity_kwh}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Natural Gas (kWh)
            </label>
            <input
              type="number"
              name="natural_gas_kwh"
              value={formData.natural_gas_kwh}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="1"
            />
          </div>
        </div>
      </div>

      {/* Waste Section */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Trash2 className="w-5 h-5 text-eco-dark mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Waste Management (per week)</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Waste to Landfill (kg)
            </label>
            <input
              type="number"
              name="waste_kg"
              value={formData.waste_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recycled Waste (kg)
            </label>
            <input
              type="number"
              name="recycled_kg"
              value={formData.recycled_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
        </div>
      </div>

      {/* Consumption Section */}
      <div className="card">
        <div className="flex items-center mb-4">
          <ShoppingBag className="w-5 h-5 text-eco-dark mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Consumption (per month)</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Clothing Purchases (kg)
            </label>
            <input
              type="number"
              name="clothing_kg"
              value={formData.clothing_kg}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Electronics Items
            </label>
            <input
              type="number"
              name="electronics_items"
              value={formData.electronics_items}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              step="1"
            />
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <div className="text-center">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary px-8 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Calculating...
            </div>
          ) : (
            'Calculate My Carbon Footprint'
          )}
        </button>
      </div>
    </form>
  );
};

export default InputForm;
