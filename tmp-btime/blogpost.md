---
title: Jak je to s časem vzniku souboru na GNU Linux distribucích
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
papersize: a4
geometry: margin=2.5cm
links-as-notes: false
...

Zarazilo vás někdy, že příkaz
[`stat(1)`](http://man7.org/linux/man-pages/man1/stat.1.html) z [GNU
Coreutils](https://www.gnu.org/software/coreutils/) na Linuxu vypisuje kromě
klasické trojice unixových časových značek *access*, *modify* a *change* navíc
také jakési *birth*, u kterého ale hodnota chybí?
Co tu vůbec to prázdné *birth* dělá?
Zajímat o tuto málo známou časovou značku jsem se začal až před pár měsíci při
debugování jednoho problému, kdy jsem se snažil chytil čeho se dalo. A i když
mi to nakonec přímo nepomohlo, postupně jsem se začal nořit do její historie a
budoucnosti, takže tento zápisek je někde na pomezí softwarové archeologie a
jaderných novinek, a mj. se v něm dozvíte, kde se tato časová značka vzala,
jak s ní dnes na GNU Linuxových distribucích pracovat a jak to s ní vypadá
do budoucna.

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

&lt;hint&gt;
Nějakou dobu se mi pletlo, jaký je rozdíl mezi mtime (modify) a ctime (change)
a např. při hledání souborů podle data jsem si to musel čas od času dohledávat.
Na základě informací z předchozího textu se ale nabízí pomůcka pro zapamatování
rozdílu: ctime je timestamp, co se lidem občas plete s *creation time* a co
nějakou dobu v Unixu vůbec nebyl, takže je z těch dvou to bude ten méně
významný, tedy ten co popisuje změnu metadat/inode (což je něco, co mě většinou
nezajímá).
&lt;/hint&gt;

Kdy se poprvé objevila časová značka pro *creation time*, neboli *birth time*
(btime), je těžké s jistotou říct, protože je možné, že to bylo v rámci
nějakého proprietárního Unixového systému. A vzhledem k tomu, že takové systémy
jsou v dnešní době většinou mrtvé bez dostupné dokumentace nebo zdrojového kódu
pod rozumnou licencí, se mi ani nechce něco takového dohledávat.
V rámci unixových systémů s otevřeným zdrojovým kódem je ale toto prvenství
jasné: časová značka pro *creation time* se poprvé objevila až v roce 2003 ve
[FreeBSD 5.0](https://www.freebsd.org/releases/5.0R/announce.html)
s příchodem souborového systému
[UFS2](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/),
a odtud se postupně rozšířila do ostatních BSD systémů, jako jsou
[NetBSD](http://cvsweb.netbsd.org/bsdweb.cgi/src/sys/sys/stat.h?rev=1.42&content-type=text/x-cvsweb-markup&only_with_tag=MAIN)
nebo
[OpenBSD](https://github.com/openbsd/src/commit/cc2fc615c6e2dee87e5a3cd5a655a2ee5ef778c8).

Za povšimnutí stojí, jak podporu pro *birth time* ve FreeBSD přidali. Díky
tomu, že FreeBSD mělo ve struktuře stat nevyužité místo, nebylo [přidání
další časové značky pojmenované `st_birthtime` do této
struktury](https://github.com/dspinellis/unix-history-repo/blob/FreeBSD-release/5.0.0/sys/sys/stat.h)
problém z hlediska zpětné kompatibility. [Aktuálně se tato časová značka ale
jmenuje `st_birthtim`](https://www.freebsd.org/cgi/man.cgi?query=stat&apropos=0&sektion=2&manpath=FreeBSD+13-current&arch=default&format=html),
aby její pojmenování a význam odpovídalo konvenci z normy POSIX
(viz tabulka výše).

[OpenSolaris](https://en.wikipedia.org/wiki/OpenSolaris) čas vzniku souboru
sice také podporuje, ale strukturu `stat` ponechal beze změn. Pro získání
hodnoty btime je tak třeba použít volání
[fgetattr(3C)](https://www.unix.com/man-page/opensolaris/3C/fsetattr/) a ze
seznamu vrácených attributů přečíst `A_CRTIME`. Tato podpora je zdá se
přítomna už v prvním commitu projektu OpenSolaris z roku 2005, takže
pravděpodobně pochází ze Solarisu.

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
místo nemá. Místo definice nové verze struktury `stat` se tak
ukázalo schůdnější navrhnout [přidání btime do zcela nového volání `xstat()`,
jehož začlenění do jádra se bohužel na nějakou dobu
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
předchozího pokusu. Pořadí časových značek ve výstupu je atime, mtime, ctime a
btime:

~~~ {.kod}
# mount -t ext2fs -o ro /dev/vtbd1 /mnt/test_ext4
# cat /mnt/test_ext4/testfile
ext4
# env TZ=CET stat /mnt/test_ext4/testfile
92 12 -rw-r--r-- 1 root wheel 127754 5 "Feb 15 15:00:32 2019" "Feb 15 15:00:14 2019" "Feb 15 15:00:14 2019" "Feb 15 15:00:14 2019" 4096 8 0 /mnt/test_ext4/testfile
~~~

## Podpora btime v GNU Linux distribucích

Takže podporu btime v Linuxových souborových systémech bychom měli. Ale aby nám
to k něčemu bylo, je potřeba mít možnost předat tuto informaci z kernelu do
userspace. Jak už jsem zmínil výše, [btime mělo být možné získat pomocí volání
`xstat()`, jehož začlenění se zadrhlo](https://lwn.net/Articles/397442/), aby
se [po několika letech vynořilo v nové podobě jako
`statx()`](https://lwn.net/Articles/685791/), které se nakonec do jádra
dostalo v
[Linuxu 4.11](https://kernelnewbies.org/Linux_4.11#statx.282.29.2C_a_modern_stat.282.29_alternative)
z dubna 2017.
[Podpora v glibc](https://sourceware.org/bugzilla/show_bug.cgi?id=21297)
existuje od
[glibc 2.28](https://www.sourceware.org/ml/libc-alpha/2018-08/msg00003.html)
ze srpna 2018. To znamená, že např. na Fedoře 29 se to dá už vyzkoušet.

Následující kód ukazuje, jak pomocí
[`statx(2)`](http://man7.org/linux/man-pages/man2/statx.2.html) přečíst pro
daný soubor právě pouze btime. To, že je možné jádru říct o která metadata máme
zájem, díky čemuž se jádro nemusí namáhat se zjišťováním hodnot, které stejně
nepoužijeme, je mimochodem jedna z hlavních výhod volání `statx(2)` oproti
`stat(2)`.

~~~ {.kod .c include="btime.c"}
~~~

Pokud máte na své distribuci glibc starší než 2.28 ale přitom jádro máte
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

### Stat z GNU Coreutils

Jak jsem připomněl v úvodu, stat z GNU Coreutils stále vypisuje btime jako "-".
Nabízí se ale otázka, proč se s tím stat vůbec obtěžuje, když tu až do
nedávné doby nebyla možnost, jak tuto informaci na Linuxu získat. Bližší pohled
však ukáže, že v knihovně [gnulib](https://www.gnu.org/software/gnulib/),
kterou stat používá, byla [podpora pro čtení btime ze struktury stat díky BSD*
systémům implementována již v roce
2007](http://git.savannah.gnu.org/cgit/gnulib.git/commit/?id=735c00a2f3a5ce7aaec8517f5438ce37b48a936c).
A samotný [kód pro zobrazování btime se do `stat(1)` přidal už v roce
2010](https://git.savannah.gnu.org/cgit/coreutils.git/commit/?id=abe5c1f9bc09753fd79e7a121c8ecfa917dfaddb),
hádám že v souvislosti s prvním návrhem systémového volání `xstat(2)`, které
se ale do jádra tehdy nakonec nedostalo. Každopádně díky tomu `stat(1)` od
[GNU Coreutils 8.6 z roku
2010](https://savannah.gnu.org/forum/forum.php?forum_id=6553) na Linuxu
vypisuje btime s hodnotou "-" (a to bez ohledu na to, co je to za souborový
systém), zatímco třeba na BSD systémech nebo
Solarisu je schopný tyto hodnoty i zobrazovat, pokud je filesystém podporuje.

Další pohled na zdrojový kód odhalí, že díky hacku řešící podporu btime pro
Solaris není až tak těžké tam btime s pomocí `statx(2)` volání dotat:

~~~ {.kod .diff include="linux-btime-hack.patch"}
~~~

Podstata tohoto hacku je v tom, že se volá klasický `stat(2)` jako předtím a
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
podle toho, že [na coreutils listu mi nikdo
neodpověděl](https://lists.gnu.org/archive/html/coreutils/2018-12/msg00016.html),
bych řekl, že na tom aktuálně nikdo nedělá.

### Stat z GNU Bash

Trochu jsem se zhrozil, když jsem četl [release notes pro Bash
5.0](https://lists.gnu.org/archive/html/bash-announce/2019-01/msg00000.html)
z ledna 2019, kde mezi novinkami je:

> d. New loadable builtins: rm, stat, fdflags.

Na první pohled by to mohlo vypadat, že než se podaří do stat z coreutils
přidat podporu pro btime, bude potřeba tuto práci udělat ještě jednou, protože
s příchodem bashe 5 budou všichni používat stat implementovaný přímo v shellu,
podobně jako např. v případě `time`:

~~~ {.kod}
$ type -a time
time is a shell keyword
time is /usr/bin/time
time is /bin/time
~~~

Ale ukázalo se, že to není tak horké, protože příslušný zdrojový kód
[`stat.c`](http://git.savannah.gnu.org/cgit/bash.git/tree/examples/loadables/stat.c)
se nachází v adresáři
[`examples/loadables/`](http://git.savannah.gnu.org/cgit/bash.git/tree/examples/loadables),
tj. jde o tzv. [*dynamic loadable
buildin*](http://www.drdobbs.com/shell-corner-bash-dynamically-loadable-b/199102950),
a vnitřní funkce umístěné zde, např. `cat.c` nebo `sleep.c`, nejsou běžně v
binárních balíčcích vůbec přítomné (jak si můžete ověřit pomocí výpisu `enable
-a`). Idea za tímto je taková, že pokud potřebujete zoptimalizovat shell
skript kde např. voláte ve smyčce sleep, [můžete si zkompilovat příslušný
buildin (případně si napsat vlastní) a pomocí `enable -f` ho do bashe
načíst](https://bbs.archlinux.org/viewtopic.php?pid=1366887#p1366887).
Osobně mi sice přijde rozumnější psát takový script třeba v pythonu, ale pokud
se není možné bashi vyhnout (např. protože jde o nějaký velký legacy skript),
ta možnost tu je.

A jak už jsem naznačil, implementace loadable buildin funkce `stat` v bashi s
btime pracovat neumí:

~~~ { .kod}
$ enable -f ~/projects/bash/examples/loadables/stat stat
$ help stat
stat: stat [-lL] [-A aname] file
    Load an associative array with file status information.

    Take a filename and load the status information returned by a
    stat(2) call on that file into the associative array specified
    by the -A option.  The default array name is STAT.  If the -L
    option is supplied, stat does not resolve symbolic links and
    reports information about the link itself.  The -l option results
    in longer-form listings for some of the fields. The exit status is 0
    unless the stat fails or assigning the array is unsuccessful.
$ stat ~/tmp/test
$ for i in "${!STAT[@]}"; do echo $i = ${STAT[$i]}; done
nlink = 1
link = /home/martin/tmp/test
perms = 0664
inode = 7377267
blksize = 4096
device = 64775
atime = 1550256766
type = -
blocks = 0
uid = 1000
size = 0
rdev = 0
name = /home/martin/tmp/test
mtime = 1550256766
ctime = 1550256766
gid = 1000
~~~

Ale v tomto případě mi přijde, že místo přidání podpory pro btime do této
`stat` buildin funkce by bylo lepší napsat jinou, která by mohla lépe využívat
možností jaderného volání `statx(2)`.

### Ostatní nástroje

Bohužel, podpora btime v základních komponentách GNU Linux distribucí zatím
končí u `statx(2)` wrapperu v glibc. Stejně jako výše uvedené implementace
nástroje `stat`, žádný základní nástroj jako např. `ls` nebo `find` s
btime na Linuxu pracovat neumí. Přitom podobně jako v případě `stat`,
např. `find` už základní podporu pro btime má, jen na Linuxu neumí jeho
hodnotu zatím přečíst. Na druhou stranu, díky tomu že btime je možné číst pouze
pomocí nového volání jádra `statx(2)`, nebudou často změny v těchto nástrojích
tak přímočaré, jak by se mohlo na první pohled zdát.

Dále také bude záležet na tom, zda se později neobjeví podpora pro změnu btime
v jaderných voláních jako
[`utimes(2)`](http://man7.org/linux/man-pages/man2/utimes.2.html) nebo
[`utimensat(2)`](http://man7.org/linux/man-pages/man2/utimensat.2.html).
Aktuální stav, kdy není možné libovolně nastavit btime má svou logiku, čas
vzniku souboru, pokud má opravdu dostát svému významu, by měl zůstat po zbytek
života souboru stejný, ale na druhé straně to také znamená, že není možné např.
archivovat soubor včetně btime pomocí `cp -a` nebo ho obnovit ze zálohy pomocí
`rsync`. Z tohoto důvodu bude asi implementace podpory btime v GNU tar trvat
trochu déle, protože není jasné, proč by tam někdo přidával podporu pro btime,
když by pak tato informace nešla na Linuxu obnovit při rozbalování archivu.

Tady se hodí poznamenat, že FreeBSD možnost měnit btime pomocí
[`utimes(2)`](https://www.freebsd.org/cgi/man.cgi?query=utimes&apropos=0&sektion=2&manpath=FreeBSD+12.0-RELEASE&arch=default&format=html)
nabízí od začátku, jak je popsané v
[článku o UFS2](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/).

## Co btime vlastně znamená a k čemu je to dobré?

Co vlastně znamená čas vzniku souboru? Jeden by řekl, že je to jasné, ale tak
jednoduché to úplně není. Nejen vzhledem k výše zmíněné nemožnosti btime
nastavit jde o low level informaci, o kterou např. při kopírování souboru
přijdeme (z pohledu fs jde o nový soubor). Jiný častý případ kdy btime ztratíme
je, když [aplikace zapisuje do souboru atomicky s pomocí přejmenování dočasného
souboru](https://unix.stackexchange.com/a/45812/58336).

Btw nikdy předtím jsem si neuvědomil, že tohle atomické zapisování dělá např.
i vim (všiměte si změny v inode a času vzniku souboru):

~~~ { .kod }
$ rm ~/tmp/test
$ touch ~/tmp/test
$ stat.hacked ~/tmp/test
  File: /home/martin/tmp/test
  Size: 0         	Blocks: 0          IO Block: 4096   regular empty file
Device: fd07h/64775d	Inode: 7377286     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  martin)   Gid: ( 1000/  martin)
Access: 2019-02-17 09:51:45.483720811 +0100
Modify: 2019-02-17 09:51:45.483720811 +0100
Change: 2019-02-17 09:51:45.483720811 +0100
 Birth: 2019-02-17 09:51:45.483720811 +0100
$ vim ~/tmp/test
$ stat.hacked ~/tmp/test
  File: /home/martin/tmp/test
  Size: 5         	Blocks: 8          IO Block: 4096   regular file
Device: fd07h/64775d	Inode: 7377267     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  martin)   Gid: ( 1000/  martin)
Access: 2019-02-17 09:52:17.151767057 +0100
Modify: 2019-02-17 09:52:17.151767057 +0100
Change: 2019-02-17 09:52:17.156767065 +0100
 Birth: 2019-02-17 09:52:17.151767057 +0100
~~~

A tímto se konečně dostáváme k otázce k čemu je to btime vlastně dobré.
Jak je vidět z doby, která byla potřeba aby se btime podpora dostala v
použitelné podobě do jádra, nikdo tomu nepřipisuje velkou prioritu. To je
vidět taky z toho, že změny implementující btime se často objevují v
commitech, jejichž hlavní náplní je něco jiného. Ať už v případě ext4, kdy
hlavní cíl byl implementovat nanosekundové časové značky. Podobně XFS přidává
btime v rámci zavádění kontrolních součtů metadat a syscall `statx(2)` nebyl
vytvořen jen kvůli čtení btime. Lecos naznačuje i to, za celou 50 letou
historii Unixu to nikdo nenavrhl na přidání do POSIX standardu.

Když se podíváme na důvody implementace btime v Linuxu, kromě stručného
"UFS2/ZFS to má taky" často vidíme zmínky o Sambě a kompatibilitě s Windows.
Bohužel, Samba nemůže Linuxový btime v současné podobně přímo využít, protože
Windows umožňuje čas vzniku souboru libovolně  měnit. Také
[NTFS-3G](https://en.wikipedia.org/wiki/NTFS-3G) by mohl teoreticky čas vzniku
souboru z Windows reportovat na Linuxu pomocí btime. Prakticky se tím ale
nikdo nebude zabývat dokud se podpora pro `statx(2)` nepřidá do FUSE a alespoň
nástroje z coreutils budou umět s btime pracovat. Navíc [NTFS-3G už teď umí
předat btime pomocí rozšířených
atributů](https://www.tuxera.com/community/ntfs-3g-advanced/extended-attributes/#filetimes),
i když možnost použít `ls` by byla rozhodně pohodlnější.

Nová časová značka se ale každopádně dá dobře využít při debugování nějakého
podivného chování, kdy se každá stopa navíc hodí, ať už je za ním útočník,
malware nebo ne zcela fungující software nebo hardware. Mimo těchto
"detektivních" případů se btime dá využít i pro opačné účely. Např.
by [teoreticky šlo do souborových časových značek nepozorovaně ukládat malé
množství dat](https://www.dfrws.org/sites/default/files/session-files/paper_anti-forensics_in_ext4_on_secrecy_and_usability_of_timestamp-based_data_hiding.pdf).
Paradoxně v obou případech je ale aktuální stav, kdy je btime podpora pouze v
kernelu, vlastně výhodný. Pro forenzní analýzu je užitečné, že je vzhledem k
menší povědomí o btime pravděpodobnost jeho falšování nižší. A pro opačné
případy je zase pěkné, že "zneužívání" btime není tak na očích.

## Reference

Články k tématu:

* [File creation times](https://lwn.net/Articles/397442/) z lwn.net (2010),
  česky v jaderných novinkách jako [Časy vytvoření
  souboru](http://www.abclinuxu.cz/clanky/jaderne-noviny-28.-7.-2010-potrebuje-linux-znat-cas-vytvoreni-souboru#casy-vytvoreni-souboru),
* Heslo [stat (system call)](https://en.wikipedia.org/wiki/Stat_(system_call)) z
  anglické wikipedie,
* Heslo [Comparison of file
  systems](https://en.wikipedia.org/wiki/Comparison_of_file_systems) z anglické
  wikipedie,
* Otázka [How to find creation date of file?](https://unix.stackexchange.com/questions/91197/how-to-find-creation-date-of-file)
  z unix.stackexchange.com,
* [task_diag and statx()](https://lwn.net/Articles/685791/) z lwn.net (2016),
* Článek [Anti-forensics in ext4: On secrecy and usability of timestamp-baseddata
  hiding](https://www.dfrws.org/sites/default/files/session-files/paper_anti-forensics_in_ext4_on_secrecy_and_usability_of_timestamp-based_data_hiding.pdf),
* Článek/přednáška [Forensic Timestamp Analysis of
  ZFS](http://www.bsdcan.org/2014/schedule/track/Security/464.en.html)
  z konference BSDCan 2014.

Historické zdroje:

* [Unix History Repository](https://github.com/dspinellis/unix-history-repo)
* [Enhancements to the Fast Filesystem To Support Multi-Terabyte Storage
  Systems](https://www.usenix.org/legacy/events/bsdcon03/tech/full_papers/mckusick/mckusick_html/):
  paper o designu UFS2 filesystému, mj. obsahuje popis jak je tu birth time
  implementovaný
* [OpenSolaris project repository](https://repo.or.cz/opensolaris.git)
