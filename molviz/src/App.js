import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import ViewerPage from './pages/ViewerPage';
import QuantumAnalysisPage from './pages/QuantumAnalysisPage';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <nav className="nav">
          <Link to="/">Home</Link>
          <Link to="/viewer">Molecule Viewer</Link>
          {/* <Link to="/quantum">Quantum Chemistry</Link> */}
        </nav>
        <main className="main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/viewer" element={<ViewerPage />} />
            {/* <Route path="/quantum" element={<QuantumAnalysisPage />} /> */}
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
