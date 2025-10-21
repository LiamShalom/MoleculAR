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
    // Wait for 3Dmol script to load, then autoload all viewers
    const waitFor3Dmol = setInterval(() => {
      if (window.$3Dmol && window.$3Dmol.autoload) {
        clearInterval(waitFor3Dmol);

        // initialize all .viewer_3Dmoljs elements
        window.$3Dmol.autoload();

        // continuous rotation like on 3Dmol.org
        const rotateInterval = setInterval(() => {
          const viewers = Object.values(window.$3Dmol.viewers || {});
          viewers.forEach((v, i) => {
            v.rotate(1);
            if (i === 0) v.setZoomLimits(100, 100);
            else if (i === 1) v.setZoomLimits(250, 250);
            else v.setZoomLimits(150, 150);
          });
        }, 50);

        // cleanup rotation on unmount
        return () => clearInterval(rotateInterval);
      }
    }, 100);

    return () => clearInterval(waitFor3Dmol);
  }, []);

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
          <h1 className="title">MoleculAR</h1>
          <p className="subtitle">Interactive 3D molecular visualization to explore moleculer structures with ease.</p>
          <div className="hero-cta">
            <Link className="cta-button primary" to="/quantum">Quantum Chemistry</Link>
            <Link className="cta-button tertiary" to="/viewer">3D Viewer</Link>
            <a className="cta-outline" href="https://3dmol.org/" target="_blank" rel="noreferrer">About 3Dmol.js</a>
          </div>
        </div>
      </div>
      <div className="examples-row">
        {EXAMPLES.map(ex => (
          <div className="example-card" key={ex.name} onClick={() => handleExampleClick(ex.pdb)} style={{ cursor: 'pointer' }}>
            <div className="example-img-wrap">
              <div
                className="viewer_3Dmoljs"
                style={{
                  width: '250px',
                  height: '250px',
                  position: 'relative',
                  borderRadius: '8px',
                  backgroundColor: '#000',
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

        {/* <section className="instructions">


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
        </section> */}
      </main>
    </div>
  );
}
