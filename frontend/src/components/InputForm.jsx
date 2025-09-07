import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Car, Utensils, Zap, Trash2, ShoppingBag, ChevronRight, ChevronLeft } from 'lucide-react';
import toast from 'react-hot-toast';

// Helpers to coerce empty inputs
const toZero = (schema) =>
  schema.transform((value, originalValue) => (originalValue === '' || originalValue == null ? 0 : value));

const toNull = (schema) =>
  schema
    .transform((value, originalValue) => (originalValue === '' || originalValue == null ? null : value))
    .nullable();

const schema = yup.object({
  // Transport
  commute_km: toZero(yup.number()).min(0, 'Distance cannot be negative').max(1000, 'Distance seems too high').required('Commute distance is required'),
  transport_mode: yup.string().required('Transport mode is required'),
  
  // Food (kg per week)
  beef_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  chicken_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  pork_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  fish_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  dairy_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  vegetables_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  fruits_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  
  // Energy
  electricity_kwh: toZero(yup.number()).min(0, 'Usage cannot be negative').max(10000, 'Usage seems too high').required('Electricity usage is required'),
  natural_gas_kwh: toZero(yup.number()).min(0, 'Usage cannot be negative').max(10000, 'Usage seems too high'),
  
  // Waste
  waste_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(100, 'Amount seems too high').required('Waste amount is required'),
  recycled_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(100, 'Amount seems too high'),
  
  // Consumption
  clothing_kg: toZero(yup.number()).min(0, 'Amount cannot be negative').max(50, 'Amount seems too high'),
  electronics_items: toZero(yup.number()).min(0, 'Amount cannot be negative').max(20, 'Amount seems too high'),
  
  // Optional ML features
  house_size: toNull(yup.number().min(0, 'Size cannot be negative').max(10000, 'Size seems too large')),
  occupants: toNull(yup.number().min(1, 'Must have at least 1 occupant').max(20, 'Too many occupants')),
  ac_hours: toNull(yup.number().min(0, 'Hours cannot be negative').max(24, 'Hours cannot exceed 24')),
});

const InputForm = ({ onSubmit, loading }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 5;

  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
    getValues,
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      commute_km: 0,
      transport_mode: 'car_petrol',
      beef_kg: 0,
      chicken_kg: 0,
      pork_kg: 0,
      fish_kg: 0,
      dairy_kg: 0,
      vegetables_kg: 0,
      fruits_kg: 0,
      electricity_kwh: 0,
      natural_gas_kwh: 0,
      waste_kg: 0,
      recycled_kg: 0,
      clothing_kg: 0,
      electronics_items: 0,
      house_size: null,
      occupants: null,
      ac_hours: null,
    },
  });

  const handleFormSubmit = async (data) => {
    try {
      await onSubmit(data);
    } catch (error) {
      toast.error('Failed to calculate footprint. Please try again.');
    }
  };

  const nextStep = async () => {
    const fieldsToValidate = getFieldsForStep(currentStep);
    const isValid = await trigger(fieldsToValidate);
    
    if (isValid && currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    } else if (!isValid) {
      toast.error('Please fill in all required fields correctly.');
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const getFieldsForStep = (step) => {
    switch (step) {
      case 1:
        return ['commute_km', 'transport_mode'];
      case 2:
        return ['beef_kg', 'chicken_kg', 'pork_kg', 'fish_kg', 'dairy_kg', 'vegetables_kg', 'fruits_kg'];
      case 3:
        return ['electricity_kwh', 'natural_gas_kwh'];
      case 4:
        return ['waste_kg', 'recycled_kg'];
      case 5:
        return ['clothing_kg', 'electronics_items'];
      default:
        return [];
    }
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

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="card">
            <div className="flex items-center mb-4">
              <Car className="w-5 h-5 text-eco-dark mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Transportation</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Daily Commute Distance (km) *
                </label>
                <input
                  {...register('commute_km')}
                  type="number"
                  className="input-field"
                  min="0"
                  step="0.1"
                  placeholder="e.g., 15"
                />
                {errors.commute_km && (
                  <p className="mt-1 text-sm text-red-600">{errors.commute_km.message}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Transport Mode *
                </label>
                <select
                  {...register('transport_mode')}
                  className="input-field"
                >
                  {transportModes.map(mode => (
                    <option key={mode.value} value={mode.value}>
                      {mode.label}
                    </option>
                  ))}
                </select>
                {errors.transport_mode && (
                  <p className="mt-1 text-sm text-red-600">{errors.transport_mode.message}</p>
                )}
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="card">
            <div className="flex items-center mb-4">
              <Utensils className="w-5 h-5 text-eco-dark mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Food Consumption (per week)</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { name: 'beef_kg', label: 'Beef (kg)' },
                { name: 'chicken_kg', label: 'Chicken (kg)' },
                { name: 'pork_kg', label: 'Pork (kg)' },
                { name: 'fish_kg', label: 'Fish (kg)' },
                { name: 'dairy_kg', label: 'Dairy (kg)' },
                { name: 'vegetables_kg', label: 'Vegetables (kg)' },
                { name: 'fruits_kg', label: 'Fruits (kg)' },
              ].map(field => (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                  </label>
                  <input
                    {...register(field.name)}
                    type="number"
                    className="input-field"
                    min="0"
                    step="0.1"
                    placeholder="0"
                  />
                  {errors[field.name] && (
                    <p className="mt-1 text-sm text-red-600">{errors[field.name].message}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="card">
            <div className="flex items-center mb-4">
              <Zap className="w-5 h-5 text-eco-dark mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Energy Usage (per month)</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Electricity (kWh) *
                </label>
                <input
                  {...register('electricity_kwh')}
                  type="number"
                  className="input-field"
                  min="0"
                  step="0.1"
                  placeholder="e.g., 300"
                />
                {errors.electricity_kwh && (
                  <p className="mt-1 text-sm text-red-600">{errors.electricity_kwh.message}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Natural Gas (kWh)
                </label>
                <input
                  {...register('natural_gas_kwh')}
                  type="number"
                  className="input-field"
                  min="0"
                  step="0.1"
                  placeholder="e.g., 150"
                />
                {errors.natural_gas_kwh && (
                  <p className="mt-1 text-sm text-red-600">{errors.natural_gas_kwh.message}</p>
                )}
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="card">
            <div className="flex items-center mb-4">
              <Trash2 className="w-5 h-5 text-eco-dark mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Waste Management (per week)</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Waste to Landfill (kg) *
                </label>
                <input
                  {...register('waste_kg')}
                  type="number"
                  className="input-field"
                  min="0"
                  step="0.1"
                  placeholder="e.g., 5"
                />
                {errors.waste_kg && (
                  <p className="mt-1 text-sm text-red-600">{errors.waste_kg.message}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Recycled Waste (kg)
                </label>
                <input
                  {...register('recycled_kg')}
                  type="number"
                  className="input-field"
                  min="0"
                  step="0.1"
                  placeholder="e.g., 3"
                />
                {errors.recycled_kg && (
                  <p className="mt-1 text-sm text-red-600">{errors.recycled_kg.message}</p>
                )}
              </div>
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
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
                    {...register('clothing_kg')}
                    type="number"
                    className="input-field"
                    min="0"
                    step="0.1"
                    placeholder="e.g., 2"
                  />
                  {errors.clothing_kg && (
                    <p className="mt-1 text-sm text-red-600">{errors.clothing_kg.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Electronics Items
                  </label>
                  <input
                    {...register('electronics_items')}
                    type="number"
                    className="input-field"
                    min="0"
                    step="1"
                    placeholder="e.g., 1"
                  />
                  {errors.electronics_items && (
                    <p className="mt-1 text-sm text-red-600">{errors.electronics_items.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* ML Features Section */}
            <div className="card bg-blue-50 border-blue-200">
              <div className="flex items-center mb-4">
                <div className="w-5 h-5 text-blue-600 mr-2">🤖</div>
                <h3 className="text-lg font-semibold text-gray-900">AI Enhancement Features (Optional)</h3>
              </div>
              <p className="text-sm text-blue-700 mb-4">
                Provide these details for more accurate AI-powered calculations and personalized insights.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    House Size (m²)
                  </label>
                  <input
                    {...register('house_size')}
                    type="number"
                    className="input-field"
                    min="0"
                    step="1"
                    placeholder="e.g., 120"
                  />
                  {errors.house_size && (
                    <p className="mt-1 text-sm text-red-600">{errors.house_size.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Occupants
                  </label>
                  <input
                    {...register('occupants')}
                    type="number"
                    className="input-field"
                    min="1"
                    step="1"
                    placeholder="e.g., 3"
                  />
                  {errors.occupants && (
                    <p className="mt-1 text-sm text-red-600">{errors.occupants.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Daily AC Hours
                  </label>
                  <input
                    {...register('ac_hours')}
                    type="number"
                    className="input-field"
                    min="0"
                    max="24"
                    step="0.5"
                    placeholder="e.g., 6"
                  />
                  {errors.ac_hours && (
                    <p className="mt-1 text-sm text-red-600">{errors.ac_hours.message}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-8">
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-green-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${(currentStep / totalSteps) * 100}%` }}
        ></div>
      </div>
      
      {/* Step Indicator */}
      <div className="flex justify-center space-x-4">
        {Array.from({ length: totalSteps }, (_, i) => (
          <div
            key={i + 1}
            className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
              i + 1 <= currentStep
                ? 'bg-green-600 text-white'
                : 'bg-gray-200 text-gray-600'
            }`}
          >
            {i + 1}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-8">
        {renderStepContent()}

        {/* Navigation Buttons */}
        <div className="flex justify-between">
          <button
            type="button"
            onClick={prevStep}
            disabled={currentStep === 1}
            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4 mr-1" />
            Previous
          </button>

          {currentStep < totalSteps ? (
            <button
              type="button"
              onClick={nextStep}
              className="flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700"
            >
              Next
              <ChevronRight className="w-4 h-4 ml-1" />
            </button>
          ) : (
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
          )}
        </div>
      </form>
    </div>
  );
};

export default InputForm;
