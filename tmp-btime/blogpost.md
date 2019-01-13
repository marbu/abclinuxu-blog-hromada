---
title: Jak je to s podporou času vzniku souboru na GNU Linux distribucích
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
...

Zarazilo vás někdy, že příkaz
[`stat`](http://man7.org/linux/man-pages/man1/stat.1.html) z [GNU
Coreutils](https://www.gnu.org/software/coreutils/) na Linuxu vypisuje kromě
klasické trojice unixových časových značek `access`, `modify` a `change` navíc
také jakési `birth`, u kterého ale hodnota chybí?
Co tu vůbec to prázdné `birth` dělá? A máme to celé číst tak, že Linux čas
vzniku souboru podporuje, ale ne u každého souborového systému?

<!--break-->

``` {.kod}
$ stat public_html
  File: public_html
  Size: 4096      	Blocks: 8          IO Block: 4096   directory
Device: fd07h/64775d	Inode: 7341469     Links: 2
Access: (0755/drwxr-xr-x)  Uid: ( 1000/  martin)   Gid: ( 1000/  martin)
Context: unconfined_u:object_r:httpd_user_content_t:s0
Access: 2018-12-09 12:59:16.321622899 +0100
Modify: 2018-05-19 21:35:13.813112882 +0200
Change: 2018-12-09 02:51:38.961313721 +0100
 Birth: -
$
```

&lt;poznámka&gt;
Jen pro úplnost, na ukázce výše je stat zavolaný na souboru uloženém na etx4.
To vše na Fedoře 29, s Coreutils 8.30 a jádrem 4.19.8.
&lt;/poznámka&gt;

## Souborové časové značky na Unixových systémech

Unixové souborové časové značky, jak je vrací [systémové volání
stat](https://en.wikipedia.org/wiki/Stat_(system_call)), jsou standardizované v
normě
[POSIX](http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_stat.h.html)
takto:

Časová značka  Položka v `struct stat`  Význam
-------------  -----------------------  ------------------------------------
access         `st_atim`                poslední přístup k datům souboru
modify         `st_mtim`                poslední změna dat souboru
change         `st_ctim`                poslední změna statusu (inode) souboru

To, že se položka pro *access time* ve struktuře `stat` aktuálně jmenuje
`st_atim` je dáno tím, že v ní je čas počítaný na nanosekundy, zatímco
původní a dnes už zastaralé `st_atime` počítá čas se sekundovou přesností a je
udržováno kvůli zpětné kompatibilitě. V Linuxu je tohle implementováno už od
verze 2.5.48, viz
[`stat(2)`](http://man7.org/linux/man-pages/man2/stat.2.html). Dál v textu budu
místo *access time* psát prostě atime, místo *modify time* mtime a pod, bez
ohledu na rozdíl mezi `st_atim` a `st_atime`.

Z pohledu tohoto zápisku je ale důležitější a na první pohled nápadné to, že
čas vzniku souboru tu nenajdeme.

Přitom pokud si někdo unixem nezasažený zběžně prohlédne jména časových značek
v struktuře `stat` (viz tabulka víše), mohl by si myslet, že že čas vzniku
souboru podporované je a že ctime je asi zkratka pro *creation time*. Další
studium man stránky by ale tento omyl rychle vyvrátilo. Podobně pokud si někdo
dnes přečte článek [The UNIX Time-Sharing
System](https://www.bell-labs.com/usr/dmr/www/cacm.html) od tvůrců Unixu z roku
1973, mohlo by ho napadnout, že ctime opravu původně vznik souboru
reprezentovalo, protože se v něm mimo jiné píše:

> The entry found thereby (the file's i-node) contains the description of the
> file:
> ...
> time of creation, last use, and last modification

Nicméně jak [upozorňuje
wikipedie](https://en.wikipedia.org/w/index.php?title=Stat_(system_call)&oldid=872237631#ctime),
to by byl opět omyl. Přeštože časné verze Unixu čas vzniku souboru skutečně
podporovaly, brzy od toho bylo upuštěno a Unix uchovával jen atime a mtime.
Tato zmněna se odehrála ještě před tím, než byl Unix přepsán do jazyka C a tím
i před první verzí struktury stat. Jinými slovy ctime od začátku opravdu
znamenalo *change time*.

<!--
unix history repo: see evidence
BSD a btime
e5e436e5f3a09f58142efaafb4d64c352b78f20a commit
Linux - no API
-->

<!-- hint
Btw docela dlouho se mi pletlo, jaký je rozdíl mezi mtime a ctime a např. při
hledání souborů podle data jsem si to musel přes man stránky dohledávat, ale .
-->

Jestli někdo uvažuje o přidání btime do POSIX standardu nevím, nepodařilo se mi
o tom nic dohledat.

## Linuxové souborové systémy

ext3 ne, zatímco ext4 už ano
nové btrfs ano
xfs původně ne (např. RHEL 7)

## GNU Linux distribuce

TODO: timeline

~~~ {.kod .c include="btime.c"}
~~~

~~~ {.kod .diff include="linux-btime-hack.patch"}
~~~

## Co to btime vlastně znamená?

TODO: example

## Reference

Pěkně články k tématu:

* [File creation times](https://lwn.net/Articles/397442/) z lwn.net (2010),
  česky v jaderných novinkách jako [Časy vytvoření
  souboru](http://www.abclinuxu.cz/clanky/jaderne-noviny-28.-7.-2010-potrebuje-linux-znat-cas-vytvoreni-souboru#casy-vytvoreni-souboru),
* Heslo [stat (system call)](https://en.wikipedia.org/wiki/Stat_(system_call)) z
  anglické wikipedie,
