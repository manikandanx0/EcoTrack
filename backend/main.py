"""
Hybrid Carbon Footprint Tracker - FastAPI Backend
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    create_tables()
    print("🌍 Hybrid Carbon Footprint Tracker API started!")
    print("📊 Emission factors loaded successfully")

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
    Refine carbon footprint calculation (placeholder for ML integration)
    For now, returns the baseline calculation with a small adjustment
    """
    try:
        # Get baseline calculation
        baseline_response = await calculate_footprint(payload, db)
        
        # Simple refinement logic (placeholder for ML)
        # In a real implementation, this would use trained ML models
        refined_breakdown = {}
        refinement_factor = 0.95  # 5% reduction as example
        
        for category, emissions in baseline_response.breakdown.items():
            refined_breakdown[category] = emissions * refinement_factor
        
        refined_total = sum(refined_breakdown.values())
        
        return CalculationResponse(
            breakdown=refined_breakdown,
            baseline_total=baseline_response.baseline_total,
            refined_total=refined_total,
            details=baseline_response.details
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