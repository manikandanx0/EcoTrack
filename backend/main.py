"""
Hybrid Carbon Footprint Tracker - FastAPI Backend
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
import joblib
import numpy as np
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from database import get_db, create_tables
from models import User, Entry, Activity, SuggestionLog
from schemas import (
    InputPayload, 
    CalculationResponse, 
    OffsetResponse, 
    OffsetRequest,
    OffsetRecommendation,
    EntryResponse,
    UserResponse,
    UserCreate,
    UserLogin,
    TokenResponse,
    LeaderboardEntry,
    SuggestionRequest,
    SuggestionsResponse,
    SuggestionResponse
)
from auth import (
    authenticate_user, 
    create_user, 
    create_access_token, 
    get_current_user,
    verify_password,
    get_password_hash
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Hybrid Carbon Footprint Tracker",
    description="API for calculating and tracking personal carbon footprints using hybrid rule-based and ML approaches",
    version="1.0.0"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
@limiter.limit("10/minute")
async def calculate_footprint(
    request: Request,
    payload: InputPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
                breakdown["transport"] = round(transport_emissions, 2)
                details["transport"] = {
                    "commute": round(transport_emissions, 2),
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
                    food_details[food_type] = round(emissions, 2)
        
        if food_emissions > 0:
            breakdown["food"] = round(food_emissions, 2)
            details["food"] = food_details
        
        # Energy calculations
        energy_emissions = 0
        energy_details = {}
        
        if payload.electricity_kwh > 0:
            # Use global average emission factor
            electricity_factor = EMISSION_FACTORS["energy"]["electricity_global_avg"]["value"]
            electricity_emissions = payload.electricity_kwh * electricity_factor
            energy_emissions += electricity_emissions
            energy_details["electricity"] = round(electricity_emissions, 2)
        
        if payload.natural_gas_kwh > 0:
            gas_factor = EMISSION_FACTORS["energy"]["natural_gas"]["value"]
            gas_emissions = payload.natural_gas_kwh * gas_factor
            energy_emissions += gas_emissions
            energy_details["natural_gas"] = round(gas_emissions, 2)
        
        if energy_emissions > 0:
            breakdown["energy"] = round(energy_emissions, 2)
            details["energy"] = energy_details
        
        # Waste calculations
        waste_emissions = 0
        waste_details = {}
        
        if payload.waste_kg > 0:
            waste_factor = EMISSION_FACTORS["waste"]["municipal_waste"]["value"]
            waste_emissions = payload.waste_kg * waste_factor
            waste_details["landfill"] = round(waste_emissions, 2)
        
        if payload.recycled_kg > 0:
            # Recycling saves emissions (negative value)
            recycling_saving = payload.recycled_kg * -0.2  # -0.2 kg CO2 per kg recycled
            waste_emissions += recycling_saving
            waste_details["recycling_saving"] = round(recycling_saving, 2)
        
        if waste_emissions != 0:
            breakdown["waste"] = round(waste_emissions, 2)
            details["waste"] = waste_details
        
        # Consumption calculations
        consumption_emissions = 0
        consumption_details = {}
        
        if payload.clothing_kg > 0:
            clothing_factor = EMISSION_FACTORS["consumption"]["clothing"]["value"]
            clothing_emissions = payload.clothing_kg * clothing_factor
            consumption_emissions += clothing_emissions
            consumption_details["clothing"] = round(clothing_emissions, 2)
        
        if payload.electronics_items > 0:
            # Average smartphone emissions as proxy
            electronics_factor = EMISSION_FACTORS["consumption"]["electronics_smartphone"]["value"]
            electronics_emissions = payload.electronics_items * electronics_factor
            consumption_emissions += electronics_emissions
            consumption_details["electronics"] = round(electronics_emissions, 2)
        
        if consumption_emissions > 0:
            breakdown["consumption"] = round(consumption_emissions, 2)
            details["consumption"] = consumption_details
        
        # Calculate total
        baseline_total = round(sum(breakdown.values()), 2)
        
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
    request: OffsetRequest,
    db: Session = Depends(get_db)
):
    """
    Get carbon offset recommendations (mocked blockchain integration)
    """
    try:
        footprint_kg = request.footprint_kg
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
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's carbon footprint entries
    """
    try:
        entries = db.query(Entry).filter(Entry.user_id == current_user.id).order_by(Entry.date.desc()).limit(limit).all()
        
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

# Authentication endpoints
@app.post("/auth/register", response_model=TokenResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Create new user
        user = create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            username=user_data.username,
            name=user_data.name
        )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                username=user.username,
                created_at=user.created_at,
                total_reduced_co2=float(user.total_reduced_co2),
                streak_days=user.streak_days,
                leaderboard_opt_in=user.leaderboard_opt_in,
                monthly_goal=float(user.monthly_goal) if user.monthly_goal else None
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/auth/login", response_model=TokenResponse)
async def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user"""
    try:
        user = authenticate_user(db, user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                username=user.username,
                created_at=user.created_at,
                total_reduced_co2=float(user.total_reduced_co2),
                streak_days=user.streak_days,
                leaderboard_opt_in=user.leaderboard_opt_in,
                monthly_goal=float(user.monthly_goal) if user.monthly_goal else None
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        username=current_user.username,
        created_at=current_user.created_at,
        total_reduced_co2=float(current_user.total_reduced_co2),
        streak_days=current_user.streak_days,
        leaderboard_opt_in=current_user.leaderboard_opt_in,
        monthly_goal=float(current_user.monthly_goal) if current_user.monthly_goal else None
    )

# Leaderboard endpoint
@app.get("/api/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get community leaderboard"""
    try:
        result = db.execute(
            select(User).filter(User.leaderboard_opt_in == True)
            .order_by(desc(User.total_reduced_co2)).limit(limit)
        )
        users = result.scalars().all()
        
        return [
            LeaderboardEntry(
                rank=i+1,
                username=user.username,
                score=float(user.total_reduced_co2)
            )
            for i, user in enumerate(users)
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch leaderboard: {str(e)}"
        )

# Suggestions endpoint
@app.post("/api/suggest", response_model=SuggestionsResponse)
async def get_suggestions(
    request_data: SuggestionRequest,
    current_user: User = Depends(get_current_user)
):
    """Get personalized carbon reduction suggestions"""
    try:
        # Load suggestion rules (safe fallback if missing)
        rules_path = Path(__file__).parent.parent / "shared" / "suggestion_rules.json"
        if rules_path.exists():
            with open(rules_path, 'r') as f:
                rules = json.load(f)
        else:
            # Minimal defaults if rules file is not present
            rules = {
                "energy": {"threshold": 0.25, "tips": [{"tip": "Improve home insulation and switch to LEDs", "savings": 15.0, "impact_level": "high"}]},
                "transport": {"threshold": 0.3, "tips": [{"tip": "Carpool or use public transport twice a week", "savings": 12.0, "impact_level": "medium"}]},
                "food": {"threshold": 0.2, "tips": [{"tip": "Try one vegetarian day per week", "savings": 8.0, "impact_level": "low"}]}
            }
        
        suggestions = []
        total_potential_savings = 0
        
        breakdown = request_data.breakdown
        total_emissions = sum(breakdown.values())
        
        if total_emissions == 0:
            return SuggestionsResponse(
                suggestions=[],
                total_potential_savings=0
            )
        
        for category, emissions in breakdown.items():
            if category in rules and emissions > 0:
                category_ratio = emissions / total_emissions
                threshold = rules[category]["threshold"]
                
                if category_ratio > threshold:
                    # Get the best tip for this category
                    best_tip = rules[category]["tips"][0]  # First tip is usually the highest impact
                    suggestions.append(SuggestionResponse(
                        category=category,
                        tip=best_tip["tip"],
                        savings=best_tip["savings"],
                        impact_level=best_tip["impact_level"]
                    ))
                    total_potential_savings += best_tip["savings"]
        
        # Limit to top 5 suggestions
        suggestions = suggestions[:5]
        
        return SuggestionsResponse(
            suggestions=suggestions,
            total_potential_savings=round(total_potential_savings, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )

# Update user preferences
@app.patch("/api/user/preferences")
async def update_user_preferences(
    leaderboard_opt_in: Optional[bool] = None,
    monthly_goal: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user preferences"""
    try:
        if leaderboard_opt_in is not None:
            current_user.leaderboard_opt_in = leaderboard_opt_in
        
        if monthly_goal is not None:
            current_user.monthly_goal = monthly_goal
        
        db.commit()
        
        return {"message": "Preferences updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update preferences: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)