import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

export default function Home() {
  return (
    <div className="home-container">
      <div className="hero">
        <div className="hero-inner">
          <h1 className="title">MolViz</h1>
          <p className="subtitle">Interactive 3D molecular visualization — load PDB files and explore structures with ease.</p>
          <div className="hero-cta">
            <Link className="cta-button" to="/viewer">Open Molecule Viewer</Link>
            <a className="cta-outline" href="https://3dmol.org/" target="_blank" rel="noreferrer">About 3Dmol.js</a>
          </div>
        </div>
      </div>

      <main className="content">
        <section className="cards">
          <article className="card">
            <div className="card-icon">🔬</div>
            <h3>Quick load</h3>
            <p>Upload a PDB file or paste PDB text and render the structure instantly.</p>
          </article>

          <article className="card">
            <div className="card-icon">🎨</div>
            <h3>Flexible styles</h3>
            <p>View protein cartoons, sticks, surfaces and switch color schemes for clarity.</p>
          </article>

          <article className="card">
            <div className="card-icon">⚡</div>
            <h3>Fast & lightweight</h3>
            <p>Uses the efficient 3Dmol.js viewer for responsive interaction even on large molecules.</p>
          </article>
        </section>

        <section className="instructions">
          <h2>Get started</h2>
          <ol>
            <li>Click "Open Molecule Viewer" or go to the Viewer page.</li>
            <li>Upload your PDB file or paste its text in the input area.</li>
            <li>Click Load to render and interact with the structure.</li>
          </ol>

          <div className="notes">
            <strong>Tip:</strong> Try a small PDB (e.g. <em>1crn</em>) first to familiarize yourself with navigation (drag, scroll to zoom).
          </div>
        </section>
      </main>
    </div>
  );
}
