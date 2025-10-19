from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import logging

from services.molecular_analysis import MolecularAnalyzer
from services.quantum_simulation import QuantumSimulator
from services.ml_predictor import MLPredictor
from services.voice_generator import VoiceGenerator
from services.database import DatabaseManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Molecular Analysis API",
    description="AI-powered molecular analysis with quantum chemistry and machine learning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
molecular_analyzer = MolecularAnalyzer()
quantum_simulator = QuantumSimulator()
ml_predictor = MLPredictor()
voice_generator = VoiceGenerator()
db_manager = DatabaseManager()

class MolecularInput(BaseModel):
    input_type: str  # 'smiles', 'pdb', 'mol'
    molecular_data: str
    timestamp: str

class AnalysisResponse(BaseModel):
    quantum_results: Dict[str, Any]
    properties: Dict[str, Any]
    ml_predictions: Dict[str, Any]
    suggested_molecules: List[Dict[str, str]]
    analysis_id: str

class VoiceRequest(BaseModel):
    text: str
    voice_settings: Optional[Dict[str, float]] = None

@app.get("/")
async def root():
    return {"message": "Molecular Analysis API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {
        "molecular_analyzer": "active",
        "quantum_simulator": "active",
        "ml_predictor": "active",
        "voice_generator": "active"
    }}

@app.post("/api/simulate_molecule", response_model=AnalysisResponse)
async def simulate_molecule(input_data: MolecularInput):
    """
    Main endpoint for molecular analysis
    """
    try:
        logger.info(f"Starting analysis for {input_data.input_type} input")
        
        # Validate molecular input
        validation_result = molecular_analyzer.validate_input(
            input_data.input_type, 
            input_data.molecular_data
        )
        
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # Run quantum simulation
        quantum_results = await quantum_simulator.simulate(
            input_data.molecular_data,
            input_data.input_type
        )
        
        # Compute physicochemical properties
        properties = molecular_analyzer.compute_properties(
            input_data.molecular_data,
            input_data.input_type
        )
        
        # Run ML predictions
        ml_predictions = await ml_predictor.predict(
            input_data.molecular_data,
            input_data.input_type,
            quantum_results,
            properties
        )
        
        # Generate suggested molecules
        suggested_molecules = ml_predictor.suggest_related_molecules(
            input_data.molecular_data,
            input_data.input_type
        )
        
        # Store analysis in database
        analysis_id = db_manager.store_analysis({
            "input_type": input_data.input_type,
            "molecular_data": input_data.molecular_data,
            "quantum_results": quantum_results,
            "properties": properties,
            "ml_predictions": ml_predictions,
            "timestamp": input_data.timestamp
        })
        
        logger.info(f"Analysis completed successfully with ID: {analysis_id}")
        
        return AnalysisResponse(
            quantum_results=quantum_results,
            properties=properties,
            ml_predictions=ml_predictions,
            suggested_molecules=suggested_molecules,
            analysis_id=analysis_id
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate_voice")
async def generate_voice(request: VoiceRequest):
    """
    Generate voice narration using ElevenLabs
    """
    try:
        audio_url = await voice_generator.generate_voice(
            request.text,
            request.voice_settings
        )
        
        return {"audio_url": audio_url}
        
    except Exception as e:
        logger.error(f"Voice generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")

@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Retrieve stored analysis results
    """
    try:
        analysis = db_manager.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Failed to retrieve analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")

@app.get("/api/examples")
async def get_example_molecules():
    """
    Get example molecules for testing
    """
    examples = [
        {
            "name": "Imatinib (Cancer)",
            "smiles": "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
            "description": "Targeted cancer therapy for chronic myeloid leukemia",
            "disease": "Cancer"
        },
        {
            "name": "Donepezil (Alzheimer's)",
            "smiles": "CN1CCN(CC1)C2=CC=CC=C2C3=CC=CC=C3",
            "description": "Acetylcholinesterase inhibitor for Alzheimer's treatment",
            "disease": "Alzheimer's"
        },
        {
            "name": "Metformin (Diabetes)",
            "smiles": "CN(C)C(=N)N=C(N)N",
            "description": "Antidiabetic drug targeting AMPK pathway",
            "disease": "Diabetes"
        },
        {
            "name": "Nirmatrelvir (COVID-19)",
            "smiles": "CC1=NC(=C(N1C2=CC=CC=C2)N)C3CCCCC3",
            "description": "COVID-19 protease inhibitor",
            "disease": "COVID-19"
        },
        {
            "name": "Losartan (Hypertension)",
            "smiles": "CC1=CC(=NO1)C2=CC=CC=C2C3=NC=CC=N3C4=CC=CC=C4",
            "description": "Angiotensin receptor blocker for blood pressure",
            "disease": "Hypertension"
        },
        {
            "name": "Levodopa (Parkinson's)",
            "smiles": "C1=CC(=CC=C1C(C(=O)O)N)O",
            "description": "Dopamine precursor for Parkinson's treatment",
            "disease": "Parkinson's"
        }
    ]
    
    return {"examples": examples}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
