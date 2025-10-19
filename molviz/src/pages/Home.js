import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Home.css';

// Example images (replace with your own or use public domain PDB images)
const EXAMPLES = [
  {
    name: '1CRN',
    img: 'https://cdn.rcsb.org/images/structures/1crn_assembly-1.jpeg',
    desc: 'Crambin (small protein)',
    pdb: '1CRN',
    link: 'https://www.rcsb.org/structure/1CRN',
  },
  {
    name: '4HHB',
    img: 'https://cdn.rcsb.org/images/structures/4hhb_assembly-1.jpeg',
    desc: 'Hemoglobin',
    pdb: '4HHB',
    link: 'https://www.rcsb.org/structure/4HHB',
  },
  {
    name: '1BNA',
    img: 'https://cdn.rcsb.org/images/structures/1bna_assembly-1.jpeg',
    desc: 'DNA Dodecamer',
    pdb: '1BNA',
    link: 'https://www.rcsb.org/structure/1BNA',
  },
];

export default function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    // Re-initialize 3Dmol.js viewers on every mount
    if (window.$3Dmol) {
      document.querySelectorAll('.viewer_3Dmoljs').forEach((el, i) => {
        // Remove previous viewer if exists
        if (el.viewer) {
          el.viewer.clear();
          el.viewer = null;
        }
        // Create new viewer
        el.viewer = window.$3Dmol.createViewer(el, {
          defaultcolors: window.$3Dmol.rasmolElementColors,
          backgroundColor: 0x000000,
        });
        const pdb = el.getAttribute('data-pdb');
        if (pdb) {
          window.$3Dmol.download("pdb:" + pdb, el.viewer, {}, function() {
            el.viewer.setStyle({}, { cartoon: { color: "spectrum" } });
            el.viewer.setBackgroundColor(0x000000);
            el.viewer.zoomTo();
            el.viewer.render();
            el.viewer.setClickable(false);
            // Set zoom limits for each example
            if (i === 0) el.viewer.setZoomLimits(100, 100);
            else if (i === 1) el.viewer.setZoomLimits(250, 250);
            else el.viewer.setZoomLimits(150, 150);
            // Auto-rotate
            if (el._rotateInterval) clearInterval(el._rotateInterval);
            el._rotateInterval = setInterval(() => {
              el.viewer.rotate(1);
            }, 50);
          });
        }
      });
    }
    // Cleanup intervals on unmount
    return () => {
      document.querySelectorAll('.viewer_3Dmoljs').forEach(el => {
        if (el._rotateInterval) clearInterval(el._rotateInterval);
      });
    };
  }); // runs on every mount

  const handleExampleClick = async (pdb) => {
    try {
      const cifUrl = `/example_cifs/${pdb}.cif`;
      const res = await fetch(cifUrl);
      const text = await res.text();
      navigate('/viewer', { state: { cifText: text, fileName: `${pdb}.cif` } });
    } catch (e) {
      alert('Failed to load CIF example.');
      navigate('/viewer');
    }
  };

  return (
    <div className="home-container">
      <div className="hero">
        <div className="hero-bg-anim" aria-hidden="true">
        </div>
        <div className="hero-inner">
          <h1 className="title">MolViz</h1>
          <p className="subtitle">Interactive 3D molecular visualization — load PDB files and explore structures with ease.</p>
          <div className="hero-cta">
            <Link className="cta-button primary" to="/quantum">Quantum Chemistry</Link>
            <Link className="cta-button secondary" to="/analysis">AI Analysis</Link>
            <Link className="cta-button tertiary" to="/viewer">3D Viewer</Link>
            <a className="cta-outline" href="https://3dmol.org/" target="_blank" rel="noreferrer">About 3Dmol.js</a>
          </div>
        </div>
      </div>
      <div className="examples-row">
        {EXAMPLES.map(ex => (
          <div className="example-card" key={ex.name} onClick={() => handleExampleClick(ex.pdb)} style={{cursor: 'pointer'}}>
            <div className="example-img-wrap">
              <div
                className="viewer_3Dmoljs"
                style={{
                  width: '250px',
                  height: '250px',
                  position: 'relative',
                  borderRadius: '8px',
                }}
                data-pdb={ex.pdb}
                data-backgroundcolor="0x000000"
                data-style='{"cartoon":{"color":"spectrum"}}'
              ></div>
            </div>
            <div className="example-label">{ex.name}</div>
            <div className="example-desc">{ex.desc}</div>
          </div>
        ))}
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
