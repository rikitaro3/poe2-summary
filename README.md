# ⚔️ PoE2 個人用ツール・ファーム計画保管庫

📖 **[ドキュメントサイト (Docsify) はこちら](https://rikitaro3.github.io/poe2-summary/)**

このリポジトリは、Path of Exile 2 (PoE2) を個人で遊ぶ際に使用するトレード検索URL生成スクリプトや、ファーム戦略ドキュメントなどを管理・保管する個人用のリポジトリです。

---

## 📂 フォルダ構成

プロジェクトは以下の通りに整理されています。

```text
.
├── config/                 # 設定・環境変数関連
│   ├── .env                # POESESSIDセッションID等の保存用ファイル
│   └── trade_queries.json  # 🔍 検索クエリおよびMod IDマッピング設定ファイル
├── src/                    # 実行スクリプト（Pythonプログラム）
│   ├── generate_trade_url.py        # 条件から公式トレード検索URLを生成するスクリプト
│   ├── generate_map_trade_url.py    # 🗺️ 8modマップ検索URLを自動生成するスクリプト
│   ├── generate_tablet_trade_url.py  # 🌀 各投資レベル別Delirium石板検索URLを生成するスクリプト
│   └── trade_client.py              # 🔌 APIリクエストおよびレートリミットを管理する共通クライアント
├── docs/                   # ガイドブック、プロンプト、計画等のドキュメント
│   ├── delirium_farming_strategy.md # 🌀 最新 Delirium ファーム戦略ガイド
│   ├── poe2_trade_search_guide.md   # トレードAPIの動作原則とMod IDガイド
│   └── memos/              # お役立ちメモ・データベース
│       ├── rite_of_passage.md      # 📜 「通過儀礼」効果一覧メモ
│       └── useful_links.md         # 🔗 お役立ちリンク集
├── scratch/                # 開発・検証用一時スクリプト・データ（Git除外ファイル含む）
│   ├── scratch_parse_pob.py        # PoBパース用の検証スクリプト
│   └── decode_pob.py               # POBコード復号用の便利スクリプト
└── README.md               # 本説明書
```

---

## 🚀 使い方

### 1. アップグレード用装備アイテムをトレード検索する
更新したい部位の条件を引数で指定して実行すると、公式トレード検索URLが自動生成されます。

```powershell
# 例: ライフ50以上、火耐性30%以上の兜 (Helmet) を即時取引限定で探す
python src/generate_trade_url.py --type "Helmet" --life 50 --res-fire 30
```

#### 主な指定可能オプション
*   `--type`: アイテムタイプ (例: `Ring`, `Amulet`, `Helmet`, `Body Armour`, `Gloves`, `Boots`, `Belt`, `Weapon`, `Shield`)
*   `--life`: 必要最小ライフ (数値)
*   `--res`: 必要最小総元素耐性 (数値)
*   `--res-fire` / `--res-cold` / `--res-lightning` / `--res-chaos`: 個別耐性の最小値
*   `--speed`: 必要最小移動速度 % (Boots等)
*   `--atk-speed`: 必要最小攻撃速度増加 %
*   `--spell-dmg`: 必要最小呪文ダメージ増加 %
*   `--phys` / `--cold` / `--fire` / `--lightning`: 攻撃フラットダメージの加点検索 (フラグ)
*   `--fire-spell` / `--cold-spell` / `--lightning-spell`: 呪文フラットダメージの加点検索 (フラグ)
*   `--cast`: キャスト速度増加の加点検索 (フラグ)
*   `--max-price`: 予算上限
*   `--currency`: 通貨タイプ (`chaos` または `exalted` / デフォルト: `chaos`)
*   `--all-sales`: インスタントバイアウト（即時購入）以外の出品も含めてオンラインプレイヤーを検索する（デフォルトは即時購入のみに制限）
*   `--any-status`: オフラインプレイヤーの出品も含めて検索する

---

### 2. マップや石板の検索URLを自動生成する
静的に登録されたクエリをもとに、8modマップやDelirium石板の検索URLを一括生成します。検索条件は `config/trade_queries.json` で管理されています。

```powershell
# T15 8modマップの検索URLを生成
python src/generate_map_trade_url.py

# 投資レベル別（低・中・高・クラフト用）のDelirium石板検索URLを一括生成
python src/generate_tablet_trade_url.py
```
