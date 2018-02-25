# GNU tar, xkcd a BSD

Pamatujete si na xkcd komix, kde atomová bomba pro odjištění vyžaduje validní
příklad použití taru?

<!--break-->

<!-- osnova:
xkcd: bomba
archlinux script: https://wiki.archlinux.org/index.php/Bash/Functions#Extract
tar mnemotech 'xaf'
// bsd aux, cliff stoll
sha1sum hack
zajimave chovani:
xkcd - new skill
odpojeni od upc
iptables detection

see also:
https://www.gnu.org/software/tar/
https://git.savannah.gnu.org/git/tar.git
https://en.wikipedia.org/wiki/Tar_(computing)
-->

Pro připomenutí (přece jen, ten díl vyšel zhruba před 5 lety):

https://www.xkcd.com/1168/

Hned z kraje musím přiznat, že mi tato narážka přišla vždycky trochu přehnaná.
Tohle sice není v rámci vtipu nic divného, ale přece jenom tar nepatří mezi
nástroje, jehož volby musím nějak často dohledávat. Což se ale nedá říct o
jiném populárním konzolovém nástroji, který by se v tomto kontextu vyjímal víc,
ale git postrádá oproti taru další bombastické asociace (narážka na [tar
bombu](https://en.wikipedia.org/wiki/Tar_(computing)#Tarbomb) nebo [Tsar
bombu](https://en.wikipedia.org/wiki/Tsar_Bomba)
), což ho pro potřeby toho vtipu zřejmě diskvalifikuje.

Na druhou stranu je ale pravda, že když jsem kdysi dávno používal na
rozbalování archivů [`extract` script z Archlinux
wiki](https://wiki.archlinux.org/index.php/Bash/Functions#Extract), používat
přímo `tar` bych bez man stránky nebo googlení taky nemohl. A přitom, jak jsem
později taky zjistil, to není nijak krkolomné :-)

Ve většině případů si vystačím tím, že `tar xf soubor.tar.gz` rozbalí archiv
(kde `xf` si pamatuji jako e**x**tract **f**ile), zatímco pro zabalení souboru
použiju `tar caf soubor.tar.gz soubor` (kde `caf` je **c**reate **a**rchive
**f**ile) a typ archivu (v tomto případě `tar.gz`) tar hádá podle přípony
cílového souboru.

Tady se hodí dodat, že i když je v předchozích příkladech použit BSD styl pro
volby příkazové řádky (který z nějakého iracionálního důvodu pro tar
preferuju), GNU tar je normálně zvládá taky. Tj. že GNU tar normálně vezme:

```
tar caf foo.tar.xz tmp/foo
tar --create --file
```

Možnost, že si komix dělá srandu mimojiné i z toho, jak různé implementace taru
(např.  GNU vs OpenBSD vs Irix verze) chápou volby příkazové řádny bych tu ale
přešel. Konec konců, tento problém mají všechny tradiční unixové nástroje, ne
jen tar.  Např.  ps aux

když se ale vrátím
test, že to a tam nemusí být
v je verbose
z,f a jiný potvory znací konkrétní verze kompresního nástroje

složitější a složitější příklady

Na všechno ostatní je tu man stránka.

pozor, jednoduchý případ může překvapit:



<!-- zajimave chovani

~~~
[root@dhcp-126-79 abrt]# tar caf ccpp-2017-03-21-23:10:55-3667.tar.gz ccpp-2017-03-21-23:10:55-3667
tar (child): Cannot connect to ccpp-2017-03-21-23: resolve failed
~~~

~~~
$ tar cvzf ccpp-2017-03-21-23\:10\:55-3667.tar.gz ccpp-2017-03-21-23\:10\:55-3667/
ccpp-2017-03-21-23:10:55-3667/
ccpp-2017-03-21-23:10:55-3667/foobar.py
tar (child): Cannot connect to ccpp-2017-03-21-23: resolve failed
tar: Child returned status 128
tar: Error is not recoverable: exiting now
~~~

Ah:

> If the archive file name includes a colon (‘:’), then it is assumed to be a
> file on another machine. If the archive file is ‘user @host :file ’, then
> file is used on the host host. The remote host is accessed using the rsh
> program
-->
