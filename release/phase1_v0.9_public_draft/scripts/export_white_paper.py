#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

import markdown
from latex2mathml.converter import convert as latex_to_mathml


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "paper" / "tly_white_paper_v0.9_public_draft_pdf_source.md"
HTML_OUT = ROOT / "paper" / "tly_white_paper_v0.9_public_draft_export.html"
PDF_OUT = ROOT / "paper" / "tly_white_paper_v0.9_public_draft.pdf"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Trailing Labor Yield: A White Paper</title>
  <style>
    @page {{
      size: letter;
      margin: 0.8in;
    }}

    :root {{
      color-scheme: light;
    }}

    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: #111111;
      background: #ffffff;
      line-height: 1.5;
      font-size: 11pt;
    }}

    main {{
      max-width: 7.2in;
      margin: 0 auto;
    }}

    h1, h2, h3, h4 {{
      line-height: 1.2;
      margin-top: 1.3em;
      margin-bottom: 0.45em;
      page-break-after: avoid;
    }}

    h1 {{
      font-size: 24pt;
      margin-top: 0;
    }}

    h2 {{
      font-size: 16pt;
      border-bottom: 1px solid #d9d9d9;
      padding-bottom: 0.18em;
    }}

    h3 {{
      font-size: 13pt;
    }}

    p, ul, ol, table, pre, blockquote {{
      margin-top: 0;
      margin-bottom: 0.9em;
    }}

    ul, ol {{
      padding-left: 1.3em;
    }}

    li + li {{
      margin-top: 0.2em;
    }}

    code {{
      font-family: "SFMono-Regular", Menlo, Consolas, monospace;
      font-size: 0.92em;
      background: #f5f5f5;
      padding: 0.1em 0.25em;
      border-radius: 3px;
    }}

    pre {{
      overflow-x: auto;
      background: #f5f5f5;
      padding: 0.75em;
      border-radius: 4px;
      white-space: pre-wrap;
      word-break: break-word;
    }}

    pre code {{
      background: transparent;
      padding: 0;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 10.5pt;
    }}

    th, td {{
      border: 1px solid #d9d9d9;
      padding: 0.4em 0.55em;
      vertical-align: top;
    }}

    th {{
      background: #f7f7f7;
      text-align: left;
    }}

    blockquote {{
      margin-left: 0;
      padding-left: 0.9em;
      border-left: 3px solid #d9d9d9;
      color: #404040;
    }}

    .math-block {{
      text-align: center;
      margin: 1em 0;
      overflow-x: auto;
    }}

    math {{
      font-size: 1.05em;
    }}

    .title-meta {{
      color: #404040;
      margin-bottom: 1.2em;
    }}

    .page-break {{
      page-break-before: always;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
BLOCK_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")


def split_preserving_code(text: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    last = 0
    for match in FENCED_CODE_RE.finditer(text):
        if match.start() > last:
            parts.append(("text", text[last : match.start()]))
        parts.append(("code", match.group(0)))
        last = match.end()
    if last < len(text):
        parts.append(("text", text[last:]))
    return parts


def convert_math_segment(segment: str) -> str:
    def repl_block(match: re.Match[str]) -> str:
        expr = match.group(1).strip()
        mathml = latex_to_mathml(expr, display="block")
        return f'\n<div class="math-block">{mathml}</div>\n'

    def repl_inline(match: re.Match[str]) -> str:
        expr = match.group(1).strip()
        mathml = latex_to_mathml(expr)
        return f'<span class="math-inline">{mathml}</span>'

    segment = BLOCK_MATH_RE.sub(repl_block, segment)
    segment = INLINE_MATH_RE.sub(repl_inline, segment)
    return segment


def markdown_to_html(text: str) -> str:
    processed = []
    for kind, value in split_preserving_code(text):
        if kind == "code":
            processed.append(value)
        else:
            processed.append(convert_math_segment(value))
    md = markdown.Markdown(
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "sane_lists",
            "smarty",
            "toc",
        ]
    )
    body = md.convert("".join(processed))
    body = body.replace(
        "<p>Version: v0.9 public draft<br />\nStatus: mechanism design proposal<br />\nRepository references: <code>sim/</code>, <code>dao/contracts/</code></p>",
        (
            '<p class="title-meta">Version: v0.9 public draft<br>\n'
            "Status: mechanism design proposal<br>\n"
            "Repository references: <code>sim/</code>, <code>dao/contracts/</code></p>"
        ),
    )
    return body


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    if not CHROME.exists():
        raise FileNotFoundError(f"Chrome not found at {CHROME}")

    url = html_path.resolve().as_uri()
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=4000",
        f"--print-to-pdf={pdf_path.resolve()}",
        url,
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    if not SOURCE.exists():
        print(f"Missing source file: {SOURCE}", file=sys.stderr)
        return 1

    markdown_text = SOURCE.read_text(encoding="utf-8")
    html_body = markdown_to_html(markdown_text)
    html_doc = HTML_TEMPLATE.format(body=html_body)
    HTML_OUT.write_text(html_doc, encoding="utf-8")

    try:
        render_pdf(HTML_OUT, PDF_OUT)
    except Exception as exc:
        print(f"HTML export succeeded: {HTML_OUT}")
        print(f"PDF export failed: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote HTML: {HTML_OUT}")
    print(f"Wrote PDF: {PDF_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
