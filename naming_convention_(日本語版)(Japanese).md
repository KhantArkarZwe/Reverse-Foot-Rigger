# Naming Convention — metaTools Reverse Foot Rigger

このドキュメントでは、Reverse Foot Riggerで想定している命名規則を説明します。

このツールは、厳密なside prefixとpivot名に依存しています。foot controller、IK joints、bind joints、leg IK handleはUIのテキストフィールドから受け取りますが、pivot名はlimb sideから自動的に構築されます。

## Side Prefix

| Side | Prefix |
|---|---|
| Left | `L_` |
| Right | `R_` |

例:

```text
L_root_pivot
R_root_pivot
```

## Required Pivot Names

左側:

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

右側:

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

ツールは以下の階層を想定しています。

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

左側の例:

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

フットコントローラー名はUIで手動入力します。

推奨命名:

```text
L_ankle_IK_ctrl
R_ankle_IK_ctrl
```

コントローラーには、必要な全てのreverse foot属性が含まれている必要があります。

## Required Foot Controller Attributes

アニメーター向け属性:

```text
Roll
Bank
ToeSway
HeelSway
ToeTap
```

設定／調整用属性:

```text
RollBack
RollEnd
ToeFlex
ToeStraightAngle
BankMultiplier
```

`Roll` は以下の範囲を持つ必要があります。

```text
minimum: -10
maximum: 20
```

## IK Foot Joints

IK foot jointsはUIで手動入力します。

推奨される左側の命名:

```text
L_ankle_IK
L_foot_IK
L_tiptoe_IK
```

推奨される右側の命名:

```text
R_ankle_IK
R_foot_IK
R_tiptoe_IK
```

想定される順序:

```text
ankle IK
ball IK
toe IK
```

## Bind Foot Joints

bind foot jointsはUIで手動入力します。

推奨される左側の命名:

```text
L_ankle
L_foot
L_tiptoe
```

推奨される右側の命名:

```text
R_ankle
R_foot
R_tiptoe
```

想定される順序:

```text
ankle bind
ball bind
toe bind
```

同じ位置にあるIKジョイントとbindジョイントは、別々のオブジェクトである必要があります。

無効な例:

```text
Ankle IK:   L_ankle
Ankle Bind: L_ankle
```

有効な例:

```text
Ankle IK:   L_ankle_IK
Ankle Bind: L_ankle
```

## Leg IK Handle

メインの脚RP IKハンドルはUIで手動入力します。

推奨命名:

```text
L_Leg_RP_ikHandle
R_Leg_RP_ikHandle
```

このIKハンドルは、reverse footツールを実行する前に既に存在している必要があります。

## Generated Utility Node Names

ツールはside prefixを使用してノードを作成します。

左側:

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

右側では `R_` を使用します。

生成されるノード名が既に存在している場合、ツールは停止します。

## Rotation Axis Convention

現在のセットアップでは、以下の軸を前提としています。

| Motion | Axis |
|---|---|
| Foot roll | rotateX |
| Foot bank | rotateZ |
| Toe sway / heel sway | rotateY |
| Toe tap | rotateX |

## Quick Pre-flight Checklist

**Build Reverse Foot Rig** を押す前に、以下を確認してください。

- Pivot名が選択したsideと一致している。
- Pivot階層が正しい。
- Pivotのrotateチャンネルがロックされていない。
- Pivotのrotateチャンネルに入力接続がない。
- Foot controllerに全ての必須属性がある。
- `Roll` の範囲が `-10` から `20` である。
- IK foot jointsが存在している。
- Bind foot jointsが存在している。
- IK jointsとbind jointsが同じオブジェクトではない。
- メインの脚RP IK handleが存在している。
