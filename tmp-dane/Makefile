PANDOCFLAGS=-f markdown

preview.html: blogpost.md
	pandoc -s --toc -t html $(PANDOCFLAGS) $? -o $@

blogpost.tmp.html: blogpost.md
	pandoc -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.tmp.html
	../bin/abclinuxu-html-filter.py $? -o $@

clean:
	rm -f blogpost.html blogpost.tmp.html preview.html
