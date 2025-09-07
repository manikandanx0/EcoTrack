# 🌍 EcoTrack - Hybrid Carbon Footprint Tracker

A comprehensive web application that helps users calculate their personal carbon footprint using a hybrid approach: rule-based baseline calculations combined with AI refinements, plus blockchain-based carbon offset recommendations.

![EcoTrack Logo](https://img.shields.io/badge/EcoTrack-Hybrid%20Carbon%20Tracker-green?style=for-the-badge&logo=leaf)

## ✨ Features

### 🔬 Hybrid Calculation Engine
- **Rule-based Baseline**: Uses official emission factors from DEFRA, EPA, and IPCC
- **AI Refinement**: Machine learning models to personalize and improve accuracy
- **Transparent Results**: Shows both baseline and refined calculations side-by-side

### 📊 Comprehensive Tracking
- **Transportation**: Cars, buses, trains, bicycles, walking
- **Food Consumption**: Meat, dairy, vegetables, fruits with detailed breakdowns
- **Energy Usage**: Electricity, natural gas with regional grid factors
- **Waste Management**: Landfill vs recycling impact
- **Consumption**: Clothing, electronics, and general goods

### 🌱 Carbon Offset Integration
- **Blockchain-Verified Projects**: Reforestation, renewable energy, energy efficiency
- **Transparent Pricing**: Real-time cost calculations per ton of CO₂
- **Digital Certificates**: Downloadable certificates for purchased offsets
- **Impact Tracking**: Detailed project information and environmental benefits

### 📈 Advanced Analytics
- **Interactive Dashboards**: Pie charts, bar charts, and trend analysis
- **Detailed Breakdowns**: Category-wise emissions with insights
- **Recommendations**: Personalized suggestions for reducing footprint
- **Export Options**: PDF reports and data export capabilities

## 🏗️ Architecture

```
EcoTrack/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Main application
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── shared/                 # Shared Resources
│   └── conversion_factors.json  # Emission factors
├── ml/                     # Machine Learning
│   ├── train_model.py      # ML training script
│   └── requirements.txt    # ML dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## 📖 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calc` | POST | Calculate baseline carbon footprint |
| `/api/refine` | POST | Refine calculation with AI |
| `/api/offset` | POST | Get carbon offset recommendations |
| `/api/entries` | GET | Get user's footprint history |

### Example API Usage

```python
import requests

# Calculate baseline footprint
payload = {
    "commute_km": 20,
    "transport_mode": "car_petrol",
    "beef_kg": 0.5,
    "electricity_kwh": 300,
    "waste_kg": 5,
    "recycled_kg": 3
}

response = requests.post("http://localhost:8000/api/calc", json=payload)
result = response.json()

print(f"Total footprint: {result['baseline_total']:.1f} kg CO₂")
```

## 🎯 Demo Flow

1. **Open the application** at `http://localhost:5173`
2. **Fill out the form** with your daily/weekly activities:
   - Transportation (commute distance and mode)
   - Food consumption (meat, dairy, vegetables)
   - Energy usage (electricity, gas)
   - Waste management (landfill vs recycling)
   - Consumption patterns (clothing, electronics)

3. **View your results**:
   - Baseline calculation using official emission factors
   - AI-refined calculation with personalized adjustments
   - Detailed breakdown by category
   - Interactive charts and visualizations

4. **Explore offset options**:
   - Browse verified carbon offset projects
   - Compare costs and environmental impact
   - Purchase offsets with blockchain verification
   - Download certificates for your contributions

## 🔬 Emission Factors

The application uses comprehensive emission factors from authoritative sources:

### Transportation
- **Cars**: 0.19 kg CO₂/km (petrol), 0.18 kg CO₂/km (diesel)
- **Public Transport**: 0.1 kg CO₂/km (bus), 0.02 kg CO₂/km (electric train)
- **Active Transport**: 0 kg CO₂/km (bicycle, walking)

### Food
- **Beef**: 60 kg CO₂/kg (highest impact)
- **Chicken**: 5.7 kg CO₂/kg
- **Vegetables**: 0.4 kg CO₂/kg
- **Dairy**: 3 kg CO₂/kg

### Energy
- **Electricity**: 0.45 kg CO₂/kWh (global average)
- **Natural Gas**: 0.4 kg CO₂/kWh

### Sources
- DEFRA (UK Government)
- EPA (US Environmental Protection Agency)
- IPCC AR6 (Intergovernmental Panel on Climate Change)
- Our World in Data
- IEA (International Energy Agency)

## 🧠 Machine Learning Integration

The hybrid approach combines rule-based calculations with ML refinements:

1. **Baseline Calculation**: Uses official emission factors
2. **ML Refinement**: Adjusts calculations based on:
   - Regional factors
   - Seasonal variations
   - User behavior patterns
   - Historical data

3. **Transparency**: Shows both calculations for comparison

## 🌐 Blockchain Integration

Carbon offset recommendations include:

- **Verified Projects**: Third-party verified carbon reduction projects
- **Blockchain Tracking**: Transparent transaction records
- **Digital Certificates**: Downloadable proof of environmental impact
- **Real-time Pricing**: Dynamic cost calculations

## 🛠️ Development

### Adding New Emission Factors

1. Edit `shared/conversion_factors.json`
2. Add new categories or update existing values
3. Update the backend calculation logic in `main.py`
4. Test with the API endpoints

### Extending ML Models

1. Add training data to `ml/` directory
2. Update `ml/train_model.py` with new features
3. Integrate model predictions in the refinement endpoint
4. Update frontend to display ML insights

### Customizing the UI

1. Modify components in `frontend/src/components/`
2. Update styling in `frontend/src/index.css`
3. Add new pages in `frontend/src/pages/`
4. Update routing in `frontend/src/App.jsx`

## 📊 Sample Data

### Typical User Input
```json
{
  "commute_km": 15,
  "transport_mode": "car_petrol",
  "beef_kg": 0.3,
  "chicken_kg": 0.5,
  "vegetables_kg": 2.0,
  "electricity_kwh": 250,
  "waste_kg": 4,
  "recycled_kg": 2
}
```

### Expected Output
- **Baseline**: ~45 kg CO₂/week
- **Refined**: ~42 kg CO₂/week (5% improvement)
- **Top Category**: Transportation (60% of footprint)
- **Recommendation**: Consider public transport or carpooling

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# API Keys (optional for enhanced features)
ELECTRICITYMAP_KEY=your_electricitymap_key
TOUCAN_API_KEY=your_toucan_api_key

# Database
DATABASE_URL=sqlite:///./app.db

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Customization Options
- **Emission Factors**: Modify `shared/conversion_factors.json`
- **UI Theme**: Update colors in `frontend/tailwind.config.js`
- **API Endpoints**: Extend `backend/main.py`
- **Database Schema**: Modify `backend/models.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Emission Factors**: DEFRA, EPA, IPCC, Our World in Data
- **UI Components**: React, Tailwind CSS, Recharts
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Blockchain**: Toucan Protocol (mock integration)

## 📞 Support

For questions or support:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the emission factors in `shared/conversion_factors.json`

---

**EcoTrack** - Making sustainability measurable and actionable through hybrid carbon footprint tracking and blockchain-verified offsets.
