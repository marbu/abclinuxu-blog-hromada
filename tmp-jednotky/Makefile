PANDOCFLAGS=

preview.html: blogpost.md
	pandoc -s --toc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.tmp.html: blogpost.md
	pandoc -f markdown -t html $(PANDOCFLAGS) $? -o $@

blogpost.html: blogpost.tmp.html
	../bin/abclinuxu-html-filter.py $? -o $@

example1: example1.adb
	gnatmake -q $<

example2: example2.adb
	gnatmake -q -gnat2012 $<

clean:
	rm -f *.html example1 example2 *.ali *.o *.s
