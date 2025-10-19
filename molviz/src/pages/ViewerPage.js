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
        <h2>Load Structure</h2>
        <input type="file" accept=".pdb,.ent,.txt,.cif,.mmcif" onChange={handleFile} />
        <p>or paste structure file content below (PDB or CIF/mmCIF)</p>
        <textarea
          value={pdbText}
          onChange={(e) => setPdbText(e.target.value)}
          placeholder="Paste PDB or mmCIF content here"
        />
        <div className="buttons">
          <button onClick={() => {
            const content = pdbText;
            const name = fileName;
            // basic format detection by filename or content
            function detectFormat(name, text) {
              if (name) {
                const ext = name.split('.').pop().toLowerCase();
                if (ext === 'cif' || ext === 'mmcif') return 'cif';
                if (ext === 'pdb' || ext === 'ent' || ext === 'txt') return 'pdb';
              }
              const t = (text || '').trim();
              if (!t) return 'pdb';
              if (t.startsWith('data_') || t.includes('_atom_site.')) return 'cif';
              if (t.split('\n')[0].startsWith('HEADER') || t.includes('ATOM') || t.includes('HETATM')) return 'pdb';
              return 'pdb';
            }

            const format = detectFormat(name, content);
            window.dispatchEvent(new CustomEvent('loadStructure', { detail: { content, name, format } }));
          }}>
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
        <div className="representation-select">
          <label htmlFor="representation">Representation:</label>
          <select
            id="representation"
            onChange={(e) => {
              window.dispatchEvent(
                new CustomEvent('changeRepresentation', { detail: e.target.value })
              );
            }}
          >
            <option value="cartoon">Cartoon</option>
            <option value="stick">Stick</option>
            <option value="ballstick">Ball and Stick</option>
            <option value="surface">Surface</option>
            <option value="sphere">Sphere (CPK)</option>
            <option value="line">Line</option>
          </select>
        </div>
      </aside>

      <section className="viewer-area">
        <MoleculeViewer />
      </section>
    </div>
  );
}
