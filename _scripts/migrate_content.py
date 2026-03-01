#!/usr/bin/env python3
"""Migrate Jekyll content pages to Hugo content/ directory."""

import os
import re
import shutil

ROOT = os.path.join(os.path.dirname(__file__), '..')
CONTENT = os.path.join(ROOT, 'content')

# Sections to migrate: (source path relative to ROOT, dest path relative to content/)
# Skip: preview/ (pre-generated tag pages, Hugo handles natively)
SECTIONS = [
    ('about/index.md',              'about/index.md'),
    ('introduction/index.html',     'introduction/index.html'),
    ('conclusions/index.html',      'conclusions/index.html'),
    ('data/index.html',             'data/index.html'),
    ('database/index.html',         'database/index.html'),
    ('faces/index.html',            'faces/index.html'),
    ('posters/index.html',          'posters/index.html'),
    ('concept-map/index.html',      'concept-map/index.html'),
    ('keyword-context/index.html',  'keyword-context/index.html'),
    ('analysis/context/index.html',       'analysis/context/index.html'),
    ('analysis/advocate/index.html',      'analysis/advocate/index.html'),
    ('analysis/progressivism/index.html', 'analysis/progressivism/index.html'),
    ('contracts/index.html',              'contracts/index.html'),
    ('contracts/1906/index.html',         'contracts/1906/index.html'),
    ('contracts/1907/index.html',         'contracts/1907/index.html'),
    ('contracts/1910/index.html',         'contracts/1910/index.html'),
    ('contracts/1911/index.html',         'contracts/1911/index.html'),
    ('contracts/1913/index.html',         'contracts/1913/index.html'),
]

def strip_layout_frontmatter(text):
    """Remove the layout: field from Jekyll front matter."""
    if not text.startswith('---'):
        return text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return text
    fm = re.sub(r'^layout:.*\n', '', parts[1], flags=re.MULTILINE)
    return f'---{fm}---{parts[2]}'

migrated = 0
for src_rel, dst_rel in SECTIONS:
    src = os.path.join(ROOT, src_rel)
    dst = os.path.join(CONTENT, dst_rel)

    if not os.path.exists(src):
        print(f'  SKIP (not found): {src_rel}')
        continue

    os.makedirs(os.path.dirname(dst), exist_ok=True)

    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    content = strip_layout_frontmatter(content)

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)

    migrated += 1
    print(f'  Migrated: {dst_rel}')

# The archive page is handled via a Hugo layout template, not content—
# just write a minimal _index.md with front matter.
archive_dst = os.path.join(CONTENT, 'archive', '_index.md')
os.makedirs(os.path.dirname(archive_dst), exist_ok=True)
with open(archive_dst, 'w') as f:
    f.write('---\ntitle: Archives\nslug: archive\n---\n')
migrated += 1
print('  Created: archive/_index.md')

# topic-model: copy all HTML files as static assets into static/
# (it's a self-contained MALLET output — no Jekyll templating inside)
tm_src = os.path.join(ROOT, 'topic-model')
tm_dst = os.path.join(ROOT, 'static', 'topic-model')
if os.path.isdir(tm_src):
    if os.path.exists(tm_dst):
        shutil.rmtree(tm_dst)
    shutil.copytree(tm_src, tm_dst,
                    ignore=shutil.ignore_patterns('index.html'))
    # The index.html goes to content/ so it renders through Hugo
    tm_index_src = os.path.join(tm_src, 'index.html')
    if os.path.exists(tm_index_src):
        tm_content_dst = os.path.join(CONTENT, 'topic-model', 'index.html')
        os.makedirs(os.path.dirname(tm_content_dst), exist_ok=True)
        with open(tm_index_src) as f:
            content = f.read()
        content = strip_layout_frontmatter(content)
        with open(tm_content_dst, 'w') as f:
            f.write(content)
    print('  Copied: topic-model/ (HTML to static, index to content)')
    migrated += 1

print(f'\nMigrated {migrated} content pages.')
