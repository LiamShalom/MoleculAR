#!/usr/bin/env python3
import gemmi
from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf, UsdUtils
import math, sys, os

# === Usage ===
if len(sys.argv) != 3:
    print("Usage: python3 cif_to_usdz_stick.py input.cif output.usdz")
    sys.exit(1)

input_cif = sys.argv[1]
output_usdz = sys.argv[2]
tmp_usda = "temp_stick.usda"

# === Load CIF structure ===
doc = gemmi.cif.read_file(input_cif)
block = doc.sole_block()
structure = gemmi.make_structure_from_block(block)
structure.remove_hydrogens()

# === USD stage ===
stage = Usd.Stage.CreateNew(tmp_usda)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
root = UsdGeom.Xform.Define(stage, "/Molecule")
stage.SetDefaultPrim(root.GetPrim())

# === Element colors ===
element_colors = {
    "H": (1.0, 1.0, 1.0),
    "C": (0.3, 0.3, 0.3),
    "N": (0.1, 0.1, 1.0),
    "O": (1.0, 0.0, 0.0),
    "S": (1.0, 1.0, 0.0),
    "P": (1.0, 0.5, 0.0),
    "Cl": (0.0, 1.0, 0.0),
    "F": (0.0, 1.0, 0.0),
    "Br": (0.6, 0.2, 0.1),
    "I": (0.5, 0.0, 0.6),
}

# === Covalent radii (for bond estimation) ===
covalent_radii = {
    "H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
    "P": 1.07, "S": 1.05, "Cl": 1.02, "Br": 1.20, "I": 1.39
}

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)

# === Collect all atoms ===
atoms = []
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                atoms.append(atom)

# === Generate bonds as cylinders ===
bond_radius = 0.1
bond_count = 0

for i, atom1 in enumerate(atoms):
    for j, atom2 in enumerate(atoms[i+1:], i+1):
        e1, e2 = atom1.element.name, atom2.element.name
        if e1 not in covalent_radii or e2 not in covalent_radii:
            continue

        max_dist = covalent_radii[e1] + covalent_radii[e2] + 0.4
        dist = distance(atom1.pos, atom2.pos)
        if dist <= max_dist:
            bond_path = f"/Molecule/Bond_{bond_count}"
            bond_count += 1

            cyl = UsdGeom.Cylinder.Define(stage, bond_path)
            cyl.GetRadiusAttr().Set(bond_radius)
            cyl.GetHeightAttr().Set(dist)

            # Compute orientation to align bond between atoms
            p1 = Gf.Vec3d(atom1.pos.x, atom1.pos.y, atom1.pos.z)
            p2 = Gf.Vec3d(atom2.pos.x, atom2.pos.y, atom2.pos.z)
            mid = (p1 + p2) * 0.5
            dir_vec = (p2 - p1).GetNormalized()

            z_axis = Gf.Vec3d(0, 0, 1)
            axis = Gf.Cross(z_axis, dir_vec)
            axis_len = axis.GetLength()

            if axis_len > 1e-5:
                axis /= axis_len
                angle = math.acos(max(min(Gf.Dot(z_axis, dir_vec), 1.0), -1.0))
                rot = Gf.Rotation(axis, math.degrees(angle))
                rot_mtx = Gf.Matrix4d(rot, mid)
            else:
                rot_mtx = Gf.Matrix4d(1)
                rot_mtx.SetTranslate(mid)

            xform = UsdGeom.Xformable(cyl)
            xform.AddTransformOp().Set(rot_mtx)  # ✅ FIXED: Use Matrix4d directly

            # Create simple material for bond
            c1 = element_colors.get(e1, (0.5, 0.5, 0.5))
            c2 = element_colors.get(e2, (0.5, 0.5, 0.5))
            color = tuple((c1[k] + c2[k]) / 2 for k in range(3))

            shader_path = f"/Molecule/Shader_{bond_count}"
            mat_path = f"/Molecule/Mat_{bond_count}"

            shader = UsdShade.Shader.Define(stage, shader_path)
            shader.CreateIdAttr("UsdPreviewSurface")
            shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
            shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
            shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

            mat = UsdShade.Material.Define(stage, mat_path)
            mat.CreateSurfaceOutput().ConnectToSource(shader.GetOutput("surface"))
            UsdShade.MaterialBindingAPI(cyl.GetPrim()).Bind(mat)

# === Save and package ===
stage.GetRootLayer().Save()
UsdUtils.CreateNewUsdzPackage(tmp_usda, output_usdz)
os.remove(tmp_usda)

print(f"✅ Successfully converted {input_cif} → {output_usdz} (stick model, {bond_count} bonds)")

