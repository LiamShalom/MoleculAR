import React, { useEffect, useRef } from 'react';
import './MoleculeViewer.css';

export default function MoleculeViewer() {
  const containerRef = useRef(null);
  const viewerRef = useRef(null);
  const currentModelRef = useRef(null);

  // Apply representation styles to the viewer
  function applyRepresentation(viewer, type) {
    // clear current styles and surfaces
    viewer.setStyle({}, {});
    viewer.removeAllSurfaces();

    switch (type) {
      case "cartoon":
        viewer.setStyle({}, {
          cartoon: {
            color: "spectrum",   // rainbow by residue index
            opacity: 1.0,        // fully opaque
            thickness: 0.4       // controls ribbon thickness
          }
        });
        break;

      case "stick":
        viewer.setStyle({}, {
          stick: {
            colorscheme: "Jmol", // element colors
            radius: 0.2
          }
        });
        break;

      case "ballstick":
        viewer.setStyle({}, {
          stick: { radius: 0.15, colorscheme: "Jmol" },
          sphere: { scale: 0.3, colorscheme: "Jmol" }
        });
        break;

      case "sphere":
        viewer.setStyle({}, {
          sphere: {
            scale: 1.0,           // 1.0 = true CPK size, larger values exaggerate radius
            colorscheme: "Jmol",  // standard element colors
            opacity: 1.0
          }
        });
        break;

      case "surface":
        viewer.mapAtomProperties(window.$3Dmol.applyPartialCharges);

        // Get all atoms to detect chains dynamically
        const atoms = viewer.selectedAtoms({});
        const chains = [...new Set(atoms.map(a => a.chain))];

        // Base molecular style
        viewer.setStyle({}, { cartoon: { color: 'spectrum' } });

        // Add chain-based surfaces dynamically
        chains.forEach((chain, i) => {
          const colorSchemes = ['RWB', 'greenCarbon', 'Jmol', 'whiteCarbon'];
          const scheme = colorSchemes[i % colorSchemes.length];

          viewer.addSurface(
            window.$3Dmol.SurfaceType.SAS,
            { opacity: 1, colorscheme: scheme },
            { chain }
          );
        });
        break;

      case "line":
        viewer.setStyle({}, {
          line: {
            linewidth: 1.5,
            color: "white"
          }
        });
        break;

      case "cross":
        viewer.setStyle({}, {
          cross: {
            radius: 0.5,
            color: "white"
          }
        });
        break;

      default:
        viewer.setStyle({}, { cartoon: { color: "spectrum" } });
    }

    viewer.render();
  };

  useEffect(() => {
    // Wait for 3Dmol to be available on window
    function ensureViewer() {
      if (!window.$3Dmol) return false;
      if (!containerRef.current) return false;
      // create viewer
      viewerRef.current = window.$3Dmol.createViewer(containerRef.current, {
        defaultcolors: window.$3Dmol.rasmolElementColors,
        backgroundColor: "black",
      });
      return true;
    }

    if (!ensureViewer()) {
      const onLoad = () => ensureViewer();
      window.addEventListener('load', onLoad);
      return () => window.removeEventListener('load', onLoad);
    }

    // Event listeners for loading structures (PDB and CIF)
    function loadStructure(content, format) {
      const v = viewerRef.current;
      if (!v) return;
      v.clear();
      try {
        // 3Dmol supports 'pdb' and 'mmcif'/'cif' in addModel
        const fmt = (format === 'cif') ? 'mmcif' : 'pdb';
        const model = v.addModel(content, fmt);
        currentModelRef.current = { model, content, format: fmt };
        v.setBackgroundColor(0x000000);
        applyRepresentation(v, 'cartoon');
        v.zoomTo();
        v.render();
      } catch (err) {
        console.error('failed to load structure', err);
      }
    }

    function onClear() {
      const v = viewerRef.current;
      if (!v) return;
      v.clear();
      currentModelRef.current = null;
      v.render();
    }

    function onChangeRepresentation(e) {
      const representation = e.detail;
      const v = viewerRef.current;
      const current = currentModelRef.current;

      if (!v || !current || !representation) return;

      try {
        v.clear();
        const model = v.addModel(current.content, current.format);
        currentModelRef.current = { ...current, model };
        v.setBackgroundColor(0x000000);
        applyRepresentation(v, representation);
        v.render();
      } catch (err) {
        console.error('failed to update representation', err);
      }
    }

    // backward compatible listener (older code used loadPDB)
    function onLoadPDB(e) {
      const { pdb } = e.detail || {};
      if (!pdb) return;
      loadStructure(pdb, 'pdb');
    }

    function onLoadStructure(e) {
      const { content, format } = e.detail || {};
      if (!content) return;
      loadStructure(content, format || 'pdb');
    }

    window.addEventListener('loadPDB', onLoadPDB);
    window.addEventListener('loadStructure', onLoadStructure);
    window.addEventListener('clearPDB', onClear);
    window.addEventListener('changeRepresentation', onChangeRepresentation);

    return () => {
      window.removeEventListener('loadPDB', onLoadPDB);
      window.removeEventListener('loadStructure', onLoadStructure);
      window.removeEventListener('clearPDB', onClear);
      window.removeEventListener('changeRepresentation', onChangeRepresentation);
    };
  }, []);

  return (
    <div className="molecule-viewer-root">
      <div ref={containerRef} className="molecule-canvas" />
      <div className="hint">Drag to rotate, scroll to zoom</div>
    </div>
  );
}
