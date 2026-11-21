[brief.md](brief.md) の前提に沿って、5項目を根拠・確かさ（`確立` / `通説` / `意見`）・具体値つきでまとめ、最後にコンセプト適合の推奨案を示します。

---

## 1. UI アニメーションの時間と easing の根拠

* **人間工学的上限（Nielsen Norman Group）** `[確立]`
  * **100ms** は「即時反応」、**1,000ms（1s）** は思考の流れが途切れない上限（Jakob Nielsen, [*Response Times: The 3 Important Limits*](https://www.nngroup.com/articles/response-times-3-important-limits/)）。
  * UI アニメーションの適正範囲は **100〜400ms**。小さな変化・マイクロインタラクションは **200〜300ms**、**500ms 以上**は日常操作で遅く感じられやすい。距離・面積が大きいほど長く、**退出（exit）は進入（enter）より短く**する（Page Laubheimer / NN/g, [*Executing UX Animations: Duration and Motion Characteristics*](https://www.nngroup.com/articles/animation-duration/)）。
* **Material Design 3（Google）** `[確立]`
  * **時間・イージングトークン**：Duration は 50ms 刻みの 16 段階（Short1–4: `50/100/150/200ms`、Medium1–4: `250/300/350/400ms`、Long1–4: `450–600ms`、ExtraLong1–4: `700–1000ms`）。Easing は Standard `cubic-bezier(0.2, 0, 0, 1)`（Decelerate `0, 0, 0, 1` / Accelerate `0.3, 0, 1, 1`）と Emphasized Decelerate `cubic-bezier(0.05, 0.7, 0.1, 1)` / Accelerate `cubic-bezier(0.3, 0, 0.8, 0.15)`（Google, [Material 3 Motion: Easing and duration](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)）。
  * **物理ベース Spring（M3 Expressive）**：位置・サイズ・形状用の **Spatial spring**（オーバーシュート可）と、色・不透明度・影用の **Effects spring**（減衰比 `1.0`・**オーバーシュート禁止**）を分離し、Fast / Default / Slow の3段階 × Standard / Expressive スキームで使い分ける（Google, [Material 3 Motion: Overview / Specs](https://m3.material.io/styles/motion/overview/specs)）。
* **IBM Carbon Design System** `[確立]`
  * 業務タスク向けの **Productive** と演出向けの **Expressive** の二系統。Duration は 6 段階（`fast-01: 70ms`, `fast-02: 110ms`, `moderate-01: 150ms`, `moderate-02: 240ms`, `slow-01: 400ms`, `slow-02: 700ms`）。
  * Productive カーブは Standard `cubic-bezier(0.2, 0, 0.38, 0.9)`、Entrance `cubic-bezier(0, 0, 0.38, 0.9)`、Exit `cubic-bezier(0.2, 0, 1, 0.9)`。Expressive は Standard `cubic-bezier(0.4, 0.14, 0.3, 1)`（IBM, [Carbon Design System — Motion](https://carbondesignsystem.com/elements/motion/overview/)）。
* **Apple HIG / WWDC23** `[確立]`
  * バネを質量・剛性ではなく **知覚時間 `duration`** と **弾み `bounce`**（`0`＝臨界減衰で弾みなし、正値でオーバーシュート）の 2 パラメータで設計する。動きは目的性（空間関係・フィードバック）と中断可能性を重視（Apple, [Human Interface Guidelines — Motion](https://developer.apple.com/design/human-interface-guidelines/motion); WWDC23 Session 10158 [*Animate with springs*](https://developer.apple.com/videos/play/wwdc2023/10158/)）。

---

## 2. Spring アニメーションの CSS 近似（`cubic-bezier()` と `linear()`）

* **`cubic-bezier()` による近似** `[確立]`
  * 制御点 y を `1` 超にすることで**1回だけのオーバーシュート**を近似できる（例：`cubic-bezier(0.34, 1.56, 0.64, 1)` や控えめな `cubic-bezier(0.22, 1.15, 0.36, 1)`）。3次ベジェの数学的制約上、**複数回の減衰振動は表現不可**（MDN, [`<easing-function>`](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function)）。
* **`linear()` による近似** `[確立]`
  * 減衰調和振動子（stiffness / damping / mass）の解をビルド時やジェネレータで 20〜60 点ほどサンプリングし、折れ線補間として CSS 変数に格納する。Chrome 113+ / Edge 113+ / Firefox 112+ / Safari 17.2+ で **Baseline Widely available**（MDN, [`linear()`](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear); Jake Archibald / Chrome for Developers, [*Create complex animation curves in CSS with the linear() easing function*](https://developer.chrome.com/docs/css-ui/css-linear-easing-function)）。
* **CSS 近似の限界** `[確立]`
  * どちらも**時間固定**であり、物理エンジンのように移動距離やドラッグ初速に応じて所要時間が変わらず、途中中断時に速度（momentum）を継承できない（Chrome for Developers 同上; Josh W. Comeau, [*A Friendly Introduction to Spring Physics*](https://www.joshwcomeau.com/animation/a-friendly-introduction-to-spring-physics/)）。
  * そのため、**クリック／トグル等の離散状態遷移は `linear()`、ドラッグ追従のみ JS 物理エンジン**とする使い分けが合理的 `[通説]`（出典なし：実務上の帰結）。

---

## 3. `prefers-reduced-motion` の正しい対応

* **一括停止（`animation: none !important`）は避ける** `[確立]`
  * 前庭障害（めまい・吐き気）を誘発する主因は、画面を横切る大きな移動・ズーム・回転・パララックス。すべての遷移を無条件に消すと「ダイアログがどこから出たか」「保存が完了したか」といった**状態変化の文脈まで失われる**（Thomas Steiner / web.dev, [*prefers-reduced-motion: Sometimes less movement is more*](https://web.dev/articles/prefers-reduced-motion); Apple HIG, [Motion](https://developer.apple.com/design/human-interface-guidelines/motion); W3C, [WCAG 2.1 SC 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)）。
* **正しい対応＝「止める」ではなく「置き換える」** `[確立]`
  1. `translate` / `scale` / `rotate` / バウンスを除去し、**`opacity` のクロスフェード（150〜200ms 程度）や色変化**に置換する（web.dev 同上; Apple HIG 同上）。
  2. パララックス、自動再生アニメーション、無限ループ装飾は停止する（WCAG 2.1 SC 2.2.2 / 2.3.3）。
  3. 実装は `@media (prefers-reduced-motion: no-preference)` 側に大きな空間移動を閉じ込める（Progressive Enhancement）か、`reduce` 側で `transform: none`＋`opacity` トランジションに差し替える（MDN, [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)）。

---

## 4. 日本語 UI の文字組み

### 本文の `font-size` / `line-height` / `letter-spacing` と `palt` の是非
* **`font-size`** `[確立]`：Web 本文の標準は **16px**。デジタル庁デザインシステムは本文 16px 以上を基本とし、14px 以下は補助情報や高密度な業務画面の例外と定義（デジタル庁, [タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/)）。
* **`line-height`** `[確立]`：単位なし数値で指定する。本文は **1.5〜1.75**（WCAG 2.1 SC 1.4.12 は 1.5 以上で破綻しないことを要求、デジタル庁は一般本文 `1.5〜1.75`、高密度業務一覧 `1.2〜1.3`、見出し `1.4`、1行ボタン `1.0`）（W3C, [WCAG 2.1 SC 1.4.12 Text Spacing](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html); デジタル庁 同上）。
* **`letter-spacing`** `[通説]`：日本語本文は **`0`〜`0.02em`（最大 `0.04em`）** 程度が可読性を損ねにくい。大見出しは `0`〜やや詰め（`-0.01em〜0`）。（デジタル庁 同上; 細部はデザインシステムごとの調整）
* **`font-feature-settings: "palt"` の是非** `[通説]`：
  * **見出し・短い UI ラベル**：間延びを抑え引き締まるため有効。
  * **本文全体**：**非推奨**。仮名や約物の幅が不均一になり行のリズム・黒味バランスが崩れやすく、メイリオ等の非対応フォントや OS 間の差が大きくなる（タイププロジェクト / FONTPLUS 等の実務知見; [MDN `font-feature-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings)）。

### 和欧混植と `text-autospace`
* W3C「日本語組版処理の要件（JLReq）」では和文と欧文・数字の間に原則 **四分アキ（全角の 1/4）** を設ける（W3C, [日本語組版処理の要件 (JLReq)](https://www.w3.org/TR/jlreq/)） `[確立]`。
* 手動の半角スペースはコピー＆ペーストや検索を汚すため、CSS **`text-autospace: normal`**（**Baseline 2025 Newly available**）を使うのが現代的正解（MDN, [`text-autospace`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-autospace)） `[確立]`。
* フォントスタックは**欧文フォントを先、和文フォントを後**に記述し、英数字を欧文グリフで描画させるのが定番 `[通説]`。

### System Font Stack（Mac / iOS / Windows / Android）
* `system-ui` 単独指定は日本語環境で OS/ブラウザにより意図しない古い UI フォントが当たる事例があり、明示的スタックが安全 `[通説]`。
* 主要 OS の標準書体 `[確立]`：
  * **macOS / iOS**：欧文 `-apple-system, BlinkMacSystemFont`（SF Pro）、和文 `"Hiragino Sans", "Hiragino Kaku Gothic ProN"`
  * **Windows 10/11**：欧文 `"Segoe UI"`、和文 `"BIZ UDPGothic"`（Win10/11 標準搭載の UD 書体）または `"Yu Gothic"` / `Meiryo`。Windows の游ゴシックは `font-weight: 400` で細くかすれやすいため、`BIZ UDPGothic` または `Yu Gothic Medium`・`Meiryo` の併用が実務上よく採られる `[通説]`。
  * **Android**：欧文 `Roboto`、和文 `"Noto Sans JP"`（`Noto Sans CJK JP`）

### `font-feature-settings` / `text-wrap` / 禁則 / `tabular-nums`
* **`font-feature-settings`** `[確立]`：下位プロパティのため、高水準プロパティ（`font-variant-numeric` 等）を優先し、高水準で代替できない `"palt"`（見出し限定）や `"chws"`（文脈依存の約物詰め）にのみ使う（MDN, [`font-feature-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings)）。
* **`text-wrap` と改行** `[確立]`：
  * 見出し：`text-wrap: balance`（各行の長さを均等化）。
  * 本文：`text-wrap: pretty`（段落末の孤児語・不自然な折り返しを抑制。Chrome/Edge 117+・Safari 26+ 対応、Firefox は安全にフォールバック）。
  * 文節改行：`word-break: auto-phrase`（`lang="ja"` 必須。Chrome/Edge 119+ のみ対応のため、見出し・カードタイトルへのプログレッシブ適用に留める）（MDN, [`text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap), [`word-break`](https://developer.mozilla.org/en-US/docs/Web/CSS/word-break)）。
* **禁則処理** `[確立]`：`line-break: strict`（JLReq 準拠で行頭禁則・小書き仮名等を厳格保護）に、`overflow-wrap: anywhere`（長大 URL 等のコンテナ溢れ防止）を併記する（MDN, [`line-break`](https://developer.mozilla.org/en-US/docs/Web/CSS/line-break); W3C, [JLReq](https://www.w3.org/TR/jlreq/)）。
* **数字の `tabular-nums`** `[確立]`：`font-variant-numeric: tabular-nums`（OpenType `tnum`）で数字 0–9 を等幅化。テーブル、金額、時刻、タイマー、習慣の連続日数などで桁揃えと更新時の横ブレを防ぐ（MDN, [`font-variant-numeric`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric)）。SF Pro / Segoe UI / Roboto のいずれも `tnum` 対応。

---

## 5. Type Scale（型の段階）の比率の実例

| 方式・システム | 比率 / 段階の実例（px 換算） | 特徴・向き | 出典・確かさ |
| :--- | :--- | :--- | :--- |
| **Major Second（1.125）** | `12 / 14 / 16 / 18 / 20 / 23 / 26` | 差が穏やか。業務ツール・ダッシュボード向き | 一般モジュラースケール `[通説]` |
| **Minor Third（1.200）** | `11 / 13 / 16 / 19 / 23 / 28 / 33` | 汎用バランス型。アプリ＋読み物両立 | 同上 `[通説]` |
| **Major Third（1.250）** | `13 / 16 / 20 / 25 / 31 / 39` | 強弱明確。マーケティング・LP 向き | 同上 `[通説]` |
| **IBM Carbon** | `12 / 14 / 16 / 18 / 20 / 24 / 28 / 32 / 36 / 42` | 12px 起点の段階式増分。Productive（本文14px）と Expressive（本文16px）を分離 | [Carbon Type sets](https://carbondesignsystem.com/elements/typography/type-sets/) `[確立]` |
| **Material 3** | Label `11/12/14`, Body `12/14/16`, Title `14/16/22`, Headline `24/28/32`, Display `36/45/57` | 役割別 15 トークン（光学調整） | [M3 Type scale tokens](https://m3.material.io/styles/typography/type-scale-tokens) `[確立]` |
| **Apple HIG (iOS)** | Caption `11/12`, Footnote `13`, Subhead `15`, Callout `16`, Body `17`, Title3–1 `20/22/28`, Large Title `34` (pt) | 光学調整＋Dynamic Type 前提 | [Apple HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography) `[確立]` |
| **デジタル庁** | 例外小 `12/14`, 本文基準 `16`, 見出し `20/24/28/32/36`, Display `45–64` | 日本語可読性重視（本文 16px 基準） | [デジタル庁 タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/) `[確立]` |

---

## コンセプト適合の推奨（テンプレート設計案）

[brief.md](brief.md) の「静か＋温かい」「業務・個人習慣アプリ（PWA/Android 含む）」「中間密度＋切替可能」「普段は短く、完了・切替でわずかに弾む」「端末標準書体・日本語中心」に当てはめた推奨です（設計判断部分は `[意見]`、根拠数値は上記 `[確立]` に基づく）。

### 1. モーショントークン推奨
* **普段の操作＝Carbon Productive 寄りの「静かで速い」カーブ**
  * `--dur-instant: 80ms`（hover / pressed / 色変化）
  * `--dur-fast: 150ms`（トグル、ドロップダウン、要素の退出）
  * `--dur-base: 220ms`（タブ切替、カード展開、トースト進入）
  * `--dur-slow: 320ms`（モーダル、ボトムシート進入。日常操作は **350ms 上限**に抑える）
  * `--ease-standard: cubic-bezier(0.2, 0, 0, 1)`（M3 Standard）／`--ease-out: cubic-bezier(0, 0, 0.2, 1)`／`--ease-in: cubic-bezier(0.3, 0, 1, 1)`
* **要所の「わずかな弾み」＝完了チェック・習慣達成・スイッチ・セグメント切替に限定**
  * **Spatial（`transform`）のみ**に適用し、色・`opacity`・影には絶対に使わない（M3 Effects 原則）。
  * 控えめな 1 回オーバーシュート（例：最大 1.04〜1.06 程度の穏やかな着地）を `linear()` で事前サンプリングして `--ease-spring-gentle` として定義（所要 `280〜360ms`）。「静か＋温かい」を壊さないよう、複数回揺れる強いバウンスは禁止事項に入れる。
* **`prefers-reduced-motion: reduce` 規則**
  * `--dur-base` / `--dur-slow` を `150ms`、`--ease-spring-gentle` を `ease-out` に上書きし、コンポーネント側の移動・拡縮（`translate` / `scale`）を `none` にして **`opacity` クロスフェードへ置換**する。

### 2. 日本語タイポグラフィ推奨
* **System Font Stack**
  ```css
  --font-sans:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Hiragino Sans", "Hiragino Kaku Gothic ProN",
    "BIZ UDPGothic", "Noto Sans JP", "Yu Gothic", Meiryo, sans-serif;
  ```
  * 欧文先・和文後で英数字の造形と `tabular-nums` を確保。Windows では `Yu Gothic` の細かすれを回避するため `BIZ UDPGothic` を優先（Android は `Roboto` + `Noto Sans JP`、iOS/macOS は SF Pro + ヒラギノが自然に当たる）。
* **Type Scale（1.125〜1.200 系の光学丸め・日本語向け 7 段階）**
  * `xs: 12px`（メタ情報・注釈、`lh: 1.4`）
  * `sm: 14px`（補助本文・高密度時の標準本文、`lh: 1.5`）
  * `base: 16px`（標準本文、`lh: 1.65`）
  * `lg: 18px`（小見出し・カードタイトル、`lh: 1.45`）
  * `xl: 20px`（セクション見出し、`lh: 1.4`）
  * `2xl: 24px`（画面タイトル、`lh: 1.35`）
  * `3xl: 32px`（オンボーディング／ヒーロー数値等、`lh: 1.25`）
  * ※業務ツール寄りかつモバイル画面（PWA/Android）で圧迫感を出さないため、1.25 のような大跳躍は避け、Carbon／Apple 寄りの細かい刻みを推奨 `[意見]`。
* **密度トークンとの連動**
  * `default`（中間）：本文 `16px` / `line-height: 1.65`
  * `compact`（業務・一覧詰め）：本文 `14px` / `line-height: 1.45`（表セルは `1.3`）
  * `relaxed`（記録・振り返り読み物）：本文 `16px` / `line-height: 1.75`、1行最大幅 `36〜42em`（日本語 35〜40 字前後 `[通説]`）
* **組版ユーティリティ規則**
  * ルート（`lang="ja"` 必須）：`line-break: strict; overflow-wrap: anywhere; text-autospace: normal;`
  * 本文：`letter-spacing: 0.02em; text-wrap: pretty;`（**`palt` は使わない**）
  * 見出し（`h1–h3`）：`font-feature-settings: "palt"; letter-spacing: 0; text-wrap: balance;`（必要に応じて `word-break: auto-phrase`）
  * 数値・日時・テーブル・習慣カウント・バッジ：`font-variant-numeric: tabular-nums;` を標準適用。
