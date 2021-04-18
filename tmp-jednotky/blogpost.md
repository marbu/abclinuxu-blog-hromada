---
title: Podpora pro rozměrovou analýzu v programovacích jazycích
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
...

TODO: úvod

<!--break-->

## Ada

Kdysi dávno jsem na root.cz četl [článek o programovacím jazyku
Ada](https://www.root.cz/clanky/bezpecne-programovani-ala-ada/), kde autor mimo
jiné ukazoval, jak lze silný typový systém jazyka použít k tomu, aby za nás
překladač hlídal fyzikální rozměr hodnot v programu podobně jako jsme na to
zvyklí u běžných datových typů. Demonstrace z toho článku vypadala nějak takto:

```
type Metry is new Float;
type Ctverecni_Metry is new Float;

-- Přetížení operátoru násobení pro datový typ metry tak, aby vracel metry
-- čtvereční.
function "*" (Left, Right : Metry) return Ctverecni_Metry is
begin
  return Ctverecni_Metry(Float(Left)*Float(Right));
  -- před násobením jsme přetypovali na float, abychom zabránili rekurzi
  -- takto donutíme překladač použít standardní násobení pro typ Float
end;

declare
  vyska : Metry := 10.0;
  sirka : Metry := 15.0;
  plocha_a : Ctverecni_Metry;
  plocha_b : Metry;
begin
  plocha_a := vyska*sirka; -- tohle je ok
  plocha_b := vyska*sirka; -- zde nastane chyba prekladu
end;
```

Pamatuju si že to na mě tenkrát udělalo dojem. Ale je to už dávno, tehdy jsem
moc programovacích jazyků neznal a ani jsem to dál nezkoumal. Na druhou stranu
jsem si z toho taky mylně na chvíli odnesl dojem, že podobné věci jsou
záležitostí silně typovaných a málo používaných jazyků jako Ada. Což ale není
úplně přesné, jak si ještě ukážeme.

Když jsem se k tomu teď ze zvědavosti vrátil a chtěl si to vyzkoušet (v
repozitáři Fedory nebo Debianu lze najít balíček s GNU Ada překladačem
[GNAT](https://en.wikipedia.org/wiki/GNAT)), ukázalo se, že je třeba ten kód
trochu vylepšit, aby to ve skutečnosti opravdu fungovalo. Což v tomto případě
znamená, aby to šlo přeložit s chybou, která demonstruje, jak to hlídání
jednotek pěkně funguje :-)

```
$ nl example1.adb
     1  procedure Example1 is
     2    type Meters is new Float;
     3    type Meters_Squared is new Float;
     4    function "*" (Left, Right : Meters) return Meters_Squared is
     5    begin
     6      return Meters_Squared(Float(Left)*Float(Right));
     7    end;
     8    function "*" (Left, Right : Meters) return Meters is abstract;
     9    len_a : Meters := 10.0;
    10    len_b : Meters := 15.0;
    11    surface : Meters_Squared;
    12    len_sum : Meters;
    13  begin
    14    len_sum := len_a + len_b; -- ok
    15    surface := len_a * len_b; -- ok
    16    len_sum := len_a * len_b; -- invalid
    17  end Example1;
```

Když opominu uhlazení dělající z toho příkladu samostatný Ada program,
bylo třeba přidat deklaraci `function "*" (Left, Right : Meters) return Meters
is abstract`, která [tuto variantu násobení zděděnou z typu `Float`
potlačí](https://stackoverflow.com/questions/67141246/naive-unit-checking-via-strong-typing-and-operator-overloading).
A překlad pak opravdu chybu v rozměru zachytí, i když ta chybová hláška vypadá
trochu zvláštně:

```
$ gnatmake -q example1.adb
example.adb:16:20: expected type "Meters" defined at line 2
example.adb:16:20: found type "Meters" defined at line 2
gnatmake: "example.adb" compilation error
```

Je z toho vidět, že modelování některých fyzikálních rozměrů tímto způsobem
nemusí být zcela přímočaré ani praktické. I když jednodušší případy můžou
fungovat pěkně, jako třeba při [práci s metry a
mílemi](https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html#strong-typing).

Pro [jazyk Ada v přehledu metod rozměrové
analýzy](https://gmpreussner.com/research/dimensional-analysis-in-programming-languages#ada)
se dozvíme, že tohle bylo jasné už někdy v 80. letech, kdy se tento problém
začal řešit. Např. [N. H. Gehani v článku z roku
1985](https://doi.org/10.1002/spe.4380150604) popisuje použití typového
systému s přetížením operátorů (podobně jako to dělá naše ukázka výše) a
dochází k tomu, že to obecně nefunguje:

> Derived types only partially solve the problem of detecting the inconsistent
> usage of objects; some valid usages of objects are also not allowed.
> Moreover, the solution is inelegant and inconvenient to use.

To vedlo k návrhu různých knihoven zavádějících datové struktury obsahující
hodnotu spolu s jednotkou a funkce pro práci s nimi. A něco takového je
možné implementovat v libovolném jazyce, i když konkrétní přístup a garance, co
knihovna programátorovi dává, se můžou v závislosti na možnosti jazyka dost
lišit.

Překladač [GNAT dnes implementuje systém pro kontrolu rozměrů
veličin](https://gcc.gnu.org/onlinedocs/gnat_ugn/Performing-Dimensionality-Analysis-in-GNAT.html),
který staví na tzv. [*Aspects* ze standadru Ada
2012](https://docs.adacore.com/gnat_rm-docs/html/gnat_rm/gnat_rm/implementation_defined_aspects.html#implementation-defined-aspects),
a je doplněn knihovnou [`System.Dim.Mks` s definicí základních fyzikálních
jednotek dle SI](https://github.com/gcc-mirror/gcc/blob/master/gcc/ada/libgnat/s-digemk.ads).

S použitím tohoto rozšíření by náš příklad vypadal takto:

```
$ nl example2.adb
     1  with System.Dim.Mks; use System.Dim.Mks;
     2  procedure Example2 is
     3    len_a : Length := 10.0*m;
     4    len_b : Length := 15.0*m;
     5    surface : Area;
     6    len_sum : Length;
     7  begin
     8    len_sum := len_a + len_b; -- ok
     9    surface := len_a * len_b; -- ok
    10    len_sum := len_a * len_b; -- invalid
    11  end Example2;
```

A jak se můžeme přesvědčit, opravdu to funguje:

```
$ gnatmake -q -gnat2012 example2.adb
example2.adb:10:11: dimensions mismatch in assignment
example2.adb:10:11: left-hand side has dimension [L]
example2.adb:10:11: right-hand side has dimension [L**2]
gnatmake: "example2.adb" compilation error
```

## F\#

Asi jediný programovací jazyk s přímou podporou pro práci s jednotkami, o
kterém jste možná už někdy slyšeli, je `F#`.

[Units of measure](https://fsharpforfunandprofit.com/posts/units-of-measure/)

## Python

[Pint](https://pint.readthedocs.io/en/stable/)

## Závěr

Pokud vás tohle téma zaujalo, doporučuji se podívat na přehledový článek
[Dimensional Analysis in Programming
Languages](https://gmpreussner.com/research/dimensional-analysis-in-programming-languages),
kde najdete rozsáhlý přehled implementací rozměrové analýzy v mnoha
programovacích jazycích.
