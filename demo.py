#!/usr/bin/env python3
"""
Demo script for EcoTrack - Hybrid Carbon Footprint Tracker
This script demonstrates the API functionality with sample data
No external API keys required - uses mock data for demonstration
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print("❌ API health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running on port 8000")
        return False

def calculate_sample_footprint():
    """Calculate carbon footprint for a sample user"""
    print("\n🌍 Calculating sample carbon footprint...")
    
    # Sample user data
    sample_data = {
        "commute_km": 20,  # 20 km daily commute
        "transport_mode": "car_petrol",
        "beef_kg": 0.5,  # 0.5 kg beef per week
        "chicken_kg": 1.0,  # 1 kg chicken per week
        "pork_kg": 0.3,  # 0.3 kg pork per week
        "fish_kg": 0.4,  # 0.4 kg fish per week
        "dairy_kg": 2.0,  # 2 kg dairy per week
        "vegetables_kg": 3.0,  # 3 kg vegetables per week
        "fruits_kg": 2.0,  # 2 kg fruits per week
        "electricity_kwh": 300,  # 300 kWh per month
        "natural_gas_kwh": 150,  # 150 kWh natural gas per month
        "waste_kg": 5,  # 5 kg waste per week
        "recycled_kg": 3,  # 3 kg recycled per week
        "clothing_kg": 0.5,  # 0.5 kg clothing per month
        "electronics_items": 0,  # No electronics this month
        "house_size": 120,  # 120 m² house (for ML prediction)
        "occupants": 3,  # 3 occupants (for ML prediction)
        "ac_hours": 6  # 6 hours AC per day (for ML prediction)
    }
    
    try:
        # Calculate baseline footprint
        print("📊 Calculating baseline footprint...")
        response = requests.post(f"{BASE_URL}/api/calc", json=sample_data)
        
        if response.status_code == 200:
            baseline_result = response.json()
            print(f"✅ Baseline calculation successful")
            print(f"   Total footprint: {baseline_result['baseline_total']:.1f} kg CO₂")
            
            # Show breakdown
            print("\n📈 Breakdown by category:")
            for category, emissions in baseline_result['breakdown'].items():
                print(f"   {category.capitalize()}: {emissions:.1f} kg CO₂")
            
            # Refine with AI
            print("\n🤖 Refining with AI...")
            refine_response = requests.post(f"{BASE_URL}/api/refine", json=sample_data)
            
            if refine_response.status_code == 200:
                refined_result = refine_response.json()
                print(f"✅ AI refinement successful")
                print(f"   Refined footprint: {refined_result['refined_total']:.1f} kg CO₂")
                
                improvement = ((baseline_result['baseline_total'] - refined_result['refined_total']) / 
                             baseline_result['baseline_total'] * 100)
                print(f"   Improvement: {improvement:.1f}% reduction")
                
                # Show ML insights if available
                if 'ml_insights' in refined_result.get('details', {}):
                    print("\n🤖 AI Insights:")
                    for insight in refined_result['details']['ml_insights']:
                        print(f"   • {insight}")
                
                return refined_result['baseline_total']
            else:
                print(f"❌ AI refinement failed: {refine_response.status_code}")
                return baseline_result['baseline_total']
        else:
            print(f"❌ Baseline calculation failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error during calculation: {e}")
        return None

def get_offset_recommendations(footprint):
    """Get carbon offset recommendations"""
    if footprint is None:
        return
    
    print(f"\n🌱 Getting offset recommendations for {footprint:.1f} kg CO₂...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/offset", 
                               json={"footprint_kg": footprint})
        
        if response.status_code == 200:
            offset_result = response.json()
            print(f"✅ Found {len(offset_result['recommendations'])} offset options")
            
            for i, project in enumerate(offset_result['recommendations'], 1):
                print(f"\n{i}. {project['project_name']}")
                print(f"   Type: {project['project_type']}")
                print(f"   Cost: ${project['total_cost']:.2f} (${project['cost_per_ton']}/ton)")
                print(f"   Impact: {project['impact_description']}")
                print(f"   Transaction ID: {project['transaction_id']}")
        else:
            print(f"❌ Offset recommendations failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting offset recommendations: {e}")

def main():
    """Main demo function"""
    print("🌍 EcoTrack - Hybrid Carbon Footprint Tracker Demo")
    print("=" * 60)
    
    # Test API health
    if not test_api_health():
        print("\n💡 To start the backend:")
        print("   cd backend")
        print("   pip install -r requirements.txt")
        print("   uvicorn main:app --reload --port 8000")
        return
    
    # Calculate sample footprint
    footprint = calculate_sample_footprint()
    
    # Get offset recommendations
    get_offset_recommendations(footprint)
    
    print("\n🎉 Demo completed!")
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:5173 in your browser")
    print("   2. Fill out the form with your own data")
    print("   3. Explore the interactive dashboard")
    print("   4. Try the carbon offset recommendations")

if __name__ == "__main__":
    main()
