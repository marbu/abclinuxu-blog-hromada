---
title: Podpora pro rozměrovou analýzu v programovacích jazycích
author: marbu
lang: cs-CZ
rights: cc by-sa 4.0
...

Kdysi dávno jsem na root.cz četl [článek o programovacím jazyku
Ada](https://www.root.cz/clanky/bezpecne-programovani-ala-ada/), kde autor mimo
jiné ukazoval, jak lze silný typový systém jazyka použít k tomu, aby za nás
překladač hlídal fyzikální rozměr hodnot v programu podobně, jako jsme na to
zvyklí u běžných datových typů. Nedávno jsem si na to znovu vzpomněl, chvíli si
s tím hrál a v tomto zápisku dal dohromady triviální demonstraci současných
možností podpory jednotek v jazycích Ada, F# a Python.

<!--break-->

## Ada

Demonstrace z toho článku o jazyku Ada vypadala nějak takto:

``` {.kod}
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

Pamatuji si, že to na mě tenkrát udělalo dojem. Ale tehdy jsem
moc programovacích jazyků neznal a ani jsem to dál nezkoumal. Na druhou stranu
jsem si z toho taky mylně na chvíli odnesl dojem, že podobné věci jsou
záležitostí silně typovaných a málo používaných jazyků jako Ada. Což ale není
úplně přesné, jak si ještě ukážeme.

Když jsem se k tomu teď ze zvědavosti vrátil a chtěl si to vyzkoušet (v
repozitáři Fedory nebo Debianu lze najít balíček s GNU Ada překladačem
[GNAT](https://en.wikipedia.org/wiki/GNAT)), ukázalo se, že je třeba ten kód
trochu vylepšit, aby to ve skutečnosti opravdu fungovalo. Což v tomto případě
znamená, aby to šlo přeložit s chybou, která demonstruje, jak to hlídání
jednotek pěkně funguje (-:

``` {.kod include="example1.adb"}
```

Když opominu uhlazení dělající z toho příkladu samostatný Ada program,
bylo třeba přidat deklaraci `function "*" (Left, Right : Meters) return Meters
is abstract`, která [tuto variantu násobení zděděnou z typu `Float`
potlačí](https://stackoverflow.com/questions/67141246/naive-unit-checking-via-strong-typing-and-operator-overloading).
A překlad pak opravdu chybu v rozměru zachytí, i když ta chybová hláška vypadá
trochu zvláštně (zkoušeno s `gcc-gnat-10.2.1-9` na Fedoře 33):

``` {.kod}
$ gnatmake -q example1.adb
example.adb:16:20: expected type "Meters" defined at line 2
example.adb:16:20: found type "Meters" defined at line 2
gnatmake: "example.adb" compilation error
```

Obecné modelování fyzikálních rozměrů tímto způsobem
nemusí být zcela přímočaré ani praktické. I když jednodušší případy, kdy se
obejdeme bez rozměrové analýzy, můžou
fungovat pěkně, jak je vidět na [příkladu práce s metry a
mílemi](https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html#strong-typing)
z [úvodního kurzu jazyka Ada](https://learn.adacore.com/courses/intro-to-ada/index.html).

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
knihovna programátorovi dává, se můžou v závislosti na možnostech jazyka dost
lišit.

Překladač [GNAT dnes implementuje systém pro kontrolu rozměrů
veličin](https://gcc.gnu.org/onlinedocs/gnat_ugn/Performing-Dimensionality-Analysis-in-GNAT.html),
který staví na tzv. [*Aspects* ze standadru Ada
2012](https://docs.adacore.com/gnat_rm-docs/html/gnat_rm/gnat_rm/implementation_defined_aspects.html#implementation-defined-aspects),
a je doplněn knihovnou [`System.Dim.Mks` s definicí základních fyzikálních
jednotek dle SI](https://github.com/gcc-mirror/gcc/blob/master/gcc/ada/libgnat/s-digemk.ads).

S použitím tohoto rozšíření by náš příklad vypadal takto:

``` {.kod include="example2.adb"}
```

A jak se můžeme přesvědčit, opravdu to funguje:

``` {.kod}
$ gnatmake -q -gnat2012 example2.adb
example2.adb:10:11: dimensions mismatch in assignment
example2.adb:10:11: left-hand side has dimension [L]
example2.adb:10:11: right-hand side has dimension [L**2]
gnatmake: "example2.adb" compilation error
```

Taková podpora jednotek je pak někde mezi implementací přímo v jazyce, a pouhou
knihovnou.

## F\#

Jeden z mála programovacích jazyků s přímou podporou pro práci s jednotkami, o
kterém jste možná už někdy slyšeli, je funkcionální jazyk
[F#](https://en.wikipedia.org/wiki/F_Sharp_(programming_language)).
Typový systém tohoto jazyka totiž umožňuje s jednotkami přímo pracovat, takže
např. typ `float<m>` reprezentuje desetinné číslo pro počet metrů, zatímco
`float` je desetinné číslo bez jednotky.
Popis jak to funguje najdete na stránce [Units of
measure](https://fsharpforfunandprofit.com/posts/units-of-measure/).

Předchozí příklad přepsaný do jazyka F# by vypadal nějak takto:

``` {.kod include="Program.fs"}
```

A když se jej pokusíme přeložit, skončíme na očekávané chybě v jednotkách:

``` {.kod}
$ dotnet run
/home/martin/projects/hello-fsharp/Program.fs(7,36): error FS0001: The unit of measure 'm' does not match the unit of measure 'm ^ 2' [/home/martin/projects/hello-fsharp/hello-fsharp.fsproj]

The build failed. Fix the build errors and run again.
```

## Python

Knihoven pro práci s jednotkami pro jazyk Python existuje hned několik (viz
[přehled Python modulů pro rozměrovou
analýzu](https://gmpreussner.com/research/dimensional-analysis-in-programming-languages#python)).
Pro ukázku jsem zvolil knihovnu [Pint](https://pint.readthedocs.io/en/stable/),
čímž ale nechci tvrdit, že jde o nejlepší nebo nejpopulárnější modul tohoto
typu (ostatní knihovny jsem nezkoušel).

Náš předchozí příklad musíme při převodu do pythonu trochu upravit. I když
python typový systém má, proměnné nelze typ explicitně přiřadit, a navíc
knihovna Pint typový systém pro reprezentaci jednotek stejně nepoužívá. Takže
místo pokusu o přiřazení metrů čtverečních do proměnné s počtem metrů, zkusíme
metry čtvereční s metry prostě sečíst:

``` {.kod include="example.py"}
```

A vidíme, že při spuštění programu dostáváme očekávanou chybu:

``` {.kod}
$ python example.py
Traceback (most recent call last):
  File "/home/martin/tmp/example.py", line 9, in <module>
    len_c = surface + len_b
  File "/usr/lib/python3.9/site-packages/pint/quantity.py", line 1018, in __add__
    return self._add_sub(other, operator.add)
  File "/usr/lib/python3.9/site-packages/pint/quantity.py", line 110, in wrapped
    return f(self, *args, **kwargs)
  File "/usr/lib/python3.9/site-packages/pint/quantity.py", line 930, in _add_sub
    raise DimensionalityError(
pint.errors.DimensionalityError: Cannot convert from 'meter ** 2' ([length] ** 2) to 'meter' ([length])
```

Další rozdíl oproti předchozím příkladům pochopitelně je, že jde o běhovou
chybu. Ale pokud vám záleží na odhalení těchto chyb už v době překladu, asi
nebudete používat python.

Ale i v jazyce jako python se imho může hodit, že vám počítač s jednotkami
pomáhá:

``` {.kod}
>>> import pint
>>> ureg = pint.UnitRegistry()
>>> current = (300 * ureg.watt) / (6 * ureg.volt)
>>> current
<Quantity(50.0, 'watt / volt')>
>>> current.dimensionality
<UnitsContainer({'[current]': 1})>
>>> current.to_base_units()
<Quantity(50.0, 'ampere')>
>>> (current * 30 * ureg.minute).to(ureg.ampere*ureg.hour)
<Quantity(25.0, 'ampere * hour')>
```

A klepne vás přes prsty, pokud po něm chcete nesmysl:

``` {.kod}
>>> (current * 30 * ureg.minute).to(ureg.watt*ureg.hour)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.9/site-packages/pint/quantity.py", line 605, in to
    magnitude = self._convert_magnitude_not_inplace(other, *contexts, **ctx_kwargs)
  File "/usr/lib/python3.9/site-packages/pint/quantity.py", line 554, in _convert_magnitude_not_inplace
    return self._REGISTRY.convert(self._magnitude, self._units, other)
  File "/usr/lib/python3.9/site-packages/pint/registry.py", line 944, in convert
    return self._convert(value, src, dst, inplace)
  File "/usr/lib/python3.9/site-packages/pint/registry.py", line 1804, in _convert
    return super()._convert(value, src, dst, inplace)
  File "/usr/lib/python3.9/site-packages/pint/registry.py", line 1410, in _convert
    return super()._convert(value, src, dst, inplace)
  File "/usr/lib/python3.9/site-packages/pint/registry.py", line 977, in _convert
    raise DimensionalityError(src, dst, src_dim, dst_dim)
pint.errors.DimensionalityError: Cannot convert from 'minute * watt / volt' ([current] * [time]) to 'hour * watt' ([length] ** 2 * [mass] / [time] ** 2)
```

(-:

## Závěr

Pokud vás tohle téma zaujalo, doporučuji se podívat na článek
[Dimensional Analysis in Programming
Languages](https://gmpreussner.com/research/dimensional-analysis-in-programming-languages),
kde najdete rozsáhlý přehled implementací rozměrové analýzy v mnoha
programovacích jazycích.

A pokud nějakou knihovnu pro práci s jednotkami ve svém kódu používáte, dejte
vědět v komentářích.
