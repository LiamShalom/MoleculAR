import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
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

  useEffect(() => {
    // Wait until the 3Dmol script is loaded and viewers are initialized
    const timeout = setTimeout(() => {
      if (window.$3Dmol && window.$3Dmol.viewers) {
        const viewers = Object.values(window.$3Dmol.viewers);
        if (viewers.length > 0) {
          setInterval(() => {
            viewers.forEach((v, i) => {
              v.rotate(1);
              v.setClickable(false);
              if (i === 0) v.setZoomLimits(100, 100);   // 1CRN closer
              else if (i === 1) v.setZoomLimits(250, 250); // 4HHB medium
              else v.setZoomLimits(150, 150);
            });
          }, 50);
        }
      }
    }, 500); // wait ~0.5 seconds for auto-render to finish

    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="home-container">
      <div className="hero">
        <div className="hero-bg-anim" aria-hidden="true">
        </div>
        <div className="hero-inner">
          <h1 className="title">MolViz</h1>
          <p className="subtitle">Interactive 3D molecular visualization — load CIF or PDB files and explore molecular structures with ease.</p>
          <div className="hero-cta">
            <Link className="cta-button" to="/viewer">Open Molecule Viewer</Link>
            <a className="cta-outline" href="https://3dmol.org/" target="_blank" rel="noreferrer">About 3Dmol.js</a>
          </div>
        </div>
      </div>

      <main className="content">
        <section className="examples-section fade-in">
          <h2>Examples</h2>
          <div className="examples-row">
            {EXAMPLES.map(ex => (
              <div className="example-card" key={ex.name}>
                <div className="example-img-wrap">
                  <div
                    className="viewer_3Dmoljs"
                    style={{
                      width: '220px',
                      height: '220px',
                      position: 'relative',
                      borderRadius: '8px',
                    }}
                    data-pdb={ex.pdb}
                    data-backgroundcolor="0x000000"
                    data-style='{"cartoon":{"color":"spectrum"}}'
                    data-ui="false"
                  ></div>

                </div>
                <div className="example-label">{ex.name}</div>
                <div className="example-desc">{ex.desc}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="cards fade-in">
          <article className="card">
            <div className="card-icon card-anim">{/* animated icon */}
              <svg width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12" fill="#4ef0ff" opacity="0.2"><animate attributeName="r" values="12;14;12" dur="2s" repeatCount="indefinite" /></circle><circle cx="16" cy="16" r="6" fill="#4ef0ff" opacity="0.5"><animate attributeName="r" values="6;8;6" dur="2s" repeatCount="indefinite" /></circle></svg>
            </div>
            <h3>Quick load</h3>
            <p>Upload or paste a CIF or PDB file and render the structure instantly.</p>
          </article>

          <article className="card">
            <div className="card-icon card-anim">
              <svg width="32" height="32" viewBox="0 0 32 32"><rect x="8" y="8" width="16" height="16" rx="8" fill="#9b5cff" opacity="0.2"><animate attributeName="rx" values="8;12;8" dur="2s" repeatCount="indefinite" /></rect></svg>
            </div>
            <h3>Flexible styles</h3>
            <p>View protein cartoons, sticks, surfaces and switch representations for clarity.</p>
          </article>

          <article className="card">
            <div className="card-icon card-anim">
              <svg width="32" height="32" viewBox="0 0 32 32"><polygon points="16,4 28,28 4,28" fill="#4ef0ff" opacity="0.2"><animate attributeName="points" values="16,4 28,28 4,28;16,8 28,24 4,24;16,4 28,28 4,28" dur="2s" repeatCount="indefinite" /></polygon></svg>
            </div>
            <h3>Fast & lightweight</h3>
            <p>Uses the efficient 3Dmol.js viewer for responsive interaction even on large molecules.</p>
          </article>
        </section>

        <section className="instructions fade-in">
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
