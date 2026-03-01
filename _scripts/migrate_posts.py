#!/usr/bin/env python3
"""Migrate Jekyll posts to Hugo content/posts/."""

import os
import re
import shutil

SRC = os.path.join(os.path.dirname(__file__), '..', '_posts')
DST = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts')

os.makedirs(DST, exist_ok=True)

def convert_concept_tags(text):
    """Convert {% c CONCEPT %}...{% ec %} to {{< c "CONCEPT" >}}...{{< /c >}}."""
    # Replace opening tag: {% c NA:Members %} -> {{< c "NA:Members" >}}
    text = re.sub(r'\{%\s*c\s+([^%}]+?)\s*%\}', r'{{< c "\1" >}}', text)
    # Replace closing tag: {% ec %} -> {{< /c >}}
    text = re.sub(r'\{%\s*ec\s*%\}', r'{{< /c >}}', text)
    return text

def convert_front_matter(fm_text):
    """Adjust front matter for Hugo."""
    lines = fm_text.split('\n')
    out = []
    skip = False
    for line in lines:
        # Drop the layout field — Hugo infers from content type
        if re.match(r'^layout:\s*', line):
            continue
        # Convert category: X  ->  categories:\n- X
        m = re.match(r'^category:\s*(.+)$', line)
        if m:
            out.append('categories:')
            out.append(f'- {m.group(1).strip()}')
            continue
        out.append(line)
    return '\n'.join(out)

converted = 0
for fname in os.listdir(SRC):
    if not fname.endswith('.md'):
        continue
    src_path = os.path.join(SRC, fname)
    dst_path = os.path.join(DST, fname)

    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split front matter from body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = convert_front_matter(parts[1])
            body = convert_concept_tags(parts[2])
            content = f'---{fm}---{body}'
        else:
            content = convert_concept_tags(content)
    else:
        content = convert_concept_tags(content)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)

    converted += 1

print(f'Migrated {converted} posts to {DST}')
