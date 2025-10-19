import React, { useState } from 'react';
import MoleculeViewer from '../viewer/MoleculeViewer';
import './ViewerPage.css';

export default function ViewerPage() {
  const [pdbText, setPdbText] = useState('');
  const [fileName, setFileName] = useState('');

  function handleFile(e) {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    setFileName(f.name);
    const reader = new FileReader();
    reader.onload = (ev) => setPdbText(ev.target.result);
    reader.readAsText(f);
  }

  return (
    <div className="viewer-page">
      <aside className="controls">
        <h2>Load PDB</h2>
        <input type="file" accept=".pdb,.ent,.txt" onChange={handleFile} />
        <p>or paste PDB text below</p>
        <textarea
          value={pdbText}
          onChange={(e) => setPdbText(e.target.value)}
          placeholder="Paste PDB content here"
        />
        <div className="buttons">
          <button onClick={() => window.dispatchEvent(new CustomEvent('loadPDB', { detail: { pdb: pdbText, name: fileName } }))}>
            Load
          </button>
          <button onClick={() => {
            setPdbText('');
            setFileName('');
            window.dispatchEvent(new CustomEvent('clearPDB'));
          }}>
            Clear
          </button>
        </div>
      </aside>

      <section className="viewer-area">
        <MoleculeViewer />
      </section>
    </div>
  );
}
