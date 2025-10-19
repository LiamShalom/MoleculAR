import SwiftUI
import RealityKit

struct MoleculeView: View {
    let modelURL: URL?
    @State private var moleculeEntity: Entity?
    @State private var scale: Float = 1.0
    
    var body: some View {
        RealityView { content in
            await loadMolecule(into: content)
        }
        .gesture(
            RotateGesture3D()
                .onChanged { value in
                    if let entity = moleculeEntity {
                        entity.orientation = entity.orientation * simd_quatf(value.rotation)
                    }
                }
        )        .gesture(
            MagnifyGesture()
                .onChanged { value in
                    let newScale = scale * Float(value.magnification)
                    moleculeEntity?.scale = SIMD3(repeating: newScale)
                }
                .onEnded { value in
                    scale *= Float(value.magnification)
                }
        )
        .gesture(
            DragGesture()
                .onChanged { value in
                    if let entity = moleculeEntity {
                        // Convert drag translation to 3D movement
                        let translation = value.translation
                        entity.position.x += Float(translation.width) * 0.001
                        entity.position.y -= Float(translation.height) * 0.001
                    }
                }
        )
        .gesture(
            SpatialTapGesture()
                .targetedToAnyEntity()
                .onEnded { value in
                    highlightEntity(value.entity)
                }
        )
    }
    
    @MainActor
    private func loadMolecule(into content: RealityViewContent) async {
        guard let url = modelURL else { return }
        
        do {
            let entity = try await Entity(contentsOf: url)
            
            // Scale down if needed
            entity.scale = SIMD3(repeating: 0.01)
            
            moleculeEntity = entity
            content.add(entity)
            
            // Add lighting
            let light = DirectionalLight()
            light.light.intensity = 5000
            light.position = [0, 2, 0]
            content.add(light)
            
            let ambientLight = PointLight()
            ambientLight.light.intensity = 2000
            content.add(ambientLight)
            
        } catch {
            print("Failed to load model: \(error)")
        }
    }
    
    private func highlightEntity(_ entity: Entity) {
        guard let modelEntity = entity as? ModelEntity else { return }
        
        // Create physical material instead of SimpleMaterial
        var material = PhysicallyBasedMaterial()
        material.baseColor = .init(tint: .yellow)
        material.emissiveColor = .init(color: .yellow)
        material.emissiveIntensity = 3.0
        
        modelEntity.model?.materials = [material]
        
        print("Selected: \(entity.name)")
    }
}
