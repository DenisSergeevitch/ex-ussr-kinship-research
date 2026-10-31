# ex-USSR Kinship Research

![ex-USSR Kinship Researchi kaanepilt](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Tõenduspõhine genealoogiaoskus tehisintellektiagentidele (Codex, Claude Code ja muud Agent Skillsi käituskeskkonnad).** See muudab agendi hoolikaks perekonnaloo uurijaks endise NSV Liidu, Nõukogude Liidu ja Vene impeeriumi alal. Agent loeb kiriku- ja perekonnaseisuregistreid, sõjaväe-, küüditamis- ja repressioonitoimikuid ning indekseerimata arhiiviskaneeringuid. Iga leiu päritolu jääb jälgitavaks, dokumendid on tõlgendusest lahus ning tõendatud ja tõendamata asjaolud selgelt eristatud.

Hõlmatud on kõik 15 endist liiduvabariiki: Venemaa, Ukraina, Valgevene, Moldova, Eesti, Läti, Leedu, Gruusia, Armeenia, Aserbaidžaan, Kasahstan, Kõrgõzstan, Tadžikistan, Türkmenistan ja Usbekistan. Arhiivid valitakse sündmuse ajal kehtinud jurisdiktsiooni ja dokumentide praeguse valdaja järgi; piirkondlik näide ei asenda kohalikku uurimist.

Oskuse juhised on vene keeles, kuid **agent suhtleb teiega teie keeles**: inglise, ukraina, vene, poola, saksa keeles jne. Allikatsitaadid esitatakse algses kirjapildis koos tõlkega ning otsingupäringud koostatakse dokumentide keeltes.

---

## Mida see teeb

- **Juhtumi lähteandmed ja ulatus.** Üks uurimisküsimus, teadaolevad asjaolud, võimalikud elusolevad inimesed ning välistatud tegevused.
- **Korratavad registrid.** Isikud, artefaktid, väited, seosed ja täielik otsingulogi (CSV) ning lõpparuande mall.
- **Ajaloolise jurisdiktsiooni mudel.** Iga sündmus seotakse riigi, provintsi, maakonna, koguduse või perekonnaseisuasutusega *sündmuse kuupäeval*, mitte tänapäevase kaardiga.
- **Nimevariantide maatriksid.** Reformieelne vene kirjapilt, ukraina, poola, rumeenia, saksa ja jidiši nimekujud, isanimed, neiupõlvenimed ning transliteratsioonid.
- **Allikastrateegia.** Esmalt originaalid, siis ametlikud kataloogid, indeksid ja avaldatud dokumendikogud; sugupuud ja foorumid on alles seejärel otsinguvihjed.
- **Tõendamisprotokoll.** Väidetele antakse põhjendatavad staatused, mitte protsendid: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Sama kirje koopiatel ja peeglitel on ühine `independence_group`, seega ei loeta neid sõltumatuteks tõenditeks.
- **Isikute eristamine.** Nimekaimud säilitavad eraldi `person_id` väärtused, kuni leitakse eristav tõend: majanumber, vanemad, ristivanemad, täpne sünniaeg või väeosa.
- **Auditi skript.** Kontrollib viidete terviklust ja juhib enne järelduste kirjutamist tähelepanu nõrgale kinnitusele. Sõltumatusrühm läheb arvesse ainult siis, kui viidatud artefakt kuulub sellesse; kinnitust ei saa pelgalt deklareerida. Kontrollib ka lõpparuannet: kõik viidatud ID-d peavad registrites olemas olema ning staatused nendega ühtima. Kokkuvõte näitab veel kinnitamata või loetamatuks märgitud materjali.
- **Päringud asutustele.** Koostab ja loa olemasolul saadab sihitud päringuid arhiividele, raamatukogudele, ülikoolidele ja muuseumidele olemasoleva e-posti või ametlike veebivahenditega. Vajadusel pakub toetatud e-postiühendust või saatmisvalmis kirja. Salvestab tulemused, väldib kordussaatmist ja käsitleb vastuseid tõenditena. Vaadake [kirjavahetuse juhendit](references/correspondence.md).
- **Riigiteenused.** Valib ametliku perekonnaseisu- või arhiivipäringu tee, kontrollides taotlusõigust ja vastuse kättetoimetamist ([riigiportaalid](references/government-portals.md)).
- **Lõpparuanne.** Iga sugulusseos avatakse lülihaaval koos vastuolude, tulemusteta otsingute ja konkreetsete järgmiste sammudega.
- **Indekseeritud kirjete sihitud uurimine.** Leiab sobivad FamilySearchi köited koha või DGS-i järgi olemasolevas õiguspärases brauseriseansis, vaatab konkreetseid kirjeid ja säilitab ainult allika lubatud tõendifragmendid. Kohalikud abivahendid otsivad salvestatud fragmentidest sugulasi, tunnistajaid ja nimevariante, säilitades konteksti ning failide kontrollsummad. [Töövoog ja hõlmatuse piirid](references/familysearch-indexes.md).
- **Ühendatud FamilySearch MCP.** Kasutab ühendatud serverit struktureeritud otsinguteks, profiilide, sugulaste ja allikate lugemiseks ning lubatud sugupuu muudatusteks selge ulatuse ja tulemuse ülelugemisega. Eristab indeksotsingut indekseerimata skaneeringute lugemisest ning kontrollib ühenduse tegelikke brauseri-, privaatsus- ja kirjutamisvõimalusi. [Töövoog ja juurdepääsupiirid](references/familysearch-mcp.md).
- **Esimese maailmasõja allikaotsing.** Otsib GWAR-i aruandeid, haigla-, autasu- ja sõjavangikirjeid isiku või paiga järgi, võrdleb salvestatud kaartide asulanimekujusid moonutatud kohanime lugemiseks ning leiab algallika pildi. [Töövoog](references/ww1-search.md). Mõlemad abivahendid täiendavad olemasolevat artefaktiregistrit ja otsingulogi; need ei tuvasta isikuid ega sugulust automaatselt.

Väljalasete ajalugu: [muudatuste logi](references/changelog.md).

<a id="install"></a>

## Paigaldamine

Kui Node.js on paigaldatud, võite kasutada valikulist [Skills CLI-d](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI võimaldab valida agendi ja paigaldab vaikimisi praegusesse projekti; lisage `-g`, et paigaldada oskus isiklikuks kasutamiseks kõigis projektides. Kehtivad Node.js-i nõuded leiate selle dokumentatsioonist.

Teise võimalusena kloonige hoidla otse oma agendi oskuste kausta:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (isiklikud oskused)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Ühe projekti puhul pange kaust hoidla sisse `.claude/skills/` alla. Skriptid vajavad ainult Python 3 ja standardteeki; `build_pdf.py` vajab lisaks Chromiumil põhinevat brauserit.

## Kasutamine

Kirjeldage perekonnaloo küsimust. Agent töötab olemasoleva teabega ja jätkab ka siis, kui küsimused või juurdepääsutaotlused ootavad vastust. Näiteks:

- *„Minu vanavanaisa saadeti 1930. aastatel Kasahstani asumisele. Aita leida tema vanemad kirikuraamatutest.”*
- *„Siin on abielutunnistuse ja sõdurikaardi skaneeringud. Kontrolli, kas need käivad sama inimese kohta, ning koosta tõendusahel.”*
- *„Leia 1890. aastate Podoolia küla kogudus ja õige FamilySearchi film ning loe perekonnanime X sünnikirjed.”*

Hoidke juhtumi privaatsed andmed väljaspool oskuse Giti töökoopiat. Oskuse kaustas:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 igale salvestatud artefaktile
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # registrite kontroll enne lõpparuannet
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` keeldub juhtumi loomisest oskuse kausta, ka valikuga `--force`. Lisakaitsena eirab Git varasemate juhtumikaustade levinud nimesid; kontrollige enne panustamist lisatud faile, eriti olemasoleva juhtumi teisaldamisel.

`build_pdf.py` vajab paigaldatud Chrome’i, Chromiumi või Edge’i (või `CHROME_PATH` väärtust). Valikuga `--png-dir` renderdab see lehed läbivaatamiseks ka PNG-vormingusse, kui `pypdfium2` on saadaval.

Kasutage staatilist HTML-i kohalike või manustatud piltidega. Aktiivne HTML ja võrgust laaditavad pildiallikad lükatakse tagasi; allikalingid jäävad klõpsatavaks. Ebaõnnestunud renderdus säilitab olemasoleva PDF-i.

## Sugupuu GEDCOM-vormingus

[GEDCOM](https://gedcom.io/specs/) on genealoogiliste andmete vahetamise standardvorming (`.ged`). Sugupuu koostamise või eksportimise soovi korral loob agent kohaliku faili koos allikate ja tõendatuse märkustega. Ühilduvuse huvides kasutab ta vaikimisi vormingut GEDCOM 5.5.1 ja UTF-8 kodeeringut; kui kasutaja nimetab muu toetatud versiooni, näiteks GEDCOM 7, kasutab ta seda.

Olemasolev sugupuu on lähtematerjal ja annab uurimisvihjeid, mitte ei tõesta sugulust. Originaal säilib; kasutaja faili ei kirjutata üle. Kinnitamata andmed, vastuolud ja ebakindlus jäävad juhtumisse. Tõendiregistrid ja otsingulogi jäävad järelduste aluseks. Impordi ja ekspordi reeglid on failis [references/gedcom.md](references/gedcom.md).

Sugupuuprogrammi valib kasutaja. Rakenduste paigaldamine, MCP seadistamine ja automaatne sünkroonimine välise sugupuuga jäävad selle oskuse ulatusest välja.

## Hoidla struktuur

```
SKILL.md                         põhijuhised (töövoog, kohustuslikud reeglid, keelepoliitika)
references/
  source-strategy.md             allikate hierarhia, päringumustrid, kataloogid, arhiivipäringud
  correspondence.md              saajad, e-postiühendus, lubatud saatmine ja vastused
  government-portals.md          perekonnaseisuteenused ja vastuse edastamine
  evidence-protocol.md           artefaktide hindamine, staatused, isikutuvastus, vastuolud
  ex-ussr-locale-guide.md        jurisdiktsioonid, nimevariandid, kalendrid, dokumendiliigid periooditi
  browser-and-captcha.md         sirvimine, sisselogimine, üks CAPTCHA-katse ja üleandmine, päringupiirangud
  privacy-and-safety.md          elusolevad inimesed, alaealised, DNA, tundlikud leiud
  seed-sources.md                valitud lähteallikad koos usaldusväärsuse klassidega
  field-lessons.md               praktilised õppetunnid tegelikust juhtumist
  changelog.md                   väljalasete ajalugu
  photo-search.md                fotode leidmine, tuvastamine, dateerimine ja säilitamine
  habsburg-galicia-bukovina.md   Galiitsia ja Bukoviina Habsburgide ajal ning hiljem
  chechnya-deportation.md        tšetšeeni perekonnad: 1944. aasta küüditamine, eriasulad, nimed ja ümbernimetatud külad
  germany-forced-labour.md       sunnitöölised Saksamaal 1941–1945: Arolsen Archives ja Saksa perekonnaseisuregistrid

  bessarabia-moldova.md          Bessaraabia, Moldova, Moldaavia ANSV ja Dnestri piiriala
  familysearch-indexes.md       sihitud brauseriuuringud, lubatud kohalikud koopiad ja hõlmatus
  familysearch-mcp.md           ühendatud vahendid, struktureeritud lugemine, piiritletud kirjutamine ja kontroll
  ww1-search.md                 GWAR-i isiku- ja paigaotsing ning allikapiltide asukoht
  gedcom.md                     sugupuude vahetamine GEDCOM-vormingus, allikad ja tõendatus
assets/                          juhtumi lähteandmed, CSV-registrid, lõpparuande mall,
                                 fotode README-mall, uurimisseisundi mall, loetava PDF-i mall (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py ja ühised kohaliku analüüsi moodulid
evals/discovery-and-logic.yaml   käivitumise ja arutluse testjuhtumid
tests/                           ühiktestid (python3 -m unittest discover -s tests)
```

## Vastutustundlik kasutamine

- **Perekonnalugu, mitte jälitamine.** Oskus keeldub elusolevate inimeste praeguste aadresside, telefoninumbrite või kontode otsimisest ja piirab nende andmeid aruannetes.
- **Juurdepääsu kontroll.** Agent võib proovida tegelikku CAPTCHA-t ühe korra sisemise brauseri tavaliste juhtelementidega, kui see on toetatud ja lubatud. Kui vaja on kasutaja tegevust, avab ta võimalusel vastava vahelehe ning annab URL-i ja vajaliku tegevuse kirjelduse; sisse logib kasutaja ise. Väliseid lahendamisteenuseid, kaitsete, tasumüüride, geopiirangute või päringupiirangute vältimist ega lekkinud andmebaase ei kasutata. Vaadake [brauserijuhendit](references/browser-and-captcha.md).
- **Teie dokumente või DNA-andmeid ei laadita** kolmandate isikute teenustesse ilma teie sõnaselge nõusolekuta.
- **Tundlikud leiud** (küüditamine, repressioonid, lapsendamine, DNA-üllatused) esitatakse neutraalselt ja ainult uurimisküsimusele vajalikus ulatuses.
- **Lubatud kirjavahetus.** Oskus võib olemasolevate vahenditega saata asutustele päringuid, kui kasutaja on selleks loa andnud; juba lubatud saatmiseks uuesti nõusolekut ei küsita. Pelgalt postkasti ühendamine ei luba saatmist, manuseid ega tasulisi teenuseid. Kontrollige kehtivat ametlikku kontaktteavet ja korda ning hoidke ligipääsuandmed ja juhtumi privaatne kirjavahetus väljaspool oskuse hoidlat.

## Panustamine

Uued allikad on oodatud faili `references/seed-sources.md`. Salvestage teadaolevad ja kontrollitud valdaja, jurisdiktsioon, kogu, päritolu, ID-d, juurdepääs, piirangud ja kontrollimise kuupäev; märkige lüngad, ärge arvake. Hoidke isikuandmed näidetest väljas.

Allikaotsingu abivahendid kasutavad Pythoni standardteeki ja juhtumi olemasolevaid registreid. Käivitage `python3 -m unittest discover -s tests`, et kontrollida sünteetiliste andmetega kohalikku parsimist, GWAR-i jätkupunkte, ligipääsutõrkeid, ebaselget hõlmatust ja tõendite registreerimist. FamilySearchi leidmine ja sihitud vaatamine kasutavad olemasolevat õiguspärast brauseriseanssi; Pythoni abivahendid analüüsivad salvestatud fragmente. Hoidke privaatsed uurimisfailid väljaspool seda töökoopiat.

## Litsents

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Haldab Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
