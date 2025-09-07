"""
Hybrid Carbon Footprint Tracker - FastAPI Backend
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import joblib
import numpy as np

from database import get_db, create_tables
from models import User, Entry, Activity
from schemas import (
    InputPayload, 
    CalculationResponse, 
    OffsetResponse, 
    OffsetRecommendation,
    EntryResponse,
    UserResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Hybrid Carbon Footprint Tracker",
    description="API for calculating and tracking personal carbon footprints using hybrid rule-based and ML approaches",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load emission factors
def load_emission_factors() -> Dict:
    """Load emission factors from shared directory"""
    factors_path = Path(__file__).parent.parent / "shared" / "conversion_factors.json"
    
    if not factors_path.exists():
        raise FileNotFoundError(f"Emission factors not found at {factors_path}")
    
    with open(factors_path, 'r') as f:
        return json.load(f)

# Global emission factors
EMISSION_FACTORS = load_emission_factors()

# Load ML model
def load_ml_model():
    """Load the trained energy prediction model"""
    model_path = Path(__file__).parent.parent / "ml" / "elec_predictor.pkl"
    
    if not model_path.exists():
        print("⚠️  ML model not found. Using baseline calculations only.")
        return None
    
    try:
        model = joblib.load(model_path)
        print("✅ ML model loaded successfully")
        return model
    except Exception as e:
        print(f"⚠️  Failed to load ML model: {e}")
        return None

# Global ML model
ML_MODEL = load_ml_model()

def predict_energy_consumption(house_size: float, occupants: int, ac_hours: float) -> Optional[float]:
    """
    Predict energy consumption using ML model
    
    Args:
        house_size: House size in square meters
        occupants: Number of occupants
        ac_hours: AC usage hours per day
    
    Returns:
        Predicted monthly energy consumption in kWh, or None if model not available
    """
    if ML_MODEL is None:
        return None
    
    try:
        # Prepare input data
        X = np.array([[house_size, occupants, ac_hours]])
        prediction = ML_MODEL.predict(X)[0]
        return max(prediction, 100)  # Minimum 100 kWh
    except Exception as e:
        print(f"⚠️  ML prediction failed: {e}")
        return None

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    create_tables()
    print("🌍 Hybrid Carbon Footprint Tracker API started!")
    print("📊 Emission factors loaded successfully")
    if ML_MODEL is not None:
        print("🤖 ML model loaded successfully")
    else:
        print("⚠️  ML model not available - using baseline calculations only")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hybrid Carbon Footprint Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/calc", response_model=CalculationResponse)
async def calculate_footprint(
    payload: InputPayload,
    db: Session = Depends(get_db)
):
    """
    Calculate baseline carbon footprint using rule-based emission factors
    """
    try:
        breakdown = {}
        details = {}
        
        # Transport calculation
        if payload.commute_km > 0:
            transport_factor = EMISSION_FACTORS["transport"].get(payload.transport_mode, {})
            if transport_factor:
                transport_emissions = payload.commute_km * transport_factor["value"]
                breakdown["transport"] = transport_emissions
                details["transport"] = {
                    "commute": transport_emissions,
                    "mode": payload.transport_mode,
                    "distance_km": payload.commute_km
                }
        
        # Food calculations
        food_emissions = 0
        food_details = {}
        
        food_items = {
            "beef": payload.beef_kg,
            "chicken": payload.chicken_kg,
            "pork": payload.pork_kg,
            "fish": payload.fish_kg,
            "milk": payload.dairy_kg,
            "vegetables": payload.vegetables_kg,
            "fruits": payload.fruits_kg
        }
        
        for food_type, amount in food_items.items():
            if amount > 0:
                factor = EMISSION_FACTORS["food"].get(food_type, {})
                if factor:
                    emissions = amount * factor["value"]
                    food_emissions += emissions
                    food_details[food_type] = emissions
        
        if food_emissions > 0:
            breakdown["food"] = food_emissions
            details["food"] = food_details
        
        # Energy calculations
        energy_emissions = 0
        energy_details = {}
        
        if payload.electricity_kwh > 0:
            # Use global average emission factor
            electricity_factor = EMISSION_FACTORS["energy"]["electricity_global_avg"]["value"]
            electricity_emissions = payload.electricity_kwh * electricity_factor
            energy_emissions += electricity_emissions
            energy_details["electricity"] = electricity_emissions
        
        if payload.natural_gas_kwh > 0:
            gas_factor = EMISSION_FACTORS["energy"]["natural_gas"]["value"]
            gas_emissions = payload.natural_gas_kwh * gas_factor
            energy_emissions += gas_emissions
            energy_details["natural_gas"] = gas_emissions
        
        if energy_emissions > 0:
            breakdown["energy"] = energy_emissions
            details["energy"] = energy_details
        
        # Waste calculations
        waste_emissions = 0
        waste_details = {}
        
        if payload.waste_kg > 0:
            waste_factor = EMISSION_FACTORS["waste"]["municipal_waste"]["value"]
            waste_emissions = payload.waste_kg * waste_factor
            waste_details["landfill"] = waste_emissions
        
        if payload.recycled_kg > 0:
            # Recycling saves emissions (negative value)
            recycling_saving = payload.recycled_kg * -0.2  # -0.2 kg CO2 per kg recycled
            waste_emissions += recycling_saving
            waste_details["recycling_saving"] = recycling_saving
        
        if waste_emissions != 0:
            breakdown["waste"] = waste_emissions
            details["waste"] = waste_details
        
        # Consumption calculations
        consumption_emissions = 0
        consumption_details = {}
        
        if payload.clothing_kg > 0:
            clothing_factor = EMISSION_FACTORS["consumption"]["clothing"]["value"]
            clothing_emissions = payload.clothing_kg * clothing_factor
            consumption_emissions += clothing_emissions
            consumption_details["clothing"] = clothing_emissions
        
        if payload.electronics_items > 0:
            # Average smartphone emissions as proxy
            electronics_factor = EMISSION_FACTORS["consumption"]["electronics_smartphone"]["value"]
            electronics_emissions = payload.electronics_items * electronics_factor
            consumption_emissions += electronics_emissions
            consumption_details["electronics"] = electronics_emissions
        
        if consumption_emissions > 0:
            breakdown["consumption"] = consumption_emissions
            details["consumption"] = consumption_details
        
        # Calculate total
        baseline_total = sum(breakdown.values())
        
        return CalculationResponse(
            breakdown=breakdown,
            baseline_total=baseline_total,
            details=details
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )

@app.post("/api/refine", response_model=CalculationResponse)
async def refine_footprint(
    payload: InputPayload,
    db: Session = Depends(get_db)
):
    """
    Refine carbon footprint calculation using ML model
    """
    try:
        # Get baseline calculation
        baseline_response = await calculate_footprint(payload, db)
        
        # Start with baseline breakdown
        refined_breakdown = baseline_response.breakdown.copy()
        refined_details = baseline_response.details.copy()
        
        # ML refinements
        ml_insights = []
        
        # 1. Energy prediction refinement
        if (payload.house_size is not None and 
            payload.occupants is not None and 
            payload.ac_hours is not None):
            
            # Predict energy consumption using ML
            predicted_kwh = predict_energy_consumption(
                payload.house_size, 
                payload.occupants, 
                payload.ac_hours
            )
            
            if predicted_kwh is not None:
                # Calculate difference between user input and ML prediction
                user_kwh = payload.electricity_kwh
                kwh_difference = predicted_kwh - user_kwh
                
                # If ML prediction is significantly different, adjust
                if abs(kwh_difference) > 50:  # 50 kWh threshold
                    # Calculate new energy emissions
                    electricity_factor = EMISSION_FACTORS["energy"]["electricity_global_avg"]["value"]
                    new_energy_emissions = predicted_kwh * electricity_factor
                    
                    # Update energy breakdown
                    if "energy" in refined_breakdown:
                        old_energy = refined_breakdown["energy"]
                        refined_breakdown["energy"] = new_energy_emissions
                        
                        # Update details
                        if "energy" in refined_details:
                            refined_details["energy"]["electricity"] = new_energy_emissions
                        
                        # Add insight
                        if kwh_difference > 0:
                            ml_insights.append(f"ML predicts {kwh_difference:.0f} kWh higher energy usage based on your house size ({payload.house_size}m²) and {payload.occupants} occupants")
                        else:
                            ml_insights.append(f"ML predicts {abs(kwh_difference):.0f} kWh lower energy usage based on your house size ({payload.house_size}m²) and {payload.occupants} occupants")
        
        # 2. Transportation refinement based on distance patterns
        if payload.commute_km > 0:
            # If commute is very high, suggest it might be overestimated
            if payload.commute_km > 100:  # 100 km daily seems high
                transport_factor = 0.9  # 10% reduction
                if "transport" in refined_breakdown:
                    refined_breakdown["transport"] *= transport_factor
                    ml_insights.append("ML adjusted transport emissions - daily commute over 100km seems unusually high")
        
        # 3. Food consumption refinement
        total_food_kg = (payload.beef_kg + payload.chicken_kg + payload.pork_kg + 
                        payload.fish_kg + payload.dairy_kg + payload.vegetables_kg + payload.fruits_kg)
        
        if total_food_kg > 20:  # More than 20kg per week seems high
            food_factor = 0.95  # 5% reduction
            if "food" in refined_breakdown:
                refined_breakdown["food"] *= food_factor
                ml_insights.append("ML adjusted food emissions - consumption over 20kg/week seems high for typical household")
        
        # 4. Seasonal and regional adjustments (mock)
        seasonal_factor = 1.02  # 2% increase for winter energy usage
        if "energy" in refined_breakdown:
            refined_breakdown["energy"] *= seasonal_factor
            ml_insights.append("ML applied seasonal adjustment (+2%) for winter energy usage")
        
        # Calculate refined total
        refined_total = sum(refined_breakdown.values())
        
        # Add ML insights to details
        if ml_insights:
            refined_details["ml_insights"] = ml_insights
        
        return CalculationResponse(
            breakdown=refined_breakdown,
            baseline_total=baseline_response.baseline_total,
            refined_total=refined_total,
            details=refined_details
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Refinement failed: {str(e)}"
        )

@app.post("/api/offset", response_model=OffsetResponse)
async def get_offset_recommendations(
    footprint_kg: float,
    db: Session = Depends(get_db)
):
    """
    Get carbon offset recommendations (mocked blockchain integration)
    """
    try:
        if footprint_kg <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Footprint must be greater than 0"
            )
        
        # Mock offset recommendations
        recommendations = [
            OffsetRecommendation(
                project_name="Amazon Rainforest Reforestation",
                project_type="Reforestation",
                cost_per_ton=15.0,
                total_cost=(footprint_kg / 1000) * 15.0,  # Convert kg to tons
                impact_description=f"Plant trees to offset {footprint_kg:.1f} kg of CO2 emissions",
                transaction_id="0x1234567890abcdef",
                certificate_url="https://example.com/certificate/123"
            ),
            OffsetRecommendation(
                project_name="Solar Energy Project - India",
                project_type="Renewable Energy",
                cost_per_ton=25.0,
                total_cost=(footprint_kg / 1000) * 25.0,
                impact_description=f"Support solar energy development to offset {footprint_kg:.1f} kg of CO2",
                transaction_id="0xabcdef1234567890",
                certificate_url="https://example.com/certificate/456"
            ),
            OffsetRecommendation(
                project_name="Wind Farm - Texas",
                project_type="Renewable Energy",
                cost_per_ton=20.0,
                total_cost=(footprint_kg / 1000) * 20.0,
                impact_description=f"Invest in wind energy to offset {footprint_kg:.1f} kg of CO2",
                transaction_id="0x9876543210fedcba",
                certificate_url="https://example.com/certificate/789"
            )
        ]
        
        return OffsetResponse(
            recommendations=recommendations,
            total_footprint=footprint_kg,
            message=f"Found {len(recommendations)} offset options for {footprint_kg:.1f} kg CO2"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Offset recommendations failed: {str(e)}"
        )

@app.get("/api/entries", response_model=List[EntryResponse])
async def get_user_entries(
    user_id: int = 1,  # Default user for MVP
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get user's carbon footprint entries
    """
    try:
        entries = db.query(Entry).filter(Entry.user_id == user_id).order_by(Entry.date.desc()).limit(limit).all()
        
        result = []
        for entry in entries:
            activities = []
            for activity in entry.activities:
                activities.append({
                    "category": activity.category,
                    "activity_type": activity.activity_type,
                    "value": activity.value,
                    "unit": activity.unit,
                    "kgco2_baseline": activity.kgco2_baseline,
                    "kgco2_refined": activity.kgco2_refined
                })
            
            result.append(EntryResponse(
                id=entry.id,
                date=entry.date,
                baseline_total=entry.baseline_total,
                refined_total=entry.refined_total,
                activities=activities
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch entries: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)