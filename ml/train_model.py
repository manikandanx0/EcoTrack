#!/usr/bin/env python3
"""
ML Training Script for Energy Prediction Model
Hybrid Carbon Footprint Tracker

This script trains a RandomForestRegressor to predict household energy consumption
based on house size, number of occupants, and AC usage hours.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from pathlib import Path

def generate_synthetic_data(n_samples=1000, random_state=42):
    """
    Generate synthetic dataset for energy prediction training.
    
    Features:
    - house_size: House size in square meters (50-300)
    - occupants: Number of occupants (1-5)
    - ac_hours: AC usage hours per day (0-24)
    
    Target:
    - monthly_kwh: Monthly energy consumption in kWh
    Formula: 200 + (house_size * 2) + (occupants * 50) + noise
    """
    np.random.seed(random_state)
    
    # Generate features
    house_size = np.random.uniform(50, 300, n_samples)
    occupants = np.random.randint(1, 6, n_samples)
    ac_hours = np.random.uniform(0, 24, n_samples)
    
    # Generate target with realistic formula + noise
    base_consumption = 200 + (house_size * 2) + (occupants * 50) + (ac_hours * 2)
    noise = np.random.normal(0, 50, n_samples)  # 50 kWh standard deviation
    monthly_kwh = np.maximum(base_consumption + noise, 100)  # Minimum 100 kWh
    
    # Create DataFrame
    data = pd.DataFrame({
        'house_size': house_size,
        'occupants': occupants,
        'ac_hours': ac_hours,
        'monthly_kwh': monthly_kwh
    })
    
    return data

def train_energy_model():
    """Train and save the energy prediction model."""
    
    print("🌱 Generating synthetic training data...")
    data = generate_synthetic_data(n_samples=1000)
    
    print(f"📊 Dataset shape: {data.shape}")
    print(f"📈 Energy consumption range: {data['monthly_kwh'].min():.1f} - {data['monthly_kwh'].max():.1f} kWh")
    
    # Prepare features and target
    X = data[['house_size', 'occupants', 'ac_hours']]
    y = data['monthly_kwh']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"🔧 Training set: {X_train.shape[0]} samples")
    print(f"🧪 Test set: {X_test.shape[0]} samples")
    
    # Train RandomForest model
    print("🤖 Training RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"📊 Model Performance:")
    print(f"   Mean Absolute Error: {mae:.2f} kWh")
    print(f"   R² Score: {r2:.3f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"🎯 Feature Importance:")
    for _, row in feature_importance.iterrows():
        print(f"   {row['feature']}: {row['importance']:.3f}")
    
    # Save model
    model_path = Path(__file__).parent / "elec_predictor.pkl"
    joblib.dump(model, model_path)
    print(f"💾 Model saved to: {model_path}")
    
    # Save training data for reference
    data_path = Path(__file__).parent / "training_data.csv"
    data.to_csv(data_path, index=False)
    print(f"📁 Training data saved to: {data_path}")
    
    return model, mae, r2

def predict_energy(house_size, occupants, ac_hours, model_path=None):
    """
    Predict energy consumption for given inputs.
    
    Args:
        house_size: House size in square meters
        occupants: Number of occupants
        ac_hours: AC usage hours per day
        model_path: Path to saved model (optional)
    
    Returns:
        Predicted monthly energy consumption in kWh
    """
    if model_path is None:
        model_path = Path(__file__).parent / "elec_predictor.pkl"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please run train_energy_model() first.")
    
    model = joblib.load(model_path)
    
    # Prepare input data
    X = np.array([[house_size, occupants, ac_hours]])
    prediction = model.predict(X)[0]
    
    return prediction

if __name__ == "__main__":
    print("🌍 Hybrid Carbon Footprint Tracker - ML Model Training")
    print("=" * 60)
    
    try:
        model, mae, r2 = train_energy_model()
        
        print("\n✅ Training completed successfully!")
        print(f"🎯 Model accuracy: {r2:.1%} (R² score)")
        print(f"📏 Average error: ±{mae:.1f} kWh")
        
        # Test prediction
        print("\n🧪 Testing prediction...")
        test_prediction = predict_energy(house_size=150, occupants=3, ac_hours=8)
        print(f"   House: 150m², 3 occupants, 8h AC → {test_prediction:.1f} kWh/month")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        raise
