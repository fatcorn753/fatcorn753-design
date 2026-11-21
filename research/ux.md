[brief.md](brief.md) の前提に沿って、6領域の調査結果とコンセプトへの推奨案をまとめます。
確かさは **`[確立]`**（研究・公式規格）、**`[通説]`**（実務慣行）、**`[意見]`** で表記します。

---

## (1) UX 原則の具体設計規則への落とし込み

- **Nielsen の 10 ヒューリスティクス** `[確立]`（Jakob Nielsen, *10 Usability Heuristics*, https://www.nngroup.com/articles/ten-usability-heuristics/ ）
  - **システム状態の可視化**: 保存中/保存済み・同期状態・現在位置を常に視認可能にする（自動保存でも最終保存状態を表示）。
  - **ユーザー制御と自由**: Undo / キャンセル / Esc で常に安全に戻れる出口を用意する。
  - **エラー予防**: 入力制約・デフォルト値・日付ピッカー等で、エラー文を出す前にミス自体を防ぐ。
  - **再認優先（想起させない）**: コマンド・フィルタ条件・前回設定は選択肢や履歴として見せる。
  - **柔軟性と効率性**: 初学者は画面 UI、熟練者はキーボードショートカット（`Cmd/Ctrl+K` 等）で同じ操作ができるようにする。
- **Fitts の法則**（$T = a + b \log_2(2D/W)$）`[確立]`（Paul M. Fitts, 1954, *Journal of Experimental Psychology* 47(6):381–391）
  - 頻繁に押す主操作（保存・記録追加）は大きく、操作元の近くまたは画面端（モバイルの下部親指圏）に置く。
  - 誤操作が痛い破壊操作（全削除など）は主操作から物理距離を離し、サイズを目立たせすぎない。
- **Hick–Hyman の法則**（$RT = a + b \log_2(n+1)$）`[確立]`（W. E. Hick, 1952; R. Hyman, 1953）
  - 1画面・1ツールバーの同時選択肢は絞り、二次操作はオーバーフローメニュー（`...`）や段階的開示（Progressive Disclosure）に逃がす。
  - 習慣・記録アプリの入力は「ワンタップで完了→詳細追記は任意」にする `[通説]`（出典なし）。
- **Doherty Threshold（400ms）と応答時間 3 閾値** `[確立]`（W. J. Doherty & A. J. Thadhani, 1982, IBM *The Economic Value of Rapid Response Time* / Jakob Nielsen, 1993, https://www.nngroup.com/articles/response-time-limits-jakob-nielsen/ ）
  - **≤ 100ms**: 即時反応と感じる。入力・トグル・タブ切替はローダーを出さず即座に状態変化させる。
  - **≤ 400ms**: 生産性が維持される閾値（Doherty）。通常操作は楽観的 UI（Optimistic UI）を含め 400ms 以内に視覚応答する。
  - **1,000ms 超**: 思考の途切れを感じるため処理中インジケータを出す。
  - **10,000ms 超**: 注意が逸れる限界。進捗率（%）＋キャンセル手段が必須。

---

## (2) 主要操作パターンの設計規則

- **フォーム・入力検証**
  - **検証タイミング**: 入力開始直後にエラーを出さず、`onBlur`（フォーカス離脱時）または送信時に検証し、修正中のみリアルタイムにエラーを消す（reward early, punish late） `[確立]`（NN/g, Inline Validation, https://www.nngroup.com/articles/errors-forms-design-guidelines/ ）。
  - **送信ボタンの `disabled` 乱用禁止**: 未入力を理由に送信ボタンを無効化せず、押下時に該当欄へ誘導＋エラー表示する `[確立]`（デジタル庁デザインシステム, https://design.digital.go.jp/ ）。
  - **エラー配置と支援技術**: 入力欄の**真下**に配置し、`aria-describedby` で紐づける。入力中の `aria-live` / `role="alert"` 乱用は読み上げを妨げるため避ける `[確立]`（デジタル庁デザインシステム, https://design.digital.go.jp/ ）。
- **空状態（Empty State）** `[通説]`（Material Design 3, https://m3.material.io/ / NN/g）
  - 「①いま空である理由（1文）＋②ここでできること＋③最初の 1 アクション（CTA ボタン）」の 3 点に絞る。初回空状態と「検索結果 0 件（条件リセット CTA）」は分けて設計する。
- **読み込み表示（Skeleton vs Spinner と閾値）**
  - **0〜300ms（最大 < 1,000ms）**: 何も出さない（一瞬のチラつきは逆に遅く見せる） `[確立]`（Jakob Nielsen, 1993, 同上 / NN/g）。
  - **300ms〜1,000ms 超・構造が既知の一覧/画面遷移**: **Skeleton** を使用。CLS（レイアウトずれ）を防ぎ体感待ち時間を短縮する `[確立]`（NN/g, *Skeleton Screens 101*, https://www.nngroup.com/articles/skeleton-screens/ ）。
  - **局所操作・送信中・構造が不定**: **Spinner**（ボタン内インライン等）を使用 `[確立]`（同上）。
  - **10,000ms 超**: 確定プログレスバー（% / 残りステップ）＋キャンセルボタン `[確立]`（Nielsen, 1993）。
- **確認ダイアログ vs Undo** `[確立]`（NN/g, *Confirmation Dialogs*, https://www.nngroup.com/articles/confirmation-dialogs/ ）
  - **原則 Undo 優先**: アーカイブ・単一項目削除・ステータス変更など可逆操作は、確認を挟まず即実行＋「元に戻す」を提示する（確認乱用による慣れ・素通り防止）。
  - **確認ダイアログを使う条件**: 不可逆・高コスト（アカウント削除、一括完全削除、外部送信）のみ。ボタン文言は「OK/キャンセル」ではなく「削除する / キャンセル」と具体的動詞にする。
- **トースト / スナックバー・通知**
  - **情報通知のみ（ボタンなし）**: 自動消滅 **4,000〜5,000ms**（最長 10,000ms 程度） `[確立]`（Material Design 3 Snackbar, https://m3.material.io/ ）。
  - **アクション付き（Undo 等）**: **自動消滅させない**か、ホバー/フォーカスでタイマー停止＋十分な猶予を設ける。重要エラーをトーストだけで消すのは WCAG 2.2.1（タイミング調整可能）違反になりうる `[確立]`（W3C WCAG 2.2 SC 2.2.1, https://www.w3.org/TR/WCAG22/ / Material Design 3, https://m3.material.io/ ）。

---

## (3) 情報密度の切り替え（Compact / Comfortable）の実例と寸法

| デザインシステム | 基準グリッド | Compact（詰める） | Comfortable / Default（標準） | Spacious / Large（広げる） | 出典・確かさ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Material Design 3** | 4dp 刻み | Scale `-2` / `-3`（1段ごとに高さ **-4dp**） | Scale `0`（行高 **48–52dp**） | —（アイコンボタン・スナックバー等は密度縮小対象外） | `[確立]` Google, https://m3.material.io/ |
| **IBM Carbon** | 8px（2x Grid） | `xs`: **24px** / `sm`: **32px** | `md`: **40px** | `lg`: **48px** / `xl`: **64px** | `[確立]` IBM, https://carbondesignsystem.com/ |
| **Microsoft Fluent 2** | 4px | `small`: 行高 **約 32px**（マウス向け） | `medium`: **44–48px**（タッチ兼務） | — | `[確立]` Microsoft, https://fluent2.microsoft.design/ |
| **Ant Design** | 4px/8px | `small`: セル上下 padding **8px**（行高 ~36px） | `middle`: セル上下 padding **12px** | `large`: セル上下 padding **16px** | `[確立]` Ant Group, https://ant.design/ |

- **共通設計原則**: 密度切替では**本文フォントサイズをむやみに縮めず**（例: 14–16px 固定）、主に**垂直パディング・行高・ギャップ**のみを調整する `[通説]`（Material 3 / IBM Carbon / SAP 等）。タッチ端末では Compact を強制しない `[確立]`（Material 3, https://m3.material.io/ ）。

---

## (4) タッチ領域の最小寸法

| 規格・ガイドライン | 最小ターゲット寸法 | 位置づけ・備考 | 出典・確かさ |
| :--- | :--- | :--- | :--- |
| **WCAG 2.2 SC 2.5.8**（Level AA） | **24 × 24 CSS px** | Web アクセシビリティの下限。24px 未満でも隣接ターゲットとの間隔が直径 24px 円相当あれば例外成立 | `[確立]` W3C, https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum |
| **Apple HIG**（iOS/iPadOS） | **44 × 44 pt** | 見た目が小さくてもヒット領域（padding 含む）で 44pt 以上を確保 | `[確立]` Apple, https://developer.apple.com/design/human-interface-guidelines/ |
| **Material Design 3**（Android） | **48 × 48 dp** | 物理サイズ約 9mm 相当。見た目アイコン（例: 24dp）＋ヒット領域拡張で確保 | `[確立]` Google, https://m3.material.io/ |

---

## (5) キーボード操作とフォーカス表示

- **フォーカス可視性・外観** `[確立]`（W3C WCAG 2.2）
  - **SC 2.4.7（Level AA）**: 全操作可能要素でフォーカスインジケータを表示する（`outline: none` の代替なし削除を禁止）。`:focus-visible` を用いてマウスクリック時の不要なリングを抑えつつキーボード操作時は必ず出す `[通説]`（出典なし）。
  - **SC 2.4.11 Focus Not Obscured（Level AA）**: フォーカス中要素が固定ヘッダー・フッター・トースト等で完全に隠れないようにする（CSS `scroll-padding` を設定） (https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum )。
  - **SC 2.4.13 Focus Appearance（Level AAA 目標値）**: 外周 **2px 以上**の太さ、非フォーカス状態とのコントラスト比 **3:1 以上** (https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance )。
- **ウィジェットのキーボード規約** `[確立]`（W3C ARIA Authoring Practices Guide, https://www.w3.org/WAI/ARIA/apg/ ）
  - **複合部品（タブ・メニュー・ツールバー・ラジオ群）**: **Roving `tabindex`**（活性要素のみ `tabindex="0"`、他は `"-1"`、内部移動は矢印キー）。
  - **モーダルダイアログ**: 展開時に内部へ初期フォーカス移動、背景を `inert` 化（または `<dialog>.showModal()`）し `Tab` / `Shift+Tab` を内側に閉じ込める（フォーカストラップ）。`Esc` で閉じて**起動元要素へフォーカス復帰**する。

---

## (6) 日本語 UI の文言の作法

- **敬体（です・ます）と常体・体言止めの使い分け** `[確立]`（SmartHR Design System, https://smarthr.design/ / デジタル庁デザインシステム, https://design.digital.go.jp/ ）
  - **説明文・エラー文・確認ダイアログ・空状態**: **敬体（です・ます調）**で動詞まで言い切る（体言止めを避け、丁寧で安心感のある対話にする）。
  - **見出し・項目ラベル・ステータス・バッジ**: **名詞 / 体言止め**（例：「保存済み」「同期中」「下書き」）で視認速度を上げる。
- **ボタンの動詞**
  - 「〜を行う」「〜を実行する」「〜することができます」のような冗長表現を避ける `[確立]`（SmartHR Design System, https://smarthr.design/ ）。
  - 業務・高密度ツールではサ変名詞の「する」を省略する流儀（`保存` `削除` `追加`） `[確立]`（同上）と、個人向け・破壊操作や誤解しやすい操作で動詞を明示する流儀（`完全に削除する` `記録を残す`） `[通説]`（Apple HIG 等）がある。同一プロダクト内で規則を統一する。
- **エラー文の型** `[確立]`（Apple HIG, https://developer.apple.com/design/human-interface-guidelines/ / デジタル庁デザインシステム, https://design.digital.go.jp/ ）
  - **「①何が起きたか（中立に）＋②どう直せばよいか（具体的手順）」**をセットで書く。ユーザーを責める語調・内部エラーコードのみの提示を避ける。
  - 例: ❌「入力値が不正です」→ ⭕「開始日は終了日より前の日付を選んでください。」

---

## コンセプト（「静か＋温かい」ツール & 個人アプリ / PWA・Android）への推奨案

以下は上記知見を [brief.md](brief.md) の方針へ当てはめたテンプレート推奨案です **`[意見]`**（各数値根拠は前節の `[確立]` 基準に依拠）。

1. **情報密度トークン（`data-density`）**
   - **基準単位 4px**。本文サイズは変えず（`15px` または `16px`、`line-height: 1.6`）、高さと余白だけ切り替える。
   - `comfortable`（標準・個人アプリ/タッチ既定）: 行高 / コントロール高 **44–48px**、ヒット領域最小 **48×48px**（Android / Material 3 準拠、Apple 44pt も包含）。
   - `compact`（業務・一覧・デスクトップ任意切替）: 行高 **32–36px**、ボタン高 **32px**。ただし `(pointer: coarse)`（タッチ端末）ではヒット領域を最小 **44px** 以上に維持し、WCAG 2.5.8 の **24px** を下回らない。
   - `spacious`（閲覧・執筆・ヘッドスペース的画面）: 行高 **52–56px**、セクション余白 1.25–1.5 倍。
2. **「静かさ」を保つフィードバック設計**
   - ローダー表示遅延 **300ms**（300ms 未満は非表示）、通常操作は楽観的 UI で **≤ 100ms** 応答。
   - 削除・アーカイブは原則 **即実行＋Undo スナックバー（自動消滅なし、または手動閉じる＋8,000ms 以上かつホバー/フォーカス停止）**。確認ダイアログは「完全削除・初期化・外部送信」のみ。
   - トーストは静かな色面で画面下部（モバイル）/右下（デスクトップ）に 1 件ずつ出し、情報通知は **4,000ms** で静かにフェードアウト（`prefers-reduced-motion: reduce` では移動なしフェードのみ）。
3. **フォーカスとアクセシビリティ**
   - `:focus-visible` にアクセント色（苔 `#4F6B3A` 系 / 琥珀 `#9A5B13` 系）でライト・ダーク双方 **コントラスト比 3:1 以上**の `outline: 2px solid` + `outline-offset: 2px`（WCAG 2.4.13 準拠）。
   - 固定バーがある画面は `scroll-padding-top / bottom` を必ずトークン連携させる（WCAG 2.4.11）。
4. **日本語ライティング規約（静か＋温かいトーン）**
   - 説明・エラー・空状態は**やわらかい敬体**（過度な敬語「〜くださいませ」や感嘆符「！」の乱用は禁止）。
   - ボタンは**通常操作は短い名詞/動詞（例：`保存` `追加` `閉じる`）**、**破壊操作や迷いやすい確認ボタンは具体動詞（例：`この記録を削除する`）**に統一。
   - 送信ボタンは `disabled` にせず、押下時に該当欄の真下へ具体的修正手順を示す（例：「タイトルを入力してください。」）。
