"""
Database models for Hybrid Carbon Footprint Tracker
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    entries = relationship("Entry", back_populates="user")

class Entry(Base):
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    baseline_total = Column(Float, nullable=False)
    refined_total = Column(Float, nullable=True)
    
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
