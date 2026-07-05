# metaTools Reverse Foot Rigger

フットコントローラー上のアニメーター向け属性、IKハンドル、フットピボット、ユーティリティノードを使用して、リバースフットリグを作成するMaya Pythonツールです。

このツールは、メインの脚IKシステムが既に存在している状態から、Foot Roll、Banking、Toe Tap、Toe Sway、Heel Sway用のノードネットワークを自動化するために制作しました。

## 主な機能

- Foot RollとFoot Banking用のリバースフットノードネットワークを作成します。
- condition、multiplyDivide、plusMinusAverageユーティリティノードを使用します。
- ballジョイントとtoeジョイント用のSC IKハンドルを作成します。
- 脚のRP IKハンドルをankleピボットの下にペアレントします。
- フットコントローラーの属性をピボット回転へ接続します。
- foot IKジョイントを対応するbindジョイントへ接続します。
- 接続前にピボットの存在と階層を検証します。
- 必要なフットコントローラー属性を検証します。
- 同じジョイントをIK用とbind用の両方に誤って使用することを防ぎます。

## ソフトウェア／環境

- Autodesk Maya 2025
- Python 3
- maya.cmds

## このツールが行うこと

このツールは、既存のフットコントローラー、既存のIK footジョイント、既存のbind footジョイント、既存の脚RP IKハンドル、既存のリバースフットピボット階層を接続します。

以下を作成します。

- ball SC IKハンドル
- toe SC IKハンドル
- conditionノード
- multiplyDivideノード
- plusMinusAverageノード
- ユーティリティノード接続
- ピボット回転接続
- foot IKジョイントからfoot bindジョイントへのparentConstraint

## このツールが行わないこと

- フットコントローラーは作成しません。
- アニメーター向け属性は作成しません。
- 調整用属性は作成しません。
- ピボットノードの作成や配置は行いません。
- ピボット位置が解剖学的に正しいかどうかは確認しません。
- 脚全体のIK/FKシステムは構築しません。
- メッシュのスキニングは行いません。
- 現時点ではcleanup／deleteツールはありません。

## 使用方法

1. Mayaを開きます。
2. メインの脚IKセットアップが既に存在していることを確認します。
3. リバースフットピボット階層が既に存在し、各ピボットが適切な位置に配置されていることを確認します。
4. フットコントローラーに必要な属性が全て存在していることを確認します。
5. スクリプトをScript Editorで開く、またはMayaのPython環境へロードします。
6. 以下を実行します。

```python
metaTools_ReverseFootRigger.openUI()
```

7. UIで以下を入力します。
   - Limb Side: `L` または `R`
   - Foot Ctrl
   - Ankle IK joint
   - Ball IK joint
   - Toe IK joint
   - Ankle bind joint
   - Ball bind joint
   - Toe bind joint
   - Leg RP IK handle
8. **Build Reverse Foot Rig** を押します。

## 必要なUI入力

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

最終的なシーン内の命名に合わせて、これらの例を調整してください。

## 必要なフットコントローラー属性

フットコントローラーには、以下の属性が既に存在している必要があります。

### アニメーター向け属性

| Attribute | Purpose |
|---|---|
| `Roll` | メインのFoot Rollコントロール |
| `Bank` | Foot Bankingコントロール |
| `ToeSway` | heelピボットからのtoe／heelの左右方向ピボット動作 |
| `HeelSway` | endピボットからのheel／endの左右方向ピボット動作 |
| `ToeTap` | Toe Tap回転 |

### 設定／調整用属性

| Attribute | Purpose |
|---|---|
| `RollBack` | Heel Roll用の倍率／コントロール |
| `RollEnd` | endピボットが動作を引き継ぎ始めるタイミングを制御 |
| `ToeFlex` | ball／toeの曲げ量 |
| `ToeStraightAngle` | Roll／Tiptoeロジックで使用する角度しきい値 |
| `BankMultiplier` | Bankingの強さを調整する倍率 |

`Roll` は `-10` から `20` の値範囲を持つ必要があります。

スクリプトは、全ての必須属性が存在し、数値属性であることを確認します。

## 必要なピボット階層

ピボットノードは既に存在しており、以下の順序でペアレントされている必要があります。

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

右側では同じ構造に `R_` プレフィックスを使用します。

スクリプトは以下を確認します。

- 全てのピボットノードが存在すること
- rotateX／rotateY／rotateZ がロックされていないこと
- ピボットのrotateチャンネルに既存の入力接続がないこと
- ピボット階層が想定された構造と一致していること
- toeピボットがendピボットの下にペアレントされていること

## 生成されるノード

ツールは、sideプレフィックス付きで以下のユーティリティノードを作成します。

### Conditionノード

```text
L_footRoll_ball_condition
L_footRoll_heel_condition
L_footRoll_end_condition
L_footRoll_clamp_condition
L_footRoll_tiptoe_condition
L_footBank_condition
```

### multiplyDivideノード

```text
L_footRoll_multi
L_footRoll_ball_multi
L_footBank_multi
```

### plusMinusAverageノード

```text
L_footRoll_pma
L_footRoll_ball_pma
L_footRoll_tiptoe_pma
```

### IKハンドル

```text
L_ball_ikHandle
L_toe_ikHandle
```

右側では `R_` を使用します。

生成予定のノード名が既に存在している場合、ツールは停止します。

## 重要な前提条件

- このフットリグは、ankle、ball、toeのクリーンな3ジョイントIK footチェーンを前提としています。
- bind footチェーンも、ankle、ball、toeジョイントを持つことを想定しています。
- IKジョイントとbindジョイントは同じオブジェクトであってはいけません。
- メインの脚RP IKハンドルが既に存在している必要があります。
- ピボットノードは既に正しい位置に配置されている必要があります。
- ピボットノードは既に正しい階層でペアレントされている必要があります。
- ピボットのrotateチャンネルは入力接続を受け取れる状態である必要があります。
- フットコントローラー属性は、ツール実行前に既に存在している必要があります。
- Foot RollはrotateXで駆動されます。
- Foot BankingはrotateZで駆動されます。
- Toe／Heel SwayはrotateYを使用します。

## 現在の制限事項

- `maya.cmds` のみで構築されています。
- ピボット作成と配置は手動です。
- コントローラー属性の作成は手動です。
- ピボット位置の正確性は検証されません。
- ピボットノードには厳密な命名規則を前提としています。
- クリーンで分岐のないfoot jointセットアップを前提としています。
- ツールはノードを直接シーン内に作成し、現時点では専用のrig module groupの下にまとめません。
- ビルドが途中で失敗した場合の自動ロールバックはありません。
- delete／rebuild機能はまだありません。

## Author

KhantArkarZwe — Rigging / Technical Artist\
Gmail: khantarkarzwe@gmail.com
