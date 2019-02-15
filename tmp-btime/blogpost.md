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

## Podpora btime v Linuxových souborových systémech

Podobně jako jiná unixová jádra, Linux dlouhou dobu btime nepodporoval.
Souborový systém ext3 nebo reiserfs btime neukládá a syscall
[`stat(2)`](http://man7.org/linux/man-pages/man2/stat.2.html) vrací
strukturu stejného jména taktéž bez této časové značky.
[O podpoře btime v Linuxu se sice mluví už nějaký
čas](https://www.redhat.com/archives/ext3-users/2006-October/msg00015.html),
ale na rozdíl od FreeBSD nešlo prostě přidat novou časovou značku někam do
volného padding místa stávající struktury `stat`, protože Linux tam takové
místo nemá. Místo definice nové verze struktury `stat` obsahující btime se
ukázalo schůdnější [přidat btime do zcela nového volání `xstat()`, jehož
začlenění do jádra se bohužel na nějakou dobu
zadrhlo](https://lwn.net/Articles/397442/).

Linuxoví vývojáři nicméně začali přidávat podporu pro btime do
nových souborových systémů dávno před tím, než bylo jasné, jak se to nakonec
vyřeší.
Např. [ext4 dostal podporu pro btime již v roce 2007 v rámci patche přidávající
podporu pro nanosekundové časové značky](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef7f38359ea8b3e9c7f2cae9a4d4935f55ca9e80)
(diskový formát ext4 je stabilní od [kernelu
2.6.28](https://kernelnewbies.org/Linux_2_6_28) z prosince 2008).
[Btrfs v roce 2012](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9cc97d646216b6f2473fa4ab9f103514b86c6814),
přičemž jeho disk. formát je stabilní [zhruba od listopadu 2013](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=4204617d142c0887e45fda2562cb5c58097b918e).
Do XFS, které původně btime neimplementovalo, se [tato podpora přidala v rámci
změny přidávající kontrolní součty metadat v roce 2013](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=93848a999cf9b9e4f4f77dba843a48c393f33c59)
a je tak dostupná od [jádra 3.10](https://kernelnewbies.org/Linux_3.10#XFS_metadata_checksums).
To znamená, že i na relativně staré distribuci souborový systém dost možná
ukládá pro každý soubor btime, i když tato informace není pro uživatele přímo
přístupná. Bez podpory v kernelu se k ní lze většinou dostat přes debugging
nástroje, které jsou ale pro každý souborový systém jiné, a které pochopitelně
vyžadují root oprávnění pro přímý přístup k blokovému zařízení se souborovým
systémem.

### Jak na čtení btime za použití debug nástrojů

Nejdříve si (pro účely tohoto blogu) vytvoříme nové oddíly na hraní:

~~~ {.kod}
# mkfs.ext4 /dev/vdc
# mount /dev/vdc /mnt/test_ext4
# echo "ext4" > /mnt/test_ext4/testfile
~~~

~~~ {.kod}
# mkfs.xfs /dev/vdd
# mount /dev/vdd /mnt/test_xfs
# echo "xfs" > /mnt/test_xfs/testfile
~~~

Jen pro úplnost: použil systém s Debianem Stretch (aktuální stable),
aby byla ukázka blíže realitě. Stretch totiž obsahuje kernel, který už má btime
podporu pro ext4 i XFS, ale ještě neumí btime předat do userspace.
Postup popsaný níže sice bude fungovat i na novějších distribucích, ale v
momentě, kdy máme možnost použít syscall, nemá smysl se s tím takto párat.
Jinak zahrnul bych sem i btrfs, ale nepodařilo se mi zjistit, jak z něj btime
dostat.

V případě ext4 použijeme
[`debugfs`](http://man7.org/linux/man-pages/man8/debugfs.8.html) a jeho příkaz
`stat`, v jehož výstupu najdeme čas vzniku souboru jako `crtime`:

~~~ {.kod}
# TZ=CET debugfs -R 'stat testfile' /dev/vdc
debugfs 1.43.4 (31-Jan-2017)
Inode: 12   Type: regular    Mode:  0644   Flags: 0x80000
Generation: 1318526178    Version: 0x00000000:00000001
User:     0   Group:     0   Project:     0   Size: 5
File ACL: 0    Directory ACL: 0
Links: 1   Blockcount: 8
Fragment:  Address: 0    Number: 0    Size: 0
 ctime: 0x5c66c5ee:2060896c -- Fri Feb 15 15:00:14 2019
 atime: 0x5c66c600:ee5ed49c -- Fri Feb 15 15:00:32 2019
 mtime: 0x5c66c5ee:2060896c -- Fri Feb 15 15:00:14 2019
crtime: 0x5c66c5ee:2060896c -- Fri Feb 15 15:00:14 2019
Size of extra inode fields: 32
Inode checksum: 0x0721e8ea
EXTENTS:
(0):32897
~~~

Pro soubor na XFS oddílu obdobně použijeme `xfs_db`. Nejdřív si však musíme
zjistit inode souboru co nás zajímá a pak odpojit (nebo připojit read only)
xfs filesystém. Čas vzniku souboru najdeme ve výpisu jako `v3.crtime.sec` a
``v3.crtime.nsec``:

~~~ {.kod}
# ls -i /mnt/test_xfs/testfile
99 /mnt/test_xfs/testfile
# umount /mnt/test_xfs
# TZ=CET xfs_db /dev/vdd
xfs_db> inode 99
xfs_db> print
core.magic = 0x494e
core.mode = 0100644
core.version = 3
core.format = 2 (extents)
core.nlinkv2 = 1
core.onlink = 0
core.projid_lo = 0
core.projid_hi = 0
core.uid = 0
core.gid = 0
core.flushiter = 0
core.atime.sec = Fri Feb 15 16:11:36 2019
core.atime.nsec = 155502016
core.mtime.sec = Fri Feb 15 16:11:36 2019
core.mtime.nsec = 155502016
core.ctime.sec = Fri Feb 15 16:11:36 2019
core.ctime.nsec = 155502016
core.size = 0
core.nblocks = 0
core.extsize = 0
core.nextents = 0
core.naextents = 0
core.forkoff = 0
core.aformat = 2 (extents)
core.dmevmask = 0
core.dmstate = 0
core.newrtbm = 0
core.prealloc = 0
core.realtime = 0
core.immutable = 0
core.append = 0
core.sync = 0
core.noatime = 0
core.nodump = 0
core.rtinherit = 0
core.projinherit = 0
core.nosymlinks = 0
core.extsz = 0
core.extszinherit = 0
core.nodefrag = 0
core.filestream = 0
core.gen = 559694043
next_unlinked = null
v3.crc = 0x40d2f493 (correct)
v3.change_count = 3
v3.lsn = 0x100000002
v3.flags2 = 0
v3.cowextsize = 0
v3.crtime.sec = Fri Feb 15 16:11:36 2019
v3.crtime.nsec = 155502016
v3.inumber = 99
v3.uuid = 425730b5-1254-45db-8e31-87f25c75f6cd
v3.reflink = 0
v3.cowextsz = 0
u3 = (empty)
~~~

Pozor na to, že příkaz `stat -v` z `xfs_io` btime neukáže:

~~~ {.kod}
# mount /dev/vdd /mnt/test_xfs
# TZ=CET xfs_io -r /mnt/test_xfs/testfile -c 'stat -v'
fd.path = "/mnt/test_xfs/testfile"
fd.flags = non-sync,non-direct,read-only
stat.ino = 99
stat.type = regular file
stat.size = 0
stat.blocks = 0
stat.atime = Fri Feb 15 16:11:36 2019
stat.mtime = Fri Feb 15 16:11:36 2019
stat.ctime = Fri Feb 15 16:11:36 2019
fsxattr.xflags = 0x0 []
fsxattr.projid = 0
fsxattr.extsize = 0
fsxattr.cowextsize = 0
fsxattr.nextents = 0
fsxattr.naextents = 0
dioattr.mem = 0x200
dioattr.miniosz = 512
dioattr.maxiosz = 2147483136
~~~

Další potenciální zádrhel u XFS je, že [podporu pro btime v XFS nenajdete
na RHELu 7](https://blog.fpmurphy.com/2014/06/rhel7-xfs-is-a-step-backwards-forensically.html),
protože jak jsme si řekli před chvílí, XFS umí ukládat btime až od jádra 3.10.

### Čteme btime z Linuxového ext4 na FreeBSD

Vtipné je, že pokud připojíte Linuxem vytvořený ext4 filesystém na
FreeBSD, tak pomocí nativního `stat` příkazu btime pro soubory
uložené na tomto Linuxovém oddílu přečtete. A to navzdory tomu, že podpora
Linuxových souborových systémů je na FreeBSD pochopitelně omezená, a např. to
ext4 lze přes
[`ext2fs`](https://www.freebsd.org/cgi/man.cgi?query=ext2fs&apropos=0&sektion=5&manpath=FreeBSD+12.0-RELEASE+and+Ports&arch=default&format=html)
připojit jen pro čtení (případně přes FUSE i pro zápis, ale to jsem nezkoušel).

Takto to dopadne, když se na FreeBSD 12 pokusíme přečíst btime na ext4 oddílu z
předchozího pokusu. Pořadí časových značek ve výstupu je `st_atime`,
`st_mtime`, `st_ctime` a `st_birthtime`:

~~~ {.kod}
# mount -t ext2fs -o ro /dev/vtbd1 /mnt/test_ext4
# cat /mnt/test_ext4/testfile
ext4
# env TZ=CET stat /mnt/test_ext4/testfile
92 12 -rw-r--r-- 1 root wheel 127754 5 "Feb 15 15:00:32 2019" "Feb 15 15:00:14
2019" "Feb 15 15:00:14 2019" "Feb 15 15:00:14 2019" 4096 8 0
/mnt/test_ext4/testfile
~~~

## Podpora btime v GNU Linux distribucích

Takže podporu btime v Linuxových souborových systémech bychom měli. Ale aby nám
to k něčemu bylo, je potřeba mít možnost předat tuto informaci z kernelu do
userspace. Jak už jsem zmínil výše, [btime mělo být možné získat pomocí volání
`xstat()`, jehož začlenění se zadrhlo](https://lwn.net/Articles/397442/), aby
se [po několika letech vynořilo v nové podobě jako
`statx()`](https://lwn.net/Articles/685791/), které se nakonec do jádra
dostalo a je tak dostupné od
[Linuxu 4.11](https://kernelnewbies.org/Linux_4.11#statx.282.29.2C_a_modern_stat.282.29_alternative)
z dubna 2017.
[Podpora v glibc](https://sourceware.org/bugzilla/show_bug.cgi?id=21297)
existuje od
[glibc 2.28](https://www.sourceware.org/ml/libc-alpha/2018-08/msg00003.html)
ze srpna 2018. To znamená, že např. na Fedoře 29 se to dá už vyzkoušet.

Následující kód ukazuje, jak pomocí
[`statx(2)`](http://man7.org/linux/man-pages/man2/statx.2.html) přečíst pro
daný soubor právě pouze btime. To že je možné jádru říct o která metadata máme
zájem, díky čemuž se jádro nemusí namáhat se zjišťováním hodnot které stejně
nepoužijeme, je mimochodem jedna z hlavních výhod volání `statx(2)` oproti
`stat(2)`.

~~~ {.kod .c include="btime.c"}
~~~

Pokud máte na své distribuce glibc starší než 2.28 ale přitom jádro máte
alespoň 4.11, musíte zavolat `statx(2)` s pomocí `syscall(2)`.

Program vypisuje pouze samotnou časovou značku v unixovém formátu, zavináč na
začátku je pro zjednodušení dekódování času pomocí nástroje `date`:

~~~
$ make btime
cc     btime.c   -o btime
$ ./btime btime
@1550254543.238843517
$ ./btime btime | date -f- --rfc-3339=ns
2019-02-15 19:15:43.238843517+01:00
~~~

Když si připojíme ext4 oddíl z předchozích pokusů, dostáváme očekávaný
výsledek:

~~~ {.kod}
$ ./btime /mnt/test_ext4/testfile | date -f- --rfc-3339=ns
2019-02-15 15:00:14.135799387+01:00
~~~

Bohužel, tímto podpora btime v základních komponentách GNU Linux distribucí
zatím končí. Stat z GNU Coreutils stále vypisuje btime jako "-" ani žádný jiný
základní nástroj jako např. `ls` nebo `tar` s btime přes `statx(2)` na Linuxu
pracovat neumí.

Díval jsem se na zdroják stat z coreutils, a ukázalo se, že díky hacku
řešící podporu btime pro Solaris není až tak těžké tam btime s pomocí
`statx(2)` dotat:

~~~ {.kod .diff include="linux-btime-hack.patch"}
~~~

Podstata tohoto patche je v tom, že se volá klasický `stat(2)` jako předtím a
pak si navíc přes `statx(2)` ještě řekneme o btime. Na hraní to stačí:

~~~ {.kod}
$ touch ~/tmp/test
$ ./stat ~/tmp/test
  File: /home/martin/tmp/test
  Size: 0               Blocks: 0          IO Block: 4096   regular empty file
Device: fd07h/64775d    Inode: 7377267     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  martin)   Gid: ( 1000/  martin)
Access: 2019-02-15 19:52:40.499658659 +0100
Modify: 2019-02-15 19:52:40.499658659 +0100
Change: 2019-02-15 19:52:40.499658659 +0100
 Birth: 2019-02-15 19:52:40.499658659 +0100
$ touch ~/tmp/test
$ ./stat ~/tmp/test
  File: /home/martin/tmp/test
  Size: 0               Blocks: 0          IO Block: 4096   regular empty file
Device: fd07h/64775d    Inode: 7377267     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  martin)   Gid: ( 1000/  martin)
Access: 2019-02-15 19:52:46.598671520 +0100
Modify: 2019-02-15 19:52:46.598671520 +0100
Change: 2019-02-15 19:52:46.598671520 +0100
 Birth: 2019-02-15 19:52:40.499658659 +0100
~~~

Tohle "řešení" ale není zcela vhodné na začlenění do coreutils, protože používá
zbytečně 2 volání jádra místo jednoho, a celé je to navíc postavená nad jiným
hackem. K tomu abych stat upravil nějak rozumně jsem se ale zatím nedostal, a
podle toho, že na coreutils listu mi nikdo neodpověděl, bych řekl, že na
tom aktuálně nikdo nedělá.

## Co to btime vlastně znamená a k čemu je dobré?

TODO: kompatibilita a windows, samba, ntfs

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
* [RHEL7 XFS Is A Step Backwards Forensically](https://blog.fpmurphy.com/2014/06/rhel7-xfs-is-a-step-backwards-forensically.html): popisuje jak z XFS a ext4 dostat btime pomocí debug nástrojů
* [How to find creation date of file?](https://unix.stackexchange.com/questions/91197/how-to-find-creation-date-of-file)
* [task_diag and statx()](https://lwn.net/Articles/685791/) z lwn.net (2016)

Historické zdroje:

* [Unix History Repository](https://github.com/dspinellis/unix-history-repo)
* [Enhancements to the Fast Filesystem To Support Multi-Terabyte Storage
  Systems](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/):
  paper o designu UFS2 filesystému, mj. obsahuje popis jak je tu birth time
  implementovaný
