desc "give title as argument and create new entry"
# usage rake write["Post Title Goes Here","date","category"]
# category is optional
# date should be in YYYY-MM-DD format
task :write, [:title, :sourcedate, :category] do |t, args|
  filename = "#{args.sourcedate}-#{args.title.gsub(/\s/, '-').downcase}.md"
  path = File.join("_posts", filename)
  if File.exist? path; raise RuntimeError.new("Won't clobber #{path}"); end
  File.open(path, 'w') do |file|
    file.write <<-EOS
---
layout: single
created: #{Time.now}
title: #{args.title}
author: 
date: #{args.sourcedate}
source: 
tags:
- 
category: #{args.category}
---

![#{args.title}](path/to/jpg.jpg "#{args.title}")

# #{args.title}

EOS
    end
    puts "Now opening #{path} in vim..."
    system "vim #{path}"
end
