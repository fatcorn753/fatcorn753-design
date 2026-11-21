[brief.md](brief.md) の前提に沿って、6項目を簡潔にまとめます。確かさは `[確立]` `[通説]` `[意見]` で示します。

---

## (1) OKLCH での段階作成と Radix / Material 3 / Tailwind v4 の比較

### OKLCH で 50〜950 を作る手順
- **知覚均等な明度設計** `[確立]`：OKLCH は Oklab に基づく円筒色空間で、明度 `L`（0〜1）、彩度 `C`（0〜約0.37）、色相 `H`（0〜360°）が人間の知覚と一致するため、`L` を揃えるだけで異色相間の見た目の明るさとコントラスト予測が安定します（Björn Ottosson, *A perceptual color space for image processing*, https://bottosson.github.io/posts/oklab/ / Andrey Sitnik & Travis Turner, Evil Martians, *OKLCH in CSS: why we moved from RGB and HSL*, https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl ）。
- **段階生成の実務パターン** `[通説]`：`50〜950`（11段階）を作る場合、`L` を `0.98`→`0.18` 付近へ非線形（明端・暗端を細かく）に配置し、`C` は中間明度（`500〜600`）を頂点に両端で `0.01〜0.03` へ絞る**釣鐘型カーブ**にします。高彩度で sRGB 色域外に出る箇所は `C` をクリップし、黄（`H≈80〜100°`）や青では暗端でわずかに色相を傾けて濁りを防ぎます（Evil Martians, 同上 / Tailwind CSS v4 実装, https://tailwindcss.com/docs/colors ）。

### 3大システムの比較

| 観点 | Radix Colors | Material Design 3 (HCT) | Tailwind CSS v4 |
| :--- | :--- | :--- | :--- |
| **色空間** | sRGB/P3 ベースで視覚調整・APCA 検証 `[確立]` | **HCT**（CAM16 の H/C + CIELAB 相当の Tone 0〜100）`[確立]` | **OKLCH**（P3 対応）`[確立]` |
| **段階数** | **12段階**（1〜12。Light/Dark/Alpha 別定義）`[確立]` | **13トーン**（0,10,20,30,40,50,60,70,80,90,95,99,100＋サーフェス用 4,6,12,17,22,87,92,94,96,98）`[確立]` | **11段階**（50〜950）`[確立]` |
| **設計思想** | **番号＝用途固定**（1–2背景、3–5要素背景、6–8枠線、9–10塗り、11–12文字）`[確立]` | **アルゴリズム自動生成＋コントラスト保証**（Tone差 40 で ≥3:1、Tone差 50 で ≥4.5:1）`[確立]` | **汎用パレット＋CSS変数**（用途は利用者が自由に割り当て）`[確立]` |
| **出典** | Radix Colors *Understanding the scale*, https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale | Material Design 3 *How the system works*, https://m3.material.io/styles/color/system/how-the-system-works | Tailwind CSS *Colors*, https://tailwindcss.com/docs/colors |

- **使い分けの要点** `[意見]`：AI（Claude Code）に毎回破綻なく使わせるテンプレートには、**「番号＝用途」が固定された Radix 型**か**「役割名＝トークン」が固定された M3 型**が有利です。自由度の高い Tailwind の `50〜950` をそのまま渡すと、毎回 AI が違う番号を選びやすく一貫性が崩れます（出典なし）。

---

## (2) わずかに色味を帯びたニュートラル（Warm Gray）の作り方

- **OKLCH での具体値** `[通説]`：色相 `H` を黄〜橙寄り（`60°〜95°`、苔寄りなら `95°〜115°`）に固定し、彩度 `C` を **`0.003〜0.012`** の極低域に抑えます。実例として Tailwind v4 の `stone` は `stone-50: oklch(98.5% 0.001 106.4)`、`stone-950: oklch(14.7% 0.004 49.3)` と `C ≤ 0.01` に収めています（Tailwind CSS *Colors*, https://tailwindcss.com/docs/colors ）。
- **Natural Pairing（色相調和）** `[確立]`：Radix Colors は無彩色（`gray`）のほかに色味付きグレーを用意し、黄・琥珀・茶系には **`sand`（黄系）**、草・ライム系には **`olive`（黄緑系）**、緑系には **`sage`（緑系）** を合わせる「Natural Pairing」を推奨しています（Radix Colors *Composing a palette*, https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette ）。
- **多色 UI での注意点** `[確立]`：Radix 公式も注意喚起している通り、特に**ダークモードで背景グレーの彩度を上げすぎる（目安 `C > 0.012`）と、上に乗る青・赤・緑のセマンティック色と濁って衝突**します（Radix Colors *Composing a palette*, 同上 / 閾値目安は `[意見]` 出典なし）。明端（`L≥0.96`）と暗端（`L≤0.22`）ほど `C` を `0.004〜0.008` に抑えると「静か＋温かい」が保てます `[意見]`（出典なし）。

---

## (3) ダークモード設計の原則

1. **真っ黒（`#000000`）と真っ白（`#FFFFFF`）を避ける** `[確立]`
   - 真っ黒背景＋真っ白文字の極端なコントラスト（21:1）は、乱視を持つ人などで文字が滲んで見える**ハレーション**を起こしやすく、通常視力でも暗背景は明背景より読書パフォーマンスが下がる研究結果が報告されています（Raluca Budiu, Nielsen Norman Group, *Dark Mode vs. Light Mode: Which Is Better?*, https://www.nngroup.com/articles/dark-mode-vs-light-mode/ ）。
   - Material 2 は基準サーフェスを **`#121212`**（OKLCH で `L≈0.18`）に設定しています（Material Design 2 *Dark theme*, https://m2.material.io/design/color/dark-theme.html ）。文字も `#FFFFFF` ではなく白 87%（本文）/ 60%（補助）または `L=0.90〜0.93` 程度のオフホワイトにします（同上 / OKLCH 換算は出典なし）。
2. **影ではなく「明るさの段差（Tonal Elevation）」で奥行きを出す** `[確立]`
   - 暗い背景上ではドロップシャドウがほとんど視認できないため、**手前（高い要素）ほど明るく**して階層を表現します（Apple HIG *Dark Mode*, https://developer.apple.com/design/human-interface-guidelines/dark-mode / Material Design 2 *Dark theme*, 同上）。
   - **Material 2（Elevation Overlay）** `[確立]`：`#121212` に半透明白を重ねて明度を上げる方式。`0dp: 0%`、`1dp(カード): 5%`、`4dp(バー): 9%`、`8dp(メニュー): 12%`、`16dp(シート): 15%`、`24dp(ダイアログ): 16%`（Material Design 2 *Dark theme*, 同上）。
   - **Material 3（Surface Container Roles）** `[確立]`：半透明重ね掛けを廃止し、Neutral トーンで固定段階を定義。ダーク時は `surfaceContainerLowest: Tone 4`、`surface: Tone 6`、`Low: Tone 10`、`Default: Tone 12`、`High: Tone 17`、`Highest: Tone 22`（ライト時は `100 / 98 / 96 / 94 / 92 / 90`）（Material Design 3 *Color roles*, https://m3.material.io/styles/color/roles ）。
3. **アクセント色の明度を上げ、彩度を下げる** `[確立]`
   - ライト用の高彩度・中明度色（Material の `500` 番台など）をダーク背景に置くと視覚的振動（ハレーション）とコントラスト不足を招くため、Material 2 は **`200` 番台（低彩度・高明度）** への切り替え、Material 3 は Primary をライト `Tone 40` → ダーク `Tone 80`（上の文字は `Tone 20`）へ切り替える規則を採っています（Material Design 2 *Dark theme*, 同上 / Material Design 3 *Color roles*, 同上）。
4. **端末設定を尊重する** `[確立]`
   - ユーザーはアプリ個別ではなく OS 全体でライト／ダークを管理するメンタルモデルを持つため、`prefers-color-scheme` への追従を既定にすべきです（Apple HIG *Dark Mode*, 同上 / Tanner Kohler & Amy Zhang, NN/g, *Dark Mode: How Users Think About It and Issues to Avoid*, https://www.nngroup.com/articles/dark-mode-usability/ ）。

---

## (4) 成功・注意・エラーの色をアクセント色と紛れさせない方法

### 共通原則
1. **トークン層を分離する** `[通説]`：`--accent-*`（操作・選択・ブランド）と `--status-success/warning/error-*`（システム状態）を別トークンにし、仮に色が近くても直接参照しません（Design Systems 実務通説。例：Radix/M3 の Role 分離, https://m3.material.io/styles/color/roles ）。
2. **色だけに頼らない（マルチモーダル表現）** `[確立]`：WCAG 2.2 の **1.4.1（色の使用・レベル A）** に従い、状態には必ず**アイコン（チェック／三角警告／円×）・文言・枠線構造**を併用します（W3C, *Understanding SC 1.4.1: Use of Color*, https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html ）。
3. **塗り面積の役割を分ける** `[意見]`：アクセント色は「主ボタン・選択中タブ・フォーカスリング」に使い、状態色は原則「薄いティント背景＋濃い文字＋アイコン＋細い枠（バッジ／バナー／インラインメッセージ）」に限定すると、色相が近くても機能上の誤認が激減します（出典なし）。

### アクセント別の分離策
- **アクセントが「苔（`#4F6B3A`, `H≈133°`）」の場合の成功色** `[通説]`＋`[意見]`
  - 苔は黄みのある低彩度グリーン（`H≈133°, C≈0.08`）なので、成功色は **青緑（ティール／ジェイド寄り `H≈162°〜168°`）へ約 `30°` ずらし、彩度をやや高く（`C≈0.10〜0.12`）** 設定して区別します（色相・彩度分離の実務通説＋具体的数値は `[意見]` 出典なし）。
  - さらに習慣・記録アプリの「完了チェック」は、システム通知の「成功」と意味が重なるため、「完了」には苔を使っても破綻しにくい一方、フォーム保存や通信成功のトーストには青緑＋チェックアイコンを割り当てると整理できます `[意見]`（出典なし）。
- **アクセントが「琥珀（`#9A5B13`, `H≈63°`）」の場合の注意色** `[通説]`＋`[意見]`
  - 琥珀は橙〜茶寄り（`H≈63°`）なので、注意色は **黄寄り（`H≈85°〜92°`）へ約 `+25°` ずらし**ます（具体的数値は `[意見]` 出典なし）。
  - 黄色単体は白背景でコントラスト不足になりやすいため、`[通説]` **背景を淡い黄（`L≈0.95`）、文字・アイコンを暗い黄土（`L≈0.45〜0.48`）、枠線を中明度黄（`L≈0.75`）** の3段構成にし、三角警告アイコンを必須にします（警告黄のアクセシビリティ対策は実務通説、WCAG 1.4.3/1.4.11 準拠）。
  - またエラー色（赤）も琥珀（`63°`）と近くならないよう、橙寄り赤ではなく **やや深いクリムゾン／レンガ赤（`H≈22°〜26°`）** にして `35°〜40°` 離します `[意見]`（出典なし）。

---

## (5) WCAG 2.2 と APCA のコントラスト基準の違い

| 比較項目 | WCAG 2.2 | APCA（WCAG 3 候補アルゴリズム） |
| :--- | :--- | :--- |
| **法的位置づけ** | 現行の国際標準・法的準拠基準（JIS X 8341-3 等と整合）`[確立]` | WCAG 3 ドラフト向けの先進アルゴリズム（現行 WCAG 2.2 では非必須）`[確立]` |
| **計算式と指標** | sRGB 相対輝度の比率 **`1:1 〜 21:1`** `[確立]` | 人間の知覚モデルに基づく **`Lc 0 〜 ±106`**（Lightness Contrast）`[確立]` |
| **極性（Light/Dark）** | **対称**（白地黒字と黒地白字が同じ数値）`[確立]` | **非対称**（明地暗字は正 `+Lc`、暗地明字は負 `-Lc` で別曲線）`[確立]` |
| **フォント依存性** | 2区分のみ（通常文字 vs 大きい文字 `18pt=24px` 以上または `14pt=18.67px` 太字）`[確立]` | **サイズ×ウェイトのルックアップ表**で連続的に要求値が変化 `[確立]` |
| **主な基準値** | **1.4.3(AA):** 通常 `4.5:1` / 大 `3:1`<br>**1.4.6(AAA):** 通常 `7:1` / 大 `4.5:1`<br>**1.4.11(AA):** UI部品・図形 `3:1` `[確立]` | **Lc 90:** 高可読本文・小文字<br>**Lc 75:** 標準本文の最低線<br>**Lc 60:** 本文以外の可読文字・太字見出し<br>**Lc 45:** 大見出し・UI境界<br>**Lc 30:** 特大見出し・プレースホルダ下限 `[確立]` |
| **弱点** | 暗背景で読みにくい組合せが通り、逆に視認性の高い橙・琥珀のボタン白文字が落ちやすい（通称オレンジ問題）`[確立]` | まだ法的標準ではなく、自動監査ツール（axe/Lighthouse 既定）は WCAG 2.2 基準 `[確立]` |

- **出典**: W3C WCAG 2.2 *Understanding SC 1.4.3 / 1.4.6 / 1.4.11*, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html , https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html / Andrew Somers (Myndex), *APCA in a Nutshell*, https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell , https://github.com/Myndex/SAPC-APCA
- **日本語 UI での補足** `[通説]`：漢字はラテン文字より画数が多く空間周波数が高いため、日本語の本文（14〜16px）では WCAG AA `4.5:1` ギリギリではなく **`7:1` 以上（APCA `|Lc| ≥ 75〜90`）** を目指すと可読性が安定します（Andrew Somers の空間周波数議論と同旨、日本語での具体的推奨は `[意見]` 出典なし）。

---

## (6) 苔と琥珀の具体的なパレット案（静か＋温かい）

いずれも `[意見]`（本コンセプト向け独自設計・出典なし。コントラスト比は sRGB 相対輝度による計算値）。
基準シードの実測 OKLCH は **苔 `#4F6B3A` = `oklch(0.493 0.081 133)`（対白 `6.0:1`）**、**琥珀 `#9A5B13` = `oklch(0.532 0.114 62.6)`（対白 `5.4:1`）** です。

### 共通のニュートラル骨格（Warm Gray）
- 苔には **`H=98°`**（ごく微かな黄緑〜生成り寄り）、琥珀には **`H=80°`**（砂・紙寄り）を使い、明度 `L` と彩度 `C` は共通化できます。

| 役割トークン | Light (`oklch`) | Dark (`oklch`) | 狙い・コントラスト目安 |
| :--- | :--- | :--- | :--- |
| `bg-canvas`（アプリ地） | `oklch(0.985 0.004 H)` | `oklch(0.180 0.005 H)` | 紙のような白／`#121212` 相当の温黒 |
| `bg-surface`（カード） | `oklch(0.996 0.002 H)` | `oklch(0.220 0.006 H)` | Light は浮き白＋細線、Dark は +0.04 明度差 |
| `bg-subtle`（サイドバー/入力） | `oklch(0.955 0.006 H)` | `oklch(0.260 0.007 H)` | 領域分け・ホバー下地 |
| `bg-elevated`（モーダル/ポップ） | `oklch(1.000 0.000 0)` | `oklch(0.300 0.007 H)` | Dark 最上位サーフェス（M3 Tone 22 相当） |
| `border-subtle`（区切り線） | `oklch(0.890 0.008 H)` | `oklch(0.310 0.008 H)` | 静かな境界（非操作要素） |
| `border-control`（入力枠等） | `oklch(0.640 0.010 H)` | `oklch(0.530 0.010 H)` | 背景比 **≥3.2:1**（WCAG 1.4.11 準拠） |
| `text-primary`（本文） | `oklch(0.240 0.008 H)` | `oklch(0.920 0.006 H)` | **約15:1 / 約14:1**（ハレーション回避＋AAA） |
| `text-secondary`（補助） | `oklch(0.490 0.008 H)` | `oklch(0.730 0.008 H)` | **約6.0:1 / 約6.5〜7.2:1**（AA余裕・APCA Lc≥65） |

### 案 A：苔（Moss, Neutral `H=98°`, Accent `H=133°`）

| 役割トークン | Light (`oklch`) | Dark (`oklch`) | 備考 |
| :--- | :--- | :--- | :--- |
| `accent-solid`（主ボタン地） | `oklch(0.493 0.081 133)` (`#4F6B3A`) | `oklch(0.720 0.090 133)` | Light: 白文字と `6.0:1` / Dark: 暗文字 `L=0.18` と `~6.7:1` |
| `accent-solid-hover` | `oklch(0.440 0.085 133)` | `oklch(0.770 0.090 133)` | 押下感の段階差 `ΔL=0.05` |
| `accent-text`（リンク・アイコン） | `oklch(0.460 0.085 133)` | `oklch(0.740 0.095 133)` | キャンバス比 **≥6.5:1** |
| `accent-tint`（選択中背景） | `oklch(0.940 0.025 133)` | `oklch(0.270 0.032 133)` | 穏やかな選択ハイライト |
| `success-text` / `tint` | `oklch(0.46 0.10 165)` / `oklch(0.94 0.03 165)` | `oklch(0.74 0.10 165)` / `oklch(0.26 0.04 165)` | 青緑 `165°` で苔 `133°` と `+32°` 分離 |
| `warning-text` / `tint` | `oklch(0.49 0.12 75)` / `oklch(0.95 0.04 85)` | `oklch(0.78 0.11 80)` / `oklch(0.28 0.04 75)` | 温かい黄土＋淡い黄地＋三角アイコン |
| `error-text` / `tint` | `oklch(0.49 0.15 26)` / `oklch(0.95 0.03 26)` | `oklch(0.71 0.14 26)` / `oklch(0.27 0.05 26)` | レンガ寄りの落ち着いた赤 |

### 案 B：琥珀（Amber, Neutral `H=80°`, Accent `H=63°`）

| 役割トークン | Light (`oklch`) | Dark (`oklch`) | 備考 |
| :--- | :--- | :--- | :--- |
| `accent-solid`（主ボタン地） | `oklch(0.532 0.114 62.6)` (`#9A5B13`) | `oklch(0.750 0.115 68)` | Light: 白文字と `5.4:1` / Dark: 暗文字 `L=0.19` と `~7.0:1`（`+5°` で泥色回避） |
| `accent-solid-hover` | `oklch(0.480 0.115 61)` | `oklch(0.800 0.115 70)` | 段階差 `ΔL=0.05` |
| `accent-text`（リンク・アイコン） | `oklch(0.490 0.115 61)` | `oklch(0.760 0.115 68)` | キャンバス比 **≥6.0:1** |
| `accent-tint`（選択中背景） | `oklch(0.945 0.032 72)` | `oklch(0.275 0.038 65)` | 温かな蜂蜜系ティント |
| `success-text` / `tint` | `oklch(0.47 0.10 155)` / `oklch(0.94 0.03 155)` | `oklch(0.74 0.10 155)` / `oklch(0.26 0.04 155)` | 自然な深緑 `155°` |
| `warning-text` / `tint` | `oklch(0.48 0.11 88)` / `oklch(0.95 0.06 94)` | `oklch(0.82 0.12 92)` / `oklch(0.29 0.05 90)` | 黄寄り `88–94°` へ `+25°` ずらし＋淡黄地＋左線＋三角アイコン |
| `error-text` / `tint` | `oklch(0.49 0.16 24)` / `oklch(0.95 0.03 24)` | `oklch(0.70 0.15 24)` / `oklch(0.27 0.05 24)` | 琥珀 `63°` から `-39°` 離した深い朱赤 |

---

## brief.md のコンセプトに当てはめた推奨

すべて `[意見]`（上の根拠を組み合わせた設計推奨・出典なし）。

1. **トークン設計は「OKLCH 定義 × 役割トークン（Radix/M3 ハイブリッド）」にする**
   - Claude Code には `50〜950` ではなく、上の表のような **約20個のセマンティックトークン名**（`bg-canvas/surface/subtle/elevated`、`border-subtle/control`、`text-primary/secondary`、`accent-*`、`success/warning/error-*`）だけを公開します。AI が毎回正しいコントラストとダーク対応を維持できます。
2. **ダークモードは「M3 型の4段サーフェス（`L=0.18 / 0.22 / 0.26 / 0.30`）＋ `prefers-color-scheme` 既定」にする**
   - PWA / Android を含むため、Android（Material 3）の設計言語とも整合します。影はライトで控えめに使い、ダークでは影をほぼ消して `L` の段差と極細枠（`border-subtle`）で奥行きを出します。
3. **コントラスト基準は「WCAG 2.2 AA を必須ゲート、本文は APCA `|Lc| ≥ 75` を目標」の二段構えにする**
   - 機械検証（WCAG 2.2: 文字 `4.5:1`・UI枠 `3:1`）を最低条件とし、日本語の標準書体（14〜16px）の本文と補助文字は `6:1〜15:1`（APCA `|Lc| 70〜100`）に収めると長時間の業務利用でも疲れにくくなります。
4. **「苔」か「琥珀」かの選び方（コンセプト適合度）**
   - **「静けさ（Things 3 / iA Writer）＋業務・記録での長時間閲覧」を優先するなら苔（`#4F6B3A`）がやや有利**：彩度が `C≈0.08` と低く目が疲れにくく、成功色（青緑 `165°`）・注意色（黄土 `75°`）・エラー色（赤 `26°`）の3状態すべてと色相を無理なく分離できます。またダークモードで明度を上げても濁りにくいです。
   - **「温かさ（Airbnb / Headspace）＋個人の習慣アプリの愛着」を優先するなら琥珀（`#9A5B13`）が有利**：紙とインクのような温もりが強く出ます。ただし警告色との近さを避けるため、警告 UI は必ず「淡黄背景＋三角アイコン」のコンポーネント規則とセットで運用してください。
   - **両案とも Neutral 骨格の明度・彩度構造が完全に同一**なので、最初はテンプレートの CSS 変数で `H` と数個のアクセント値だけを切り替えられるテーマスイッチとして設計しておくと、実画面で比較して後から確定できます。
