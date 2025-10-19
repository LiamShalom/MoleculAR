import React from 'react';
import './Home.css';

export default function Home() {
  return (
    <div className="home">
      <h1>MolViz</h1>
      <p>
        MolViz is a lightweight React app for visualizing molecular structures from
        PDB files. Use the Molecule Viewer page to upload a PDB file or paste PDB
        text and explore the structure in 3D.
      </p>

      <section>
        <h2>How to use</h2>
        <ol>
          <li>Go to the "Molecule Viewer" page.</li>
          <li>Upload a .pdb file or paste PDB formatted text.</li>
          <li>Click "Load" to render the molecule.</li>
          <li>Use your mouse to rotate, zoom, and pan.</li>
        </ol>
      </section>

      <section>
        <h2>Notes</h2>
        <ul>
          <li>This demo uses 3Dmol.js (loaded from CDN).</li>
          <li>Large PDB files may take longer to render.</li>
        </ul>
      </section>
    </div>
  );
}
