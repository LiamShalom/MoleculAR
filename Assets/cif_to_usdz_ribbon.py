import sys
import math
import os
import gemmi
from pxr import Usd, UsdGeom, Gf, UsdUtils

if len(sys.argv) != 3:
    print("Usage: python3 cif_to_usdz_ribbon.py input.cif output.usdz")
    sys.exit(1)

input_cif, output_usdz = sys.argv[1], sys.argv[2]
temp_usd = output_usdz.replace(".usdz", ".usd")

# === Load the structure ===
doc = gemmi.cif.read_file(input_cif)
structure = gemmi.make_structure_from_block(doc.sole_block())

# === Create temporary USD stage ===
stage = Usd.Stage.CreateNew(temp_usd)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
root = UsdGeom.Xform.Define(stage, "/Molecule")

# === Extract CA trace ===
for model in structure:
    for chain in model:
        ca_points = []
        for residue in chain:
            try:
                atom = residue.find_atom("CA", "")  # altloc empty string required
                pos = atom.pos
                ca_points.append(Gf.Vec3f(pos.x, pos.y, pos.z))
            except Exception:
                continue

        if len(ca_points) < 2:
            continue

        # === Create smooth ribbon ===
        curve_path = f"/Molecule/Chain_{chain.name}"
        curve = UsdGeom.BasisCurves.Define(stage, curve_path)
        curve.CreatePointsAttr(ca_points)
        curve.CreateCurveVertexCountsAttr([len(ca_points)])
        curve.CreateTypeAttr("cubic")
        curve.CreateWrapAttr("nonperiodic")
        curve.CreateWidthsAttr([0.8])
        curve.CreateDisplayColorAttr([Gf.Vec3f(0.2, 0.6, 1.0)])  # blue ribbons

stage.GetRootLayer().Save()

# === Convert to USDZ ===
print(f"📦 Converting {temp_usd} → {output_usdz} ...")
UsdUtils.CreateNewARKitUsdzPackage(temp_usd, output_usdz)
os.remove(temp_usd)

print(f"✅ Saved ribbon model as {output_usdz}")

