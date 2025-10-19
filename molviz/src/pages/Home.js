import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

export default function Home() {
  return (
    <div className="home-container">
      <div className="hero">
        <div className="hero-inner">
          <h1 className="title">MolViz AI</h1>
          <p className="subtitle">AI-powered molecular analysis with quantum chemistry, machine learning, and natural language insights.</p>
          <div className="hero-cta">
            <Link className="cta-button primary" to="/quantum">Quantum Chemistry</Link>
            <Link className="cta-button secondary" to="/analysis">AI Analysis</Link>
            <Link className="cta-button tertiary" to="/viewer">3D Viewer</Link>
            <a className="cta-outline" href="https://3dmol.org/" target="_blank" rel="noreferrer">About 3Dmol.js</a>
          </div>
        </div>
      </div>

      <main className="content">
        <section className="cards">
          <article className="card">
            <div className="card-icon">⚛️</div>
            <h3>Quantum Chemistry</h3>
            <p>VQE, EOM, time evolution, and spectral estimation using cutting-edge quantum computing.</p>
          </article>

          <article className="card">
            <div className="card-icon">🔬</div>
            <h3>Quantum Spectroscopy</h3>
            <p>Interactive absorption/emission spectra with phase estimation and shadow tomography.</p>
          </article>

          <article className="card">
            <div className="card-icon">⏰</div>
            <h3>Quantum Dynamics</h3>
            <p>Trotterized time evolution for reaction mechanisms and electron transfer processes.</p>
          </article>

          <article className="card">
            <div className="card-icon">🧠</div>
            <h3>AI Analysis</h3>
            <p>ML predictions, drug-likeness scoring, and Gemini-powered quantum chemistry insights.</p>
          </article>

          <article className="card">
            <div className="card-icon">🎯</div>
            <h3>Error Mitigation</h3>
            <p>Advanced noise resilience with confidence scores and statistical error analysis.</p>
          </article>

          <article className="card">
            <div className="card-icon">🔬</div>
            <h3>3D Visualization</h3>
            <p>Interactive molecular viewer with quantum orbital visualization and real-time manipulation.</p>
          </article>
        </section>

        <section className="instructions">
          <h2>Get started with Quantum Chemistry</h2>
          <ol>
            <li>Click "Quantum Chemistry" to access the advanced quantum computing platform.</li>
            <li>Input your molecule and configure quantum simulation parameters (VQE, EOM, time evolution).</li>
            <li>Run quantum circuits for ground state, excited states, and spectral estimation.</li>
            <li>Explore interactive quantum spectroscopy and time evolution dynamics.</li>
            <li>Get AI-powered insights with confidence scores and error analysis.</li>
          </ol>

          <div className="example-molecules">
            <h3>Try these quantum chemistry examples:</h3>
            <div className="example-grid">
              <div className="example-item">
                <strong>Benzene (Aromatic)</strong>
                <code>C1=CC=CC=C1</code>
              </div>
              <div className="example-item">
                <strong>Ethylene (π-system)</strong>
                <code>C=C</code>
              </div>
              <div className="example-item">
                <strong>Formaldehyde (Carbonyl)</strong>
                <code>C=O</code>
              </div>
            </div>
          </div>

          <div className="notes">
            <strong>Advanced Features:</strong> VQE ground state calculations, EOM excited states, Trotterized time evolution, phase estimation spectroscopy, error mitigation, and quantum confidence scoring.
          </div>
        </section>
      </main>
    </div>
  );
}
