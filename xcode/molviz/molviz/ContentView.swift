//
//  ContentView.swift
//  molviz
//
//  Created by Swaraag Sistla on 10/18/25.
//

import SwiftUI
import UniformTypeIdentifiers

struct ContentView: View {
    @State private var showFilePicker = false
    @State private var selectedFileURL: URL?
    @State private var errorMessage: String?
    
    var body: some View {
        VStack {
            if let fileURL = selectedFileURL {
                MoleculeView(modelURL: fileURL)
                    .toolbar {
                        ToolbarItem(placement: .bottomOrnament) {
                            Button("Load Different Molecule") {
                                showFilePicker = true
                            }
                        }
                    }
            } else {
                // Welcome screen
                VStack(spacing: 30) {
                    Text("🧬 Molecule Viewer")
                        .font(.extraLargeTitle)
                    
                    Text("Load a USDZ molecule to begin")
                        .font(.title2)
                        .foregroundStyle(.secondary)
                    
                    Button {
                        showFilePicker = true
                    } label: {
                        Label("Load USDZ File", systemImage: "doc.badge.plus")
                    }
                    .buttonStyle(.borderedProminent)
                    
                    Button {
                        loadBundledMolecule()
                    } label: {
                        Label("Load Sample Molecule", systemImage: "flask")
                    }
                    .buttonStyle(.bordered)
                    
                    if let error = errorMessage {
                        Text(error)
                            .foregroundColor(.red)
                            .font(.caption)
                    }
                }
                .padding()
            }
        }
        .fileImporter(
            isPresented: $showFilePicker,
            allowedContentTypes: [.usdz],
            allowsMultipleSelection: false
        ) { result in
            handleFileImport(result)
        }
    }
    
    private func handleFileImport(_ result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            guard let url = urls.first else { return }
            
            // Start accessing security-scoped resource
            guard url.startAccessingSecurityScopedResource() else {
                errorMessage = "Cannot access file"
                return
            }
            
            selectedFileURL = url
            errorMessage = nil
            
            // Don't forget to stop accessing when done
            // url.stopAccessingSecurityScopedResource()
            
        case .failure(let error):
            errorMessage = "Failed to load: \(error.localizedDescription)"
        }
    }
    
    private func loadBundledMolecule() {
        if let url = Bundle.main.url(forResource: "toy_drummer", withExtension: "usdz") {
            selectedFileURL = url
            errorMessage = nil
        } else {
            errorMessage = "Sample molecule not found in bundle"
            
            // Debug: Print all files in bundle
            if let bundlePath = Bundle.main.resourcePath {
                let files = try? FileManager.default.contentsOfDirectory(atPath: bundlePath)
                print("Files in bundle: \(files ?? [])")
            }
        }
    }
}

#Preview(windowStyle: .volumetric) {
    ContentView()
}
