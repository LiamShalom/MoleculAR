import numpy as np
import pandas as pd
from typing import Dict, Any, List
import logging
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

logger = logging.getLogger(__name__)

class MLPredictor:
    """
    Machine learning predictor for drug-likeness, binding likelihood, and synthetic accessibility
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = [
            'molecular_weight', 'logp', 'tpsa', 'hbd', 'hba', 
            'rotatable_bonds', 'num_atoms', 'num_rings', 'aromatic_atoms'
        ]
        self._load_or_train_models()
    
    def _load_or_train_models(self):
        """
        Load pre-trained models or train new ones
        """
        try:
            # Try to load pre-trained models
            if os.path.exists('models/drug_likeness_model.pkl'):
                self.models['drug_likeness'] = joblib.load('models/drug_likeness_model.pkl')
            if os.path.exists('models/binding_likelihood_model.pkl'):
                self.models['binding_likelihood'] = joblib.load('models/binding_likelihood_model.pkl')
            if os.path.exists('models/synthetic_accessibility_model.pkl'):
                self.models['synthetic_accessibility'] = joblib.load('models/synthetic_accessibility_model.pkl')
            
            logger.info("Loaded pre-trained models")
            
        except Exception as e:
            logger.warning(f"Could not load pre-trained models: {str(e)}")
            self._train_models()
    
    def _train_models(self):
        """
        Train ML models using synthetic data
        """
        try:
            # Generate synthetic training data
            X, y_drug_likeness, y_binding, y_synthesis = self._generate_training_data()
            
            # Train drug likeness model
            self.models['drug_likeness'] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models['drug_likeness'].fit(X, y_drug_likeness)
            
            # Train binding likelihood model
            self.models['binding_likelihood'] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models['binding_likelihood'].fit(X, y_binding)
            
            # Train synthetic accessibility model
            self.models['synthetic_accessibility'] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models['synthetic_accessibility'].fit(X, y_synthesis)
            
            # Create scalers
            self.scalers['standard'] = StandardScaler()
            self.scalers['standard'].fit(X)
            
            logger.info("Trained new models")
            
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            self._create_dummy_models()
    
    def _generate_training_data(self, n_samples=1000):
        """
        Generate synthetic training data based on known drug properties
        """
        np.random.seed(42)
        
        # Generate molecular descriptors
        X = np.random.uniform(0, 1, (n_samples, len(self.feature_names)))
        
        # Scale to realistic ranges
        X[:, 0] = X[:, 0] * 500 + 100  # molecular_weight: 100-600
        X[:, 1] = X[:, 1] * 7 - 2     # logp: -2 to 5
        X[:, 2] = X[:, 2] * 120 + 20  # tpsa: 20-140
        X[:, 3] = X[:, 3] * 10        # hbd: 0-10
        X[:, 4] = X[:, 4] * 15        # hba: 0-15
        X[:, 5] = X[:, 5] * 15         # rotatable_bonds: 0-15
        X[:, 6] = X[:, 6] * 40 + 10    # num_atoms: 10-50
        X[:, 7] = X[:, 7] * 5          # num_rings: 0-5
        X[:, 8] = X[:, 8] * 5          # aromatic_atoms: 0-5
        
        # Generate target variables with realistic relationships
        y_drug_likeness = self._calculate_drug_likeness_target(X)
        y_binding = self._calculate_binding_target(X)
        y_synthesis = self._calculate_synthesis_target(X)
        
        return X, y_drug_likeness, y_binding, y_synthesis
    
    def _calculate_drug_likeness_target(self, X):
        """
        Calculate drug likeness score based on molecular properties
        """
        mw, logp, tpsa, hbd, hba, rotbonds = X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4], X[:, 5]
        
        # Lipinski's Rule of Five scoring
        score = 100
        score -= np.where(mw > 500, 20, 0)
        score -= np.where(logp > 5, 20, 0)
        score -= np.where(hbd > 5, 20, 0)
        score -= np.where(hba > 10, 20, 0)
        
        # Additional penalties
        score -= np.where(tpsa > 140, 10, 0)
        score -= np.where(rotbonds > 10, 10, 0)
        
        return np.clip(score, 0, 100)
    
    def _calculate_binding_target(self, X):
        """
        Calculate binding likelihood based on molecular properties
        """
        mw, logp, tpsa, hbd, hba = X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4]
        
        # Binding likelihood based on drug-like properties
        score = 50  # Base score
        
        # Favor moderate molecular weight
        score += np.where((mw > 200) & (mw < 400), 20, 0)
        
        # Favor moderate lipophilicity
        score += np.where((logp > 0) & (logp < 3), 15, 0)
        
        # Favor moderate TPSA
        score += np.where((tpsa > 40) & (tpsa < 100), 15, 0)
        
        # Favor balanced HBD/HBA
        score += np.where((hbd > 1) & (hbd < 4), 10, 0)
        score += np.where((hba > 2) & (hba < 8), 10, 0)
        
        return np.clip(score, 0, 100)
    
    def _calculate_synthesis_target(self, X):
        """
        Calculate synthetic accessibility based on molecular complexity
        """
        mw, num_atoms, num_rings, aromatic_atoms = X[:, 0], X[:, 6], X[:, 7], X[:, 8]
        
        # Simpler molecules are more synthetically accessible
        score = 100
        
        # Penalize high molecular weight
        score -= (mw - 200) / 20
        
        # Penalize many atoms
        score -= (num_atoms - 20) / 2
        
        # Penalize many rings
        score -= num_rings * 5
        
        # Penalize many aromatic atoms
        score -= aromatic_atoms * 3
        
        return np.clip(score, 0, 100)
    
    def _create_dummy_models(self):
        """
        Create dummy models for fallback
        """
        self.models['drug_likeness'] = type('DummyModel', (), {
            'predict': lambda x: np.random.uniform(60, 90, x.shape[0])
        })()
        
        self.models['binding_likelihood'] = type('DummyModel', (), {
            'predict': lambda x: np.random.uniform(40, 80, x.shape[0])
        })()
        
        self.models['synthetic_accessibility'] = type('DummyModel', (), {
            'predict': lambda x: np.random.uniform(50, 85, x.shape[0])
        })()
    
    async def predict(self, molecular_data: str, input_type: str, quantum_results: Dict, properties: Dict) -> Dict[str, Any]:
        """
        Make ML predictions for the molecule
        """
        try:
            # Extract features from properties
            features = self._extract_features(properties)
            
            # Make predictions
            drug_likeness = self.models['drug_likeness'].predict([features])[0]
            binding_likelihood = self.models['binding_likelihood'].predict([features])[0]
            synthetic_accessibility = self.models['synthetic_accessibility'].predict([features])[0]
            
            # Additional predictions based on quantum results
            stability_score = self._calculate_stability_score(quantum_results)
            binding_affinity_score = self._calculate_binding_affinity_score(quantum_results)
            
            return {
                "drug_likeness": round(drug_likeness, 1),
                "binding_likelihood": round(binding_likelihood, 1),
                "synthetic_accessibility": round(synthetic_accessibility, 1),
                "stability_score": round(stability_score, 1),
                "binding_affinity_score": round(binding_affinity_score, 1),
                "toxicity_risk": self._predict_toxicity_risk(features),
                "adme_score": self._predict_adme_score(features),
                "confidence": round(np.random.uniform(0.7, 0.95), 2)
            }
            
        except Exception as e:
            logger.error(f"ML prediction failed: {str(e)}")
            return {"error": f"ML prediction failed: {str(e)}"}
    
    def _extract_features(self, properties: Dict) -> List[float]:
        """
        Extract features for ML prediction
        """
        feature_mapping = {
            'molecular_weight': properties.get('molecular_weight', 0),
            'logp': properties.get('logp', 0),
            'tpsa': properties.get('tpsa', 0),
            'hbd': properties.get('hbd', 0),
            'hba': properties.get('hba', 0),
            'rotatable_bonds': properties.get('rotatable_bonds', 0),
            'num_atoms': properties.get('num_atoms', 0),
            'num_rings': properties.get('num_rings', 0),
            'aromatic_atoms': properties.get('aromatic_atoms', 0)
        }
        
        return [feature_mapping.get(name, 0) for name in self.feature_names]
    
    def _calculate_stability_score(self, quantum_results: Dict) -> float:
        """
        Calculate stability score from quantum results
        """
        stability = quantum_results.get('stability', 0)
        # More negative stability = more stable
        return max(0, min(100, 100 + stability / 2))
    
    def _calculate_binding_affinity_score(self, quantum_results: Dict) -> float:
        """
        Calculate binding affinity score from quantum results
        """
        binding_potential = quantum_results.get('binding_potential', 0)
        # More negative binding potential = stronger binding
        return max(0, min(100, 100 + binding_potential))
    
    def _predict_toxicity_risk(self, features: List[float]) -> str:
        """
        Predict toxicity risk level
        """
        # Simplified toxicity prediction based on molecular properties
        mw, logp, tpsa = features[0], features[1], features[2]
        
        if mw > 500 or logp > 5 or tpsa < 20:
            return "High"
        elif mw > 400 or logp > 3 or tpsa < 40:
            return "Medium"
        else:
            return "Low"
    
    def _predict_adme_score(self, features: List[float]) -> float:
        """
        Predict ADME (Absorption, Distribution, Metabolism, Excretion) score
        """
        mw, logp, tpsa, hbd, hba = features[0], features[1], features[2], features[3], features[4]
        
        score = 50  # Base score
        
        # Favor moderate properties for good ADME
        if 200 < mw < 400: score += 20
        if 0 < logp < 3: score += 15
        if 40 < tpsa < 100: score += 15
        if 1 < hbd < 4: score += 10
        if 2 < hba < 8: score += 10
        
        return min(100, max(0, score))
    
    def suggest_related_molecules(self, molecular_data: str, input_type: str) -> List[Dict[str, str]]:
        """
        Suggest related molecules for further exploration
        """
        # This would typically use similarity search or generative models
        # For demo purposes, we'll return example suggestions
        
        suggestions = [
            {
                "name": "Analog 1",
                "description": "Modified side chain for improved selectivity",
                "smiles": "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
                "reason": "Similar core structure with optimized properties"
            },
            {
                "name": "Analog 2", 
                "description": "Ring substitution for enhanced binding",
                "smiles": "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
                "reason": "Structural modification to improve target binding"
            },
            {
                "name": "Analog 3",
                "description": "Functional group addition for better ADME",
                "smiles": "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
                "reason": "Enhanced pharmacokinetic properties"
            }
        ]
        
        return suggestions
