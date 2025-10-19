//
//  PDBParser.swift
//  molviz
//
//  Created by Swaraag Sistla on 10/18/25.
//

import Foundation

struct Atom {
    let element: String
    let position: SIMD3<Float>
    let index: Int
}

struct Bond {
    let atom1: Int
    let atom2: Int
}

struct Molecule {
    let atoms: [Atom]
    let bonds: [Bond]
}

class PDBParser {
    static func parse(_ fileURL: URL) -> Molecule {
        guard let content = try? String(contentsOf: fileURL, encoding: .utf8) else {
            print("❌ Failed to read PDB file")
            return Molecule(atoms: [], bonds: [])
        }
        
        var atoms: [Atom] = []
        var bonds: [Bond] = []
        
        content.enumerateLines { line, _ in
            // Parse ATOM/HETATM lines
            if line.starts(with: "ATOM") || line.starts(with: "HETATM") {
                guard line.count >= 54 else { return }
                
                // Element (columns 77-78, or derive from atom name)
                var element = ""
                if line.count >= 78 {
                    let start = line.index(line.startIndex, offsetBy: 76)
                    let end = line.index(start, offsetBy: min(2, line.count - 76))
                    element = String(line[start..<end]).trimmingCharacters(in: .whitespaces)
                }
                
                // Fallback: get element from atom name (columns 13-16)
                if element.isEmpty && line.count >= 16 {
                    let nameStart = line.index(line.startIndex, offsetBy: 12)
                    let nameEnd = line.index(nameStart, offsetBy: 4)
                    let atomName = String(line[nameStart..<nameEnd]).trimmingCharacters(in: .whitespaces)
                    element = String(atomName.prefix(1)) // First char usually element
                }
                
                // X coordinate (columns 31-38)
                let xStart = line.index(line.startIndex, offsetBy: 30)
                let xEnd = line.index(xStart, offsetBy: 8)
                let x = Float(String(line[xStart..<xEnd]).trimmingCharacters(in: .whitespaces)) ?? 0
                
                // Y coordinate (columns 39-46)
                let yStart = line.index(line.startIndex, offsetBy: 38)
                let yEnd = line.index(yStart, offsetBy: 8)
                let y = Float(String(line[yStart..<yEnd]).trimmingCharacters(in: .whitespaces)) ?? 0
                
                // Z coordinate (columns 47-54)
                let zStart = line.index(line.startIndex, offsetBy: 46)
                let zEnd = line.index(zStart, offsetBy: 8)
                let z = Float(String(line[zStart..<zEnd]).trimmingCharacters(in: .whitespaces)) ?? 0
                
                atoms.append(Atom(
                    element: element.isEmpty ? "C" : element,
                    position: SIMD3(x, y, z),
                    index: atoms.count
                ))
            }
            // Parse CONECT lines (bond connectivity)
            else if line.starts(with: "CONECT") {
                let parts = line.split(separator: " ").compactMap { Int($0) }
                if parts.count >= 2 {
                    let sourceAtom = parts[0] - 1 // PDB is 1-indexed
                    for i in 1..<parts.count {
                        let targetAtom = parts[i] - 1
                        // Avoid duplicate bonds
                        if sourceAtom < targetAtom && sourceAtom >= 0 && targetAtom < atoms.count {
                            bonds.append(Bond(atom1: sourceAtom, atom2: targetAtom))
                        }
                    }
                }
            }
        }
        
        print("✅ Parsed \(atoms.count) atoms and \(bonds.count) bonds")
        return Molecule(atoms: atoms, bonds: bonds)
    }
}
