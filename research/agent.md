[brief.md](brief.md) の前提に沿って、4つのテーマを簡潔にまとめます。

---

## 1. AI コーディングエージェントにデザイン規則を守らせる書き方

* **常時読み込む規則は極小にし、重要ルールを先頭に置く**（確かさ：**確立**）
  * 同時指示数が増えるほど LLM の遵守率は低下し、最上位モデルでも 500 指示で正答率約 **68%** まで落ち、プロンプト後半の指示ほど見落とされる（プライマシー効果）。
  * リポジトリ全体の長大なコンテキストファイルはタスク成功率をほとんど改善せず、推論コストを平均 **20% 以上**押し上げる。一方で明示的なツール・規約指定は従われやすい。
  * *出典*: Jaroslawicz et al. (Distyl AI), *How Many Instructions Can LLMs Follow at Once?* (IFScale), https://arxiv.org/abs/2507.11538 ／ Gloaguen et al. (ETH Zurich / LogicStar.ai), *Evaluating AGENTS.md*, https://arxiv.org/abs/2602.11988
* **「常時ロード」「必要時ロード」「機械的強制」の 3 層に分ける**（確かさ：**確立**）
  * **`CLAUDE.md`**: 全セッション常時読込。**200 行以内**を目安に、参照先ポインタと絶対厳守事項のみ置く。
  * **Claude Skills (`.claude/skills/<name>/SKILL.md`)**: UI 実装時だけ段階的開示（Progressive Disclosure）で読み込む。本体は **500 行以内**、参照ファイルは **1 階層まで**に留め、`description` に起動条件を三人称で明記する。
  * **Hooks (`.claude/settings.json`)**: 「毎回必ず守る」規則（生の色指定の禁止、トークン未使用の検知、Lint）はプロンプト頼みにせずフックで決定論的に弾く。
  * *出典*: Anthropic, *Claude Code Documentation / Best Practices & Agent Skills*, https://code.claude.com/docs/en/best-practices
* **Cursor rules (`.cursor/rules/*.mdc`) と `DESIGN.md` の分離**（確かさ：**通説**）
  * Cursor は単一 `.cursorrules` ではなく `.mdc` の `globs`（例: `*.tsx`, `*.css`）で UI ファイル編集時だけ規則を適用する。
  * 実装作法（`CLAUDE.md` / `AGENTS.md`）と見た目の正本（**`DESIGN.md`**）を分けると、エージェント間で視覚のブレが減る。Google Labs (Stitch) も `DESIGN.md` を視覚仕様の標準形式として提唱している。
  * *出典*: Google Labs (Stitch), *DESIGN.md Format*, https://stitch.withgoogle.com/docs/design-md/overview/ ／ Cursor, *Rules Documentation*, https://docs.cursor.com/context/rules
* **v0 / Lovable のシステムプロンプトに見られる効く書き方**（確かさ：**通説**）
  * **トークン先行宣言**: コンポーネントを書く前に必ず `globals.css` / トークン定義を先に生成・編集させる。
  * **具体的な禁止（Negative Constraints）と Good/Bad 対比**: 「統一感を出して」ではなく「JSX 内で `text-white` `bg-white` `bg-slate-100` や生 HEX を使わず、`bg-card text-card-foreground` を使う」「背景を上書きしたら必ず前景色もペアで上書きする」と書く。
  * *出典*: v0 / Lovable 公開システムプロンプト解析コミュニティ資料（GitHub 公開アーカイブ群、一次公式仕様は非公開のため「通説」扱い）

---

## 2. デザイントークンの形式とエージェントへの渡し方

| 形式 | 特徴・最新仕様 | エージェントに渡す向き不向き |
| :--- | :--- | :--- |
| **CSS 変数** (`:root` + Tailwind v4 `@theme inline`) | ブラウザ標準。OKLCH やライト/ダーク切替をそのまま記述でき、トークン数（文字数）が少ない。 | **Web / PWA のエージェント読込に最適**。コード生成時にそのまま `var(--...)` やユーティリティクラスへ直結でき、推論ミスが少ない。 |
| **W3C DTCG JSON** (`*.tokens.json`) | 2025年10月に初の安定版 **`2025.10`** が公開。`$value` / `$type` / `$description` と `{alias}` 参照、OKLCH / P3・複合型に対応。 | **正本（Single Source of Truth）に最適**。ただし JSON は冗長でコンテキストを消費しやすく、直接 UI 実装時に読ませると変換ミスが起きやすい。 |
| **Style Dictionary** (v4 / v5) | DTCG 形式をネイティブ対応。1つの正本から CSS / TS / Android XML / Jetpack Compose 等へ変換するビルドエンジン。 | **エージェントに読ませる形式ではない**（ツール）。Web（PWA）と Android の両方を扱う場合の変換パイプラインとして使う。 |

* *確かさ*: W3C DTCG 仕様と Style Dictionary 連携は**確立**、エージェントへの向き不向きは**通説／意見**。
* *出典*: W3C Design Tokens Community Group, *Design Tokens Format Module 2025.10*, https://www.designtokens.org/TR/2025.10/format/ ／ Style Dictionary Documentation, https://styledictionary.com/ ／ Tailwind CSS v4 Theme Variables, https://tailwindcss.com/docs/theme （エージェントの変換ミス・トークン消費比較は実務知見ベースで**出典なし**）

---

## 3. AI 生成 UI の「AI っぽさ（AI slop）」一覧と避け方

原因は学習データ内で高頻出な安全策へ偏る**分布収束（Distributional Convergence）**にある（確かさ：**確立**／出典: Anthropic, *Improving frontend design through Skills*, https://claude.com/blog/improving-frontend-design-through-skills ）。

| AI っぽさの典型（兆候） | 具体的な避け方（テンプレートに書く規則） | 確かさ |
| :--- | :--- | :--- |
| **紫〜青のグラデーション、光るぼかし玉、文字グラデーション** (`bg-clip-text`) | 装飾グラデーションと光彩（glow）を禁止。単色サーフェス＋1つのアクセント色のみ許可。 | 確立 |
| **絵文字を UI アイコン代わりに使う**（🚀✨📊 など） | 絵文字のアイコン利用を禁止。単色ストロークの SVG アイコン（線幅統一、例: 1.5px〜1.75px）に限定。 | 通説 |
| **何でも中央寄せ（見出し・本文・リストまで中央）** | 業務・記録 UI の基本は**左揃え**。中央揃えは空状態（Empty State）や完了画面など限定箇所のみ。 | 通説 |
| **全部カード化・カードの入れ子（Cardocalypse）** | カードのネスト禁止。一覧はまず余白・区切り線（1px）で整理し、カードは独立した操作単位に限定。 | 通説 |
| **左端に太いアクセント線** (`border-left: 4px`) | コールアウト・アラート以外での色付きサイドボーダーを禁止。 | 通説 |
| **無目的なグラスモーフィズム** (`backdrop-blur`) と硬い影 | ぼかしは浮遊バー等に限定。段差は影ではなく背景明度差（サーフェス階層）と 1px 枠線で作る。 | 通説 |
| **均等な 3 カラム機能カード＋ピルバッジ＋巨大数字の量産構成** | 情報の優先度に応じて非対称・単一カラム・リスト形式を選び、飾りバッジを置かない。 | 確立 |
| **過剰なバウンス演出、`prefers-reduced-motion` 無視** | 通常操作は減衰の速い短い遷移にし、弾みは完了・切替の要所のみ。`prefers-reduced-motion` 時はフェードまたは即時切替へ置換。 | 確立 |
| **モーダル乱用・グレー文字の低コントラスト** | 設定や入力はまずインライン展開・専用画面を検討。色背景に薄いグレー文字を載せず WCAG AA（4.5:1）を満たす。 | 確立 |

* *出典*: Anthropic, *Improving frontend design through Skills* & `anthropics/skills` (`frontend-design`), https://github.com/anthropics/skills ／ Paul Bakaus, *Impeccable (Design Anti-Patterns)*, https://impeccable.style/ ／ Vercel Labs, *web-design-guidelines*, https://github.com/vercel-labs/agent-skills

---

## 4. 6つのデザインシステムから個人テンプレートに取り入れる価値が高い規則

| デザインシステム | 個人テンプレートに取り入れる価値が高い規則・数値 | 確かさ | 出典 |
| :--- | :--- | :--- | :--- |
| **shadcn/ui** | ① セマンティックな **表面＋文字のペア命名**（`--card` / `--card-foreground`、`--primary` / `--primary-foreground`）でコントラスト事故を防ぐ。② **OKLCH** で色階調を定義。③ 単一の `--radius` から `sm/md/lg` を `calc()` で派生。 | 確立 | shadcn/ui Theming & Tailwind v4 Docs, https://ui.shadcn.com/docs/theming |
| **Radix Primitives** | ① WAI-ARIA APG 準拠のキーボード操作・フォーカストラップ・Escape 閉じを前提にする。② スタイルはクラス増殖より **`data-state="open\|closed"`** 等の状態属性に紐付ける。③ `asChild` 的な合成設計。 | 確立 | Radix Primitives Docs (Accessibility & Styling), https://www.radix-ui.com/primitives/docs/overview/accessibility |
| **Material 3** | ① タッチ領域最小 **48×48dp**（見た目が 24dp でも当たり判定を拡張）。② 影に頼らず背景色の段階（Surface / Surface Container）で奥行きを作る（ダークモードでも破綻しない）。③ モーションの分離: 位置・変形は **Spatial（わずかに弾む spring）**、色・不透明度は **Effects（絶対にオーバーシュートしない）**。従来目安は `short2` **100ms**、`short4` **200ms**、`medium2` **300ms**。 | 確立 | Google Material Design 3 (Accessibility / Color / Motion), https://m3.material.io/styles/motion/overview |
| **Apple HIG** | ① 最小タッチ領域 **44×44pt**。② 意味ベースの動的カラー（ライト／ダークで単なる反転ではなく明度・彩度を再調整）。③ **Reduce Motion** 時は移動・拡大を消し **クロスフェード** に置き換える（フィードバック自体は消さない）。 | 確立 | Apple Human Interface Guidelines (Layout / Color / Motion), https://developer.apple.com/design/human-interface-guidelines/motion |
| **GOV.UK Design System** | ① 複雑な入力は「**1画面（1ステップ）1トピック**（One thing per page）」に分解。② バリデーション失敗時はページ上部に **Error Summary**（自動フォーカス移動＋各項目へのリンク）と項目横のインラインエラーを併用。③ 誰が見ても分かる明確なフォーカス表示（太さ **3px** 級の高コントラスト輪郭）。 | 確立 | GOV.UK Design System (Error summary / Focus states / One thing per page), https://design-system.service.gov.uk/ |
| **デジタル庁デザインシステム (DADS)** | ① 日本語本文の基本サイズ **16px 以上**。② 用途別 **行間（line-height）**: ワンライン UI **1.0**、管理画面・高密度 **1.2〜1.3**、標準本文 **1.5**（最低ライン）、読みやすさ・心理的負荷軽減 **1.6〜1.7**。③ コントラストは通常文字 **4.5:1 以上**、枠線・アイコン等の非テキスト **3:1 以上**。④ 状態伝達を色だけに頼らない（ラベル／アイコン併用）。 | 確立 | デジタル庁デザインシステム (DADS), https://design.digital.go.jp/ |

---

## 5. [brief.md](brief.md) のコンセプトに当てはめた推奨

以下は上記知見をあなたのコンセプト（**静か＋温かい／業務＋習慣・記録／PWA＋Android／密度切替／ライト・ダーク同等／苔or琥珀／角丸6〜10px／要所で弾む／日本語標準書体**）へ落とし込んだ設計提案です（確かさ：**意見**、個別数値の根拠は上記 1〜4 の確立・通説に準拠）。

1. **Claude Code 向けの 4 点構成にする**
   * `CLAUDE.md`（100 行以内）: 「UI 実装・修正時は必ず `design-system` Skill を読み、`tokens.css` のセマンティック変数のみ使う」とだけ明記。
   * `.claude/skills/design-system/SKILL.md`（300 行以内）: 印象言語（静か＋温かい）、禁止事項（第 3 章の AI slop 一覧）、レイアウト・UX 規則（GOV.UK のエラー処理・Radix 準拠の操作性）を記述。
   * `DESIGN.md`（1 階層下の参照）: 視覚仕様の正本（Good/Bad コード例つき）。
   * **Hooks（PostToolUse / PreCommit）**: JSX/TSX 内の生 HEX、`text-white` / `bg-black`、絵文字アイコン、カードネスト候補を grep/lint で自動検出して止める。
2. **トークンは「DTCG JSON を正本 → CSS 変数＆Android へ出力」**
   * PWA と Android の両方を作るため、正本は **W3C DTCG `2025.10`** 形式（`tokens/*.tokens.json`）にし、**Style Dictionary** で Web 用 `tokens.css`（OKLCH・shadcn 式 `surface` / `on-surface` ペア）と Android 用（Compose `Color`/`Dp`）を生成する。
   * **Claude Code が UI を書くときに読ませるのは生成済みの短い `tokens.css`（＋ `@theme inline`）のみ**にする（JSON はトークン変更時だけ触る）。
3. **「静か＋温かい」を数値と禁止ルールで固定する**
   * **配色**: ライトは純白 `#FFFFFF` ではなくわずかに温かみのあるオフホワイト（低彩度の暖色寄りグレー）、ダークは純黒 `#000000` を避け暗いチャコール系にし、Material 3 式の **Surface 3 段階**（背景 / カード / 浮遊面）で奥行きを作る。アクセントは **苔 (`#4F6B3A` 前後)** でも **琥珀 (`#9A5B13` 前後)** でも、ライトとダークでそのまま使い回さず OKLCH の明度（L）と彩度（C）をダーク側で調整し、**文字 4.5:1・非テキスト 3:1** を両モードで担保する（注：業務ツールでの「警告・注意」に琥珀色を使う場合、メインアクセントは **苔** にするとセマンティックな警告色と衝突しにくい — 確かさ：**意見**、出典なし）。
   * **角丸**: `--radius-md: 8px` を基準に、`sm: 6px`（小ボタン・入力欄）・`lg: 10px`（カード・シート）の 3 段階に固定し、`rounded-full` はスイッチ・チェック完了丸印など限定用途にする。
   * **情報密度の切替**: `[data-density="compact" | "comfortable" | "spacious"]` をルートに置き、余白倍率・コントロール高さ・行間だけを切り替える（例：標準本文 **16px / 行間 1.6**、compact は **14〜15px / 行間 1.35**、タッチ領域はモバイル・Android 向けに **最小 44〜48px** を維持）。
   * **動き**: Material 3 の分離を採用し、色・ホバー等の **Effects は 120〜180ms（オーバーシュートなし）**、習慣のチェック完了・タブ切替などの **Spatial のみ 220〜300ms の軽い spring** にする。`prefers-reduced-motion: reduce` では全移動を消し、100ms 以下のフェードへフォールバックする。
   * **書体**: 端末標準書体スタック（`system-ui, -apple-system, "Hiragino Sans", "Yu Gothic UI", "Noto Sans JP", sans-serif`）＋数値・記録ログは **`font-variant-numeric: tabular-nums`** を必須にする（習慣カウンターや業務表の桁揃えで「静けさ」が保たれる — 確かさ：**通説**／出典: Apple HIG & Vercel `web-design-guidelines`）。
