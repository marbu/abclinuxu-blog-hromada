PANDOCFLAGS=-f markdown

preview.html: blogpost.md preklady.png
	pandoc -s --toc $(PANDOCFLAGS) -t html $< -o $@

preklady.png: preklady.py preklady.tsv
	./preklady.py -o $@

blogpost.tmp.html: blogpost.md preklady.png
	pandoc $(PANDOCFLAGS) -t html $< -o $@

blogpost.html: blogpost.tmp.html
	../bin/abclinuxu-html-filter.py $? -o $@

clean:
	rm -f preklady.png blogpost.html preview.html
