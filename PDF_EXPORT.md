# PDF Export Notes

This package includes everything needed for the PDF export except the final PDF file itself.

The current local environment does not have `pandoc`, `pdflatex`, `xelatex`, or `wkhtmltopdf`, so the last step still needs to be done with a local editor or browser print flow.

## Recommended Source File

Use:

- `docs/tly_white_paper_v0.9_public_draft_pdf_source.md`

That file swaps the Mermaid block for a static SVG reference so the mechanism diagram is more reliable in print/export workflows.

## Recommended Output File

Save the exported PDF as:

- `docs/tly_white_paper_v0.9_public_draft.pdf`

## Suggested Export Methods

1. Open the PDF-source Markdown file in a Markdown app with math support and export to PDF.
2. Or push the repo, open the PDF-source file on GitHub, verify rendering, and print to PDF from the browser.

## Export Quality Check

Before committing the PDF, verify:

- equations render cleanly;
- the mechanism diagram appears as a graphic, not raw source;
- tables are not clipped;
- page breaks feel intentional;
- links remain legible;
- the title page shows `v0.9 public draft`.
