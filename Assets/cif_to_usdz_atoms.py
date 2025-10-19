#!/usr/bin/env python3
import gemmi
from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf, UsdUtils
import re
import sys
import os

# === Usage ===
if len(sys.argv) != 3:
    print("Usage: python cif_to_usdz.py input.cif output.usdz")
    sys.exit(1)

input_cif = sys.argv[1]
output_usdz = sys.argv[2]
tmp_usda = "temp.usda"

# === Load CIF structure ===
doc = gemmi.cif.read_file(input_cif)
block = doc.sole_block()
structure = gemmi.make_structure_from_block(block)
structure.remove_hydrogens()

# === Create USD stage ===
stage = Usd.Stage.CreateNew(tmp_usda)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# === Create root transform ===
root = UsdGeom.Xform.Define(stage, "/Molecule")
stage.SetDefaultPrim(root.GetPrim())

# === Atom color map ===
element_colors = {
    "C": (0.3, 0.3, 0.3),
    "O": (1.0, 0.0, 0.0),
    "N": (0.0, 0.0, 1.0),
    "H": (1.0, 1.0, 1.0),
    "S": (1.0, 1.0, 0.0),
    "P": (1.0, 0.5, 0.0),
}

# === Create spheres for atoms ===
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                pos = atom.pos
                color = element_colors.get(atom.element.name, (0.5, 0.5, 0.5))

                # Clean name for valid USD paths
                atom_name = re.sub(r'[^A-Za-z0-9_]', '_', atom.name)
                sphere_path = f"/Molecule/{atom_name}_{atom.serial}"

                sphere = UsdGeom.Sphere.Define(stage, sphere_path)
                sphere.AddTranslateOp().Set(Gf.Vec3f(pos.x, pos.y, pos.z))
                sphere.GetRadiusAttr().Set(0.5)

                # --- Material setup ---
                shader_path = f"/Molecule/Shader_{atom_name}_{atom.serial}"
                material_path = f"/Molecule/Material_{atom_name}_{atom.serial}"

                shader = UsdShade.Shader.Define(stage, shader_path)
                shader.CreateIdAttr("UsdPreviewSurface")
                shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
                shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
                shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)  # define shader output

                material = UsdShade.Material.Define(stage, material_path)
                material.CreateSurfaceOutput().ConnectToSource(shader.GetOutput("surface"))

                # Bind material to sphere
                UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(material)

# === Save and package ===
stage.GetRootLayer().Save()
UsdUtils.CreateNewUsdzPackage(tmp_usda, output_usdz)
os.remove(tmp_usda)

print(f"✅ Successfully converted {input_cif} → {output_usdz}")

