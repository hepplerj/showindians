preview :
	jekyll serve --watch --drafts

build :
	rm -rf _site/*
	jekyll build

deploy : build
	
	sh _scripts/permissions_fix.sh
	
	rsync --omit-dir-times --exclude-from=rsync-excludes \
		--checksum -avz \
		--itemize-changes \
		_site/ reclaim:~/progressivewildwest.org/ | egrep -v '^\.'

.PHONY: preview build deploy