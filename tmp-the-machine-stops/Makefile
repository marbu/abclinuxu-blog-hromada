PANDOCFLAGS=--filter pandoc-codeblock-include

preview.html: blogpost.md
	pandoc -s --toc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.tmp.html: blogpost.md
	pandoc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.tmp.html
	../bin/abclinuxu-html-filter.py $? -o $@

clean:
	rm -f blogpost.html blogpost.tmp.html preview.html
