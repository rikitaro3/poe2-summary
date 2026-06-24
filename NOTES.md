# 📝 調査・試行錯誤メモ (PoE2 装備更新計画の更新)

## 2026-06-02
- タスク開始。
- 最新の装備URL: `https://pobb.in/G-t_eu2rRSKv`
- `get_pob_data.py` でパースした結果、ユーザー装備は前回の `gear_requirements.md` に記録されていたものと一致していることを確認。
- `scratch_parse_pob.py` から抽出したステータス：
  - Level: 77
  - Str: 122 / Dex: 137 / Int: 65
  - Life: 1,930 (非常に優秀、参考ビルドの 1,890 を超えている)
  - Evasion: 1,698
  - Deflection Rating: 203.76 (Deflect Chance: 5%) -> 変換ルーンが無いため極めて低い
  - 火耐性: 67% (キャップまであと 8% 不足)
  - 冷気耐性: 75% (+8% over)
  - 雷耐性: 75% (+1% over)
  - カオス耐性: 43%
  - メイン武器: Entropy Edge (火・雷属性フラット槍、物理DPSは無し)
  - サブ武器: Baron's Omen Sceptre (Spirit・Malice用、高速移動スワップ槍は未導入)
- 分析結果：
  - 火力の飛躍的な向上には、物理DPS特化の Akoyan Spear が必要だが、装備要求値である Dex 157 (あと20必要) の確保が必要。
  - 耐久力の向上には、まず火耐性キャップ (75%) を達成すること。次に、頭・胴・足での「Evasionの21%をDeflectionに変換」ルーンの付与が必要。
  - 移動速度と立ち回りの快適さのために、サブ高速スワップ槍 (Winged Spear with AS 25%) を導入すべき。
- 更新方針：
  - `docs/gear_requirements.md` を最新のステータス情報に基づいてブラッシュアップし、よりステップバイステップで親切なアップグレード計画に改定する。

## 2026-06-21
- タスク：Nick 2 による PoE2 最新 Delirium ファーム戦略の動画文字起こしを要約し、`docs/delirium_farming_strategy.md` を新規作成する。
- 調査メモ（動画の要点）：
  - パッチ変更点：Delirium エリート（レア/マジック）のスポンバグが修正され、大量のエリートがスポンするようになり、非常に美味しくなった。
  - 収益性：低投資で1マップあたり 5〜8 Divine 程度の利益（1ランで Simulacrum 1〜2枚、約 4〜6 Div が安定。さらに Voices などの超高額品も狙える）。
  - 必須Mod: `delirium fog in map spawns increased fracturing mirrors` (マップ内の霧で分裂ミラー出現率増加)
  - 攻略の注意：敵が大量に湧き非常に難易度が高いため、弱いビルドではモディファイアを抑えること。
  - Spirit Walker (Twister) ビルドの視点：Nick 2 は Spirit Walker でファームしているが、スペースキーによる回避（Dodge）を連打しなければならないのがストレスで、ビルドを変更予定。
- 追加タスク：
  - 石板（Precursor Tablet）の検索URL自動生成ツール `src/generate_tablet_trade_url.py` を作成（インスタントバイアウト限定）。
  - マップ（Waystone）の検索URL自動生成ツール `src/generate_map_trade_url.py` を作成（8mod限定フィルタ、インスタントバイアウト限定）。





