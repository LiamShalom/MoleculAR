# MolViz AI - Molecular Analysis Platform

A comprehensive AI-powered molecular analysis platform that combines quantum chemistry simulations, machine learning predictions, and natural language processing to provide insights for drug discovery and molecular research.

## 🚀 Features

### Frontend (React)
- **Interactive 3D Molecular Visualization** using 3Dmol.js
- **AI-Powered Analysis Interface** with multiple input methods
- **Real-time Results Dashboard** with comprehensive metrics
- **Voice Narration** powered by ElevenLabs
- **Feature Flags & Telemetry** via Statsig
- **Responsive Design** with modern UI/UX

### Backend (Python FastAPI)
- **Quantum Chemistry Simulations** using Qiskit Nature/PennyLane
- **Physicochemical Property Analysis** via RDKit
- **Machine Learning Predictions** for drug-likeness and ADME/Tox
- **Molecular Docking** integration (AutoDock Vina/DiffDock)
- **Database Storage** with Supabase/PostgreSQL support
- **RESTful API** with comprehensive documentation

### AI Integration
- **Gemini API** for natural language molecular summaries
- **ElevenLabs** for voice narration of results
- **Statsig** for feature flags and user analytics
- **ML Models** trained on BindingDB/ChEMBL datasets

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Python Backend │    │   AI Services   │
│                 │    │                 │    │                 │
│ • 3Dmol.js      │◄──►│ • FastAPI       │◄──►│ • Gemini API    │
│ • Analysis UI   │    │ • RDKit         │    │ • ElevenLabs    │
│ • Statsig       │    │ • Qiskit        │    │ • Statsig       │
│ • Voice Player  │    │ • ML Models     │    │ • ML Predictors │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Frontend Setup
```bash
cd molviz
npm install
npm start
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python start.py
```

### Environment Configuration
Copy `backend/env.example` to `backend/.env` and configure your API keys:

```env
# API Keys
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
STATSIG_SDK_KEY=your-statsig-sdk-key

# Database (optional)
DATABASE_TYPE=file  # or supabase, postgresql
```

## 🧬 Usage

### 1. Molecular Input
- **SMILES Strings**: Direct chemical notation input
- **PDB Files**: Upload protein structure files
- **Molecular Drawing**: Interactive chemical structure editor

### 2. Analysis Pipeline
1. **Input Validation**: RDKit-based molecular validation
2. **Quantum Simulation**: DFT calculations, HOMO-LUMO analysis
3. **Property Calculation**: Lipinski's Rule, LogP, TPSA, etc.
4. **ML Predictions**: Drug-likeness, binding affinity, ADME/Tox
5. **AI Summary**: Gemini-generated natural language insights
6. **Voice Narration**: ElevenLabs audio summary

### 3. Example Molecules
Try these known drugs for testing:

**Cancer (Imatinib)**
```
SMILES: CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3
```

**Diabetes (Metformin)**
```
SMILES: CN(C)C(=N)N=C(N)N
```

**Alzheimer's (Donepezil)**
```
SMILES: CN1CCN(CC1)C2=CC=CC=C2C3=CC=CC=C3
```

## 📊 Output Analysis

### Quantum Chemistry Results
- **Stability**: Total energy in kcal/mol
- **HOMO-LUMO Gap**: Electronic band gap in eV
- **Binding Potential**: Predicted binding affinity
- **Dipole Moment**: Molecular polarity
- **Vibrational Frequencies**: IR spectrum predictions

### Physicochemical Properties
- **Molecular Weight**: Dalton units
- **LogP**: Lipophilicity measure
- **TPSA**: Topological polar surface area
- **Lipinski Violations**: Drug-likeness assessment
- **ADME Score**: Absorption, distribution, metabolism, excretion

### ML Predictions
- **Drug Likeness**: 0-100% score
- **Binding Likelihood**: Target interaction probability
- **Synthetic Accessibility**: Ease of synthesis
- **Toxicity Risk**: Low/Medium/High assessment
- **Confidence Score**: Model prediction confidence

## 🔬 Scientific Applications

### Drug Discovery
- Lead compound optimization
- ADME/Tox profiling
- Target binding prediction
- Synthetic route planning

### Chemical Research
- Molecular property analysis
- Quantum chemistry insights
- Structure-activity relationships
- Chemical space exploration

### Education
- Interactive molecular visualization
- Quantum chemistry concepts
- Drug design principles
- AI in chemistry

## 🚀 Deployment

### Local Development
```bash
# Frontend
cd molviz && npm start

# Backend
cd backend && python start.py
```

### Production Deployment
- **Frontend**: Deploy to Vercel/Netlify
- **Backend**: Deploy to AWS Lambda/Google Cloud Run
- **Database**: Use Supabase or PostgreSQL
- **CDN**: CloudFlare for static assets

## 📈 Performance

- **Quantum Simulations**: 30-60 seconds per molecule
- **ML Predictions**: <1 second
- **Voice Generation**: 5-10 seconds
- **3D Rendering**: Real-time interaction
- **API Response**: <2 seconds average

## 🔧 API Endpoints

### Core Analysis
- `POST /api/simulate_molecule` - Main analysis endpoint
- `GET /api/analysis/{id}` - Retrieve stored results
- `POST /api/generate_voice` - Voice narration

### Utility
- `GET /api/examples` - Example molecules
- `GET /health` - Health check
- `GET /` - API information

## 🧪 Testing

### Frontend Tests
```bash
cd molviz
npm test
```

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Example Analysis
```bash
curl -X POST "http://localhost:8000/api/simulate_molecule" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "smiles",
    "molecular_data": "CN(C)C(=N)N=C(N)N",
    "timestamp": "2024-01-01T00:00:00Z"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **3Dmol.js** for molecular visualization
- **RDKit** for cheminformatics
- **Qiskit Nature** for quantum chemistry
- **Google Gemini** for AI insights
- **ElevenLabs** for voice synthesis
- **Statsig** for feature management

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**MolViz AI** - Bringing AI and quantum chemistry together for molecular discovery 🧬✨