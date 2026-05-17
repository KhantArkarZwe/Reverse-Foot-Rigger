# metaTools Reverse Foot Rigger

A Maya Python tool that creates a reverse foot rig setup using utility nodes, IK handles, foot pivots, and animator-facing attributes on a foot controller.

The tool was built to automate the node network for foot roll, banking, toe tap, toe sway, and heel sway after the main leg IK system already exists.


## Main Features

- Builds a reverse foot node network for foot roll and foot banking.
- Uses condition, multiplyDivide, and plusMinusAverage utility nodes.
- Creates SC IK handles for ball and toe joints.
- Parents the leg RP IK handle under the ankle pivot.
- Connects foot controller attributes to pivot rotations.
- Connects ball and toe IK joints to their bind joints.
- Validates pivot existence and hierarchy before connecting the setup.
- Validates required foot controller attributes.
- Prevents accidental use of the same IK and bind joints.

## Software / Environment

- Autodesk Maya 2025
- Python 3
- maya.cmds

## What This Tool Does

The tool connects an existing foot controller, existing IK foot joints, existing bind foot joints, an existing leg RP IK handle, and an existing reverse foot pivot hierarchy.

It creates:

- ball SC IK handle
- toe SC IK handle
- condition nodes
- multiplyDivide nodes
- plusMinusAverage nodes
- utility node connections
- pivot rotation connections
- parent constraints from foot IK joints to foot bind joints

## What This Tool Does Not Do

- It does not create the foot controller.
- It does not create the animator-facing attributes.
- It does not create the tuning attributes.
- It does not create or place the pivot nodes.
- It does not check whether pivot positions are anatomically correct.
- It does not build the full leg IK/FK system.
- It does not skin the mesh.
- It does not currently provide a cleanup/delete tool.

## How to Use

1. Open Maya.
2. Make sure the main leg IK setup already exists.
3. Make sure the reverse foot pivot hierarchy already exists.
4. Make sure the foot controller has all required attributes.
5. Open the script in the Script Editor or load it into Maya's Python environment.
6. Run:

```python
metaTools_ReverseFootRigger.openUI()
```

7. In the UI, fill in:
   - Limb Side: `L` or `R`
   - Foot Ctrl
   - Ankle IK joint
   - Ball IK joint
   - Toe IK joint
   - Ankle bind joint
   - Ball bind joint
   - Toe bind joint
   - Leg RP IK handle
8. Press **Build Reverse Foot Rig**.

## Required UI Inputs

| UI Field | Example |
|---|---|
| Limb Side | `L` |
| Foot Ctrl | `L_ankle_IK_ctrl` |
| Ankle IK | `L_ankle_IK` |
| Ball IK | `L_foot_IK` |
| Toe IK | `L_tiptoe_IK` |
| Ankle Bind | `L_ankle` |
| Ball Bind | `L_foot` |
| Toe Bind | `L_tiptoe` |
| Leg RP IK | `L_Leg_RP_ikHandle` |

Adjust these examples to match the final scene naming.

## Required Foot Controller Attributes

The foot controller must already have these attributes:

### Animator-facing attributes

| Attribute | Purpose |
|---|---|
| `Roll` | Main foot roll control |
| `Bank` | Foot banking control |
| `ToeSway` | Side-to-side toe/heel pivot movement from the heel pivot |
| `HeelSway` | Side-to-side heel/end pivot movement from the end pivot |
| `ToeTap` | Toe tap rotation |

### Setting / tuning attributes

| Attribute | Purpose |
|---|---|
| `RollBack` | Heel roll multiplier/control |
| `RollEnd` | Controls when the end pivot starts taking over |
| `ToeFlex` | Ball/toe flex amount |
| `ToeStraightAngle` | Angle threshold used by roll/tiptoe logic |
| `BankMultiplier` | Multiplier for banking strength |

`Roll` must have a value range of `-10` to `20`.

The script checks that all required attributes exist and are numeric.

## Required Pivot Hierarchy

The pivot nodes must already exist and must be parented in this order:

```text
L_root_pivot
└── L_heel_pivot
    └── L_inner_pivot
        └── L_outer_pivot
            └── L_end_pivot
                ├── L_ball_pivot
                │   └── L_ankle_pivot
                └── L_toe_pivot
```

Right side uses the same structure with `R_` prefix.

The script checks:

- all pivot nodes exist
- rotateX / rotateY / rotateZ are not locked
- pivot rotate channels do not already have incoming connections
- pivot hierarchy matches the expected hierarchy
- toe pivot is parented under the end pivot

## Generated Nodes

The tool creates these utility nodes with side prefixes.

### Condition nodes

```text
L_footRoll_ball_condition
L_footRoll_heel_condition
L_footRoll_end_condition
L_footRoll_clamp_condition
L_footRoll_tiptoe_condition
L_footBank_condition
```

### multiplyDivide nodes

```text
L_footRoll_multi
L_footRoll_ball_multi
L_footBank_multi
```

### plusMinusAverage nodes

```text
L_footRoll_pma
L_footRoll_ball_pma
L_footRoll_tiptoe_pma
```

### IK handles

```text
L_ball_ikHandle
L_toe_ikHandle
```

Right side uses `R_` instead.

The tool will stop if a generated node name already exists.

## Important Assumptions

- The foot rig is built for a clean 3-joint IK foot chain: ankle, ball, toe.
- The bind foot chain is also expected to have ankle, ball, toe joints.
- IK joints and bind joints must not be the same objects.
- The main leg RP IK handle already exists.
- Pivot nodes are already positioned correctly.
- Pivot nodes are already parented correctly.
- Pivot rotate channels are free to receive incoming connections.
- Foot controller attributes already exist before running the tool.
- Foot roll is driven on rotateX.
- Foot banking is driven on rotateZ.
- Toe/heel sway uses rotateY.

## Current Limitations

- Built with `maya.cmds` only.
- Pivot creation and placement are manual.
- Controller attribute creation is manual.
- Pivot position correctness is not validated.
- The tool assumes strict naming for pivot nodes.
- The tool assumes the foot joint setup is clean and non-branching.
- The tool creates nodes directly in the scene and does not currently group them under a dedicated rig module group.
- There is no automatic rollback if the build fails halfway.
- There is no delete/rebuild function yet.

## File Structure Suggestion

Recommended GitHub layout:

```text
Reverse-Foot-Rigger/
├── README.md
├── naming_convention.md
├── metaTools_ReverseFootRigger.py
└── media/
    ├── ui_screenshot.png
    └── demo.gif
```

## Author

Kang — Rigging / Technical Artist
