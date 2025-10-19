import React, { useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Upload, FileText, Zap, Brain, Target, Play, Volume2 } from 'lucide-react';
import './AnalysisPage.css';

function AnalysisPage() {
  const [inputType, setInputType] = useState('smiles');
  const [molecularInput, setMolecularInput] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [geminiSummary, setGeminiSummary] = useState('');
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);

  // Mock logEvent function for demo
  const logEvent = (event, data) => {
    console.log('Event logged:', event, data);
  };

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setMolecularInput(e.target.result);
        setInputType('pdb');
      };
      reader.readAsText(file);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.pdb', '.mol', '.sdf'],
      'chemical/x-pdb': ['.pdb'],
      'chemical/x-mdl-molfile': ['.mol']
    }
  });

  const analyzeMolecule = async () => {
    if (!molecularInput.trim()) return;

    setIsAnalyzing(true);
    logEvent('molecule_analysis_started', { input_type: inputType });

    try {
      // Mock analysis for demo - in production this would call the backend
      const mockResults = {
        quantum_results: {
          stability: -Math.random() * 200 - 50,
          homo_lumo_gap: Math.random() * 4 + 2,
          binding_potential: -Math.random() * 10 - 5,
          dipole_moment: Math.random() * 5 + 1,
          polarizability: Math.random() * 30 + 20
        },
        properties: {
          molecular_weight: Math.random() * 400 + 100,
          logp: Math.random() * 5 - 1,
          tpsa: Math.random() * 100 + 20,
          hbd: Math.floor(Math.random() * 8),
          hba: Math.floor(Math.random() * 10),
          rotatable_bonds: Math.floor(Math.random() * 10),
          lipinski_violations: Math.floor(Math.random() * 3),
          formal_charge: Math.floor(Math.random() * 3) - 1,
          num_atoms: Math.floor(Math.random() * 40) + 10,
          num_bonds: Math.floor(Math.random() * 50) + 10,
          num_rings: Math.floor(Math.random() * 4),
          aromatic_atoms: Math.floor(Math.random() * 5)
        },
        ml_predictions: {
          drug_likeness: Math.random() * 40 + 50,
          binding_likelihood: Math.random() * 40 + 40,
          synthetic_accessibility: Math.random() * 30 + 60,
          stability_score: Math.random() * 20 + 70,
          binding_affinity_score: Math.random() * 30 + 50,
          toxicity_risk: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
          adme_score: Math.random() * 30 + 60,
          confidence: Math.random() * 0.3 + 0.7
        },
        suggested_molecules: [
          {
            name: "Analog 1",
            description: "Modified side chain for improved selectivity",
            smiles: "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
            reason: "Similar core structure with optimized properties"
          },
          {
            name: "Analog 2", 
            description: "Ring substitution for enhanced binding",
            smiles: "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
            reason: "Structural modification to improve target binding"
          }
        ]
      };

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      setAnalysisResults(mockResults);
      logEvent('molecule_analysis_completed', { 
        input_type: inputType,
        stability: mockResults.quantum_results?.stability,
        binding_potential: mockResults.quantum_results?.binding_potential
      });

      // Generate summary
      await generateGeminiSummary(mockResults);
    } catch (error) {
      console.error('Analysis failed:', error);
      logEvent('molecule_analysis_failed', { error: error.message });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateGeminiSummary = async (results) => {
    setIsGeneratingSummary(true);
    
    try {
      // Mock summary for demo
      const summary = `
**Molecular Analysis Summary**

Your molecule shows ${results.quantum_results?.stability < -200 ? 'excellent' : 'good'} stability with a total energy of ${results.quantum_results?.stability.toFixed(1)} kcal/mol. The HOMO-LUMO gap of ${results.quantum_results?.homo_lumo_gap.toFixed(2)} eV indicates ${results.quantum_results?.homo_lumo_gap > 4 ? 'good' : 'moderate'} electronic stability.

**Drug-Likeness Assessment:**
- Molecular weight: ${results.properties?.molecular_weight.toFixed(1)} Da (${results.properties?.molecular_weight < 500 ? 'within optimal range' : 'slightly high'})
- LogP: ${results.properties?.logp.toFixed(2)} (${results.properties?.logp > 0 && results.properties?.logp < 3 ? 'optimal lipophilicity' : 'may need optimization'})
- TPSA: ${results.properties?.tpsa.toFixed(1)} Ų (${results.properties?.tpsa < 140 ? 'good permeability' : 'may have absorption issues'})
- Lipinski violations: ${results.properties?.lipinski_violations} (${results.properties?.lipinski_violations === 0 ? 'excellent drug-likeness' : 'some optimization needed'})

**AI Predictions:**
- Drug likeness: ${results.ml_predictions?.drug_likeness.toFixed(1)}% (${results.ml_predictions?.drug_likeness > 70 ? 'high potential' : 'moderate potential'})
- Binding likelihood: ${results.ml_predictions?.binding_likelihood.toFixed(1)}% (${results.ml_predictions?.binding_likelihood > 60 ? 'strong binding potential' : 'moderate binding potential'})
- Synthetic accessibility: ${results.ml_predictions?.synthetic_accessibility.toFixed(1)}% (${results.ml_predictions?.synthetic_accessibility > 70 ? 'easily synthesizable' : 'moderate complexity'})

**Recommendations:**
${results.properties?.lipinski_violations > 0 ? '• Consider reducing molecular weight or LogP to improve drug-likeness' : '• Excellent drug-likeness profile maintained'}
• Focus on target validation and binding studies
• Consider formulation optimization for better bioavailability
• Explore structural analogs for improved selectivity
      `;
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setGeminiSummary(summary);
      logEvent('gemini_summary_generated', { summary_length: summary.length });
    } catch (error) {
      console.error('Summary generation failed:', error);
    } finally {
      setIsGeneratingSummary(false);
    }
  };

  const generateVoiceNarration = async () => {
    if (!geminiSummary) return;

    setIsGeneratingAudio(true);
    
    try {
      // Mock voice generation for demo
      await new Promise(resolve => setTimeout(resolve, 2000));
      setAudioUrl("https://example.com/mock-audio.mp3");
      logEvent('voice_narration_generated');
    } catch (error) {
      console.error('Voice generation failed:', error);
    } finally {
      setIsGeneratingAudio(false);
    }
  };

  const exampleMolecules = [
    {
      name: "Imatinib (Cancer)",
      smiles: "CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3",
      description: "Targeted cancer therapy for chronic myeloid leukemia"
    },
    {
      name: "Donepezil (Alzheimer's)",
      smiles: "CN1CCN(CC1)C2=CC=CC=C2C3=CC=CC=C3",
      description: "Acetylcholinesterase inhibitor for Alzheimer's treatment"
    },
    {
      name: "Metformin (Diabetes)",
      smiles: "CN(C)C(=N)N=C(N)N",
      description: "Antidiabetic drug targeting AMPK pathway"
    }
  ];

  return (
    <div className="analysis-page">
      <div className="analysis-header">
        <h1>Molecular Analysis Platform</h1>
        <p>Upload PDB files, draw molecules, or input SMILES for comprehensive quantum chemistry and AI analysis</p>
      </div>

      <div className="analysis-container">
        <div className="input-section">
          <div className="input-tabs">
            <button 
              className={`tab ${inputType === 'smiles' ? 'active' : ''}`}
              onClick={() => setInputType('smiles')}
            >
              <FileText size={20} />
              SMILES Input
            </button>
            <button 
              className={`tab ${inputType === 'pdb' ? 'active' : ''}`}
              onClick={() => setInputType('pdb')}
            >
              <Upload size={20} />
              PDB Upload
            </button>
            <button 
              className={`tab ${inputType === 'draw' ? 'active' : ''}`}
              onClick={() => setInputType('draw')}
            >
              <Target size={20} />
              Draw Molecule
            </button>
          </div>

          {inputType === 'smiles' && (
            <div className="input-area">
              <label htmlFor="smiles-input">Enter SMILES string:</label>
              <input
                id="smiles-input"
                type="text"
                value={molecularInput}
                onChange={(e) => setMolecularInput(e.target.value)}
                placeholder="e.g., CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3"
                className="smiles-input"
              />
              <div className="example-molecules">
                <h4>Try these examples:</h4>
                {exampleMolecules.map((mol, index) => (
                  <button
                    key={index}
                    className="example-btn"
                    onClick={() => setMolecularInput(mol.smiles)}
                  >
                    <strong>{mol.name}</strong>
                    <span>{mol.description}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {inputType === 'pdb' && (
            <div className="input-area">
              <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
                <input {...getInputProps()} />
                <Upload size={48} />
                <p>Drag & drop PDB/MOL files here, or click to select</p>
                <p className="file-types">Supported: .pdb, .mol, .sdf</p>
              </div>
              {molecularInput && (
                <div className="file-preview">
                  <h4>File loaded:</h4>
                  <pre>{molecularInput.substring(0, 500)}...</pre>
                </div>
              )}
            </div>
          )}

          {inputType === 'draw' && (
            <div className="input-area">
              <div className="drawing-area">
                <p>Molecular drawing interface would be integrated here</p>
                <p className="coming-soon">Coming soon: Interactive molecular drawing with ChemDoodle</p>
              </div>
            </div>
          )}

          <button 
            className="analyze-btn"
            onClick={analyzeMolecule}
            disabled={!molecularInput.trim() || isAnalyzing}
          >
            {isAnalyzing ? (
              <>
                <Zap className="spinning" size={20} />
                Analyzing...
              </>
            ) : (
              <>
                <Brain size={20} />
                Analyze Molecule
              </>
            )}
          </button>
        </div>

        {analysisResults && (
          <div className="results-section">
            <div className="results-header">
              <h2>Analysis Results</h2>
              <div className="result-actions">
                <button 
                  className="voice-btn"
                  onClick={generateVoiceNarration}
                  disabled={!geminiSummary || isGeneratingAudio}
                >
                  {isGeneratingAudio ? (
                    <>
                      <Volume2 className="spinning" size={16} />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Play size={16} />
                      Generate Voice
                    </>
                  )}
                </button>
                {audioUrl && (
                  <audio controls src={audioUrl} className="audio-player">
                    Your browser does not support the audio element.
                  </audio>
                )}
              </div>
            </div>

            <div className="results-grid">
              <div className="result-card quantum">
                <h3>Quantum Simulation</h3>
                <div className="metric">
                  <span className="label">Stability:</span>
                  <span className="value">{analysisResults.quantum_results?.stability.toFixed(1)} kcal/mol</span>
                </div>
                <div className="metric">
                  <span className="label">HOMO-LUMO Gap:</span>
                  <span className="value">{analysisResults.quantum_results?.homo_lumo_gap.toFixed(2)} eV</span>
                </div>
                <div className="metric">
                  <span className="label">Binding Potential:</span>
                  <span className="value">{analysisResults.quantum_results?.binding_potential.toFixed(1)} kcal/mol</span>
                </div>
              </div>

              <div className="result-card properties">
                <h3>Physicochemical Properties</h3>
                <div className="metric">
                  <span className="label">Molecular Weight:</span>
                  <span className="value">{analysisResults.properties?.molecular_weight.toFixed(1)} Da</span>
                </div>
                <div className="metric">
                  <span className="label">LogP:</span>
                  <span className="value">{analysisResults.properties?.logp.toFixed(2)}</span>
                </div>
                <div className="metric">
                  <span className="label">TPSA:</span>
                  <span className="value">{analysisResults.properties?.tpsa.toFixed(1)} Ų</span>
                </div>
                <div className="metric">
                  <span className="label">Lipinski Violations:</span>
                  <span className={`value ${analysisResults.properties?.lipinski_violations > 0 ? 'warning' : 'success'}`}>
                    {analysisResults.properties?.lipinski_violations}
                  </span>
                </div>
              </div>

              <div className="result-card ml">
                <h3>AI Predictions</h3>
                <div className="metric">
                  <span className="label">Drug Likeness:</span>
                  <span className="value">{analysisResults.ml_predictions?.drug_likeness.toFixed(1)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Binding Likelihood:</span>
                  <span className="value">{analysisResults.ml_predictions?.binding_likelihood.toFixed(1)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Synthetic Accessibility:</span>
                  <span className="value">{analysisResults.ml_predictions?.synthetic_accessibility.toFixed(1)}%</span>
                </div>
              </div>
            </div>

            {geminiSummary && (
              <div className="ai-summary">
                <h3>AI Analysis Summary</h3>
                {isGeneratingSummary ? (
                  <div className="loading">
                    <Brain className="spinning" size={20} />
                    Generating AI summary...
                  </div>
                ) : (
                  <div className="summary-content">
                    {geminiSummary}
                  </div>
                )}
              </div>
            )}

            {analysisResults.suggested_molecules && (
              <div className="suggestions">
                <h3>Related Molecules to Explore</h3>
                <div className="suggestion-list">
                  {analysisResults.suggested_molecules.map((mol, index) => (
                    <div key={index} className="suggestion-item">
                      <h4>{mol.name}</h4>
                      <p>{mol.description}</p>
                      <code>{mol.smiles}</code>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalysisPage;