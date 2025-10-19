import React, { useEffect, useRef } from 'react';
import './MoleculeViewer.css';

export default function MoleculeViewer() {
  const containerRef = useRef(null);
  const viewerRef = useRef(null);

  useEffect(() => {
    // Wait for 3Dmol to be available on window
    function ensureViewer() {
      if (!window.$3Dmol) return false;
      if (!containerRef.current) return false;
      // create viewer
      viewerRef.current = window.$3Dmol.createViewer(containerRef.current, {
        defaultcolors: window.$3Dmol.rasmolElementColors,
      });
      return true;
    }

    if (!ensureViewer()) {
      const onLoad = () => ensureViewer();
      window.addEventListener('load', onLoad);
      return () => window.removeEventListener('load', onLoad);
    }

    // Event listeners for load/clear
    function onLoadPDB(e) {
      const { pdb } = e.detail || {};
      if (!pdb) return;
      const v = viewerRef.current;
      v.clear();
      try {
        v.addModel(pdb, 'pdb');
        v.setStyle({}, { cartoon: { color: 'spectrum' }, stick: {} });
        v.zoomTo();
        v.render();
      } catch (err) {
        console.error('failed to load pdb', err);
      }
    }

    function onClear() {
      const v = viewerRef.current;
      if (!v) return;
      v.clear();
      v.render();
    }

    window.addEventListener('loadPDB', onLoadPDB);
    window.addEventListener('clearPDB', onClear);

    return () => {
      window.removeEventListener('loadPDB', onLoadPDB);
      window.removeEventListener('clearPDB', onClear);
    };
  }, []);

  return (
    <div className="molecule-viewer-root">
      <div ref={containerRef} className="molecule-canvas" />
      <div className="hint">Drag to rotate, scroll to zoom</div>
    </div>
  );
}
