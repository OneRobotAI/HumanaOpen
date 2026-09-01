# Hardware

The mechanical / electrical / printable design files for HumanaOpen.

## Directory layout

| Path | Contents |
|------|----------|
| [`BOM/`](BOM/bom.md) | Bill of Materials — every part needed to build the robot, with specs, quantity, and sourcing. |
| [`assembly/`](assembly/assembly.md) | Step-by-step build instructions (subsystems: arms, head, lift, base, electronics). |
| [`cad/`](cad/) | CAD source files. |
| `cad/fusion360/` | Fusion 360 source design files (`.f3d`). |
| `cad/step/` | STEP file exports (`.step`/`.stp`, open, importable anywhere). |
| [`stl/`](stl/) | Ready-to-print 3D printing files (`.stl`). |
| [`urdf/`](urdf/) | Robot description (`.urdf` / `.xacro`) for RViz / Gazebo / simulation. |
| `urdf/meshes/` | Mesh files referenced by the URDF (may reuse the STL meshes). |
| [`electronics/`](electronics/wiring.md) | Wiring / electronics layout and power notes. |

## Conventions

- **Units**: STL/STEP are in millimetres (mm).
- **URDF**: inertial properties should be filled from the CAD export so
  simulation matches the physical robot.
- Keep every exported STEP/STL in sync with the Fusion 360 source: re-export
  after any design change and note the revision in the file name or this README.
