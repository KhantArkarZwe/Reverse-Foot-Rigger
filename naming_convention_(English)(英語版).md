# Naming Convention — metaTools Reverse Foot Rigger

This document explains the expected naming convention for the Reverse Foot Rigger.

The tool relies on strict side prefixes and pivot names. It receives the foot controller, IK joints, bind joints, and leg IK handle from UI text fields, but pivot names are constructed automatically from the limb side.

## Side Prefix

| Side | Prefix |
|---|---|
| Left | `L_` |
| Right | `R_` |

Example:

```text
L_root_pivot
R_root_pivot
```

## Required Pivot Names

For the left side:

```text
L_root_pivot
L_heel_pivot
L_inner_pivot
L_outer_pivot
L_end_pivot
L_ball_pivot
L_ankle_pivot
L_toe_pivot
```

For the right side:

```text
R_root_pivot
R_heel_pivot
R_inner_pivot
R_outer_pivot
R_end_pivot
R_ball_pivot
R_ankle_pivot
R_toe_pivot
```

## Required Pivot Hierarchy

The tool expects this hierarchy:

```text
<side>_root_pivot
└── <side>_heel_pivot
    └── <side>_inner_pivot
        └── <side>_outer_pivot
            └── <side>_end_pivot
                ├── <side>_ball_pivot
                │   └── <side>_ankle_pivot
                └── <side>_toe_pivot
```

Example left side:

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

## Foot Controller

The foot controller name is entered manually in the UI.

Recommended naming:

```text
L_ankle_IK_ctrl
R_ankle_IK_ctrl
```

The controller must contain all required reverse foot attributes.

## Required Foot Controller Attributes

Animator-facing attributes:

```text
Roll
Bank
ToeSway
HeelSway
ToeTap
```

Setting / tuning attributes:

```text
RollBack
RollEnd
ToeFlex
ToeStraightAngle
BankMultiplier
```

`Roll` must have this range:

```text
minimum: -10
maximum: 20
```

## IK Foot Joints

The IK foot joints are entered manually in the UI.

Recommended left-side naming:

```text
L_ankle_IK
L_foot_IK
L_tiptoe_IK
```

Recommended right-side naming:

```text
R_ankle_IK
R_foot_IK
R_tiptoe_IK
```

The expected order is:

```text
ankle IK
ball IK
toe IK
```

## Bind Foot Joints

The bind foot joints are entered manually in the UI.

Recommended left-side naming:

```text
L_ankle
L_foot
L_tiptoe
```

Recommended right-side naming:

```text
R_ankle
R_foot
R_tiptoe
```

The expected order is:

```text
ankle bind
ball bind
toe bind
```

The IK joint and bind joint at the same position must be separate objects.

Invalid example:

```text
Ankle IK:   L_ankle
Ankle Bind: L_ankle
```

Valid example:

```text
Ankle IK:   L_ankle_IK
Ankle Bind: L_ankle
```

## Leg IK Handle

The main leg RP IK handle is entered manually in the UI.

Recommended naming:

```text
L_Leg_RP_ikHandle
R_Leg_RP_ikHandle
```

This IK handle must already exist before running the reverse foot tool.

## Generated Utility Node Names

The tool creates nodes using the side prefix.

For left side:

```text
L_footRoll_ball_condition
L_footRoll_heel_condition
L_footRoll_end_condition
L_footRoll_clamp_condition
L_footRoll_tiptoe_condition
L_footBank_condition

L_footRoll_multi
L_footRoll_ball_multi
L_footBank_multi

L_footRoll_pma
L_footRoll_ball_pma
L_footRoll_tiptoe_pma

L_ball_ikHandle
L_toe_ikHandle
```

Right side uses `R_` instead.

The tool will stop if any generated node already exists.

## Rotation Axis Convention

The current setup assumes:

| Motion | Axis |
|---|---|
| Foot roll | rotateX |
| Foot bank | rotateZ |
| Toe sway / heel sway | rotateY |
| Toe tap | rotateX |

## Quick Pre-flight Checklist

Before pressing **Build Reverse Foot Rig**, confirm:

- Pivot names match the selected side.
- Pivot hierarchy is correct.
- Pivot rotate channels are unlocked.
- Pivot rotate channels have no incoming connections.
- Foot controller has all required attributes.
- `Roll` has range `-10` to `20`.
- IK foot joints exist.
- Bind foot joints exist.
- IK and bind joints are not the same objects.
- Main leg RP IK handle exists.
