#!/usr/bin/env python3
"""fatcorn753-design の規則に反する書き方を探す。

使い方: python3 check_design.py <ディレクトリかファイル> [...]
指摘があれば「ファイル:行: [規則] 内容」を出し、終了コード 1 を返す。
見た目の良し悪しは判定できない。機械的に見つかる違反だけを拾う。
"""
import os
import re
import sys

EXTS = {'.css', '.scss', '.html', '.htm', '.jsx', '.tsx', '.js', '.ts', '.vue', '.svelte', '.astro'}
SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '.next', 'out', 'coverage', 'vendor', '.svelte-kit'}
# assets/ からコピーした Skill 本体のファイルは、先頭のコメントで見分けて除外する
SIGNATURE = re.compile(r'fatcorn753-design (tokens|base|components)')

COLOR_LITERAL = re.compile(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb)\(')
NAMED_COLOR = re.compile(r'(?:color|background(?:-color)?|border(?:-[a-z]+)?-color|fill|stroke)\s*:\s*(white|black|gray|grey|red|blue|green|purple)\b', re.I)
TAILWIND_RAW = re.compile(r'\b(?:bg|text|border|ring|fill|stroke|from|to|via)-(?:\[#|(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b|white\b|black\b)')
GRADIENT = re.compile(r'\b(?:linear|radial|conic)-gradient\(|\bbg-gradient-to-|\bbg-linear-to-')
CLIP_TEXT = re.compile(r'background-clip\s*:\s*text|\bbg-clip-text\b')
BACKDROP = re.compile(r'backdrop-filter\s*:|\bbackdrop-blur')
BORDER_LEFT = re.compile(r'border-left(?:-width)?\s*:\s*(?:[3-9]|\d{2,})px|\bborder-l-(?:[4-9]|\[)')
TRANSITION_ALL = re.compile(r'transition\s*:\s*all\b|\btransition-all\b')
OUTLINE_NONE = re.compile(r'outline\s*:\s*(?:none|0)\b|\boutline-none\b')
WEIGHT_HEAVY = re.compile(r'font-weight\s*:\s*(?:700|800|900|bold|bolder)\b|\bfont-(?:bold|extrabold|black)\b')
WEB_FONT = re.compile(r'fonts\.googleapis\.com|@font-face')
FONT_FAMILY = re.compile(r'font-family\s*:\s*(?!var\(|inherit|monospace)')
LOREM = re.compile(r'lorem ipsum', re.I)
HTML_TAG = re.compile(r'<html\b[^>]*>', re.I)
EMOJI = re.compile('[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⬆↔-↪]')

RULES = [
    (COLOR_LITERAL, 'color', '色の生値。var(--…) のトークンを使う'),
    (NAMED_COLOR, 'color', '色の名前の直書き。トークンを使う'),
    (TAILWIND_RAW, 'color', 'Tailwind の既定色。@theme inline で対応させたトークンの名前を使う'),
    (GRADIENT, 'ai-look', '装飾のグラデーションは禁止'),
    (CLIP_TEXT, 'ai-look', '文字のグラデーションは禁止'),
    (BACKDROP, 'ai-look', 'すりガラス効果は目的があるときだけ。浮くバー以外では使わない'),
    (BORDER_LEFT, 'ai-look', '左端の太い色線は禁止(お知らせ部品は .td-notice を使う)'),
    (TRANSITION_ALL, 'motion', 'transition: all は禁止。変える性質だけを列挙する'),
    (OUTLINE_NONE, 'focus', 'フォーカスの輪郭を消している。:focus-visible で代わりの輪郭を出しているか確かめる'),
    (WEIGHT_HEAVY, 'type', '太さは 400/500/600 だけ。600 は var(--weight-bold)'),
    (WEB_FONT, 'type', 'Web フォントは使わない。var(--font-sans) を使う'),
    (FONT_FAMILY, 'type', '書体の直書き。var(--font-sans) か var(--font-mono) を使う'),
    (LOREM, 'copy', 'ダミー文。実際に使われそうな文言にする'),
]


REF_CONTEXT = re.compile(r'(?:href|querySelector(?:All)?|getElementById|location|closest|matches)\W{0,4}$')


def is_selector_ref(line, m):
    """#add や #face のような、色ではないページ内リンクやセレクタを除外する。"""
    if not m.group(0).startswith('#'):
        return False
    return bool(REF_CONTEXT.search(line[max(0, m.start() - 24):m.start()]))


def in_custom_prop(line, m):
    """トークンの定義と上書き(--name: 値)の中なら、色の生値を許す。"""
    start = max(line.rfind(';', 0, m.start()), line.rfind('{', 0, m.start())) + 1
    return line[start:m.start()].lstrip().startswith('--')


def strip_comment(line, state):
    """CSS/JS の /* */ を大まかに取り除く。state は複数行コメントの中かどうか。"""
    out, i = '', 0
    while i < len(line):
        if state['in']:
            j = line.find('*/', i)
            if j < 0:
                return out, state
            state['in'] = False
            i = j + 2
        else:
            j = line.find('/*', i)
            if j < 0:
                out += line[i:]
                break
            out += line[i:j]
            state['in'] = True
            i = j + 2
    return out, state


def check_file(path):
    found = []
    try:
        text = open(path, encoding='utf-8').read()
    except (UnicodeDecodeError, OSError):
        return found
    if SIGNATURE.search(text[:400]):
        return found
    ext = os.path.splitext(path)[1].lower()
    is_markup = ext in {'.html', '.htm', '.jsx', '.tsx', '.vue', '.svelte', '.astro'}
    state = {'in': False}
    for no, raw in enumerate(text.splitlines(), 1):
        if 'td-ignore' in raw:  # 意図した例外は行末に「td-ignore: 理由」と書く
            continue
        line, state = strip_comment(raw, state)
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            continue
        for pattern, rule, msg in RULES:
            hits = [m for m in pattern.finditer(line)
                    if not (pattern is COLOR_LITERAL and is_selector_ref(line, m))
                    and not (rule == 'color' and in_custom_prop(line, m))]
            if not hits:
                continue
            found.append(f'{path}:{no}: [{rule}] {msg}')
        if is_markup and EMOJI.search(line):
            found.append(f'{path}:{no}: [ai-look] 絵文字。線のアイコン(SVG)を使う')
        if is_markup:
            for tag in HTML_TAG.findall(line):
                if not re.search(r'\blang\s*=\s*["\']ja["\']', tag):
                    found.append(f'{path}:{no}: [type] <html> に lang="ja" がない')
    return found


def walk(target):
    if os.path.isfile(target):
        yield target
        return
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            if os.path.splitext(f)[1].lower() in EXTS and not f.endswith('.min.css') and not f.endswith('.min.js'):
                yield os.path.join(root, f)


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    findings = []
    for t in argv:
        if not os.path.exists(t):
            print(f'見つからない: {t}', file=sys.stderr)
            return 2
        for p in walk(t):
            findings.extend(check_file(p))
    for f in findings:
        print(f)
    print(f'指摘 {len(findings)} 件', file=sys.stderr)
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
