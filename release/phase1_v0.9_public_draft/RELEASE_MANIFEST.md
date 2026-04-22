# Release Manifest

This package contains the publication assets for the TLY Phase 1 release.

## Included

- `LICENSE`
  - MIT license for the publication package, simulator, and reference code in this repo.
- `CONTRIBUTING.md`
  - Guidance for Discussions, Issues, and the kinds of critique this draft is seeking.
- `README.md`
  - Repo-facing entrypoint for the public draft.
- `GITHUB_SETUP.md`
  - Suggested repo name, description, topics, and front-page structure.
- `PUBLISH_CHECKLIST.md`
  - Final pre-publication and launch checklist.
- `PDF_EXPORT.md`
  - Instructions for generating the white paper PDF.
- `release/phase1_v0.9_public_draft/scripts/export_white_paper.py`
  - Local export utility for regenerating the checked-in PDF artifact.
- `paper/tly_white_paper_v0.9_public_draft.md`
  - Canonical Markdown white paper.
- `paper/tly_white_paper_v0.9_public_draft.pdf`
  - Checked-in PDF artifact for review, sharing, and download.
- `paper/tly_white_paper_v0.9_public_draft_pdf_source.md`
  - PDF-friendly Markdown variant of the white paper.
- `paper/tly_one_page_summary.md`
  - One-page summary.
- `paper/tly_faq_objections.md`
  - FAQ and objections memo.
- `paper/tly_visual_diagrams.md`
  - Diagram notes and additional Mermaid figures.
- `sim/pyproject.toml`
  - Reproducible simulator dependency manifest.
- `sim/uv.lock`
  - Locked simulator environment for `uv sync`.
- `release/phase1_v0.9_public_draft/launch/hacker_news_post.md`
  - Hacker News launch copy.
- `release/phase1_v0.9_public_draft/launch/reddit_launch_posts.md`
  - Reddit launch copy.
- `release/phase1_v0.9_public_draft/launch/long_form_launch_post.md`
  - Longer-form launch note for Mirror, Substack, Notion, or a blog.

## Referenced From The Main Repo

- `sim/`
  - Python simulator and Streamlit dashboard.
- `dao/`
  - Solidity contracts, interfaces, tests, and DAO architecture notes.

## Explicitly Out Of Scope For Phase 1

- pricing and commercialization materials;
- deployment sales collateral;
- legal wrappers;
- contract factory design;
- audits.
