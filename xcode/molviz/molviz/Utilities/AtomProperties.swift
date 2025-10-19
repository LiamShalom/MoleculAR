//
//  AtomProperties.swift
//  molviz
//
//  Created by Swaraag Sistla on 10/18/25.
//

import UIKit

struct AtomProperties {
    // CPK coloring scheme
    static func color(for element: String) -> UIColor {
        switch element.uppercased() {
        case "C": return .gray
        case "O": return .red
        case "N": return .blue
        case "H": return .white
        case "S": return .yellow
        case "P": return .orange
        case "CL", "Cl": return .green
        case "F": return UIColor(red: 0.56, green: 0.88, blue: 0.31, alpha: 1.0)
        case "BR", "Br": return UIColor(red: 0.65, green: 0.16, blue: 0.16, alpha: 1.0)
        case "I": return UIColor(red: 0.58, green: 0.0, blue: 0.58, alpha: 1.0)
        case "FE", "Fe": return UIColor(red: 0.88, green: 0.4, blue: 0.2, alpha: 1.0)
        case "CA", "Ca": return UIColor(red: 0.24, green: 1.0, blue: 0.0, alpha: 1.0)
        default: return .purple
        }
    }
    
    // Van der Waals radii (in Angstroms, scaled for visualization)
    static func radius(for element: String) -> Float {
        switch element.uppercased() {
        case "H": return 0.25
        case "C": return 0.4
        case "N": return 0.35
        case "O": return 0.35
        case "S": return 0.5
        case "P": return 0.45
        case "CL", "Cl": return 0.45
        case "F": return 0.3
        case "BR", "Br": return 0.5
        case "I": return 0.55
        default: return 0.4
        }
    }
}
