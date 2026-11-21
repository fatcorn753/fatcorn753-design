# 部品の書き方

`assets/components.css` のクラスを使ったマークアップの見本と、部品ごとの規則をまとめる。
状態は class ではなく ARIA 属性と疑似クラスで表す。見た目の状態とアクセシビリティの状態が、ずれないようにするため。

## アイコン

絵文字は使わない。線のアイコンを使い、線幅は 1.75 にそろえる。
npm を使えるなら Lucide(`lucide` / `lucide-react`)を使い、`strokeWidth={1.75}` を指定する。
使えないときは下の SVG をそのまま使う。どれも `viewBox="0 0 24 24"` で、次の属性を付ける。

```html
fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"
```

| 用途 | 中身 |
|---|---|
| 成功 | `<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 5-5.5"/>` |
| 注意 | `<path d="M12 4 2.8 19.5h18.4L12 4Z"/><path d="M12 10v4.5"/><path d="M12 17.5h.01"/>` |
| エラー | `<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5"/><path d="M12 16.5h.01"/>` |
| 情報 | `<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.5h.01"/>` |
| 追加 | `<path d="M12 5v14M5 12h14"/>` |
| 空の箱 | `<path d="M3 13h5l1.5 2.5h5L16 13h5"/><path d="M5.5 5h13L21 13v6H3v-6L5.5 5Z"/>` |

アイコンだけのボタンには `aria-label` を付ける。

## ボタン

```html
<button class="td-btn" data-variant="primary" type="button">保存</button>
<button class="td-btn" type="button">キャンセル</button>
<button class="td-btn" data-variant="ghost" type="button">詳細</button>
<button class="td-btn" data-variant="danger" type="button">この記録を削除する</button>
<button class="td-btn" data-icon-only aria-label="追加" type="button"><svg …>追加</svg></button>
<button class="td-btn" data-variant="primary" aria-busy="true" type="button">保存</button>
```

- 主ボタン(`primary`)は 1 つの画面に 1 つまでにする。2 つ目以降は無印か `ghost` にする。
- ボタンを並べるときは、主ボタンを右端(モバイルでは下端)に置く。
- `danger` は取り返しのつかない操作だけに使う。元に戻せる削除は無印のボタンにし、実行後に Undo を出す。
- 送信ボタンは、未入力を理由に `disabled` にしない。押されたら、入力欄の真下にエラーを出す。
- 処理中は `aria-busy="true"` にする。ボタンの幅は変わらない。処理が 300ms 未満で終わる見込みなら、付けなくてよい。

## 入力欄

```html
<div class="td-field">
  <label class="td-label" for="title">タイトル</label>
  <input class="td-input" id="title" name="title" aria-describedby="title-help">
  <p class="td-help" id="title-help">あとから変更できます。</p>
</div>

<div class="td-field">
  <label class="td-label" for="date">開始日<span class="td-optional">任意</span></label>
  <input class="td-input" id="date" type="date" aria-invalid="true" aria-describedby="date-error">
  <p class="td-error" id="date-error"><svg …エラー…></svg>開始日は終了日より前の日付を選んでください。</p>
</div>
```

- ラベルは入力欄の上に置く。placeholder をラベルの代わりにしない。
- 必須の印ではなく、任意の欄に「任意」と付ける(必須の欄のほうが多いため)。
- 検証はフォーカスが外れたときか、送信時に行う。エラーが出たあとは、入力中に直った時点で消す。
- エラー文は「何が起きたか」と「どう直すか」を書く。入力欄の真下に出し、`aria-describedby` でつなぐ。
- 送信時にエラーが複数あるときは、最初のエラーの欄にフォーカスを移す。
- `type`、`inputmode`、`autocomplete` を必ず適切に付ける(メールは `type="email" autocomplete="email"` など)。

## チェックボックスとスイッチ

```html
<label class="td-check">
  <input type="checkbox" name="done">
  <span class="td-check-text" data-strike>レポートの下書き</span>
</label>

<label class="td-check">
  <span>通知</span>
  <input class="td-switch" type="checkbox" role="switch" checked>
</label>
```

- チェックボックスは「選んでから保存する」項目に使う。スイッチは「押した瞬間に効く設定」に使う。
- `data-strike` を付けると、完了時に文字が薄くなり打ち消し線が引かれる。やることリストの項目だけに付ける。
- チェックの印とスイッチのつまみは弾む。これは決定済みの「要所の動き」なので、ほかの部品に弾みを足さない。

## 一覧

```html
<ul class="td-list">
  <li class="td-row">
    <label class="td-check"><input type="checkbox"><span class="td-check-text" data-strike>出席データの確認</span></label>
    <span class="td-row-end"><time datetime="2026-11-21">11/21</time></span>
  </li>
  <li><a class="td-row" href="/notes/12" aria-current="page">
    <span class="td-row-main"><span class="td-row-title">週のふりかえり</span><span class="td-row-meta">3 日前</span></span>
    <span class="td-row-end">12 件</span>
  </a></li>
</ul>
```

- 一覧は、カードを並べるのではなく行と区切り線で作る。
- 選択中の行は `aria-selected="true"` か `aria-current="page"` にする。
- 追加した行には `data-new` を付ける。進入時に一度だけ弾む。次の描画で属性を外す必要はない。
- 行を消すときは確認を出さずに消し、トーストで Undo を出す。

## カード

```html
<section class="td-card" aria-labelledby="week">
  <h2 id="week">今週</h2>
  …
</section>
```

- カードは、独立して操作するまとまり(1 件の記録、1 つの設定群)だけに使う。
- カードの中にカードを入れない。中の区切りは余白か `<hr>` で作る。
- 画面の区画分けにはカードを使わない。見出しと余白で分ける。

## 状態の表示

```html
<span class="td-badge" data-tone="success"><svg …成功…></svg>同期済み</span>
<span class="td-badge">下書き</span>

<div class="td-notice" data-tone="warning" role="status">
  <svg …注意…></svg>
  <div><p class="td-notice-title">保存されていない変更があります</p><p>画面を閉じる前に保存してください。</p></div>
</div>
```

- `data-tone` は `accent` `success` `warning` `error` のどれか。省略すると中立になる。
- `success` `warning` `error` には、必ずアイコンを添える。色だけで状態を伝えない。
- 琥珀を使うときは、`warning` の色が主役の色と近い。注意のアイコンを省かない。
- 置く場所に応じて `role` を付ける。すぐ伝えたいエラーは `role="alert"`、それ以外は `role="status"`。

## 切り替えとタブ

```html
<div class="td-segmented" role="group" aria-label="表示">
  <button type="button" aria-pressed="true">週</button>
  <button type="button" aria-pressed="false">月</button>
</div>

<div class="td-tabs" role="tablist">
  <button role="tab" aria-selected="true" aria-controls="p1" id="t1">記録</button>
  <button role="tab" aria-selected="false" aria-controls="p2" id="t2" tabindex="-1">集計</button>
</div>
```

- 同じ内容の見せ方を変えるときは segmented、別の内容に移るときはタブを使う。
- タブは矢印キーで移動できるようにする。選ばれていないタブは `tabindex="-1"` にする。

## 表

```html
<div class="td-table-wrap">
  <table class="td-table">
    <thead><tr><th>日付</th><th>項目</th><th data-align="end">時間</th></tr></thead>
    <tbody><tr><td>11/21</td><td>読書</td><td data-align="end">45 分</td></tr></tbody>
  </table>
</div>
```

- 数値の列は右揃え(`data-align="end"`)にする。`td` は自動で `tabular-nums` になる。
- 表は `.td-table-wrap` で包む。狭い画面では表だけが横にスクロールし、ページは横にスクロールしない。

## ダイアログ

```html
<dialog class="td-dialog" id="confirm-delete" aria-labelledby="cd-title">
  <h2 id="cd-title">アカウントを削除しますか?</h2>
  <p class="td-dialog-body">記録 128 件もすべて削除されます。元に戻せません。</p>
  <form method="dialog" class="td-dialog-actions">
    <button class="td-btn" value="cancel">キャンセル</button>
    <button class="td-btn" data-variant="danger" value="delete">削除する</button>
  </form>
</dialog>
```

```js
const dlg = document.getElementById('confirm-delete');
openButton.addEventListener('click', () => dlg.showModal());
dlg.addEventListener('close', () => { if (dlg.returnValue === 'delete') deleteAccount(); });
```

- 確認ダイアログは、取り返しのつかない操作か、外部へ送る操作だけに使う。
- 見出しは問いの形にし、本文には何が失われるかを具体的に書く。
- ボタンは「OK」ではなく、操作を表す動詞にする(「削除する」「送信する」)。
- `showModal()` で開く。フォーカスの閉じ込め、Esc での閉じ、開いた元へのフォーカスの戻りは、ブラウザが行う。
- 設定や入力のためにダイアログを使わない。その場で展開するか、専用の画面にする。

## トースト

```html
<div class="td-toast-region" aria-live="polite"></div>
```

```js
// 情報だけのトーストは 4 秒で消す。Undo 付きは自動で消さず、閉じるか次の操作まで残す
function toast(message, { actionLabel, onAction } = {}) {
  const region = document.querySelector('.td-toast-region');
  const el = document.createElement('div');
  el.className = 'td-toast';
  el.innerHTML = '<span></span>';
  el.firstChild.textContent = message;
  const close = () => {
    el.dataset.leaving = '';
    el.addEventListener('animationend', () => el.remove(), { once: true });
  };
  if (actionLabel) {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = actionLabel;
    b.addEventListener('click', () => { onAction?.(); close(); });
    el.append(b);
  } else {
    let t = setTimeout(close, 4000);
    el.addEventListener('pointerenter', () => clearTimeout(t));
    el.addEventListener('pointerleave', () => { t = setTimeout(close, 2000); });
  }
  region.replaceChildren(el); // 1 件ずつ出す
}
// 例: toast('「買い物リスト」を削除しました', { actionLabel: '元に戻す', onAction: restore });
```

- トーストは 1 件ずつ出す。新しいトーストは古いものと入れ替える。
- 文は「何をしたか」を過去形で書く(「保存しました」)。
- エラーをトーストだけで伝えない。原因の場所にエラーを出す。

## 空状態

```html
<div class="td-empty">
  <svg …空の箱…></svg>
  <p class="td-empty-title">まだ記録がありません</p>
  <p>今日やったことを 1 つ書くと、ここに並びます。</p>
  <button class="td-btn" data-variant="primary" type="button">最初の記録を書く</button>
</div>
```

- 書くのは「いま空である理由」「ここで何ができるか」「最初の 1 操作」の 3 つ。
- 検索結果が 0 件のときは別の文にする(「条件に合う記録はありません」と「条件をクリア」のボタン)。
- 空状態と完了画面だけは中央揃えにしてよい。

## 読み込み表示

```html
<span class="td-skeleton" style="height: 1em; width: 60%"></span>
<span class="td-spinner" role="status" aria-label="読み込み中"></span>
```

- 300ms 未満で終わる処理には何も出さない。一瞬だけ出ると、かえって遅く見える。
- 画面の形が分かっている一覧や画面の切り替えには skeleton を使う。局所の処理には spinner を使う。
- 10 秒を超えそうな処理には、進み具合とキャンセルの手段を出す。
- 書き込みは、可能なら先に画面へ反映し(楽観的更新)、失敗したら戻してエラーを出す。

## 画面の骨組み

- デスクトップ(720px 以上): 左にサイドバー(幅 240px、地は `--bg-subtle`)、右に本文(地は `--bg-canvas`)。
- モバイル: 下にタブバー(項目は 3〜5 個、高さ 56px + `env(safe-area-inset-bottom)`)。主な操作は親指の届く下半分に置く。
- 本文の最大幅は、読む画面なら `--measure`、作業画面なら 1200px 前後にする。
- 左右の余白は `max(16px, env(safe-area-inset-left))` 以上にする。
- 見出し・本文・一覧は左揃えにする。
