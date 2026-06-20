default: preview

preview:
    python3 _scripts/extract_concepts.py
    hugo server

build:
    python3 _scripts/extract_concepts.py
    hugo --minify

deploy: build
    sh _scripts/permissions_fix.sh
    rsync --omit-dir-times --exclude-from=rsync-excludes \
        --checksum -avz \
        --itemize-changes \
        public/ reclaim:~/progressivewildwest.org/ | egrep -v '^\.'
