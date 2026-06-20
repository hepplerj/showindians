# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Digital history project ("Progressive Wild West") examining Native American performers in Buffalo Bill's Wild West shows (1883–1917). Hugo static site deployed to progressivewildwest.org.

Recently migrated from Jekyll to Hugo. Archived Jekyll source lives in `_archive/`.

## Build Commands

```bash
just preview    # Run extract_concepts.py then hugo server
just build      # Run extract_concepts.py then hugo --minify
just deploy     # Build + permissions fix + rsync to reclaim hosting
```

Hugo config is in `hugo.toml`. The legacy `Makefile` is outdated (Jekyll-era); use `justfile` instead.

## Architecture

- **content/** — Hugo content: `posts/` (81+ document transcriptions), `analysis/`, `contracts/`, `database/`, `topic-model/`, etc.
- **layouts/** — Hugo templates. `_default/baseof.html` is the main wrapper. `shortcodes/c.html` is the concept annotation shortcode.
- **static/** — CSS, JS, images, figures, MALLET topic model output
- **_scripts/** — Python/bash build scripts (migration, concept extraction, deployment permissions)
- **_archive/** — Archived Jekyll source (reference only, not built)
- **docs/** — Project documentation (e.g., missing-annotations.md)

## Concept Annotation System

Posts use a Hugo shortcode for semantic annotation of concepts:

```
{{< c "CATEGORY:CONCEPT" >}}text{{< /c >}}
```

Categories: `NA` (Native Americans), `BBWW` (Buffalo Bill's Wild West), `Progressivism`. The `extract_concepts.py` script derives the concept map visualization from these annotations. `docs/missing-annotations.md` tracks posts still needing manual annotation.

## Content Format

Posts use YAML front matter with fields: `title`, `date`, `author`, `source`, `tags`, `categories`, `xml_source` (TEI XML URL). Post bodies mix HTML and Markdown (goldmark `unsafe: true` is enabled).

Permalinks for posts follow `/:year/:month/:day/:slug/`.

## Deployment

Deployed via rsync to Reclaim hosting (`reclaim:~/progressivewildwest.org/`). The `_scripts/permissions_fix.sh` script sets dirs to 755 and files to 644 before sync.
