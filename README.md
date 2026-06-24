# ⚔️ PoE2 装備自動取得＆更新計画・検索URL生成ツール

このツールは、Path of Exile 2 (PoE2) のキャラクター装備データを自動または手動で取得し、生存能力の弱点（ライフや耐性）を自動解析して、更新に必要なアイテムを公式トレードサイトで探すための検索URLを生成します。

---

## 📂 フォルダ構成

プロジェクトは以下の通りに整理されています。

```text
apps/97_poe/
├── config/                 # 設定・環境変数関連
│   └── .env                # POESESSIDセッションID等の保存用ファイル
├── src/                    # 実行スクリプト（Pythonプログラム）
│   ├── generate_trade_url.py  # 条件から公式トレード検索URLを生成するスクリプト
│   ├── get_character_gear.py  # 装備データの取得と簡易分析を行うスクリプト
│   └── get_pob_data.py       # pobb.inから直接XMLをロード・パースしてJSON化するスクリプト
├── docs/                   # ガイドブック、プロンプト、計画等のドキュメント
│   ├── farming_guide.md            # ファーミングガイド
│   ├── gear_requirements.md        # 🌟 最新の装備要件＆アップグレード計画（参考ビルドとの比較）
│   ├── poe2_gear_upgrade_assistant_prompt.md # AIに高度な更新計画を作らせるプロンプト
│   ├── poe2_pob_weights_guide.md   # POBウェイトガイド
│   └── poe2_trade_search_guide.md  # トレードAPIの動作原則とMod IDガイド
├── scratch/                # 開発・検証用一時スクリプト・データ（Git除外ファイル含む）
│   ├── scratch_parse_pob.py        # PoBパース用の検証スクリプト
│   └── pob_code.txt                # 検証用PoBコードファイル
├── output/                 # スクリプトが生成する成果物（JSON/Markdown）
│   ├── current_gear.json           # 取得した現在装備の生JSONデータ
│   ├── current_gear_summary.md     # ライフや耐性を合算した読みやすい装備詳細
│   ├── reference_gear.json         # 参考ビルドのパース済みJSONデータ
│   ├── my_gear.json                # ユーザービルドのパース済みJSONデータ
│   └── level51_gear_search_links.md  # 以前作成したレベル51時点のトレードURL集
└── README.md               # 本説明書
```

---

## 📊 登録されているビルド情報 & 装備要件

最新のビルド比較情報および今後の装備アップグレード方針については、以下のドキュメントにまとめています。

*   **[装備アップグレード計画・要件書 (gear_requirements.md)](file:///c:/Users/4in4o/Documents/git/nexus-ai/apps/97_poe/docs/gear_requirements.md)**
    *   **参考ビルド**: [https://pobb.in/kLNjcjtCzrcN](https://pobb.in/kLNjcjtCzrcN) (Lv95 Spirit Walker - Twister槍ビルド)
    *   **現在のビルド**: [https://pobb.in/G-t_eu2rRSKv](https://pobb.in/G-t_eu2rRSKv) (ユーザー現在のビルド)

---

## 🚀 使い方

### 1. pobb.in からデータを取得する

pobb.in のURLから直接装備データをJSONファイルとしてダウンロードしてパースします（SSLエラー対策版）。

```powershell
# 例: 参考ビルドデータを取得して保存
python src/get_pob_data.py "https://pobb.in/kLNjcjtCzrcN" "output/reference_gear.json"

# 例: 自分のビルドデータを取得して保存
python src/get_pob_data.py "https://pobb.in/10y0ghlrmstM" "output/my_gear.json"
```

### 2. 現在の装備データを公式プロフィールから取得・解析する
ご自身のプロフィール設定が「公開（Public）」になっている場合、アカウント名とキャラクター名から直接取得できます。

```powershell
python src/get_character_gear.py "soukana-5504" "rikitaro_htrs" --analyze
```
*※実行後、`output/current_gear_summary.md` および `output/current_gear.json` に結果が書き出されます。*
*※`--analyze` を付けると、耐性の不足状況と更新用コマンド例がコンソールに表示されます。*

---

### 3. アップグレード用アイテムをトレード検索する
取得した装備データを基に、更新したい部位の条件を引数で指定して実行すると、公式トレード検索URLが自動生成されます。

```powershell
# 例: ライフ50以上、火耐性30%以上の兜 (Helmet) を即時取引(Instant Buyout)限定で探す
python src/generate_trade_url.py --type "Helmet" --life 50 --res-fire 30 --instant-only
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
*   `--max-price`: 予算上限 (Chaos Orb単位)
*   `--instant-only`: インスタントバイアウト (ゲーム内自動取引所での即時購入) のみに制限する (フラグ)
