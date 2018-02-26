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

Hned z kraje musím přiznat, že mi tato narážka přišla tak trochu přehnaná.
Tohle sice není v rámci vtipu nic divného, ale přece jenom tar nepatří mezi
nástroje, jehož volby musím nějak často dohledávat. Což se nedá tak úplně říct o
jiném populárním konzolovém nástroji, který by se v tomto kontextu vyjímal víc,
ale git postrádá oproti taru další bombastické asociace (narážka na [tar
bombu](https://en.wikipedia.org/wiki/Tar_(computing)#Tarbomb) nebo [Tsar
bombu](https://en.wikipedia.org/wiki/Tsar_Bomba)
), což ho pro potřeby toho vtipu maličko diskvalifikuje.

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

Tady se hodí dodat, že i když na strojích, kam mám aspoň ssh přístup, je skoro
vždy nainstalován [GNU tar](https://www.gnu.org/software/tar/)
implementace taru, je v předchozích příkladech použit pro volby příkazové
řádky BSD styl, který z nějakého iracionálního důvodu pro tar preferuju.

Možná je to tím, že v unixovém stylu bych oproti BSD verzi musel psát jeden
znak navíc:

```
tar -caf soubor.tar.gz soubor
```

a srovnání s GNU stylem snad ani nemá cenu komentovat (btw tady si můžete
všimnout jedné drobnosti, a to  že jsem v předchožím odstavci trochu kecal, a
to `a` není od *archive*):

```
tar --create --auto-compress --file soubor.tar.gz soubor
```

Skutečnost ale bude asi trochu jednodušší na vysvětlení. Ty BSD volby
používám dost možná jen proto, že jsem to velmi dávno někde viděl a od té
doby to tak pořád dokola ze setrvačnosti používám, anichž bych se na tím nějak
extra zamýšlel. A trochu hádám, že tahle, možná trochu náhodná setrvačnost,
nebude jenom můj případ.

Podobně můžete různě po internetu vidět ukázky použití taru s písmenky jako
`z` nebo `j`, které určují typ použitého kompresního programu (`z` je pro
`gzip`, `j` pro `bzip2`).
Pokud ale budete chtít použít např. `xz`, nevím jestli budete mít radost z
toho, až z man stránky zjistíte že odpovídající jednopísmenková volba je `J`.
I když na druhou stranu, je to GNU tar ... takže je tam i rozumná dlouhá verze
té volby `--xz` a díky tomu, že už jim došly písmenka, se žádné další
jednoznakové zkratky pro kompresní algoritmy nepřidávájí.
A přitom výše zmíněná volba auto compress je v GNU tar již skoro 10 let (podle
changelog souboru od verze 1.20 vydané 14. 4. 2008), takže se to už mezitím
aktuálně dostalo i do distribucí typu RHEL 6 nebo [Debianu
oldstable](https://packages.debian.org/jessie/tar).

Na druhou stranu ale hodně štěstí, pokud byste tuhle GNU fíčuru chtěli použít
na např. OpenBSD:

```
$ tar caf archive.tar.gz random.c file1.c
tar: unknown option a
usage: tar {crtux}[014578befHhjLmNOoPpqsvwXZz]
           [blocking-factor | archive | replstr] [-C directory] [-I file]
           [file ...]
       tar {-crtux} [-014578eHhjLmNOoPpqvwXZz] [-b blocking-factor]
           [-C directory] [-f archive] [-I file] [-s replstr] [file ...]
```

A tady se dostáváme k možnosti, že si ten komix dělá dost možná srandu i z
toho, jak různé implementace taru (např. výše zmíněná GNU vs OpenBSD) chápou
volby příkazové řadky. Proč by na té bombě nemohla běžet nějaká extra stará
Linuxová distribuce, FreeBSD nebo snad Solaris? Tuhle možnost bych ale dál
dovolil pro potřeby tohoto blogu zanedbat. Konec konců, tento problém mají
všechny tradiční unixové nástroje, ne jen tar.

Když se ale na chvíli vrátím k těm volbám nástroje GNU tar a měl bych vybrat
ještě jednu která stojí za zmínku, je to `t` neboli `--list`, která vypisuje
seznam souborů v archivu:

```
$ tar tf passthrough.tar.xz
Makefile
passthrough.1
passthrough.c
```

Tím bychom měli výčet command line voleb, co si stojí za zapamatování
kompletní. Na všechno ostatní je tu man stránka.

složitější a složitější příklady
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

<!-- anketa
používám volbu:
* gnu
* unix
* bsd

bombu z komixu bych:
* odjistil
* ...
-->
