---
title: Jak je to s podporou času vzniku souboru na GNU Linux distribucích
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
papersize: a4
geometry: margin=2.5cm
links-as-notes: false
...

Zarazilo vás někdy, že příkaz
[`stat`](http://man7.org/linux/man-pages/man1/stat.1.html) z [GNU
Coreutils](https://www.gnu.org/software/coreutils/) na Linuxu vypisuje kromě
klasické trojice unixových časových značek *access*, *modify* a *change* navíc
také jakési *birth*, u kterého ale hodnota chybí?
Co tu vůbec to prázdné *birth* dělá? A máme to celé číst tak, že Linux čas
vzniku souboru podporuje, ale ne u každého souborového systému?
<!-- TODO: dopsat shrnutí o čem to je -->

<!--break-->

Pro lepší představu o čem tu píšu. Na následující ukázce je stat zavolaný
na souboru uloženém na etx4. To vše na Fedoře 29, s GNU Coreutils 8.30 a jádrem
4.19.8:

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
change         `st_ctim`                poslední změna statusu souboru (inode)

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
v struktuře `stat` (viz tabulka výše), mohl by si myslet, že čas vzniku
souboru podporovaný je a že ctime je asi zkratka pro *creation time*. Další
studium man stránky by ale tento omyl rychle vyvrátilo. Podobně pokud si
dnes přečtete článek [The UNIX Time-Sharing
System](https://www.bell-labs.com/usr/dmr/www/cacm.html) od tvůrců Unixu z roku
1973, mohlo by vás napadnout, že ctime opravu původně vznik souboru
reprezentovalo aby se jeho význam později změnil, protože v tomto článku se
mimo jiné píše:

> The entry found thereby (the file's i-node) contains the description of the
> file:
> ...
> time of creation, last use, and last modification

Nicméně jak [upozorňuje
wikipedie](https://en.wikipedia.org/w/index.php?title=Stat_(system_call)&oldid=872237631#ctime),
to by byl opět omyl. Několik prvních verzí tzv. [Research
Unixu](https://en.wikipedia.org/wiki/Research_Unix) sice čas vzniku souboru
skutečně
podporovalo, jak se můžeme přesvědčit např. v [man stránce pro `stat(2)` z
verze 3
](https://github.com/dspinellis/unix-history-repo/blob/Research-V3-Snapshot-Development/man/man2/stat.2)
z února roku 1973:

``` {.kod}
NAME            stat  --  get file status

SYNOPSIS        sys stat; name; buf  / stat = 18.

DESCRIPTION     name  points to a null-terminated string naming a
file; buf is the address of a 34(10) byte buffer into  which  in-
formation  is  placed  concerning the file.  It is unnecessary to
have any permissions at all with respect to the file, but all di-
rectories leading to the file must be readable.

After stat, buf has the following format:

buf, +1         i-number
+2,+3           flags (see below)
+4              number of links
+5              user ID of owner
+6,+7           size in bytes
+8,+9           first indirect block or contents block
+22,+23         eighth indirect block or contents block
+24,+25,+26,+27 creation time
+28,+29,+30,+31 modification time
+32,+33         unused
```

Btw zajímavé taky je, že příkaz stat z téže verze *creation time* neuvádí, tedy
aspoň dle [man stránky
`stat(1)`](https://github.com/dspinellis/unix-history-repo/blob/Research-V3-Snapshot-Development/man/man1/stat.1),
zdroják se mi nepodařilo dohledat:

``` {.kod}
NAME            stat  --  get file status

SYNOPSIS        stat name1 ...

DESCRIPTION     stat gives several kinds of information about one
or more files:

   i-number
   access mode
   number of links
   owner
   size in bytes
   date and time of last modification
   name (useful when several files are named)
```

Ale hned v další verzi (Research) Unixu, tj. verzi 4 z listopadu 1973, již
čas vzniku souboru nenajdeme. Za povšimnutí stojí, že V4 byla první verze
Unixu napsaná v céčku. Díky tomu tak byly (mimo jiné) poprvé
zavedeny názvy položek ve struktuře stat, které se ale trochu liší od dnes
používaných.  Viz opět [manstránka `stat(2)` z
V4](https://github.com/dspinellis/unix-history-repo/blob/Research-V4-Snapshot-Development/man/man2/stat.2):

``` {.kod}
stat  get file status (stat = 18.)
sys stat; name; buf stat(name, buf)
char *name;
struct  inode  *buf;  points to a null-terminated string naming a
file; is the address of a 36(10) byte buffer into which  informa-
tion  is  placed  concerning the file.  It is unnecessary to have
any permissions at all with respect to the file, but all directo-
ries leading to the file must be readable.  After has the follow-
ing structure (starting offset given in bytes):
struct {
   char  minor;         /* +0: minor device of i-node */
   char  major;         /* +1: major device */
   int   inumber        /* +2 */
   int   flags;         /* +4: see below */
   char  nlinks;        /* +6: number of links to file */
   char  uid;           /* +7: user ID of owner */
   char  gid;           /* +8: group ID of owner */
   char  size0;         /* +9: high byte of 24-bit size */
   int   size1;         /* +10: low word of 24-bit size */
   int   addr[8];       /* +12: block numbers or device number */
   int   actime[2];     /* +28: time of last access */
   int   modtime[2];    /* +32: time of last modification */
};
```

Časová značka ctime se pak poprvé objevila až [ve verzi
7](https://github.com/dspinellis/unix-history-repo/blob/Research-V7-Snapshot-Development/usr/sys/h/stat.h)
z ledna 1979, a to hned v dnešním významu *change time*, takže ctime opravdu
*creation time* nikdy neznamenalo:

``` {.kod}
struct	stat
{
	dev_t	st_dev;
	ino_t	st_ino;
	unsigned short st_mode;
	short	st_nlink;
	short  	st_uid;
	short  	st_gid;
	dev_t	st_rdev;
	off_t	st_size;
	time_t	st_atime;
	time_t	st_mtime;
	time_t	st_ctime;
};
```

V této podobě pak časové značky ze struktury stat vydržely až do POSIX
standardu a dnešních dní (tedy až na ten výše zmiňovaný detail s milisekundovou
přesností).

Časová značka pro *creation time*, neboli *birth time* (btime), se
poprvé objevila až v roce 2003 ve [FreeBSD
5.0](https://www.freebsd.org/releases/5.0R/announce.html)
s příchodem souborového systému
[UFS2](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/),
a odtud se postupně rozšířila do ostatních BSD systémů, jako jsou
[NetBSD](http://cvsweb.netbsd.org/bsdweb.cgi/src/sys/sys/stat.h?rev=1.42&content-type=text/x-cvsweb-markup&only_with_tag=MAIN)
nebo
[OpenBSD](https://github.com/openbsd/src/commit/cc2fc615c6e2dee87e5a3cd5a655a2ee5ef778c8).
Je možné, že podobné rozšíření implementoval i jiný proprietární Unixový systém
o něco dřív a trochu jinak, ale těžko se to dá ověřit, když takové systémy jsou
v dnešní době mrtvé bez dostupné dokumentace nebo zdrojového kódu pod rozumnou
licencí (k Solarisu se ještě později vrátím).

Za povšimnutí stojí, jak podporu pro *birth time* ve FreeBSD přidali. Díky
tomu, že FreeBSD mělo ve struktuře stat nevyužité místo, nebylo [přidání
další časové značky pojmenované `st_birthtime` do této
struktury](https://github.com/dspinellis/unix-history-repo/blob/FreeBSD-release/5.0.0/sys/sys/stat.h)
problém z hlediska zpětné kompatibility. [Aktuálně se tato časová značka ale
jmenuje `st_birthtim`](https://www.freebsd.org/cgi/man.cgi?query=stat&apropos=0&sektion=2&manpath=FreeBSD+13-current&arch=default&format=html),
aby její pojmenování a význam odpovídalo konvenci z normy POSIX
2008 (viz tabulka výše).

<!-- hint
Btw docela dlouho se mi pletlo, jaký je rozdíl mezi mtime a ctime a např. při
hledání souborů podle data jsem si to musel přes man stránky dohledávat, ale .
-->

Jestli někdo uvažuje o přidání btime do POSIX standardu nevím, nepodařilo se mi
o tom nic dohledat. Řekl bych, že to dnes asi už nikomu nestojí za námahu.

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

Přehledové články k tématu:

* [File creation times](https://lwn.net/Articles/397442/) z lwn.net (2010),
  česky v jaderných novinkách jako [Časy vytvoření
  souboru](http://www.abclinuxu.cz/clanky/jaderne-noviny-28.-7.-2010-potrebuje-linux-znat-cas-vytvoreni-souboru#casy-vytvoreni-souboru),
* Heslo [stat (system call)](https://en.wikipedia.org/wiki/Stat_(system_call)) z
  anglické wikipedie,
* Heslo [Comparison of file
  systems](https://en.wikipedia.org/wiki/Comparison_of_file_systems) z anglické
  wikipedie,

Historické zdroje:

* [Unix History Repository](https://github.com/dspinellis/unix-history-repo)
* [Enhancements to the Fast Filesystem To Support Multi-Terabyte Storage
  Systems](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/)
  paper o designu UFS2 filesystému, mj. obsahuje popis jak je tu birth time
  implementovaný
