PANDOCFLAGS=--filter pandoc-codeblock-include

preview.html: blogpost.md
	pandoc -s --toc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.md
	pandoc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.pdf: blogpost.md
	pandoc -s -f markdown -t latex $(PANDOCFLAGS) $? -o $@

clean:
	rm -f blogpost.html blogpost.pdf preview.html btime
