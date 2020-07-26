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
na konec června. [Pak se ale termín opět posunul](https://www.financnisprava.cz/cs/financni-sprava/media-a-verejnost/tiskove-zpravy/tz-2020/terminy-pro-podani-a-zaplaceni-nekterych-dani-bez-sankci-10740),
a mě se tak výjimečně
podařilo podat přiznání více než měsíc před termínem. Popis jak tohle
funguje přes internet bez kvalifikovaného certifikátu nebo datové schránky by
tak teď v červenci mohl být pořád možná
někomu i užitečný, ale na druhou stranu stávající webová aplikace finanční
správy je v provozu již více než 10 let, a moje hlavní motivace k sepsání
tohoto zápisku je tak spíše poznamenat si jak to přesně funguje (což se může
příští rok navzdory připravovaným novinkám stále hodit) a zároveň sondovat
jaké zkušenosti s tím máte vy.

<!-- break -->

Malé upozornění na úvod. **Toto není návod jak řešit daně.** Nedovíte se tu
kdy a proč musíte daňové přiznání řešit, co do které položky uvést ani jaké
přílohy dodat.

## Možnosti podání daňového přiznání

Pokud máte nějaký důvod podat *daňové přiznání z příjmů fyzických osob* sami
místo toho, aby to za vás udělal váš zaměstnavatel nebo daňový poradce, máte
hned několik *oficiálních* možností.

- Dojít si pro formulář na úřad, ručně to vypsat a fyzicky na úřadě odevzdat.
  Tohle asi dělat nebudete, ale zmiňuji to tady proto, že historicky je to
  primární use case a spousta věcí z něj vychází.

- [Stáhnout si z webu finanční správy tzv. *klasický tiskopis* v
  pdf](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu),
  vytisknout a pak pokračovat stejně jako v předchozím případě.

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
  vyplněná data ani omezeně zobrazit (takže je dobrý nápad to aspoň na
  virtuální tiskárně vytisknout do pdf souboru).
  Vy přitom ale chcete mít možnost
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
zas o tolik lepší a navíc nemáte jistotu, že ten formulář je správně.

Když jsem tohle řešil před pár lety poprvé, zvolil jsem interaktivní pdf
tiskopis pro Acrobat Reader, a pak jsem toho později několikrát těžce litoval.
Možnost elektronického podání jsem ke své škodě tenkrát ignoroval, protože jsem
se mylně domníval, že k tomu je třeba mít datovou schránku.

## Přiznání přes daňový portál

Podat některé daňové přiznání přes internet jde minimálně [od roku
2003](https://www.businessinfo.cz/navody/podani-danoveho-priznani-pomoci/).
Pro *daň z příjmů fyzických osob* pak tato možnost existuje minimálně [od roku
2009](http://mareklutonsky.blog.zive.cz/2009/03/jak-jsem-podaval-danove-priznani-pres-internet/)
(viz také [heslo EPO na
wikiverzitě](https://cs.wikiversity.org/wiki/Da%C5%88/EPO)).
Současná podoba webového rozhraní je pak zdá se min. z roku
[2015](https://www.youtube.com/watch?v=zt-24yaxAEc). Rozhodně tu tedy neřeším
nějakou novinku.

Webovou aplikaci *Elektronická podání pro finanční správu* (EPO), která podání
přes internet umožňuje, najdeme na *daňovém portálu* na url:

<https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/uvod/vstup.faces>

Jelikož ale takové url není dost cool, na EPO se lze dostat i z separátního
rozcestníku na adrese:

<https://www.daneelektronicky.cz/>

Začneme tím, že v seznamu formulářů vybereme ten správný. Takový seznam se dá
najít na dvou místech jako:

- [Databáze daňových tiskopisů](https://www.financnisprava.cz/cs/danove-tiskopisy/databaze-aktualnich-danovych-tiskopisu)
  na webu finanční správy (poslední sloupec v tabulce tiskopisů s názvem EPO
  obsahuje odkaz, který otevře daný formulář ve webové aplikaci)
- [Elektronické formuláře](https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/uvod/vstup_expert.faces)
  na webu Elektronických podání (EPO)

Na první pohled je seznam na webu EPO mnohem kratší a srozumitelnější. Pokud
ale nevíte, že [pro *daň z příjmů fyzických osob* od roku 2016 existuje navíc
zjednodušená dvoustránková verze formuláře](https://www.financnisprava.cz/cs/financni-sprava/media-a-verejnost/tiskove-zpravy/2016/novy-tiskopis-pro-podani-priznani-7551?),
nebude vám hned jasné, proč ten seznam z webu EPO obsahuje formuláře dva a
který z nich máte použít. Navíc s velkou pravděpodobností stejně nakonec
zvolíte původní plnou verzi, protože pokud už toto řešíte sami,
[šance že můžete zkrácený formulář použít je malá](https://finexpert.e15.cz/financni-sprava-zjednodusuje-formular-dane-z-prijmu-ma-to-ale-hacek).
Pokud byste ale např. zpracovávali větší množství daňových přiznání na
papírových formulářích, mohl by vám ten zkrácený formulář teoreticky ušetřit
určité množství papíru (-:

Tento přístup má imho dva drobné problémy. Bez ohledu na to že existuje několik
různě obsáhlých papírových verzí formuláře bych čekal, že elektronický formulář
bude z pohledu uživatele existovat pouze jeden. Hádám že finanční správa asi
nechce kvůli tomu EPO nijak upravovat (třeba přidat funkcionalitu, která by
výběr toho formuláře nějak inteligentně řešila), bylo by ale dobré aspoň v
seznamu na webu EPO zalinkovat [to oznámení o zkráceném formuláři](https://www.financnisprava.cz/cs/financni-sprava/media-a-verejnost/tiskove-zpravy/2016/novy-tiskopis-pro-podani-priznani-7551?),
aby bylo hned jasnější o co se jedná.

Otevřeme tedy aplikaci EPO s plným formulářem, tj. [daň z příjmů fyzických
osob - od roku 2013
včetně](https://adisepo.mfcr.cz/adistc/adis/idpr_epo/epo2/form/form_uvod.faces?pisemnost=DPFDP5).

<center>![](screenshot_DPFDP5_01.png){ width=50% }</center>

Vpravo nahoře vidíme, že nejsme přihlášení. Hned o kus dál je pak odkaz na
login přes [NIA](https://cs.wikipedia.org/wiki/N%C3%A1rodn%C3%AD_bod_pro_identifikaci_a_autentizaci).
Pokud tedy např. máte aktivovanou [novou občanku s čipem](https://www.lupa.cz/clanky/jak-se-prihlasuje-pomoci-nove-elektronicke-obcanky/)
([další možnosti přibyly teprve nedávno](https://www.lupa.cz/clanky/eobcanky-ztratily-monopol-na-prihlasovani-ke-sluzbam-egovernmentu-jak-funguje-karta-starcos/)),
můžete se přes ni přihlásit. Více se tomu věnuje server lupa.cz v
článku [Přes Portál občana se můžete přihlásit i k Daňovému
portálu](https://www.lupa.cz/clanky/pres-portal-obcana-se-muzete-prihlasit-i-k-danovemu-portalu-kolik-prace-to-realne-usetri/).
Sám jsem možnosti přihlášení nevyužil (občanku s čipem nemám a další metody
autentizace jsem zatím nestudoval) a dál se jí věnovat nebudu. Pointa tohoto
zápisku je totiž i v tom, že pro to, abyste mohli aplikaci EPO použít k podání
daňového přiznání, se přihlašovat nemusíte.

## Vyplňujeme a podáváme formulář

Teď můžeme buď využít průvodce, který se nás nejprve zeptá na typ příjmů a
podle toho omezí políčka formuláře, které po nás bude chtít vyplnit, nebo přes
odkaz "Další stránka" přejít na vyplňování první části, která více méně
odpovídá začátku papírového formuláře. Ve výsledku se ale oba
přístupy zas tolik neliší. Postupně vyplníme všechny položky, které bychom
museli vyplnit na papírovém formuláři, ale EPO alespoň umí některé položky
dopočítat (ty jsou podbarvené žlutě) a upozorní nás na konflikty nebo na
chybějící přílohy. Stránku formuláře nebo celý formulář je možné také nechat
zkontrolovat.

<center>![](screenshot_DPFDP5_02.png){ width=50% }</center>

Během vyplňování je třeba dávat pozor na to, že server data drží jen asi půl
hodinu od poslední změny ve formuláři. Pokud tedy na hodinu odejdeme od
rozpracovaného formuláře, o vyplněná data můžeme přijít.
Na druhou stranu nám ale aplikace umožňuje všechna data, co jsme dosud
vyplnili, stáhnout ve formě XML souboru (po kliknutí
na odkaz *Uložení prac. souboru*), který můžeme později načíst a pokračovat v
zadávání dat. Schéma XML opět přesně odpovídá
papírovému formuláři, a tak obsahuje jak hodnoty, co jsme ručně zadali, tak ty
dopočítané (jako např. základ daně). Případné binární přílohy jsou v XML
souboru uložené jako base64 kódovaný CDATA text.

Možnost stáhnout data je imho velká výhoda. Porovnáním průběžně uložených XML
dat lze zjistit jaký vliv má vyplnění konkrétní přílohy nebo položky. Případně
pokud máme XML export z předchozího roku, lze se také přímo podívat, v čem
je letošní přiznání jiné, resp. zda se liší ve věcech co bychom čekali.
Takové porovnání lze v případě potřeby automatizovat a podobně funkce importu
XML dat otevírá možnost, že data pro formulář vygenerujeme, třeba jen
částečně, nějakým skriptem.

Pro demonstrační účely v rámci tohoto zápisku jsem formulář částečně vyplnil, a
abych si nemusel vymýšlet úplné blbosti, použil jsem veřejně dostupné osobní
údaje paní Specimen ze [vzoru občanského průkazu z roku
2012](https://commons.wikimedia.org/wiki/File:ID-card_CZ_2012.jpg) (-:

Pracovní export XML dat z formuláře, kde byl vyplněn pouze 1. oddíl *Údaje o
poplatníkovi*, vypadá následovně:


~~~ {.kod .xml include="DPFDP5-8160080610-20200717-001524-pracovni.xml"}
~~~

Co který atribut znamená lze dohledat v
[dokumentaci tiskopisu DPFDP5](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/epo2_info/popis_struktury_detail.faces?zkratka=DPFDP5)
(že jde právě o tento lze poznat mimo jiné z prefixu XML souboru), kde se dá
také stáhnout jeho XML schéma.

Zatím mi ale vždy stačilo [XML soubor skriptem
přeformátovat](https://github.com/marbu/scriptpile/blob/master/xml-pretty-data.py)
tak, abych mohl použít běžné textové nástroje pro zobrazení rozdílů (např.
vimdiff nebo meld):

~~~ {.kod}
$ xml-pretty-data DPFDP5-8160080610-20200717-001524-pracovni.xml
<?xml version="1.0" encoding="UTF-8"?>
<Pisemnost
  nazevSW="EPO MF ČR"
  verzeSW="41.10.5"
  >
  <DPFDP5
    verzePis="06.02"
    >
    <VetaD
      audit="N"
      c_ufo_cil="456"
      dap_typ="B"
      dokument="DP5"
      k_uladis="DPF"
      pln_moc="N"
      prop_zahr="N"
      rok="2019"
      zdobd_do="31.12.2019"
      zdobd_od="01.01.2019"
      >
    </VetaD>
    <VetaP
      c_obce="567892"
      c_orient="43"
      c_pop="257"
      c_pracufo="2501"
      email="specimen.vzor@post.cz"
      jmeno="Vzor"
      k_stat="CZ"
      naz_obce="ÚSTÍ NAD LABEM-MĚSTO"
      prijmeni="Specimen"
      psc="40001"
      rod_c="8160080610"
      st_prislus="ČR"
      stat="ČESKÁ REPUBLIKA"
      titul="Mgr."
      ulice="Pražská"
      >
    </VetaP>
    <VetaB
      priloh_celk="0"
      >
    </VetaB>
  </DPFDP5>
</Pisemnost>
~~~

Když jsme s vyplňováním formuláře hotovi, můžeme přiznání v aplikaci EPO podat
jedním z těchto 3 způsobů:

- přes datovou schránku
- s použitím [kvalifikovaného
  certifikátu](https://cs.wikipedia.org/wiki/Digit%C3%A1ln%C3%AD_certifik%C3%A1t#Kvalifikovan%C3%BD_certifik%C3%A1t)
- bez elektronického podpisu

Tady ještě doplním, že aplikace EPO umožňuje stáhnout pdf verzi vyplněného
formuláře i před samotným podáním. Můžeme tedy místo výše popsaných možností
podání formulář prostě vytisknout a donést na úřad. V takovém případě bychom
vlastně použili EPO pouze jako nástroj k vyplnění a základní kontrole
formuláře.

Jelikož datovou schránku ani kvalifikovaný certifikát nemám, zbývá mi jen
poslední možnost. Ta spočívá v tom, že vyplněná data se odešlou na server,
který je podepíše, uloží a vygeneruje mi o tom potvrzení.

<center>![](screenshot_DPFDP5_03.png){ width=50% }</center>

Pak je třeba do 5 dnů vytisknout, podepsat a na úřad osobně doručit
jednostránkové potvrzení o podaní (na screenshotu výše jde o *e-tiskopis
podání*). Fyzické ověření totožnosti tu tak úřadu nahrazuje elektronický
podpis. Teprve od okamžiku přijetí tohoto potvrzení úřadem je přiznání
oficiálně podáno. Pokud bychom to do těch 5 dnů nestihli, je to jako bychom
přiznání vůbec nepodali.

E-tiskopis kvůli identifikaci podávajícího obsahuje naše rodné číslo, jméno a
adresu, dále pak 3 hodnoty ze samotného přiznání (daňový bonus, daň a ztráta) a
identifikaci elektronického podání (název souboru s podáním, číslo podání a
tzv. kontrolní číslo). Není mi sice jasné jak a z čeho přesně se to kontrolní
číslo spočítá, ale je možné ho nalézt i ve finálním XML exportu dat formuláře.

Pokud vám aplikace spočítá nedoplatek, tak jistě oceníte, že vám vygeneruje i
kompletní platební informace: částku k platbě, číslo účtu a variabilní symbol
A to včetně QR kódu pro platbu přes mobilní aplikace.
Bez této funkce by bylo dohledávání platebních informací vyloženě za trest:
každý kraj má totiž vlastní sadu několika různých účtů, každý pro jiný
typ daně. Naopak v případě přeplatku se žádné překvapení nekoná, během
vyplňování formuláře by bylo třeba vyplnit číslo účtu kam vám mají peníze
vrátit v oddílu "Vrácení přeplatku".

Mimo pdf s e-tiskopisem je dobré stáhnout a uschovat minimálně potvrzení v
souboru s příponou `.p7s`. Ten obsahuje jak metadata o podání (včetně čísla
podání a přístupového hesla) a kompletní XML data vyplněná do formuláře, tak
podpis všech těchto dat s certifikátem. Na tento soubor je proto vhodné dávat
dobrý pozor.

Dále je ještě možné stáhnout XML data nebo pdf verzi formuláře, ale pokud máte
ten `.p7s` soubor, vše ostatní lze s jeho pomocí později získat.

Při zadání čísla a hesla podání na stránce [Stav zpracování elektronických
podání](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/sepo/sepo.faces) vám
aplikace EPO zobrazí jeho strohý stav zpracování (buď "Podání bylo přijato
cílovým úřadem" nebo "Podání bylo přijato na společném technickém zařízení
správců daně."), zatímco pokud necháme [načíst celý `.p7s`
soubor](https://epodpora.mfcr.cz/cs/seznam-okruhu/navody-pro-praci-v-aplikaci-epo/jak-nacist-soubor-s-potvrzenim--potvrzen-4483),
dostaneme se znovu ke všem informacím o podání, včetně možnosti zaslat úpravy
(to jsem ale nezkoušel).

## Pitváme (a ověřujeme) potvrzení podání

Jelikož potvrzení podání v `.p7s` souboru se důrazně doporučuje stáhnout a
uschovat, podíváme se na něj podrobněji. Jde o [PKCS
#7](https://en.wikipedia.org/wiki/PKCS) `signedData` zprávu kódovanou
v binárním [DER formátu](https://wiki.openssl.org/index.php/DER). Tento soubor
tedy obsahuje jak samotná [data o podání v XML
formátu](https://adisepo.mfcr.cz/adis/jepo/info/epo_podani.htm) (včetně
vloženého XML našeho vyplněného
[DPFDP5](https://adisepo.mfcr.cz/adistc/adis/idpr_pub/epo2_info/popis_struktury_detail.faces?zkratka=DPFDP5)
formuláře) tak podpis těchto dat s [X.509](https://en.wikipedia.org/wiki/X.509)
certifikátem.

Nejprve se zaměříme na samotný certifikát. Pro demonstrační účely si jej
vyexportujeme do souboru `potvrzeni.crt` v textového PEM formátu:

~~~ {.kod}
$ openssl pkcs7 -inform DER -in DPFDP5-8160080610-20200719-133006-17102653-potvrzeni.p7s -print_certs -outform PEM -out potvrzeni.crt
~~~

Vidíme že certifikát vydala I. CA:

~~~ {.kod}
$ openssl x509 -in potvrzeni.crt -issuer -noout
issuer=C = CZ, CN = I.CA Qualified 2 CA/RSA 02/2016, O = "Prvn\C3\AD certifika\C4\8Dn\C3\AD autorita, a.s.", serialNumber = NTRCZ-26439395
~~~

V [seznamu kvalifikovaných certifikátů I.
CA](https://www.ica.cz/HCA-kvalifikovany) tedy najdeme příslušný záznam "I.CA
Qualified 2 CA/RSA 02/2016" a stáhneme jej v PEM formátu:

~~~ {.kod}
$ wget https://www.ica.cz/userfiles/files/certifikaty/HCA_kvalifikovany/2qca16_rsa.pem
$ openssl x509 -in 2qca16_rsa.pem -noout -subject
subject=C = CZ, CN = I.CA Qualified 2 CA/RSA 02/2016, O = "Prvn\C3\AD certifika\C4\8Dn\C3\AD autorita, a.s.", serialNumber = NTRCZ-26439395
~~~

Jak ale vidíme, pro ověření potřebujeme ještě
minimálně [příslušný kořenový certifikát I. CA](https://www.ica.cz/HCA-root):

~~~ {.kod}
$ openssl x509 -in 2qca16_rsa.pem -noout -issuer
issuer=C = CZ, O = "Prvn\C3\AD certifika\C4\8Dn\C3\AD autorita, a.s.", CN = I.CA Root CA/RSA, serialNumber = NTRCZ-26439395
$ wget https://www.ica.cz/userfiles/files/certifikaty/HCA_root/rca15_rsa.pem
~~~

Důkladnější ověření pravosti kořenového certifikátu (včetně zohlednění
revocation seznamů) už ale nechám na vás (-:

~~~ {.kod}
$ openssl x509 -in rca15_rsa.pem -noout -fingerprint -sha256
SHA256 Fingerprint=D3:D6:07:A9:FF:24:A1:95:23:B6:DA:9D:2C:64:94:46:F8:78:8C:B9:6D:9F:D1:30:97:2E:12:0C:13:67:77:30
~~~

Vidíme, že řetězec certifikátů podle očekávání sedí k sobě, tj. že kořenový
`rca15_rsa.pem` opravdu podepsal mezilehlý `2qca16_rsa.pem` a ten pak
certifikát `potvrzeni.crt` z podání:

~~~ {.kod}
$ openssl verify -CAfile rca15_rsa.pem -untrusted 2qca16_rsa.pem potvrzeni.crt
potvrzeni.crt: OK
~~~

Pojďme ale udělat něco užitečnějšího: data z PKCS#7 zprávy vytáhneme a
zvalidujeme. Oba kořenové certifikáty ale kvůli tomu nejprve uložíme do jednoho
PEM souboru:

~~~ {.kod}
$ cat rca15_rsa.pem 2qca16_rsa.pem > certchain.pem
$ openssl cms -verify -inform DER -in DPFDP5-8160080610-20200719-133006-17102653-potvrzeni.p7s -CAfile certchain.pem -out potvrzeni.pkcs7-data.xml
Verification successful
~~~

Když se teď podíváme na data z potvrzení, co jsme takto dostali, vidíme, že
formulář samotný [není v potvrzení vložený
přímo](https://adisepo.mfcr.cz/adis/jepo/info/epo_podani.htm):

~~~ {.kod}
$ xml-pretty-data potvrzeni.pkcs7-data.xml
<?xml version="1.0" encoding="UTF-8"?>
<Pisemnost>
  <Data>
  </Data>
  <Kontrola>
    <Soubor
      Delka="783"
      KC="8e3ddda5a61e40aac7f268973aa5d9ac"
      Nazev="DPFDP5-8160080610-20200719-133006"
      c_ufo="456"
      >
    </Soubor>
  </Kontrola>
  <Podani
    Cislo="17102653"
    Datum="2020-07-19T13:33:54"
    Email="specimen.vzor@post.cz"
    Heslo="XXXXXXXX"
    KC="a52e16cc1e2648d2c393e2722e71c2d3"
    ZAREP="false"
    >
  </Podani>
</Pisemnost>
~~~

Resp. nevidíme, protože můj skript `xml-pretty-data` nevypisuje textový obsah
XML elementů. Pro účely porovnávání XML dokumentů lezoucích z EPO je to ale
výhoda, protože taková data obsahují pouze jiné velké vložené soubory a přímo
by ani porovnat nešla.
Na XML našeho DPFDP5 formuláře v hexadecimálním formátu v elementu `Data` by
stejně nebyl pěkný pohled.

~~~ {.kod}
$ xmlstarlet sel -t -v "/Pisemnost/Data" potvrzeni.pkcs7-data.xml > potvrzeni.pkcs7-data.DPFDP5.hex
$ xxd -r -p potvrzeni.pkcs7-data.DPFDP5.hex > potvrzeni.pkcs7-data.DPFDP5.xml
~~~

Takže pokud přemýšlíte proč je ten soubor tak velký, tohle by mohl být ten
důvod.

Když pak porovnáme XML soubor, co jsme právě vytáhly z potvrzení, s tím, co
jsme si stáhli při samotném podání, obsah souborů by se neměl nijak lišit.
Porovnání s pracovní verzí formulářových dat uloženou těsně před podáním ale
ukáže, že po podání se v datech objeví element `Kontrola`, všechna ostatní data
by ale měla zůstat stejná.

~~~ {.kod}
$ diff potvrzeni.pkcs7-data.DPFDP5.xml DPFDP5-8160080610-20200719-133006.xml
$ diff potvrzeni.pkcs7-data.DPFDP5.xml DPFDP5-8160080610-20200717-001524-pracovni.xml
8c8
< <Kontrola><Uzivatel jmeno="null" prijmeni="null" /><Soubor Delka="503" KC="8e3ddda5a61e40aac7f268973aa5d9ac" Nazev="DPFDP5-8160080610-20200719-133006" c_ufo="456" /></Kontrola></Pisemnost>
---
> </Pisemnost>
~~~

Tímto si tedy můžeme být jisti, že nám daňový portál opravdu podepsal data,
které jsme zadali do formuláře.

Jak si ale můžeme mít jistotu, že na papírovém potvrzení (e-tiskopisu)
podepisujeme stejnou informaci? Když se podrobně na e-tiskopis znovu podíváme,
vidíme následující údaje, které podání identifikují:

<center>![](etiskopis.png){ width=50% }</center>

Jak jsem poznamenal už výše, nejsem si jistý z čeho a jak se kontrolní
číslo počítá, takže žádnou z těchto hodnot nelze brát jako checksum všech
formulářových dat. Ale na druhou stranu máme tyto údaje spolu se všemi
ostatními daty, co jsme vyplnily do formuláře, podepsané v PKCS#7 souboru od
finanční správy. Můžeme se tak podívat, že tyto údaje z papírového potvrzení
sedí k těm podepsaným:

~~~ {.kod}
$ xmlstarlet sel -t -v "/Pisemnost/Kontrola/Soubor/@Nazev" potvrzeni.pkcs7-data.xml; echo
DPFDP5-8160080610-20200719-133006
$ xmlstarlet sel -t -v "/Pisemnost/Kontrola/Soubor/@KC" potvrzeni.pkcs7-data.xml; echo
8e3ddda5a61e40aac7f268973aa5d9ac
$ xmlstarlet sel -t -v "/Pisemnost/Podani/@Cislo" potvrzeni.pkcs7-data.xml; echo
17102653
~~~

Jak daňová správa tak my tedy můžeme zpětně dokázat, co bylo přesně ve
formuláři podáno.

A nakonec pro jistotu dodám, že o něco uživatelsky přívětivější je pro validaci
podpisu v PKCS#7 potvrzení použít GUI nástroje typu
[Kleopatra](https://kde.org/applications/en/utilities/org.kde.kleopatra),
kde po naimportování a ověření kořenových certifikátů I. CA, lze popis
potvrzení pohodlně zvalidovat.

<center>![](screenshot_kleopatra.png){ width=50% }</center>

Validaci samotného podepsaného obsahu to ale samo o sobě pochopitelně neřeší.

## Moje dojmy

Samotná aplikace bohužel otrocky vychází z papírových formulářů, což je hádám
problém i současných zákonů a předpisů, takže musíte např. vypisovat k
jakému finančnímu úřadu patříte, i když později vyplňujete adresu trvalého
pobytu, ze které by tento detail šel odvodit. Jak [píše lupa.cz ve výše
odkazovaném článku](https://www.lupa.cz/clanky/pres-portal-obcana-se-muzete-prihlasit-i-k-danovemu-portalu-kolik-prace-to-realne-usetri/),
při přihlášení přes portál občana sice je možné některé osobní údaje nechat
předvyplnit, ale ideálně bych si představoval, že pokud už se přihlásím přes
občanku s čipem, žádné údaje které již stát o mě má nebudu vůbec muset znovu
zadávat.

Naopak dobrá ukázka využitého potenciálu strojového zpracování při
podání je vygenerování platebních pokynů včetně bankovního QR kódu.
Další pozitivní aspekt systému EPO je možnost z aplikace stáhnout veškerá data
nebo naopak data do aplikace nahrát. A to ve strukturovaném zdokumentovaném
formátu, který používá otevřené standardy. Otvírá to možnosti počítačového
zpracování dat, včetně tvorby pomocných aplikací (skutečně rozumně
navržené aplikace na ulehčení vyplňování daňového přiznání generují XML data,
která si pak můžete sami přes EPO podat).

Použití XML jako datového formátu tu imho dává smysl. I když bohužel se autorům
aplikace nepodařilo na řadě míst vyvarovat podivným hackům, jako např. při
vkládání XML do XML. Ale to by bylo na další XML flamewar ...

Škoda jen, že alespoň některé části aplikace EPO nejsou státem zveřejněny jako
open source knihovny, když už si to platíme z daní. Ještě více je ale škoda, že
příslušné zdrojáky nevlastní ani samotný stát. [Informační systém
ADIS](https://cs.wikipedia.org/wiki/Automatizovan%C3%BD_da%C5%88ov%C3%BD_informa%C4%8Dn%C3%AD_syst%C3%A9m),
kde data vyplněná přes EPO nakonec skončí, totiž zaujímá přední postavení v
[zástupu vendor lock-in systémů používané v naší státní
správě](https://archiv.ihned.cz/c7-66631500-oo1d8-c11990f2918a0b9).

Dále je těžké pochopit, proč stát lidi k používání el. podání nijak
pozitivně nemotivuje. Už jen to, že na úřadě nikdo nemusí formuláře ručně
přepisovat do počítače musí finančáku ušetřit spoustu času. Stát ale
"motivuje" jen ve speciálních případech, a pouze sankcemi. Pokud např. máte
datovou schránku a podáte přiznání jiným způsobem, [automaticky vám vzniká
neprominutelná pokuta ve výši 2000
Kč](https://www.zakonyprolidi.cz/cs/2009-280#p247a-2).
[Když ale povinnost používat datovou schránku nedodrží stát, nezbývá vám než se
v případě problémů bránit zpětně u
soudu](https://ekonom.ihned.cz/c7-66477830-oo1d8-d62cf79c4b4eff7). Problém
tohoto typu [už stihl řešit i Nejvyšší správní
soud](http://nssoud.cz/files/SOUDNI_VYKON/2016/0026_3As__1600045_20161209104735_prevedeno.pdf),
takže by dnes snad mělo být jasné, že úřad použít datovou schránku prostě musí,
a že tu nelze použít tzv. [fikci
doručení](https://cs.wikipedia.org/wiki/Pr%C3%A1vn%C3%AD_fikce) a považovat
nepřevzatý dopis za doručený. Na druhou stranu pokud ale dopis, co měl být
poslán datovou schránkou, skutečně převezmete, legitimizujete tím chybný úřední
postup a zaniká vám možnost si na něj dál stěžovat.
Ve výsledku tak takové prostředí spíše od zřízení datové schránky
odrazuje aniž by to propagaci el. podání nějak pomohlo.

## Budoucnost

Zhruba před rokem [se finanční správa pochlubila plánem, jak získat autorská
práva k systému
ADIS](https://www.financnisprava.cz/cs/financni-sprava/media-a-verejnost/tiskove-zpravy/tz-2019/zavislost-na-jedinem-dodavateli-IT-systemu-ADIS-po-30-letech-skonci-9969),
vyřešit problém s vendor lockinem a umožnit jeho modernizaci. Drobný zádrhel
ovšem je, že [na implementaci nového systému má ministerstvo financí omezený
čas](https://archiv.ihned.cz/c7-66622840-oo1d8-c94189555e5996d), a tak teď
těžko říct, jestli se to opravdu podaří vyřešit.

Kromě toho se už nějaký čas připravuje novela *daňového řádu*, která by mohla
některé problémy zmiňované výše řešit. Automatická [pokuta za nepodání daňového
přiznání pro držitele datových schránek by měla být
omezena](https://www.lupa.cz/clanky/elektronicky-bic-na-danove-poplatniky-by-mohl-zmirnit/)
a naopak při elektronickém podání by se měla lhůta pro podání prodloužit o
měsíc.

Novela také zahrnuje vznik tzv. "online finančního úřadu" [MOJE
daně](https://www.mojedane.cz/), který vznikne rozšířením a
modernizací současného systému [daňových informačních schránek](https://www.financnisprava.cz/cs/dane-elektronicky/danovy-portal/danova-informacni-schranka),
o kterém jsem se tu zatím vůbec nezmiňoval. Pokud chápu [stručný popis nového
portálu](https://www.penize.cz/dan-z-prijmu-fyzickych-osob/414851-dane-konecne-vyridite-online-schillerove-vlajkova-lod-proplula)
dobře, půjde o další možnost jak daně podat, která by měla umožnit
nejen předvyplnit data co finanční správa už ví, ale i dostat se ke stavu a
údajům z předchozích podání a plateb. Mělo být také možné se do systému
přihlásit i bez datové schránky, kvalifikovaného certifikátu nebo e-občanky.
Jak to má ale přesně fungovat jsem nedohledal.

Já teď zvažuji možnosti, jak bych příště podal přiznání zcela elektronicky.
Nová občanka s čipem vypadá na první pohled zajímavě, ale když jsem si začal
dohledávat detaily, byl jsem z toho poněkud rozpačitý. Možná nakonec skončím
u datové schránky. A co vy? Máte kvalifikovaný podpisový certifikát, datovou
schránku nebo novou občanku s čipem?

<!-- Anketa

Daňové přiznání:

- nepodávám (nejsem daňový rezident ČR, nemám práci, ...)
- podává za mně někdo jiný (zaměstnavatel, daňový poradce, ...)
- podávám sám

Pokud podávám přiznání sám, tak použiji:

- papírový formulář, který ručně vypíšu a pak donesu na úřad
- interaktivní formulář pro adobe acrobat reader, vytisknu a doručím na úřad
- nějaký neoficiální spreadsheet, který vytisknu a doručím na úřad
- EPO, ale formulář jen vytisknu a pak doručím na úřad
- EPO a podám bez el. podpisu, na úřad dodám potvrzení
- EPO a podám podepsané kvalifikovaným certifikátem
- EPO a podám přes datovou schránku
- EPO s přihlášením přes Portál občana
- jiný způsob (napíšu v diskusi)
-->
