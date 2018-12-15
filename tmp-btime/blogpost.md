---
title: Jak je to s podporou btime na (GNU) Linuxu
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
...

TODO: intro (zmínit co je btime, aka birth time)

<!--break-->

Zarazilo vás někdy, že
[`stat`](http://man7.org/linux/man-pages/man1/stat.1.html) z [GNU
Coreutils](https://www.gnu.org/software/coreutils/) vypisuje kromě klasické
trojice unixových časových značek navíc také "Birth", u kterého ale hodnota
chybí?

```
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
Jen pro úplnost, na ukázce výše je stat z gnu coreutils 8.30, zavolaný na
souboru uloženém na etx4, to vše s jádrem 4.19.8.
&lt;/poznámka&gt;

Pro jistotu v rychlosti připomenu, že [unixové operační systémy pro každý
soubor udržují alespoň tyto tři časové
značky](https://en.wikipedia.org/wiki/Stat_(system_call)):

 * atime Access
 * mtime Modiry
 * ctime Change

A jak jste si jistě všimli, čas vzniku souboru mezi nimi není. Co tedy dělá to
"Birth" ve výstupu příkazu `stat`? A máme to celé číst tak, že Linux čas vzniku
souboru podporuje, ale zrovna ext4 to neumí?
