"""
Database models for Hybrid Carbon Footprint Tracker
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # New fields for enhanced features
    total_reduced_co2 = Column(Numeric(10, 2), default=0)
    streak_days = Column(Integer, default=0)
    leaderboard_opt_in = Column(Boolean, default=False)
    monthly_goal = Column(Numeric(10, 2), nullable=True)
    last_entry_date = Column(DateTime, nullable=True)
    
    # Relationships
    entries = relationship("Entry", back_populates="user")
    suggestions_log = relationship("SuggestionLog", back_populates="user")

class Entry(Base):
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    baseline_total = Column(Float, nullable=False)
    refined_total = Column(Float, nullable=True)
    reduction_achieved = Column(Float, default=0)  # CO2 reduction compared to previous entry
    
    # Relationships
    user = relationship("User", back_populates="entries")
    activities = relationship("Activity", back_populates="entry")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id"))
    category = Column(String(50), nullable=False)  # transport, food, energy, waste, consumption
    activity_type = Column(String(100), nullable=False)  # car_petrol, beef, etc.
    value = Column(Float, nullable=False)  # amount/quantity
    unit = Column(String(20), nullable=False)  # km, kg, kWh, etc.
    kgco2_baseline = Column(Float, nullable=False)
    kgco2_refined = Column(Float, nullable=True)
    
    # Relationships
    entry = relationship("Entry", back_populates="activities")

class SuggestionLog(Base):
    __tablename__ = "suggestions_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    tip_id = Column(String(100), nullable=False)  # Unique identifier for the tip
    category = Column(String(50), nullable=False)  # transport, food, energy, etc.
    tip_text = Column(Text, nullable=False)
    applied_date = Column(DateTime, default=datetime.utcnow)
    savings_achieved = Column(Float, default=0)  # CO2 savings from applying this tip
    
    # Relationships
    user = relationship("User", back_populates="suggestions_log")
