PANDOCFLAGS=-f markdown

preview.html: blogpost.md
	pandoc -s --toc $(PANDOCFLAGS) -t html $< -o $@

robinson.epub: blogpost.md
	pandoc -s --toc $(PANDOCFLAGS) -t epub $< -o $@

blogpost.html: blogpost.md
	pandoc $(PANDOCFLAGS) -t html $< -o $@

clean:
	rm -f blogpost.html preview.html
