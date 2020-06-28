---
title: Podáváme daňové přiznání přes web finanční správy
author: Martin "marbu" B.
lang: cs-CZ
papersize: a4
geometry: margin=2.5cm
links-as-notes: false
rights: cc by-sa 4.0
...

Letos jsem tak jako každý rok podával daňové přiznání na poslední chvíli, tedy
s tím rozdílem, že vzhledem k epidemii tato chvíle vycházela místo konce března
na konec června. Ani ne dva týdny zpět se ale termín opět posunul, a mě se tak
podařilo podat přiznání více než měsíc před deadlinem. Popis jak tohle
(částečně) funguje přes internet by tak tento rok v červenci mohl být pořád
někomu i užitečný, ale na druhou stranu stávající webová aplikace finanční
správy je v provozu již více než 10 let, a moje hlavní motivace k sepsání
tohoto zápisku je tak spíše sondovat jaké zkušenosti máte vy.

<!-- break -->

Malé upozornění na úvod. **Toto není návod jak řešit daně.** Nedovíte se tu
kdy a proč musíte daňové přiznání řešit, co do které položky uvést a jaké
přílohy dodat.

## Možnosti podání daňového přiznání

Pokud máte nějaký důvod podat *daňové přiznání z příjmů fyzických osob* sami
místo toho aby to za vás udělal váš zaměstnavatel nebo daňový poradce, máte
hned několik *oficiálních* možností.

- Dojít si pro formulář na úřad, ručně to vypsat a fyzicky na úřadě odevzdat.
  Tohle asi dělat nebudete, ale zmiňuji to tady proto, že historicky je to
  primární use case a spousta věcí z něj vychází.

- [Stáhnout si z webu finanční správy tzv. *klasický tiskopis* v
  pdf](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu),
  vytisknout a pak pokračovat stejně jako v předchozím případě. Opět hádám, že
  tohle asi nikdo, kdo to tu čte, dělat nebude.

- Stáhnout si ze webu tzv. *interaktivní tiskopis*, nainstalovat *[Adobe
  Acrobat](https://en.wikipedia.org/wiki/Adobe_Acrobat) Reader* (ve verzi
  alespoň 9.1) a tiskopis v Acrobatu vyplnit s tím, že položky co lze odvodit
  z jiných umí tento interaktivní pdf formulář sám dopočítat. Takto vyplněné
  je to pak nutné vytisknout a fyzicky donést na úřad.
  Když opomenu fakt, že poslední Acrobat Reader pro Linux byla verze 9.5.5
  z roku 2013 a dnes se již blbě shání, proprietární binární datový formát je
  v tomto případě dostatečný důvod proč se této možnosti vyhnout. Jednotlivé
  formuláře nemůžete rozumně porovnat nebo zpracovat skriptem, a bez Acrobatu
  se ke svým datům nedostanete, žádný *free software* pdf prohlížeč neumí takto
  vyplněná data ani omezeně zobrazit. Vy přitom ale chcete mít možnost
  jednoduše formulář přečíst a opravit pro případ, že by se vám
  kvůli nějaké nesrovnalosti ozval finančák (a to až 3 roky zpětně).
  A drobnost, že vyplňujete data na počítači abyste je vytiskly na papír
  a pak na úřadě někdo jiný opět přepsal do počítače, tu dál rozebírat raději
  ani nebudu (-:

- Podat přiznání elektronicky pomocí daňového portálu, což je imho
  nejrozumnější možnost a věnuji se jí ve zbytku tohoto zápisku.

Mimo to existují neoficiální tabulky pro excel/libreoffice calc, do kterých
můžete naládovat data, některé položky se dopočítají a po vytisknutí vypadá
podobně jako oficiální tištěný formulář, který pak donesete fyzicky na úřad.
Je to tak podobné jako v případě oficiálního interaktivního pdf s tím rozdílem,
že data jsou uložená v o něco čitelnějším formátu, ale na druhou stranu to není
zas o tolik lepší a navíc nemáte jistotu, že ten formulář je správně. Opět si
dovoluji tvrdit, že toto nechcete podstupovat.

## Podáváme přiznání přes daňový portál

Možnost podat daňové přiznání přes internet existuje minimálně [od roku
2003](https://www.businessinfo.cz/navody/podani-danoveho-priznani-pomoci/),
resp. 2009, a bez větších změn v uživatelském webovém rozhraní zhruba od
roku [2015](https://www.youtube.com/watch?v=zt-24yaxAEc). Rozhodně tu tedy
neřeším nějakou novinku (pro popis jak podání v té době fungovalo viz např.
zápisek [Jak jsem podával daňové přiznání přes
internet](http://mareklutonsky.blog.zive.cz/2009/03/jak-jsem-podaval-danove-priznani-pres-internet/)
Marka Lutonského nebo [heslo EPO na
wikiverzitě](https://cs.wikiversity.org/wiki/Da%C5%88/EPO)).

Webovou aplikaci *Elektronická podání pro finanční správu* (EPO), která podání
přes internet umožňuje, najdeme na *daňovém portálu* na url:

<https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/uvod/vstup.faces>

Jelikož ale někomu z finanční správy došlo, že takové url není dost cool, na
EPO se lze dostat i z separátního rozcestníku na adrese:

<https://www.daneelektronicky.cz/>

Začneme tím, že v seznamu formulářů vybereme ten správný. Takový seznam se dá
najít na dvou místech jako:

- [Databáze daňových tiskopisů](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu)
  na webu finanční správy (poslední sloupec v tabulce tiskopisů s názvem EPO
  obsahuje odkaz, který otevře daný formulář we webové aplikaci)
- [Elektronické formuláře](https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/uvod/vstup_expert.faces)
  na webu Elektronichých podání (EPO)

Pro daň z příjmů
fyzických osob by mělo jít o [Daň z příjmů fyzických osob - od roku 2013
včetně](https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/form/form_uvod.faces?pisemnost=DPFDP5).
Tady je vidět fail.
Už jen tohle je pain.

## Daňové kalkulačky

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

- [Elektronická podání pro finanční
  správu](https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/uvod/vstup.faces),
  tj. aplikace EPO na Daňovém portálu
- [Databáze daňových tiskopisů](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu)
  včetně linků do aplikace EPO
- [Přehled dokumentace pro služby daňového
  portálu](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/dpr_info/dokumentace.faces)
  obsahuje seznam dokumentace k aplikaci EPO
- [Struktury XML souborů EPO](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/epo2_info/popis_struktury_seznam.faces)
