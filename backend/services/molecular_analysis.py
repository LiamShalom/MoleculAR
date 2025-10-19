from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen
from rdkit.Chem import rdMolDescriptors
import numpy as np
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class MolecularAnalyzer:
    """
    Handles molecular input validation and physicochemical property computation
    """
    
    def __init__(self):
        self.supported_formats = ['smiles', 'pdb', 'mol', 'sdf']
    
    def validate_input(self, input_type: str, molecular_data: str) -> Dict[str, Any]:
        """
        Validate molecular input based on type
        """
        try:
            if input_type == 'smiles':
                mol = Chem.MolFromSmiles(molecular_data)
                if mol is None:
                    return {"valid": False, "error": "Invalid SMILES string"}
                
            elif input_type == 'pdb':
                # Basic PDB validation - check for ATOM/HETATM records
                if not any(line.startswith(('ATOM', 'HETATM')) for line in molecular_data.split('\n')):
                    return {"valid": False, "error": "Invalid PDB format - no ATOM/HETATM records found"}
                
            elif input_type == 'mol':
                # MOL file validation
                if not molecular_data.startswith('$MOL'):
                    return {"valid": False, "error": "Invalid MOL format"}
                
            else:
                return {"valid": False, "error": f"Unsupported input type: {input_type}"}
            
            return {"valid": True, "error": None}
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {"valid": False, "error": f"Validation failed: {str(e)}"}
    
    def compute_properties(self, molecular_data: str, input_type: str) -> Dict[str, Any]:
        """
        Compute physicochemical properties using RDKit
        """
        try:
            # Convert to RDKit molecule object
            mol = self._get_molecule_object(molecular_data, input_type)
            
            if mol is None:
                raise ValueError("Could not create molecule object")
            
            # Basic descriptors
            mw = Descriptors.MolWt(mol)
            logp = Crippen.MolLogP(mol)
            tpsa = Descriptors.TPSA(mol)
            hbd = Descriptors.NumHDonors(mol)
            hba = Descriptors.NumHAcceptors(mol)
            rotbonds = Descriptors.NumRotatableBonds(mol)
            
            # Lipinski's Rule of Five
            lipinski_violations = 0
            if mw > 500: lipinski_violations += 1
            if logp > 5: lipinski_violations += 1
            if hbd > 5: lipinski_violations += 1
            if hba > 10: lipinski_violations += 1
            
            # Additional descriptors
            formal_charge = Chem.rdmolops.GetFormalCharge(mol)
            num_atoms = mol.GetNumAtoms()
            num_bonds = mol.GetNumBonds()
            num_rings = Descriptors.RingCount(mol)
            aromatic_atoms = Descriptors.NumAromaticRings(mol)
            
            # Drug-likeness score (simplified)
            drug_likeness_score = self._calculate_drug_likeness_score(
                mw, logp, tpsa, hbd, hba, rotbonds, lipinski_violations
            )
            
            return {
                "molecular_weight": round(mw, 2),
                "logp": round(logp, 2),
                "tpsa": round(tpsa, 2),
                "hbd": hbd,
                "hba": hba,
                "rotatable_bonds": rotbonds,
                "lipinski_violations": lipinski_violations,
                "formal_charge": formal_charge,
                "num_atoms": num_atoms,
                "num_bonds": num_bonds,
                "num_rings": num_rings,
                "aromatic_atoms": aromatic_atoms,
                "drug_likeness_score": round(drug_likeness_score, 2)
            }
            
        except Exception as e:
            logger.error(f"Property computation failed: {str(e)}")
            return {"error": f"Property computation failed: {str(e)}"}
    
    def _get_molecule_object(self, molecular_data: str, input_type: str):
        """
        Convert molecular data to RDKit molecule object
        """
        try:
            if input_type == 'smiles':
                return Chem.MolFromSmiles(molecular_data)
            elif input_type == 'pdb':
                # For PDB, we'll need to extract SMILES or use other methods
                # This is a simplified approach - in practice, you'd use more sophisticated methods
                return None  # Placeholder - would need PDB to SMILES conversion
            elif input_type == 'mol':
                return Chem.MolFromMolBlock(molecular_data)
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to create molecule object: {str(e)}")
            return None
    
    def _calculate_drug_likeness_score(self, mw, logp, tpsa, hbd, hba, rotbonds, violations):
        """
        Calculate a simplified drug-likeness score
        """
        score = 100
        
        # Penalize Lipinski violations
        score -= violations * 20
        
        # Penalize extreme values
        if mw < 150 or mw > 500:
            score -= 10
        if logp < -2 or logp > 5:
            score -= 10
        if tpsa < 20 or tpsa > 140:
            score -= 10
        if hbd > 5:
            score -= 10
        if hba > 10:
            score -= 10
        if rotbonds > 10:
            score -= 10
        
        return max(0, min(100, score))
