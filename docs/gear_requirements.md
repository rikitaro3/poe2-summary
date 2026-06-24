# ⚔️ PoE2 Twister Huntress 装備アップグレード計画 & 装備要件

このドキュメントは、参考にしたいビルド（参考ビルド）、MobalyticsのTwister Huntressレベリングガイド（2本槍スワップ前提）、およびご自身の最新ビルド（G-t_eu2rRSKv）を詳細に比較し、今後の装備更新計画をまとめたものです。

---

## 1. 参考ビルド詳細 (`https://pobb.in/kLNjcjtCzrcN`)

参考ビルドは **レベル95 Huntress (Spirit Walker)** で、物理・冷気ハイブリッドの槍投射物スキル（Twister）を主軸としたビルドです。PoE2の特有システムである **「2つの武器セットのスワップ（切り替え）」** をフル活用して、火力と移動速度・バフ性能を両立させています。

### 📊 防御ステータス概要
*   **最大ライフ**: 1,890 (装備合計: +395)
*   **回避 (Evasion)**: 8,527
*   **デフレクション (Deflection Rating)**: 10,232 (デフレクション率: 55%)
*   **元素耐性**: 火 75% (+3% over), 冷気 75% (+66% over), 雷 76% (+10% over), カオス 17%

### ⚔️ 部位別装備詳細

| 部位 | 装備名 (ベースタイプ) | レアリティ | 主要Mod・役割 |
| :--- | :--- | :--- | :--- |
| **武器セット 1 (メイン)** | **Apocalypse Edge**<br>(Akoyan Spear) | Rare | **主力火力用・物理DPS特化槍**<br>・149% 物理ダメージ増加<br>・物理フラットダメージ追加<br>・ダメージの19%を冷気として追加獲得<br>※ `Twister` や `Barrage` などの攻撃スキルをこの武器セットに割り当てる。 |
| **武器セット 2 (サブ)** | **Damnation Edge**<br>(Winged Spear) ＋ <br>**Guiding Palm of the Eye** (セプター) | Magic / Unique | **移動・バフ・Spirit確保用スワップ武器**<br>・`Winged Spear`: 攻撃速度（AS）25%増加。`Whirling Slash`（移動）や `Vivid Stampede`（バフ）などのスキルをこのセットに割り当て、高速移動を実現。<br>・`Guiding Palm of the Eye`: Spiritと冷気ダメージ獲得。Purity of Iceオーラの維持。 |
| **頭 (Helmet)** | **Golem Cowl**<br>(Runeforged Trapper Hood) | Rare | **回避・デフレクション頭**<br>・ライフ+75, 冷気耐性+31%, 火耐性+18% (Rune)<br>・**Evasionの21%をDeflectionに変換** (必須防御Mod) |
| **胴 (Body Armour)** | **Hate Jack**<br>(Wyrmscale Coat) | Rare | **高回避・防御胴**<br>・Evasion 2,581 (超高数値)<br>・火耐性+21%, 雷耐性+29%<br>・**Evasionの21%をDeflectionに変換** |
| **手 (Gloves)** | **Gale Clutches**<br>(Runeforged Ornate Cuffs) | Rare | **攻撃力・ライフ吸収手袋**<br>・ライフ+102, 雷耐性+37%, 火耐性+18% (Rune)<br>・攻撃に追加冷気・雷ダメージ<br>・**物理攻撃ダメージの8.72%をライフ吸収 (Leech)** |
| **足 (Boots)** | **Vortex Slippers**<br>(Cavalry Boots) | Rare | **移動速度・デフレクション靴**<br>・ライフ+28, 移動速度25%増加, 冷気耐性+34%, 火耐性+18% (Rune)<br>・**Evasionの21%をDeflectionに変換** |
| **首 (Amulet)** | **Carrion Beads**<br>(Bloodstone Amulet) | Rare | **スキルレベル・パッシブ特化首**<br>・**+2 to Level of all Projectile Skills** (火力超強化)<br>・ライフ+38, 最大ライフ8%増加, 冷気耐性+35%<br>・**Allocates Serrated Edges** (パッシブ自動割り当て) |
| **指輪 1** | **Brimstone Twirl**<br>(Prismatic Ring) | Rare | **ライフ・耐性指輪**<br>・ライフ+90, 全耐性+16% (合計耐性+48%)<br>・攻撃に追加雷ダメージ |
| **指輪 2** | **Corpse Twirl**<br>(Lazuli Ring) | Rare | **マナ・追加属性指輪**<br>・最大マナ+120, 全耐性+16%, 雷/カオス耐性+14%<br>・攻撃に追加冷気・雷ダメージ |
| **腰 (Belt)** | **Ingenuity**<br>(Utility Belt) | **Unique** | **ベルトの核・指輪バフ**<br>・**左指輪の効果+23% / 右指輪の効果+25%**<br>・チャームスロット2個<br>・フラスコ回復の20%を即時適用 |

---

## 2. ユーザービルドとの詳細比較

現在の装備データ（PoB: `G-t_eu2rRSKv`）を基にした、参考ビルドとのギャップ分析です。

| 部位 | ユーザービルド (現在) | 参考ビルド | ギャップと課題 |
| :--- | :--- | :--- | :--- |
| **メイン武器 (火力)** | **レア属性槍** (Entropy Edge)<br>・火/雷フラットダメージ追加<br>・物理DPSはほぼ無し | **レア物理DPS槍** (Akoyan Spear) | **物理DPSの不足**。主力攻撃の Twister は武器の物理ダメージを参照するため、火耐性・雷耐性などを稼ぐ属性槍（Entropy Edge）から、高物理DPSの Akoyan Spear への移行が次のステップです。 |
| **サブ武器 (移動/AS)** | **レア槍＋マジックセプター**（メイン）<br>・スワップ側：**マジック槍** (Orichalcum Spear) | **高速マジック槍** (Winged Spear) ＋ **ユニークセプター** | メイン武器セットに `Baron's Omen` セプターを装備して Spirit を確保し、スワップセットに `Orichalcum Spear` を装備して武器スワップ自体は正しく設定されています。ただし、スワップ側の槍が高速ベース（Winged Spear）ではないため、移動時の恩恵を最大限受けられていません。 |
| **防御性能** | 回避防具が一部導入され、**Evasion 1,698** / **Deflection Rating 203 (確率5%)** に上昇 | **Evasion (回避) ベースに統一** | 回避値は1,698まで向上しましたが、頭・胴・足での「回避の21%をデフレクションに変換」Mod/ルーンが不足しているため、物理防御確率が5%と非常に脆い状態です。 |
| **ベルト** | **レアベルト (Soul Cord)**<br>・ライフ+80, カオス耐性+23% | **Unique Belt (Ingenuity)** | カオス耐性やライフが優秀なレアベルトを装備しています。将来的に指輪強化とチャーム枠確保のため、ユニークベルト Ingenuity への移行を目指します。 |
| **指輪・首** | ライフ・全耐性・フラット追加を両立した優秀な構成 | 指輪でライフ・ダメージ・耐性を両立 | アミュレットや指輪でライフ・耐性が大幅に安定しました。首に `Projectile Skill Level +2` やパッシブ自動割り当てが無い点が主なギャップです。 |

---

## 3. 今後の装備更新ロードマップ

ギャップを踏まえ、以下の順番で装備を購入・更新することをお勧めします。

### 🚨 STEP 1: 火耐性キャップ (75%) の達成 (最優先)
現在の火耐性は67%と、キャップ（75%）まであと8%不足しています。マップ周回時の即死を防ぐために、まずは火耐性を75%以上に引き上げましょう。
*   **方法**:
    *   空いている装備のクラフト枠で火耐性を付与する。
    *   ルーン（Rune of Fire Resistance等）を防具の空きソケットに貼り付ける。
    *   トレードサイトで火耐性が高い別の部位に更新する。

### 🚨 STEP 2: 属性要求値 (Dex 157) の確保
強力な物理槍である **Akoyan Spear** を装備するには、Dexterityが157以上必要です（現在137で、20不足）。
*   **対策**:
    *   パッシブツリーで「+30 to Dexterity」などの大ノードを一時的に取得する。
    *   指輪やアミュレット、または防具のModで Dexterity が付いているものを探す。
    *   装備品に「% reduced Attribute Requirements（装備要求値減少）」のModを付ける（現在の手袋 Ghoul Talons には 20% 減少が付いていますが、武器には適用されません）。

### 🚨 STEP 3: メイン物理槍の更新 (火力の大幅強化)
主力攻撃の Twister は武器の物理ダメージを参照して威力を計算するため、現在の属性フラット槍（Entropy Edge）から、物理DPSが高い槍への更新で火力が劇的に伸びます。
*   **目標アイテム**: **Akoyan Spear** (または物理DPSの高い槍)
*   **必須Mod**:
    *   `% increased Physical Damage` (物理ダメージ増加)
    *   `Adds # to # Physical Damage` (物理ダメージ追加)
    *   できれば `increased Attack Speed` (攻撃速度増加)
*   **トレード検索推奨条件**: 物理DPS (pdps) が 150 以上の槍
*   **自動生成トレードURL**: [👉 トレードサイトで物理槍を検索](https://www.pathofexile.com/trade2/search/Runes%20of%20Aldur/X3bzGOlRIP) (物理追加ダメージ付きの槍検索)

### 🚨 STEP 4: スワップ槍の「高速ベース（Winged Spear）」への切り替え
※すでにアタスピ25%付きの Winged Spear を所持されている場合は、スワップスロットの武器をそちらに差し替えるだけでこのステップは完了です！
スワップ側にベース攻撃速度が最も速い `Winged Spear`（アタスピ25%増加）を装備することで、移動速度がさらに劇的に向上します。
*   **目標アイテム**: **Winged Spear** (マジックレアリティでOK、アタスピ25%付き)
*   **設定手順**:
    1. 武器セット2（スワップ側）の左手に Winged Spear を装備します。
    2. すでにバインドされている `Whirling Slash` や `Vivid Stampede` などの移動・バフスキルに「武器セット2」が紐付いていることを確認します。これにより、攻撃速度+25%された Winged Spear の超高速モーションで移動できます。

### 🛡️ STEP 5: 防御機構の再構築 (回避＋デフレクション変換)
ライフが1,930と安定しているため、防御面での次のステップは「高Evasion＋デフレクション変換」のシナジー導入による被ダメージ激減です。
1.  **頭・足・胴を「Evasion (回避)」ベースの装備に更新する**。
2.  各部位に以下のModが付いているものを探すか、ルーンでクラフトします。
    *   `Gain Deflection Rating equal to 21% of Evasion Rating` (回避の21%をデフレクション値に変換)
    *   `+ maximum Life`
    *   不足している耐性（火耐性、カオス耐性など）
*   **自動生成トレードURL (回避防具ベース検索)**:
    *   [👉 トレードサイトで兜 (Helmet) を検索 (Life50+, Res40+)](https://www.pathofexile.com/trade2/search/Runes%20of%20Aldur/bGvz3JKDtL)
    *   [👉 トレードサイトで胴防具 (Chest) を検索 (Life50+, Res40+)](https://www.pathofexile.com/trade2/search/Runes%20of%20Aldur/2K5gM8D0ck)
    *   [👉 トレードサイトで靴 (Boots) を検索 (Life30+, Res30+)](https://www.pathofexile.com/trade2/search/Runes%20of%20Aldur/5n5VWn92fa)
    *   *※購入後、回避の21%をデフレクションに変換するルーンを貼り付けるか、トレードサイトの「Stat Filters」で "Gain Deflection Rating..." の個別Modを追加して再検索してください。*

### 💍 STEP 6: ユニークベルト `Ingenuity` の購入
ベルトが優秀なレアになったため優先度は下がりましたが、最終的な火力・耐久力引き上げのために導入を目指します。
*   **効果**: 左右の指輪の効果を約25%強化します。チャームスロットが2つになります。
*   **トレード検索推奨条件**: `Ingenuity Utility Belt` を直接検索
*   **自動生成トレードURL**: [👉 トレードサイトで Ingenuity を検索](https://www.pathofexile.com/trade2/search/Runes%20of%20Aldur/mkJZR2gRT6)

---

## 4. ステータス & ジェム (スキル) の比較

参考ビルドと現在のご自身のビルドについて、ステータス数値およびスキルジェム（サポートジェム含む）の構成を比較しました。

### 📊 ステータス比較表

| ステータス | ユーザービルド (Lv77) | 参考ビルド (Lv95) | 分析とギャップ |
| :--- | :--- | :--- | :--- |
| **レベル (Lv)** | **77** | **95** | レベルが77です。パッシブポイントや基礎ステータスが順調に強化されています。 |
| **Strength (Str)** | 122 | 72 | 装備要件は満たしていますが、必要以上に高く確保されています。 |
| **Dexterity (Dex)** | 137 | 159 | **槍の装備要求Dex（157）が依然として不足**（あと20不足）。強力なメイン物理槍（Akoyan Spear）を装備するため、さらに積む必要があります。 |
| **Intelligence (Int)** | 65 | 132 | **依然としてInt不足**（あと67不足）。高レベルのオーラジェム（Purity of Ice等）を運用するには、装備やツリーでIntを盛る必要があります。 |
| **Life (ライフ)** | **1,930** | **1,890** | **参考ビルドを上回りました！🎉** 装備によるライフ補強が非常に優秀です。 |
| **Evasion (回避)** | **1,698** | **8,527** | 参考ビルド（約8.5k）と比較するとまだ大幅な開きがあります。防具をEvasionベースに統一する必要があります。 |
| **Deflection Rating** | **203 (確率5%)** | **10,232 (確率55%)** | デフレクション率が5%に留まっています。頭・胴・足での「Evasionの21%をDeflectionに変換」するModを揃える必要があります。 |
| **雷耐性 (Lightning Res)** | **75% (+1% over) 🎉** | **76%** | **完璧にキャップ到達を維持しています。** |
| **火耐性 (Fire Res)** | **67%** | **75%** | あと8%不足しています。キャップ（75%）にするための微調整が必要です。 |
| **冷気耐性 (Cold Res)** | **75% (+8% over) 🎉** | **75%** | **完全にキャップ到達しています。** |
| **カオス耐性 (Chaos Res)** | **43% 🎉** | **17%** | **参考ビルドを大きく上回っています！** 非常に安全性が高まっています。 |

### 🔮 ジェム（スキル・サポートジェム）の比較

#### 1. メインスキル: Twister (竜巻)
*   **参考ビルド**: `Twister` (Lv20/Q20) ＋ `Pinpoint Critical`, `Projectile Acceleration III`, `Elemental Armament II`, `Prolonged Duration II`, `Rakiata's Flow`
*   **ユーザービルド**: `Twister` (Lv16/Q10) ＋ `Retreat III`, `Frost Nexus`, `Elemental Armament II`, `Projectile Acceleration III`, `Salvo` (5リンク)
*   **ギャップ**: 
    *   ジェムレベルが16に成長し、サポートに `Salvo` (サルヴォ) が追加されて5リンクになりました！火力が大幅に向上しています。
    *   さらなるダメージ向上のため、火力サポートの **`Rakiata's Flow` (ラキアタの波動)** や **`Pinpoint Critical`** への入れ替えが有効です。

#### 2. オーラ・バフ・ミニオン (Spirit / Reserved)
*   **参考ビルド**: `Purity of Ice` (Lv17/武器から獲得), `Herald of Ice` (Lv10), `Wild Protector` (Lv20) ＋ `Meat Shield II`
*   **ユーザービルド**: `Herald of Thunder` (Lv16), `Herald of Ice` (Lv12), `Combat Frenzy` (Lv12), `Malice` (Lv8)
*   **ギャップ**: 
    *   参考ビルドはミニオン `Wild Protector`（野生の守護者）に `Meat Shield`（肉壁）を繋いで**頑強なデコイ**として召喚し、敵のヘイト（タゲ）を逸らして安全に攻撃していますが、ユーザーはまだデコイミニオンを運用していません。

---

## 5. 総合優先度ランキング

| 順位 | 項目 | 具体的なアクション | 理由 |
| :---: | :--- | :--- | :--- |
| **1位** | **火耐性のキャップ（75%）到達** | ・装備の空き枠でのクラフト、またはルーンで火耐性をあと8%補強する | 即死を防ぐための最優先事項です。雷・冷気は完璧なので、ここを75%にすれば防御面が安定します。 |
| **2位** | **メイン火力槍の物理特化への更新** &<br>**Dex 157の確保** | ・物理DPSが高い **Akoyan Spear** (pdps 150+) を購入する<br>・装備に必要な **Dexを+20** 装備やツリーで補う | 現在は属性フラットダメージの高い槍ですが、Twisterの火力を飛躍的に伸ばすには物理DPS特化の Akoyan Spear への移行が最優先です。 |
| **3位** | **スワップ槍の高速ベースへの切り替え** | ・所持している場合は **Winged Spear**（アタスピ25%）に装備を切り替える（未所持の場合は購入） | すでにスワップ設定はされていますが、スワップ槍をさらに高速な Winged Spear に変更することで、移動モーションが劇的に速くなります。 |
| **4位** | **Evasion（回避）防具化** &<br>**デフレクション変換ルーン/Mod** | ・頭・胴・足で「回避の21%をデフレクションに変換」を積む<br>・Evasion値をさらに伸ばす | 回避値は1,698まで伸びましたが、変換がないためデフレクション率が5%に留まっています。変換を積むことで物理被ダメージを激減させられます。 |
| **5位** | サポートジェムの最適化<br>(**`Rakiata's Flow` 等**) | ・Twisterのサポートから `Retreat` や `Frost Nexus` を外す<br>・火力サポートの **`Rakiata's Flow`** と **`Pinpoint Critical`** を導入する | 5リンク化は完了しましたが、ユーティリティ用サポートを火力特化（属性貫通・クリティカル）に入れ替えることで、Twisterのダメージ  がさらに跳ね上がります。 |
| **6位** | Intの確保 &<br>**デコイミニオン of 導入** | ・Intを100〜130程度まで確保する (現在65)<br>·**`Wild Protector` ＋ `Meat Shield`** をリンクして召喚する | 高レベルのオーラを有効化し、頑強な肉壁ミニオンを囮（デコイ）として運用することで、被弾を大きく減らして安全に攻撃できます。 |
| **7位** | ユニークベルト<br>**`Ingenuity` の導入** | ・ユニークベルト `Ingenuity Utility Belt` を購入する | 優秀なレアベルト（Soul Cord）があるため急ぎませんが、最終的な火力と耐久力（指輪強化＋チャームスロット拡張）の限界突破に必要です。 |

---

## 6. クリティカルビルドへの移行ロードマップ

エンドゲーム（マップ以降）で高難度コンテンツをスムーズに攻略するためには、ダメージ倍率が跳ね上がる **クリティカルビルド（Crit Build）** への移行が不可欠です。

### 📅 移行のステップとチェックリスト

#### STEP 1: 基礎命中率 (Accuracy) の確保 (最優先)
*   **目標**: キャラクター画面での **命中率（Hit Chance）を 95%〜100%** に維持する（現在は100%で完璧です）。
*   **対策**: 今後装備を更新する際も、Accuracyが下がりすぎないように注意します。

#### STEP 2: 武器のベースクリティカル率 (Local Crit) の更新
*   **目標**: 武器自体に **`+ #% to Critical Hit Chance` (ローカルクリティカル率追加)** のModが付いた槍を装備する。
*   **ベースタイプ**: `Akoyan Spear` など、ベースの基礎クリティカル率が高い槍を採用します（参考ビルドは `+4.71% to Critical Hit Chance` を武器に付与しています）。

#### STEP 3: パッシブツリーの再配分 (リスペック)
*   レベル75〜80に達したら、アクト中で取得していた「非クリティカル用の単純なダメージノード」を削り、クリティカル関連ノードに振り分けます。

#### STEP 4: 各種チャージ（Power / Frenzy）の生成機構の導入
*   `Barrage`（バラージ）などの多段ヒットスキルに **`Perpetual Charge`** などのサポートジェムを繋ぎ、戦闘中にチャージを自動で維持できるようにします（参考ビルドのスキル構成を参照）。

#### STEP 5: 防具・アクセサリーでの「クリティカル倍率」の補強
*   クリティカル率が十分に確保できたら、次はダメージを何倍にも膨らませる **「クリティカルダメージ（Critical Damage Bonus / Multiplier）」** を装備で稼ぎます。
*   **手袋 / アミュレット**: `increased Critical Damage Bonus` のMod付き

---

## 7. 武器セット2（スワップ）のスピアとユニーク槍検索・火力スケールガイド

ユーザーから提示されたPoBデータを元に、Huntress (Spirit Walker) ビルドで「武器セット2（スワップ用武器セット）」として装備すべきユニーク槍の選定、検索用URL、および火力を最大化するためのスケール手法をまとめました。

### ⚔️ 武器セット2（スワップ）に装備するスピアの選定と検索URL

PoE2のスピアHuntress（Spirit Walker）ビルドにおいて、武器セット2（Swap）は通常「移動スキルの高速化」「Spiritの確保」または「一時的な強力なバフスキルの発動」に使用されます。

スワップ武器として最も推奨されるユニーク槍は **Atziri's Contempt (Pronged Spear)** です。この槍が付与する専用スキル **Shattering Spite** は、物理・出血ダメージを大幅に引き上げるバフを展開するため、戦闘開始時やボス戦直前にスワップして発動するローテーションが非常に強力です。

以下に、PoE2公式トレードサイトで同様のユニーク槍を即座にオンライン検索するためのURL（セッションID不要で誰でも直接開けるクエリ埋め込み型URL）を用意しました。

*   **Atziri's Contempt (Pronged Spear)** (バフ・物理・出血特化スワップ槍)
    [👉 Atziri's Contempt をトレードで検索する](https://www.pathofexile.com/trade2/search/poe2/Early%20Access?q=%7B%22query%22%3A%7B%22status%22%3A%7B%22option%22%3A%22online%22%7D%2C%22name%22%3A%22Atziri%27s%20Contempt%22%2C%22type%22%3A%22Pronged%20Spear%22%2C%22rarity%22%3A%22unique%22%7D%7D)
*   **Daevata's Wind (War Spear)** (近接/投射物ハイブリッド・アタスピ強化槍)
    [👉 Daevata's Wind をトレードで検索する](https://www.pathofexile.com/trade2/search/poe2/Early%20Access?q=%7B%22query%22%3A%7B%22status%22%3A%7B%22option%22%3A%22online%22%7D%2C%22name%22%3A%22Daevata%27s%20Wind%22%2C%22type%22%3A%22War%20Spear%22%2C%22rarity%22%3A%22unique%22%7D%7D)
*   **Chainsting (Hunting Spear)** (投射物速度・Pin蓄積強化槍)
    [👉 Chainsting をトレードで検索する](https://www.pathofexile.com/trade2/search/poe2/Early%20Access?q=%7B%22query%22%3A%7B%22status%22%3A%7B%22option%22%3A%22online%22%7D%2C%22name%22%3A%22Chainsting%22%2C%22type%22%3A%22Hunting%20Spear%22%2C%22rarity%22%3A%22unique%22%7D%7D)
*   **Skysliver (Winged Spear)** (雷フラット・感電効果特化槍)
    [👉 Skysliver をトレードで検索する](https://www.pathofexile.com/trade2/search/poe2/Early%20Access?q=%7B%22query%22%3A%7B%22status%22%3A%7B%22option%22%3A%22online%22%7D%2C%22name%22%3A%22Skysliver%22%2C%22type%22%3A%22Winged%20Spear%22%2C%22rarity%22%3A%22unique%22%7D%7D)
*   **【一括検索】PoE2内の全ユニークスピア検索** (現在の全ユニーク槍の出品状況を一覧で確認)
    [👉 すべてのユニーク槍をトレードで一括検索する](https://www.pathofexile.com/trade2/search/poe2/Early%20Access?q=%7B%22query%22%3A%7B%22status%22%3A%7B%22option%22%3A%22online%22%7D%2C%22filters%22%3A%7B%22type_filters%22%3A%7B%22filters%22%3A%7B%22category%22%3A%7B%22option%22%3A%22weapon.spear%22%7D%2C%22rarity%22%3A%22unique%22%7D%7D%7D%7D%7D)

---

### 📈 スピアHuntressの火力をスケールする主要Modと手法

槍ビルド（特にSpirit Walker）で火力を最大化するために、優先して集めるべきModとその役割を詳しく解説します。

#### 1. 攻撃に追加されるフラットダメージ (Adds # to # Damage to Attacks)
*   **対象Mod**: `Adds # to # Physical Damage to Attacks` / `Adds # to # Cold/Lightning/Fire damage to Attacks`
*   **付与部位**: 指輪、アミュレット、手袋、武器ローカル
*   **スケール理由**: Huntressは攻撃速度が非常に速いため、ヒットごとに固定ダメージが上乗せされる「フラットダメージ」の価値が極めて高いです。特に物理・冷気ビルドであれば、物理および冷気のフラット値を優先します。

#### 2. 武器およびグローバルの攻撃速度 (Attack Speed)
*   **対象Mod**: `#% increased Attack Speed`
*   **付与部位**: 武器ローカル (必須)、手袋、指輪、パッシブ
*   **スケール理由**: 手数を増やして `Whirling Slash` や `Barrage` のヒット数を稼ぐことは、Owl Spiritによるフェザー生成や `Twister`（竜巻）の発生確率を最大化させるために直結します。

#### 3. クリティカル率と倍率 (Crit Chance & Multiplier)
*   **対象Mod**:
    *   `+#% to Critical Hit Chance` (武器自体の基礎クリ率を底上げするローカルMod、最重要)
    *   `#% increased Critical Damage Bonus` (クリティカル時のダメージを跳ね上げる倍率Mod)
*   **付与部位**: 武器 (Crit Chance)、手袋、アミュレット、パッシブ
*   **スケール理由**: エンドゲームでの最大のスケール要素です。特に物理ベースの `Akoyan Spear` にローカルクリ率を付けて基礎クリ率を高め、防具やアクセサリーで倍率（Multiplier）を稼ぐことで、火力が乗算で伸びてしていきます。

#### 4. 投射物関連のMod (Projectile Mods)
*   **対象Mod**: `+# to Level of all Projectile Skills` / `Projectile Damage` / `Projectile Speed`
*   **付与部位**: アミュレット、パッシブ、ジュエル
*   **スケール理由**: メイン火力スキルである `Twister` や、スワップバフからの投射物スキルはすべて投射物（Projectile）タグを持ちます。特にアミュレットの「投射物スキルレベル +2」はベースダメージが爆発的に伸びるため強力です。また、`Projectile Speed` は Twister の移動速度と射程を伸ばし、クリア速度を格段に上げます。

#### 5. PoE2特有のデバフ・状態異常メカニズム
*   **感電 (Shock)**: 雷ダメージ（Lightning Spear等）を主軸にする場合、敵に付与する Shock の効果量（Shock Effectiveness）をスケールすることで、敵の被ダメージを最大 50% 以上増幅できます。
*   **固定 (Pin Buildup)**: 一部の槍スキルやModで発生する「Pin（固定）」の蓄積速度を高め、敵の足を止めつつ大ダメージを与えるチャンスを作ります。
*   **Bloodstone Lance**: `Atziri's Contempt` スピアから得られるスタック。敵に出血を伴う槍撃を当ててスタックを消費することで、圧倒的な単体物理DPSを発揮します。
