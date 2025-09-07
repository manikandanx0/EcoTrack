"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime

class InputPayload(BaseModel):
    """User input data for carbon footprint calculation"""
    
    # Transport
    commute_km: float = Field(0, ge=0, description="Daily commute distance in km")
    transport_mode: str = Field("car_petrol", description="Transport mode")
    
    # Food consumption (kg per week)
    beef_kg: float = Field(0, ge=0, description="Beef consumption in kg per week")
    chicken_kg: float = Field(0, ge=0, description="Chicken consumption in kg per week")
    pork_kg: float = Field(0, ge=0, description="Pork consumption in kg per week")
    fish_kg: float = Field(0, ge=0, description="Fish consumption in kg per week")
    dairy_kg: float = Field(0, ge=0, description="Dairy consumption in kg per week")
    vegetables_kg: float = Field(0, ge=0, description="Vegetables consumption in kg per week")
    fruits_kg: float = Field(0, ge=0, description="Fruits consumption in kg per week")
    
    # Energy
    electricity_kwh: float = Field(0, ge=0, description="Monthly electricity usage in kWh")
    natural_gas_kwh: float = Field(0, ge=0, description="Monthly natural gas usage in kWh")
    
    # Waste
    waste_kg: float = Field(0, ge=0, description="Weekly waste in kg")
    recycled_kg: float = Field(0, ge=0, description="Weekly recycled waste in kg")
    
    # Consumption
    clothing_kg: float = Field(0, ge=0, description="Monthly clothing purchases in kg")
    electronics_items: int = Field(0, ge=0, description="Monthly electronics purchases")
    
    # Optional ML features
    house_size: Optional[float] = Field(None, ge=0, description="House size in square meters")
    occupants: Optional[int] = Field(None, ge=1, description="Number of occupants")
    ac_hours: Optional[float] = Field(None, ge=0, le=24, description="Daily AC usage hours")
    
    @validator("commute_km", "electricity_kwh", "beef_kg", "waste_kg")
    def check_non_negative(cls, v):
        if v < 0:
            raise ValueError("Value cannot be negative")
        return v
    
    @validator("transport_mode")
    def check_transport_mode(cls, v):
        valid_modes = [
            "car_petrol", "car_diesel", "car_hybrid", "car_ev",
            "bus_diesel", "bus_electric", "train_diesel", "train_electric",
            "motorcycle", "bicycle", "walking", "airplane_shorthaul", "airplane_longhaul"
        ]
        if v not in valid_modes:
            raise ValueError(f"Invalid transport mode. Must be one of: {', '.join(valid_modes)}")
        return v

class CalculationResponse(BaseModel):
    """Response for carbon footprint calculation"""
    
    breakdown: Dict[str, float] = Field(description="CO2 emissions breakdown by category")
    baseline_total: float = Field(description="Total baseline CO2 emissions in kg")
    refined_total: Optional[float] = Field(None, description="Total refined CO2 emissions in kg")
    # Allow details to include strings or numbers (e.g., transport mode)
    details: Dict[str, Dict[str, Any]] = Field(description="Detailed breakdown by activity")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OffsetRecommendation(BaseModel):
    """Carbon offset recommendation"""
    
    project_name: str = Field(description="Name of the offset project")
    project_type: str = Field(description="Type of project (reforestation, renewable energy, etc.)")
    cost_per_ton: float = Field(description="Cost per ton of CO2 in USD")
    total_cost: float = Field(description="Total cost for offsetting in USD")
    impact_description: str = Field(description="Description of environmental impact")
    transaction_id: Optional[str] = Field(None, description="Blockchain transaction ID")
    certificate_url: Optional[str] = Field(None, description="URL to download certificate")

class OffsetResponse(BaseModel):
    """Response for offset recommendations"""
    
    recommendations: List[OffsetRecommendation] = Field(description="List of offset recommendations")
    total_footprint: float = Field(description="Total footprint to offset in kg CO2")
    message: str = Field(description="Response message")

class EntryResponse(BaseModel):
    """Response for user entries"""
    
    id: int
    date: datetime
    baseline_total: float
    refined_total: Optional[float]
    activities: List[Dict[str, Any]]

class UserResponse(BaseModel):
    """Response for user data"""
    
    id: str
    name: str
    email: Optional[str]
    username: str
    created_at: datetime
    total_reduced_co2: float
    streak_days: int
    leaderboard_opt_in: bool
    monthly_goal: Optional[float]
    entries: List[EntryResponse] = []

# Authentication schemas
class UserCreate(BaseModel):
    """Schema for user registration"""
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    name: str = Field(..., min_length=2, max_length=100, description="Full name")

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

class TokenResponse(BaseModel):
    """Response for authentication token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Leaderboard schemas
class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry"""
    rank: int
    username: str
    score: float  # total_reduced_co2 or streak_days

# Suggestion schemas
class SuggestionRequest(BaseModel):
    """Schema for suggestion request"""
    breakdown: Dict[str, float]

class SuggestionResponse(BaseModel):
    """Schema for suggestion response"""
    category: str
    tip: str
    savings: float
    impact_level: str  # low, medium, high

class SuggestionsResponse(BaseModel):
    """Schema for suggestions response"""
    suggestions: List[SuggestionResponse]
    total_potential_savings: float

class OffsetRequest(BaseModel):
    """Request body for offset recommendations"""
    footprint_kg: float = Field(..., ge=0, description="Footprint to offset in kg CO2")
