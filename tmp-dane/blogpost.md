---
title: Podáváme daň z příjmů fyzických osob přes web finanční správy
author: Martin "marbu" B.
lang: cs-CZ
papersize: a4
geometry: margin=2.5cm
links-as-notes: false
rights: cc by-sa 4.0
...

<!-- TODO: perex -->

Malé upozornění na úvod. **Toto není návod jak řešit daně.** Předpokládám že
víte kdy a proč podáváte daňové přiznání sami, co do které položky uvést a jaké
přílohy dodat. Jestliže ne, místo tohoto zápisku se obraťte na weby typu
[penize.cz](https://www.penize.cz/formulare/66945-danove-priznani-k-dani-z-prijmu-fyzickych-osob)
nebo [mesec.cz](https://www.mesec.cz/danovy-portal/dan-z-prijmu/), anebo se
zeptejte daňového poradce.

## Možnosti podání daňového přiznání

Pokud máte nějaký důvod podat *daňové přiznání z příjmů fyzických osob* sami
místo toho aby to za vás udělal váš zaměstnavatel nebo daňový poradce, máte
hned několik *oficiálních* možností.

- Dojít si pro formulář na úřad, ručně to vypsat a fyzicky na úřadě odevzdat.
  Tohle asi dělat nebudete, ale zmiňuji to tady proto, že historicky je to
  primární use case a spousta věcí z něj vychází.
- [Stáhnout si z webu finanční správy tzv. *klasický tiskopis* v
  pdf](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu),
  vytisknout a pak pokračovat stejně jako v předchozím případě. Opět platí, že
  tohle asi nechcete.
- Stáhnout si ze webu tzv. *Interaktivní tiskopis*, nainstalovat *[Adobe
  Acrobat](https://en.wikipedia.org/wiki/Adobe_Acrobat) Reader* (ve verzi
  alespoň 9.1) a tiskopis v Acrobatu vyplnit s tím, že položky co lze odvodit
  z jiných umí tento interaktivní formulář sám dopočítat. Takto vyplněné
  je to pak nutné vytisknout a fyzicky odevzdat na úřad.
  Když opomenu fakt, že poslední Acrobat Reader pro Linux byla verze 9.5.5
  z roku 2013 a dnes se již blbě shání, proprietární binární datový formát je
  v tomto případě dostatečný důvod proč se této možnosti vyhnout. Jednotlivé
  formuláře nemůžete rozumně porovnat nebo zpracovat skriptem, a bez Acrobatu
  se ke svým datům nedostanete, žádný free software pdf prohlížeč neumí takto
  vyplněná data ani omezeně zobrazit. Vy přitom ale chcete mít možnost
  jednoduše formulář přečíst a opravit pro případ, že by se vám
  kvůli nějaké nesrovnalosti ozval finančák (a to až 3 roky zpětně).
- Podat přiznání elektronicky pomocí daňového portálu, což je téma rozebírané
  ve zbytku tohoto zápisku.

Mimo to existují neoficiální tabulky pro excel/libreoffice calc, do kterých
můžete naládovat data, některé položky se dopočítají a po vytisknutí vypadá
podobně jako oficiální tištěný formulář, který pak donesete fyzicky na úřad.
Je to tak podobné jako v případě oficiálního interaktivního pdf s tím rozdílem,
že data jsou uložená v o něco čitelnějším formátu, ale na druhou stranu to není
zas o tolik lepší a navíc nemáte jistotu, že ten formulář je správně. Opět si
dovoluji tvrdit, že toto nechcete podstupovat.

## Podáváme přiznání přes daňový portál

<!-- TODO -->

## Letošní termíny a sankce

<!-- TODO -->

## Budoucnost

Jak jsme možná zaznamenali, připravuje se novela *daňového řádu*, která
zahrnuje vznik online finančního úřadu a projektu [Moje
daně](https://www.mojedane.cz/).

<!-- TODO -->

- <https://www.penize.cz/dan-z-prijmu-fyzickych-osob/414851-dane-konecne-vyridite-online-schillerove-vlajkova-lod-proplula>
- <https://www.mfcr.cz/cs/verejny-sektor/dane/moje-dane/aktualni-informace>

## Reference

- [Databáze daňových tiskopisů](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu)
- [Daňový portál](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/dpr/uvod.faces)
- [Přehled dokumentace pro služby daňového
  portálu](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/dpr_info/dokumentace.faces)
- [Struktury XML souborů EPO](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/epo2_info/popis_struktury_seznam.faces)
