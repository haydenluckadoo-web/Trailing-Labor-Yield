# PDF Export Notes

This package now includes a checked-in PDF artifact:

- `paper/tly_white_paper_v0.9_public_draft.pdf`

It can be regenerated locally without `pandoc` or LaTeX by rendering the
publication-ready Markdown source to HTML and printing through headless Chrome.

## Recommended Source File

Use:

- `paper/tly_white_paper_v0.9_public_draft_pdf_source.md`

That file is the publication-ready Markdown source for PDF export.

## Recommended Output File

Save the exported PDF as:

- `paper/tly_white_paper_v0.9_public_draft.pdf`

## Included Export Script

Run:

```bash
uv run --with markdown --with latex2mathml \
  python release/phase1_v0.9_public_draft/scripts/export_white_paper.py
```

This generates:

- `paper/tly_white_paper_v0.9_public_draft.pdf`
- `paper/tly_white_paper_v0.9_public_draft_export.html` as an intermediate
  export file

The HTML intermediate is ignored by `.gitignore` and does not need to be
committed.

## Export Requirements

- `uv`
- Google Chrome installed at `/Applications/Google Chrome.app`

## Fallback Export Methods

1. Open the PDF-source Markdown file in a Markdown app with math support and export to PDF.
2. Or push the repo, open the PDF-source file on GitHub, verify rendering, and print to PDF from the browser.

## Export Quality Check

Before committing the PDF, verify:

- equations render cleanly;
- tables are not clipped;
- page breaks feel intentional;
- links remain legible;
- the title page shows `v0.9 public draft`.
