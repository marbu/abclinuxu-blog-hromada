PANDOCFLAGS=-f markdown

preview.html: blogpost.md
	pandoc -s --toc $(PANDOCFLAGS) -t html $< -o $@

robinson.epub: blogpost.md
	pandoc -s --toc $(PANDOCFLAGS) -t epub $< -o $@

blogpost.tmp.html: blogpost.md
	pandoc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.tmp.html
	../bin/abclinuxu-html-filter.py $? -o $@

clean:
	rm -f blogpost.html blogpost.tmp.html preview.html
