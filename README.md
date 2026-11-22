# fatcorn753-design

Claude Code が Web アプリ・PWA・サイトの画面を作るときに読み込む、個人用のデザインシステムです。[Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) の形で配布しています。

印象は「静か + 温かい」です。日本語 UI を中心に、ツール・業務アプリと、記録や習慣などの個人向けアプリを想定しています。

## 特徴

このデザインシステムの顔になる見た目が 3 つあります。

- **葉の形**: 部品の角は、左上と右下だけを大きく丸めます(`--shape-control: 10px 3px`、`--shape-panel: 16px 4px`)。ボタン・入力欄・お知らせ・トーストは小さい葉、カード・ダイアログ・表の枠は大きい葉にします。
- **芽吹き**: やることを完了にした瞬間だけ、チェックの上に小さな芽が出て、約 1 秒で消えます。ページを開いたときから完了している項目には出しません。完了の演出はこれ 1 つだけです。
- **数字の目盛り**: 集計の数字は等幅で大きく出し、単位は小さく添えます。その下に、GitHub の草のような日ごとの目盛りを並べます。目盛りは 4 段階の濃さで、今日の刻みには枠を付けます。

ほかの特徴は次のとおりです。

- **色**: OKLCH の役割トークン(`--bg-*` `--text-*` `--accent-*` など)を使います。ライトとダークは同じ扱いで作っています。主役の色は苔(落ち着いた緑)です。琥珀(黄褐色)にも切り替えられます。すべての組み合わせで WCAG 2.2 AA を計算で確かめました(本文 7:1 以上、補助の文字 4.5:1 以上、部品の輪郭 3:1 以上)。
- **密度**: `data-density="compact|spacious"` で、詰めた表示と広げた表示を切り替えられます。指で操作する端末では、押せる範囲を 44px 以上にします。
- **動き**: 普段の動きは短くし、チェックや行の追加でだけ少し弾ませます。`prefers-reduced-motion` のときは移動をやめ、フェードだけを残します。芽吹きも、芽がその場で薄れて消えるだけになります。
- **文字**: 端末の標準書体を使います。日本語の禁則処理、和欧間の空き、見出しだけのプロポーショナル詰め、数字の等幅表示を設定しています。
- **部品**: `.td-` から始まるクラスで、ボタン、入力欄、チェック、スイッチ、一覧、カード、表、ダイアログ、トースト、空状態、読み込み表示をそろえています。状態は class ではなく ARIA 属性で表します。
- **規則**: UX と文言の規則(確認より Undo、送信ボタンを無効にしない、エラーは欄の真下に出す、など)と、AI が作ったように見える見た目の禁止事項をまとめています。
- **検査**: `scripts/check_design.py` で、色の直書き、グラデーション、太すぎる文字、Web フォント、絵文字などを機械的に見つけます。

## 使い方

Claude Code の Skill として入れます。

```bash
git clone https://github.com/fatcorn753/fatcorn753-design.git
```

```bash
ln -s "$PWD/fatcorn753-design/skill" ~/.claude/skills/fatcorn753-design
```

入れたあとに画面を作るよう頼むと、Claude が Skill を読み込みます。読み込んだ Claude は `assets/` の CSS をプロジェクトにコピーし、規則に沿って作ります。Skill を使わずに CSS だけ使うこともできます。

```html
<html lang="ja" data-accent="koke">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="components.css">
```

検査は次のように実行します。違反が見つかると終了コード 1 を返します。

```bash
python3 skill/scripts/check_design.py path/to/project
```

見本は `skill/examples/showcase.html` です。ブラウザで直接開けます。

## 構成

```
skill/
  SKILL.md                 使い方と規則(Claude が最初に読む)
  assets/                  tokens.css / base.css / components.css
  references/components.md 部品のマークアップと規則
  scripts/check_design.py  規則違反の検査
  examples/showcase.html   全部品を使った見本
research/                  設計の根拠にした調査とまとめ
explore/candidates.html    アクセント色・動き・書体の比較ページ
```

`research/` の調査は、生成 AI(Gemini)に書かせたものです。その中から一次情報で確かめた内容を [research/summary.md](research/summary.md) にまとめ、確かめられなかった主張には印を付けています。

## ライセンス

[MIT](LICENSE)
