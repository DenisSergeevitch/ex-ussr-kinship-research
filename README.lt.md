# ex-USSR Kinship Research

![ex-USSR Kinship Research viršelis](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Įrodymais grindžiamas genealogijos įgūdis DI agentams (Codex, Claude Code ir kitoms Agent Skills vykdymo aplinkoms).** Jis paverčia agentą kruopščiu šeimos istorijos tyrėju buvusios SSRS, Sovietų Sąjungos ir Rusijos imperijos teritorijoje. Agentas skaito bažnytines ir civilinės būklės knygas, karines, tremties ir represijų bylas bei neindeksuotus archyvų skenavimus. Kiekvieno radinio kilmę galima atsekti; dokumentai atskiriami nuo interpretacijos ir aiškiai nurodoma, kas įrodyta, o kas ne.

Aprėpiamos visos 15 buvusių sovietinių respublikų: Rusija, Ukraina, Baltarusija, Moldova, Estija, Latvija, Lietuva, Sakartvelas, Armėnija, Azerbaidžanas, Kazachstanas, Kirgizija, Tadžikistanas, Turkmėnistanas ir Uzbekistanas. Archyvai parenkami pagal istorinę įvykio jurisdikciją ir dabartinį dokumentų saugotoją; regioninis pavyzdys neatstoja vietinio tyrimo.

Įgūdžio instrukcijos parašytos rusiškai, tačiau **agentas su jumis kalba jūsų kalba**: angliškai, ukrainietiškai, rusiškai, lenkiškai, vokiškai ir kitomis. Šaltiniai cituojami originalia rašyba su vertimu, o paieškos užklausos sudaromos dokumentų kalbomis.

---

## Ką jis daro

- **Bylos pradiniai duomenys ir apimtis.** Vienas tyrimo klausimas, žinomi faktai, kas gali būti gyvas ir kas neleistina.
- **Atkuriami registrai.** Asmenys, artefaktai, teiginiai, ryšiai ir visas paieškos žurnalas (CSV), taip pat galutinės ataskaitos šablonas.
- **Istorinės jurisdikcijos modelis.** Kiekvienas įvykis priskiriamas valstybei, provincijai, apskričiai, parapijai ar civilinės metrikacijos įstaigai *įvykio dieną*, o ne pagal dabartinį žemėlapį.
- **Vardų variantų matricos.** Ikireforminės rusų, ukrainiečių, lenkų, rumunų, vokiečių ir jidiš formos, tėvavardžiai, mergautinės pavardės ir transliteracijos.
- **Šaltinių strategija.** Pirmiausia originalai, tada oficialūs katalogai, rodyklės ir publikuoti dokumentų rinkiniai, o genealoginiai medžiai ir forumai – tik vėlesnės paieškos užuominos.
- **Įrodymų protokolas.** Teiginiams suteikiamos paaiškinamos būsenos, ne procentai: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Vieno įrašo kopijos ir veidrodžiai turi bendrą `independence_group`, todėl niekada nelaikomi nepriklausomais įrodymais.
- **Asmenų atskyrimas.** Bendravardžių `person_id` lieka atskiri, kol atsiranda skiriantis įrodymas: namo numeris, tėvai, krikštatėviai, tiksli gimimo data ar karinis dalinys.
- **Audito scenarijus.** Tikrina nuorodų vientisumą ir prieš rašant išvadas pažymi silpną patvirtinimą. Nepriklausomumo grupė skaičiuojama tik tada, kai jai priklauso cituojamas artefaktas; patvirtinimo negalima sukurti vien pareiškimu. Tikrina ir galutinę ataskaitą: visi cituojami ID turi būti registruose, o būsenos su jais sutapti. Suvestinė rodo, kas dar nepatvirtinta arba pažymėta kaip neįskaitoma.
- **Užklausos institucijoms.** Rengia ir, gavęs leidimą, siunčia tikslias užklausas archyvams, bibliotekoms, universitetams ir muziejams turimomis el. pašto ar oficialiomis žiniatinklio priemonėmis. Prireikus pasiūlo palaikomą pašto integraciją arba parengtą siųsti laišką. Užfiksuoja rezultatą, vengia pakartotinio siuntimo ir atsakymus vertina kaip įrodymus. Žr. [susirašinėjimo gaires](references/correspondence.md).
- **Valstybės paslaugos.** Parenka oficialų civilinės metrikacijos ar archyvo užklausos kelią, tikrindamas teisę pateikti prašymą ir rezultato gavimo būdą ([valstybės portalai](references/government-portals.md)).
- **Galutinė ataskaita.** Kiekvienas giminystės ryšys išdėstomas grandis po grandies su prieštaravimais, nesėkmingomis paieškomis ir konkrečiais tolesniais žingsniais.
- **Tikslinis indeksuotų įrašų tyrimas.** Randa tinkamas FamilySearch knygas pagal vietą ar DGS esamoje teisėtoje naršyklės sesijoje, peržiūri konkrečius įrašus ir išsaugo tik šaltinio leidžiamus įrodymų fragmentus. Vietinės pagalbinės priemonės išsaugotuose fragmentuose ieško giminaičių, liudytojų ir vardų variantų, išlaikydamos kontekstą bei failų kontrolines sumas. [Darbo eiga ir aprėpties ribos](references/familysearch-indexes.md).
- **Prijungtas FamilySearch MCP.** Naudoja prijungtą serverį struktūrinei paieškai, profiliams, giminaičiams ir šaltiniams bei leistiniems medžio pakeitimams su aiškia apimtimi ir rezultato pakartotiniu nuskaitymu. Atskirkite rodyklių paiešką nuo neindeksuotų skenavimų skaitymo ir tikrinkite tikrąsias jungties naršymo, privatumo ir rašymo galimybes. [Darbo eiga ir prieigos ribos](references/familysearch-mcp.md).
- **Pirmojo pasaulinio karo šaltinių paieška.** Ieško GWAR pranešimų, ligoninių, apdovanojimų ir karo belaisvių įrašų pagal asmenį ar vietovę, lygina gyvenviečių rašybą išsaugotose kortelėse, kad iššifruotų iškraipytą vietovardį, ir randa šaltinio vaizdą. [Darbo eiga](references/ww1-search.md). Abi priemonės papildo esamą artefaktų registrą ir paieškos žurnalą; jos automatiškai nenustato tapatybės ar giminystės.

Laidų istorija: [pakeitimų žurnalas](references/changelog.md).

<a id="install"></a>

## Diegimas

Įdiegus Node.js, galima pasirinktinai naudoti [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI leidžia pasirinkti agentą ir pagal numatytuosius nustatymus įdiegia į dabartinį projektą; pridėkite `-g`, jei norite asmeninio diegimo visiems projektams. Dabartinius Node.js reikalavimus žr. jo dokumentacijoje.

Arba klonuokite saugyklą tiesiai į agento įgūdžių aplanką:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (asmeniniai įgūdžiai)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Vienam projektui aplanką įdėkite į saugyklos `.claude/skills/`. Scenarijams pakanka Python 3 ir standartinės bibliotekos; `build_pdf.py` dar reikia Chromium pagrindu sukurtos naršyklės.

## Naudojimas

Aprašykite klausimą apie šeimą. Agentas dirba su turima informacija ir tęsia darbą, kol klausimai ar prieigos prašymai laukia atsakymo. Pavyzdžiui:

- *„Mano prosenelis XX a. ketvirtajame dešimtmetyje buvo ištremtas į Kazachstaną. Padėk rasti jo tėvus bažnytinėse knygose.“*
- *„Štai santuokos liudijimo ir kario kortelės skenavimai. Patikrink, ar tai tas pats asmuo, ir sudaryk įrodymų grandinę.“*
- *„Surask parapiją ir tinkamą FamilySearch filmą XIX a. paskutinio dešimtmečio Podolės kaimui ir perskaityk X pavardės gimimo įrašus.“*

Privačius bylos duomenis laikykite už įgūdžio Git darbinės kopijos ribų. Iš įgūdžio aplanko:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # kiekvieno išsaugoto artefakto SHA-256
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # patikrinti registrus prieš galutinę ataskaitą
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` atsisako kurti bylą įgūdžio aplanke, net su `--force`. Papildomai apsaugai Git ignoruoja dažnus senųjų bylų aplankų pavadinimus; prieš prisidėdami patikrinkite commit parengtus failus, ypač perkeldami esamą bylą.

`build_pdf.py` reikia įdiegtos Chrome, Chromium arba Edge (arba `CHROME_PATH`). Naudojant `--png-dir`, puslapiai taip pat atvaizduojami PNG peržiūrai, jei yra `pypdfium2`.

Naudokite statinį HTML su vietiniais arba įterptais vaizdais. Aktyvus HTML ir tinklo vaizdų šaltiniai atmetami; šaltinių nuorodos lieka paspaudžiamos. Nepavykus atvaizduoti, esamas PDF failas išsaugomas.

## Genealoginis medis GEDCOM formatu

[GEDCOM](https://gedcom.io/specs/) yra standartinis genealoginių duomenų mainų formatas (`.ged`). Paprašius sudaryti ar eksportuoti medį, agentas sukuria vietinį failą su šaltiniais ir pastabomis apie įrodymų pagrįstumą. Dėl suderinamumo pagal nutylėjimą naudojamas GEDCOM 5.5.1 su UTF-8 koduote; jei naudotojas nurodo kitą palaikomą versiją, pavyzdžiui, GEDCOM 7, naudojama ji.

Esamas medis yra pradinė medžiaga ir paieškos užuominos, o ne giminystės įrodymas. Originalas išsaugomas; naudotojo failas neperrašomas. Nepatvirtinti duomenys, prieštaravimai ir neapibrėžtumas lieka byloje. Įrodymų registrai ir paieškos žurnalas lieka išvadų pagrindu. Importo ir eksporto taisyklės pateiktos [references/gedcom.md](references/gedcom.md).

Medžio programą pasirenka naudotojas. Programų diegimas, MCP konfigūravimas ir automatinis sinchronizavimas su išoriniu medžiu nepatenka į šio įgūdžio taikymo sritį.

## Saugyklos struktūra

```
SKILL.md                         pagrindinės instrukcijos (darbo eiga, privalomos taisyklės, kalbos politika)
references/
  source-strategy.md             šaltinių hierarchija, užklausų šablonai, katalogai, archyvų užklausos
  correspondence.md              gavėjai, pašto integracija, leistas siuntimas ir atsakymai
  government-portals.md          civilinės metrikacijos paslaugos ir rezultatų gavimo būdai
  evidence-protocol.md           artefaktų vertinimas, būsenos, asmenų atskyrimas, prieštaravimai
  ex-ussr-locale-guide.md        jurisdikcijos, vardų variantai, kalendoriai, dokumentų rūšys pagal laikotarpį
  browser-and-captcha.md         naršymas, prisijungimas, vienas CAPTCHA bandymas ir perdavimas, dažnio ribojimai
  privacy-and-safety.md          gyvi asmenys, nepilnamečiai, DNR, jautrūs atradimai
  seed-sources.md                atrinkti pradiniai šaltiniai su patikimumo klasėmis
  field-lessons.md               praktinės tikros bylos pamokos
  changelog.md                   laidų istorija
  photo-search.md                nuotraukų paieška, atpažinimas, datavimas ir saugojimas
  habsburg-galicia-bukovina.md   Galicija ir Bukovina valdant Habsburgams ir vėliau
  chechnya-deportation.md        čečėnų šeimos: 1944 m. tremtis, specialiosios gyvenvietės, vardai ir pervadinti kaimai
  germany-forced-labour.md       priverstiniai darbininkai Vokietijoje 1941–1945: Arolsen Archives ir Vokietijos civiliniai registrai

  bessarabia-moldova.md          Besarabija, Moldova, Moldavijos ASSR ir Dniestro pasienis
  familysearch-indexes.md       tikslinis tyrimas naršykle, leistinos vietinės kopijos ir aprėptis
  familysearch-mcp.md           prijungtos priemonės, struktūrinis skaitymas, ribotas rašymas ir tikrinimas
  ww1-search.md                 GWAR asmens/vietovės paieška ir šaltinių vaizdų radimas
  gedcom.md                     medžių mainai GEDCOM formatu, šaltiniai ir įrodymų pagrįstumas
assets/                          bylos pradiniai duomenys, CSV registrai, galutinės ataskaitos šablonas,
                                 nuotraukų README, tyrimo būsenos ir skaitomo PDF šablonai (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py ir bendri vietinės analizės moduliai
evals/discovery-and-logic.yaml   suaktyvinimo ir samprotavimo bandymų atvejai
tests/                           vienetų testai (python3 -m unittest discover -s tests)
```

## Atsakingas naudojimas

- **Šeimos istorija, ne sekimas.** Įgūdis atsisako ieškoti dabartinių gyvų žmonių adresų, telefono numerių ar paskyrų ir mažina jų duomenų kiekį ataskaitose.
- **Prieigos patikros.** Agentas gali vieną kartą bandyti išspręsti tikrą CAPTCHA įprastais vidinės naršyklės valdikliais, kai tai palaikoma ir leidžiama. Jei reikia naudotojo veiksmų, prireikus atveria atitinkamą kortelę ir pateikia URL bei reikiamą veiksmą; prisijungia pats naudotojas. Nenaudojami išoriniai sprendimo servisai, neapeinamos apsaugos, mokėjimo sienos, geografiniai ar dažnio ribojimai ir nenaudojamos nutekėjusios duomenų bazės. Žr. [naršyklės gaires](references/browser-and-captcha.md).
- **Jūsų dokumentai ar DNR duomenys neįkeliami** į trečiųjų šalių paslaugas be aiškaus jūsų sutikimo.
- **Jautrūs atradimai** (tremtis, represijos, įvaikinimas, DNR netikėtumai) pateikiami neutraliai ir tik tiek, kiek reikia klausimui atsakyti.
- **Leistas susirašinėjimas.** Įgūdis gali turimomis priemonėmis siųsti užklausas institucijoms, kai naudotojas tai leido; jau leistam siuntimui pakartotinio leidimo neprašo. Vien pašto dėžutės prijungimas neleidžia siųsti laiškų, priedų ar naudotis mokamomis paslaugomis. Patikrinkite dabartinį oficialų kontaktą ir tvarką; prisijungimo duomenis bei privatų bylos susirašinėjimą laikykite už įgūdžio saugyklos ribų.

## Prisidėjimas

Nauji šaltiniai laukiami `references/seed-sources.md`. Įrašykite patikrintą saugotoją, jurisdikciją, kolekciją, kilmę, ID, prieigą, ribojimus ir patikros datą, jei žinoma; pažymėkite spragas, užuot spėlioję. Pavyzdžiuose neturi būti asmens duomenų.

Šaltinių paieškos priemonės naudoja Python standartinę biblioteką ir esamus bylos registrus. Paleiskite `python3 -m unittest discover -s tests`, kad su sintetiniais duomenimis patikrintumėte vietinį parsavimą, GWAR kontrolinius taškus, prieigos klaidas, neaiškią aprėptį ir įrodymų registravimą. FamilySearch atradimas ir tikslinė peržiūra naudoja esamą teisėtą naršyklės sesiją; Python priemonės analizuoja išsaugotus fragmentus. Privačius tyrimo failus laikykite už šios darbinės kopijos ribų.

## Licencija

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Prižiūri Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
