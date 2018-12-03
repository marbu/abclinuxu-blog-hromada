preview.html: blogpost.md
	pandoc -s --toc -f markdown -t html $? -o $@

blogpost.html: blogpost.md
	pandoc -f markdown -t html $? -o $@

clean:
	rm -f blogpost.html preview.html
