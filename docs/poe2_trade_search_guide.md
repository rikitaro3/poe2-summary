# PoE2 トレード検索URL生成スクリプト仕様書 (`generate_trade_url.py`)

このドキュメントは、Path of Exile 2 (PoE2) 公式トレードAPIと連携して、アイテム検索URLを自動生成するPythonスクリプト `src/generate_trade_url.py` の技術仕様と使用方法をまとめたものです。
AIがユーザーの要望に基づいて適切な引数を選択し、スクリプトを実行して検索URLを生成するためのコンテキストとして使用します。

---

## 🚀 PoE2 トレードAPIの基本動作原理

PoE2のトレードサイトは、クエリパラメータを含んだ単純なURLによる直接検索をサポートしていません。
動作する正しい検索URLを生成するには、以下の2ステップを行います。

1. **検索条件JSONを公式APIにPOST送信する**
   - **エンドポイント**: `https://www.pathofexile.com/api/trade2/search/{League}`
   - **必須ヘッダー**:
     - `Content-Type: application/json`
     - `User-Agent: PoE2TradeHelper/1.0 (Contact: mail@example.com)` (公式APIポリシーの遵守)
     - `Cookie: POESESSID={POESESSID}` (複雑な検索を許可するために必須)
   - **リクエストボディ**: アイテム検索条件（Mod IDや値の範囲）を記述したJSONクエリ

2. **レスポンス内のIDから検索URLを構築する**
   - APIが返却するレスポンスから `"id"`（Search ID）を取得し、以下のURLを組み立てて出力します。
   - **完成URL**: `https://www.pathofexile.com/trade2/search/{League}/{SearchId}`

---

## 🔑 アカウントセッションID（POESESSID）の設定

未ログイン（ゲスト）状態で多数のModや複雑なフィルタをAPIに送信すると、公式サーバー側で「Query is too complex.」エラーが発生して検索できません。
個人アカウントでログインした状態の `POESESSID` を使用することで、複雑なクエリの送信制限が解除されます。

- **保存先**: `config/.env`
- **記述形式**:
  ```env
  POESESSID=あなたのPOESESSIDの値（32文字の英数字）
  ```
- **注意点**: セッションIDの有効期限が切れるとAPIが `403 Forbidden` や `Query is too complex.` を返すようになるため、その場合はブラウザから再取得して `.env` を更新する必要があります。

---

## ⚡ スクリプトのパラメータ引数仕様

AIはユーザーの要望を解析し、`src/generate_trade_url.py` を実行する際に以下の適切な引数を選択してください。

### 1. 基本設定
- `--type`: 検索するアイテムの部位を指定します。
  - 指定可能値: `Ring`, `Amulet`, `Helmet`, `Body Armour`, `Boots`, `Gloves`, `Belt`, `Weapon`, `Shield`
- `--league`: 対象リーグ（デフォルト: `"Runes of Aldur"`)
- `--session`: 明示的に `POESESSID` を渡す場合に使用（指定しない場合は `config/.env` から自動ロード）

### 2. 生存能力・基本ステータス（ANDフィルター）
- `--life`: 必要最小ライフ (数値)
- `--res`: 必要最小総属性耐性合計 (数値)
- `--res-fire`: 必要最小火炎耐性 (数値)
- `--res-cold`: 必要最小冷気耐性 (数値)
- `--res-lightning`: 必要最小稲妻耐性 (数値)
- `--res-chaos`: 必要最小カオス耐性 (数値)
- `--speed`: 最小移動速度 % (数値、Boots用)
- `--atk-speed`: 最小攻撃速度増加 % (数値)
- `--spell-dmg`: 最小呪文ダメージ増加 % (数値)

### 3. 火力・特殊効果（加点 Weight フィルター）
指定したフラグに基づいて、条件に合致するModにウェイト（重み）を付けて検索します（いずれか1つ以上が含まれるアイテムがヒットします）。
- `--phys`: 物理追加ダメージを検索対象にする (フラグ)
- `--cold`: 冷気追加ダメージを検索対象にする (フラグ)
- `--fire`: 火炎追加ダメージを検索対象にする (フラグ)
- `--lightning`: 雷電追加ダメージを検索対象にする (フラグ)
- `--cast`: キャスト速度を検索対象にする (フラグ)
- `--fire-spell` / `--cold-spell` / `--lightning-spell`: 呪文への各属性フラット追加ダメージを検索対象にする (フラグ)

### 4. 取引・価格制限
- `--max-price`: 予算上限 (数値)
- `--currency`: 予算の通貨単位。`chaos`（Chaos Orb）または `exalted`（Exalted Orb）を指定（デフォルト: `chaos`）
- `--any-status`: オフラインの出品も含めて検索する (フラグ)
- `--all-sales`: 通常トレードを含むすべてのオンライン出品を検索する (フラグ)
  - **重要**: このフラグを指定しない場合、デフォルトでは **インスタントバイアウト（ゲーム内自動取引所での即時購入）のみ** に制限されます。通常トレードの出品も含めて広く探したい場合は、必ずこのフラグを付与してください。

### 5. 特殊検索
- `--custom-ring`: 特定の指輪（火炎ダメージ増加＋レア度増加＋筋力＋フラット追加）を狙い撃ちするカスタムクエリを生成します。

---

## 📝 主要なPoE2 Mod ID（スタッツID）マッピング

スクリプト内部で利用されている、公式のStat IDと引数のマッピングです。

| 引数オプション | 内部マッピングID (Stat ID) |
|---|---|
| `--life` | `pseudo.pseudo_total_life` |
| `--res` | `pseudo.pseudo_total_resistance` |
| `--res-fire` | `pseudo.pseudo_total_fire_resistance` |
| `--res-cold` | `pseudo.pseudo_total_cold_resistance` |
| `--res-lightning` | `pseudo.pseudo_total_lightning_resistance` |
| `--res-chaos` | `pseudo.pseudo_total_chaos_resistance` |
| `--speed` | `explicit.stat_2100679358` (Movement Speed) |
| `--atk-speed` | `explicit.stat_210067635` (Attack Speed) |
| `--spell-dmg` | `explicit.stat_1241851921` (Spell Damage) |
| `--phys` | `explicit.stat_1940865751` / `pseudo.pseudo_adds_physical_damage_to_attacks` |
| `--cold` | `explicit.stat_1037193709` / `pseudo.pseudo_adds_cold_damage_to_attacks` |
| `--cast` | `explicit.stat_2624005898` (Cast Speed) |

---

## 💡 AIのスクリプト呼び出し判定ルール (ユースケース別例)

AIはユーザーからの自然言語でのリクエストを元に、以下のようにスクリプトの引数を組み立てて実行してください。

### 例1: 「ライフ50以上、火と冷気の耐性がそれぞれ30%以上ある兜を探して」
- **選択引数**: `--type Helmet --life 50 --res-fire 30 --res-cold 30`
- **実行コマンド**:
  ```bash
  python src/generate_trade_url.py --type Helmet --life 50 --res-fire 30 --res-cold 30
  ```

### 例2: 「物理ダメージが高いAkoyan Spearの通常トレード（オンライン）を探して」
※通常トレードを含めるため、`--all-sales` を付与します。
- **選択引数**: `--type Weapon --phys --all-sales`
- **実行コマンド**:
  ```bash
  python src/generate_trade_url.py --type Weapon --phys --all-sales
  ```

### 例3: 「即時購入（オート取引）限定でカオス耐性付きの指輪を20c以下で探して」
※即時購入限定（デフォルト挙動）のため、`--all-sales` は付与せず、予算を指定します。
- **選択引数**: `--type Ring --res-chaos 15 --max-price 20`
- **実行コマンド**:
  ```bash
  python src/generate_trade_url.py --type Ring --res-chaos 15 --max-price 20
  ```

### 例4: 「移動速度20%以上、ライフと冷気耐性付きのブーツを探して。価格は安め（10c以下）で」
- **選択引数**: `--type Boots --speed 20 --life 30 --res-cold 20 --max-price 10`
- **実行コマンド**:
  ```bash
  python src/generate_trade_url.py --type Boots --speed 20 --life 30 --res-cold 20 --max-price 10
  ```
