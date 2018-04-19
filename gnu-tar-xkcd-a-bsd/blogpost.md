Pamatujete si na xkcd komix, kde atomová bomba pro odjištění vyžaduje validní
příklad použití taru? Ať ano či ne, v tomto blogu se o nástroji GNU tar dozvíte
co už dost možná stejně víte, případně co jste asi ani nechtěli vědět.

<!--break-->

Pro připomenutí (přece jen, ten díl vyšel už před pár lety):

[![tar](tar.png)](https://www.xkcd.com/1168/)

Poznámka: pro alt text musíte kliknout na odkaz.

Hned z kraje musím přiznat, že mi tato narážka přišla tak trochu přehnaná.
Tohle sice není v rámci vtipu nic divného, ale přece jenom tar nepatří mezi
nástroje, jehož volby musím nějak často dohledávat. Možná by se v tomto
kontextu lépe vyjímal např. git, ale ten postrádá oproti taru další
bombastické asociace (narážka na [tar
bombu](https://en.wikipedia.org/wiki/Tar_(computing)#Tarbomb) nebo [Tsar
bombu](https://en.wikipedia.org/wiki/Tsar_Bomba)
), což ho pro potřeby toho vtipu maličko diskvalifikuje.

Na druhou stranu je ale pravda, že když jsem kdysi dávno používal na
rozbalování archivů [`extract` script z Archlinux
wiki](https://wiki.archlinux.org/index.php/Bash/Functions#Extract), používat
přímo `tar` bych bez man stránky nebo googlení taky nemohl. A přitom, jak jsem
později taky zjistil, to není nijak krkolomné :-)

Ve většině případů si vystačím s tím, že `tar xf soubor.tar.gz` rozbalí archiv
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

``` {.kod}
tar -caf soubor.tar.gz soubor
```

a srovnání s GNU stylem snad ani nemá cenu komentovat (btw tady si můžete
všimnout jedné drobnosti, a to  že jsem v předchožím odstavci trochu kecal, a
to `a` není od *archive*):

``` {.kod}
tar --create --auto-compress --file soubor.tar.gz soubor
```

Skutečnost ale může být jednodušší na vysvětlení. Ty BSD volby
používám dost možná jen proto, že jsem to velmi dávno někde viděl a od té
doby to tak pořád dokola ze setrvačnosti používám, anichž bych se na tím nějak
extra zamýšlel. A trochu hádám, že tahle, možná trochu náhodná setrvačnost,
nebude jenom můj případ.

Podobně můžete různě po internetu vidět ukázky použití taru s písmenky jako
`z` nebo `j`, které určují typ použitého kompresního programu (`z` je pro
`gzip`, `j` pro `bzip2`).
Pokud ale budete chtít použít např. `xz`, nevím jestli budete mít radost,
až z man stránky zjistíte, že odpovídající jednopísmenková volba je `J`.
I když na druhou stranu, je to GNU tar ... takže je tam i rozumná dlouhá verze
té volby `--xz` a díky tomu, že už jim došly písmenka, se žádné další
jednoznakové zkratky pro kompresní algoritmy nepřidávají.
A přitom výše zmíněná volba auto compress je v GNU tar již skoro 10 let
(od verze 1.20 vydané 14. 4. 2008), takže se to už mezitím
aktuálně dostalo i do distribucí typu [RHEL 6](http://ftp.redhat.com/redhat/linux/enterprise/6Server/en/os/SRPMS/tar-1.23-15.el6_8.src.rpm)
nebo [Debianu oldstable](https://packages.debian.org/jessie/tar).

Na druhou stranu ale hodně štěstí, pokud byste tuhle GNU fičuru chtěli použít
na např. OpenBSD:

``` {.kod}
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
volby příkazové řádky. Proč by na té bombě nemohla běžet nějaká extra stará
Linuxová distribuce, FreeBSD nebo snad Solaris? Tuhle možnost bych ale dál
dovolil pro potřeby tohoto blogu zanedbat. Konec konců, tento problém mají
všechny tradiční unixové nástroje, ne jen tar.

Když se ale na chvíli vrátím k volbám nástroje GNU tar a měl bych vybrat
ještě jednu která stojí za zmínku, je to `t` neboli `--list`, která vypisuje
seznam souborů v archivu:

``` {.kod}
$ tar tf passthrough.tar.xz
Makefile
passthrough.1
passthrough.c
```

Tím bychom měli výčet command line voleb pro GNU tar, co imho stojí za
zapamatování, kompletní. Všechno ostatní hledám v man stránce, která ale dokáže
už jen díky samotnému počtu funkcí implementovaných v GNU taru občas překvapit.

Např. nedávno jsem potřeboval vygenerovat checksum ze všech souborů v archivu
aniž bych celý archiv rozbaloval (jednak to není nutné a druhak jsem
na to ani zrovna neměl volný diskový prostor) a ukázalo se, že tar umožňuje
volbou `--to-command` specifikovat příkaz, kterému se předá obsah každého
jednotlivého rozbaleného souboru na standardní vstup.
Takže pomocí wrapper skriptu pro `sha1sum` (pro potřeby dalšího příkladu
uloženého v `~/bin/tar-sha1-t.sh`):

``` {.kod}
#!/bin/bash
# see also: man tar, https://unix.stackexchange.com/questions/303667/
echo -n $(sha1sum) | sed 's/ .*$//'
echo " $TAR_FILENAME"
```

Lze nechat tar přímo vypsat sha1 checksum souborů v archivu:

``` {.kod}
$ tar xf foo.tar.gz --to-command=~/bin/tar-sha1-t.sh
384dcab2b0e67e940406d1bbfd1b083c61319ce4 foobar.png
e1c272d5abe7d339c4047d76294e7400c31e63b4 README
```

A nebo se taky může stát, že narazíte na vám dosud neznámou tar fičuru zcela
náhodou. Např. v tomto případě jsem nejdřív moc nechápal, co se děje:

``` {.kod}
$ tar caf ccpp-2018-03-03-23:10:55-3667.tar.gz ccpp-2018-03-03-23:10:55-3667
tar (child): Cannot connect to ccpp-2018-03-03-23: resolve failed
tar: Child returned status 128
tar: Error is not recoverable: exiting now
```

Proč by jako tar měl komunikovat s někým po sítí na základě jména souboru? Ale
po chvíli hledání se ukázalo, že:

> An archive name that has a colon in it specifies a file or device on a
> remote machine. The part before the colon is taken as the machine name or IP
> address, and the part after it as the file or device pathname, e.g.:
>
> --file=remotehost:/dev/sr0
>
> An optional username can be prefixed to the hostname, placing a @ sign
> between them.

A pokud se vám to nelíbí, tak GNU tar nabízí volbu:

> --force-local
>
> Archive file is local even if it has a colon.

Takže následující příkaz již funguje bezvadně:

``` {.kod}
$ tar --force-local -caf ccpp-2018-03-03-23:10:55-3667.tar.gz ccpp-2018-03-03-23:10:55-3667
```

Ale pokud se takový archiv pokusíte přečíst a zapomenete na tu dvojtečku, opět
máte problém:

``` {.kod}
$ tar tf ccpp-2018-03-03-23\:10\:55-3667.tar.gz
tar: Cannot connect to ccpp-2018-03-03-23: resolve failed
```

Ať žijí rozumné výchozí volby a zpětná kompatibilita. Schválně jsem se musel
podívat, jak dlouho tam tohle chování je a v NEWS souboru jsem našel:

``` {.kod}
Version 1.11 - Michael Bushnell, 1992-09.
Version 1.10.16 - 1992-07.
Version 1.10.15 - 1992-06.
Version 1.10.14 - 1992-05.
Version 1.10.13 - 1992-01.

* Remote archive names no longer have to be in /dev: any file with a
':' is interpreted as remote.  If new option --force-local is given,
then even archive files with a ':' are considered local.
```

Upřímně nechápu, jak tohle někomu přišlo jako rozumný nápad, ale asi mi chybí
historický kontext. A asi není ani třeba dodávat, že tar z OpenBSD tohle
neimplementuje.

Důležitý detail, který jsem zatím vynechal je, jakým protokolem se tar chce
na vzdálený stroj připojit:

> By default, the remote host is accessed via the rsh(1) command.  Nowadays it
> is common to use ssh(1) instead.

Takže dneska už ssh, což si můžete sami zkusit na vhodně pojmenovaném tarballu:

``` {.kod}
$ tar tf localhost:foo.tar.gz
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:TgLgqk9xkWb2oGtBRgk1vKPvWzbgdkp0InR0PZHXnbQ.
ECDSA key fingerprint is MD5:48:16:9c:eb:b8:22:0f:ab:22:b4:71:a5:3e:54:2c:7f.
Are you sure you want to continue connecting (yes/no)?
```

:-)

To už možná stojí za úvahu, zda takové [chování není natolik
podivné](http://www.abclinuxu.cz/blog/c/2018/1/shellova-zabava/diskuse#5), že
by se dalo považovat do jisté míry za bezpečnostní problém. Např. by šlo
pojmenovat tarball tak, že při pokusu o jeho rozbalení [vás UPC
odpojí](http://www.abclinuxu.cz/portal/poradna/show/434589#2) nebo by šlo
pokusit se o deanomizaci nepozorného uživatele tor sítě. Ale oba ty příklady
jsou víc absurdní než praktické.

O něco lepší by bylo např. nachystat na vzdáleném
serveru tarball s jiným obsahem, který by si oběť nevědomky stáhla a rozbalila
místo skutečného obsahu tarballu - teda za předpokladu, že nikomu nebude divné,
že v názvu tarballu je vaše doména a název souboru, že odhadnete jaký login
oběť používá, že budete mít ssh public key oběti a že oběť buď pro tento ssh
klíč nepoužívá heslo nebo jej má v cache ssh agenta a k tomu všemu by bylo taky
dobré, aby fingerprint vašeho ssh serveru oběť už měla mezi known hosts nebo
ještě lépe, aby bylo toto ověřování zcela vypnuté. Něco
málo z toho by mohl usnadnit github a jeho automatické zveřejňování public ssh
klíčů ...  ale to už si připadám jako v jiném xkcd komixu, jen místo příběhu s
hackováním regexpů v perlu na laně dosaďte tento odstavec (I know GNU tar colon
hack!), je to asi tak stejně praštěné:

[![regular expressions](regular_expressions.png)](https://www.xkcd.com/208/)

Nicméně, vážně to funguje:

``` {.kod}
$ cd ~/tmp
$ touch good-file bad-file
$ tar caf bad.tar.gz bad-file
$ tar --force-local -caf localhost:bad.tar.gz good-file
$ cp bad.tar.gz ~
$ tar tf localhost:bad.tar.gz
bad-file
$ tar --force-local -tf localhost:bad.tar.gz
good-file
```

Opačná varianta, kdy někomu poradíte jak "správně" pojmenovat tarball aby pak
posléze nahrál data na váš server je asi taky možná, ale ještě uhozenější.

Takže ve výsledku tohle nevypadá použitelně ani jako kanadský žertík ... možná
snad kdyby byl někdo extra šikovný při vymýšlení a nasazování shell skriptu
používajícího tar, ale i to mi přijde dost nepravděpodobné :)

Pokud jsem někoho snad inspiroval k nahlédnutí man stránky pro GNU tar, nebo
ještě lépe k prostudování [GNU tar
dokumentace](https://www.gnu.org/software/tar/manual/tar.html), nechť se podělí
v komentářích o jeho oblíbenou funkcionalitu.

<!-- anketa

V příkazové řádce používám pro tar volby typu:
* bsd (c)
* unix (-c)
* gnu (--create)

Bombu z komixu bych:
* s klidem odjistil
* nechal/přinutil explodovat

Tu věc s dvojteckou v názvu tarballu jsem:
* neznal
* znal ale nepoužíval
* znal a používal

Je ta věc s dvojteckou bezpečnostní problém?:
* ano
* ne
-->
