PANDOCFLAGS=--filter pandoc-codeblock-include

preview.html: blogpost.md
	pandoc -s --toc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.md
	pandoc -f markdown -t html $(PANDOCFLAGS) $? -o $@

clean:
	rm -f blogpost.html preview.html
