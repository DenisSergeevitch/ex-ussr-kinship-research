# ex-USSR Kinship Research

![ex-USSR Kinship Research vāka attēls](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Pierādījumos balstīta ģenealoģijas prasme AI aģentiem (Codex, Claude Code un citām Agent Skills izpildvidēm).** Tā padara aģentu par rūpīgu dzimtas vēstures pētnieku bijušās PSRS, Padomju Savienības un Krievijas impērijas teritorijā. Aģents lasa baznīcu grāmatas un civilstāvokļa reģistrus, militārās, deportāciju un represiju lietas, kā arī neindeksētus arhīvu skenējumus. Katra atraduma izcelsme ir izsekojama; dokumenti ir nošķirti no interpretācijas, un skaidri norādīts, kas ir pierādīts un kas nav.

Aptvertas visas 15 bijušās padomju republikas: Krievija, Ukraina, Baltkrievija, Moldova, Igaunija, Latvija, Lietuva, Gruzija, Armēnija, Azerbaidžāna, Kazahstāna, Kirgizstāna, Tadžikistāna, Turkmenistāna un Uzbekistāna. Arhīvus izvēlas pēc notikuma vēsturiskās jurisdikcijas un dokumentu pašreizējā glabātāja; reģionāls piemērs neaizstāj vietējo izpēti.

Prasmes instrukcijas ir rakstītas krieviski, taču **aģents ar jums sarunājas jūsu valodā**: angliski, ukrainiski, krieviski, poliski, vāciski un citās valodās. Avotus tas citē sākotnējā rakstībā ar tulkojumu un meklēšanas vaicājumus veido dokumentu valodās.

---

## Ko tā dara

- **Lietas sākotnējie dati un robežas.** Viens izpētes jautājums, zināmie fakti, iespējami dzīvie cilvēki un nepieļaujamās darbības.
- **Atkārtojami reģistri.** Personas, artefakti, apgalvojumi, radniecības saites un pilns meklēšanas žurnāls (CSV), kā arī gala pārskata veidne.
- **Vēsturiskās jurisdikcijas modelis.** Katru notikumu saista ar valsti, provinci, apriņķi, draudzi vai civilstāvokļa iestādi *notikuma datumā*, nevis pēc mūsdienu kartes.
- **Vārdu variantu matricas.** Pirmsreformas krievu, ukraiņu, poļu, rumāņu, vācu un jidiša formas, tēvavārdi, pirmslaulības uzvārdi un transliterācijas.
- **Avotu stratēģija.** Vispirms oriģināli, tad oficiālie katalogi, indeksi un publicēti dokumentu krājumi; dzimtas koki un forumi kalpo tikai par turpmākām norādēm.
- **Pierādījumu protokols.** Apgalvojumiem piešķir izskaidrojamus statusus, nevis procentus: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Viena ieraksta kopijām un spoguļvietnēm ir kopīga `independence_group`, tādēļ tās nekad netiek uzskaitītas kā neatkarīgi pierādījumi.
- **Personu nošķiršana.** Vārdabrāļiem saglabā atsevišķus `person_id`, līdz parādās atšķiroši pierādījumi: mājas numurs, vecāki, krustvecāki, precīzs dzimšanas datums vai karaspēka daļa.
- **Audita skripts.** Pārbauda atsauču integritāti un pirms secinājumiem atzīmē vāju apstiprinājumu. Neatkarības grupu ieskaita tikai tad, ja tai pieder citēts artefakts; apstiprinājumu nevar radīt ar deklarāciju vien. Pārbauda arī gala pārskatu: katram citētajam ID jābūt reģistros, un visiem statusiem jāsakrīt ar tiem. Kopsavilkums parāda vēl neapstiprināto vai par nesalasāmu atzīmēto.
- **Pieprasījumi iestādēm.** Sagatavo un, ja ir atļauja, nosūta mērķētus pieprasījumus arhīviem, bibliotēkām, universitātēm un muzejiem ar pieejamo e-pastu vai oficiāliem tīmekļa rīkiem. Vajadzības gadījumā piedāvā atbalstītu pasta integrāciju vai nosūtīšanai gatavu vēstuli. Reģistrē rezultātu, izvairās no atkārtotas nosūtīšanas un atbildes izmanto kā pierādījumus. Skatiet [sarakstes vadlīnijas](references/correspondence.md).
- **Valsts pakalpojumi.** Izvēlas oficiālu civilstāvokļa vai arhīva pieprasījuma ceļu, pārbaudot tiesības pieprasīt un rezultāta saņemšanu ([valsts portāli](references/government-portals.md)).
- **Gala pārskats.** Katra radniecības saite izklāstīta pa posmiem, norādot pretrunas, neveiksmīgas meklēšanas un konkrētus nākamos soļus.
- **Mērķēta indeksēto ierakstu izpēte.** Atrod atbilstošas FamilySearch grāmatas pēc vietas vai DGS esošā tiesiski izmantotā pārlūka sesijā, skata konkrētus ierakstus un saglabā tikai avota atļautus pierādījumu fragmentus. Vietējie palīgrīki saglabātajos fragmentos meklē radiniekus, lieciniekus un vārdu variantus, saglabājot kontekstu un failu kontrolsummas. [Darba gaita un aptvēruma robežas](references/familysearch-indexes.md).
- **Pievienots FamilySearch MCP.** Izmanto pievienotu serveri strukturētai meklēšanai, profiliem, radiniekiem un avotiem, kā arī atļautām koka izmaiņām ar skaidru apjomu un rezultāta atkārtotu nolasīšanu. Nošķir meklēšanu indeksos no neindeksētu skenējumu lasīšanas un pārbauda savienotāja faktiskās pārlūka, privātuma un rakstīšanas iespējas. [Darba gaita un piekļuves ierobežojumi](references/familysearch-mcp.md).
- **Pirmā pasaules kara avotu meklēšana.** Meklē GWAR ziņojumus, slimnīcu, apbalvojumu un karagūstekņu ierakstus pēc personas vai vietas; salīdzina apdzīvoto vietu rakstību saglabātajās kartītēs, lai atšifrētu sagrozītu vietvārdu, un atrod avota attēlu. [Darba gaita](references/ww1-search.md). Abi palīgrīki papildina esošo artefaktu reģistru un meklēšanas žurnālu; tie automātiski nenosaka identitāti vai radniecību.

Laidienu vēsture: [izmaiņu žurnāls](references/changelog.md).

<a id="install"></a>

## Instalēšana

Ja instalēts Node.js, varat izmantot izvēles [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI ļauj izvēlēties aģentu un pēc noklusējuma instalē pašreizējā projektā; pievienojiet `-g` personīgai instalācijai visos projektos. Pašreizējās Node.js prasības skatiet tā dokumentācijā.

Vai arī klonējiet repozitoriju tieši aģenta prasmju mapē:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (personīgās prasmes)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Vienam projektam ievietojiet mapi repozitorija `.claude/skills/` mapē. Skriptiem nepieciešams tikai Python 3 un standarta bibliotēka; `build_pdf.py` vajadzīgs arī Chromium saimes pārlūks.

## Lietošana

Aprakstiet jautājumu par dzimtu. Aģents strādā ar pieejamo informāciju un turpina, kamēr jautājumi vai piekļuves pieprasījumi gaida atbildi. Piemēram:

- *„Manu vecvectēvu 20. gadsimta 30. gados izsūtīja uz Kazahstānu. Palīdzi atrast viņa vecākus baznīcu grāmatās.”*
- *„Šeit ir laulības apliecības un karavīra kartītes skenējumi. Pārbaudi, vai runa ir par vienu personu, un izveido pierādījumu ķēdi.”*
- *„Atrodi draudzi un pareizo FamilySearch filmu Podolijas ciemam 1890. gados un izlasi dzimšanas ierakstus ar uzvārdu X.”*

Lietas privātos datus glabājiet ārpus prasmes Git darba kopijas. No prasmes mapes:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 katram saglabātajam artefaktam
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # pārbaudīt reģistrus pirms gala pārskata
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` atsakās veidot lietu prasmes mapē, arī ar `--force`. Papildu aizsardzībai Git ignorē bieži lietotus agrāko lietu mapju nosaukumus; pirms ieguldījuma pārbaudiet commit sagatavotos failus, īpaši pārvietojot esošu lietu.

`build_pdf.py` nepieciešams instalēts Chrome, Chromium vai Edge (vai `CHROME_PATH`). Ar `--png-dir` tas pārskatīšanai izveido arī lapu PNG attēlus, ja pieejams `pypdfium2`.

Izmantojiet statisku HTML ar vietējiem vai iegultiem attēliem. Aktīvs HTML un tīkla attēlu avoti netiek pieņemti; saites uz avotiem paliek klikšķināmas. Neveiksmīga renderēšana saglabā esošo PDF failu.

## Dzimtas koks GEDCOM formātā

[GEDCOM](https://gedcom.io/specs/) ir standarta formāts ģenealoģisko datu apmaiņai (`.ged`). Pēc lūguma izveidot vai eksportēt dzimtas koku aģents sagatavo lokālu failu ar avotiem un piezīmēm par pierādījumu stiprumu. Saderībai pēc noklusējuma izmanto GEDCOM 5.5.1 ar UTF-8 kodējumu; ja lietotājs norāda citu atbalstītu versiju, piemēram, GEDCOM 7, izmanto to.

Esošais koks ir sākotnējais materiāls un meklēšanas pavedieni, nevis radniecības pierādījums. Oriģināls tiek saglabāts; lietotāja failu nepārraksta. Neapstiprinātas ziņas, pretrunas un nenoteiktība paliek lietā. Pierādījumu reģistri un meklēšanas žurnāls paliek secinājumu pamats. Importa un eksporta noteikumi ir [references/gedcom.md](references/gedcom.md).

Dzimtas koka programmu izvēlas lietotājs. Lietotņu uzstādīšana, MCP konfigurēšana un automātiska sinhronizācija ar ārēju koku neietilpst šīs prasmes tvērumā.

## Repozitorija struktūra

```
SKILL.md                         galvenās instrukcijas (darba gaita, obligātie noteikumi, valodas politika)
references/
  source-strategy.md             avotu hierarhija, vaicājumu paraugi, katalogi, arhīvu pieprasījumi
  correspondence.md              saņēmēji, pasta integrācija, atļauta sūtīšana un atbildes
  government-portals.md          civilstāvokļa pakalpojumi un rezultātu saņemšana
  evidence-protocol.md           artefaktu novērtēšana, statusi, personu nošķiršana, pretrunas
  ex-ussr-locale-guide.md        jurisdikcijas, vārdu varianti, kalendāri, dokumentu veidi pa periodiem
  browser-and-captcha.md         pārlūkošana, pierakstīšanās, viens CAPTCHA mēģinājums un nodošana, biežuma ierobežojumi
  privacy-and-safety.md          dzīvi cilvēki, nepilngadīgie, DNS, sensitīvi atradumi
  seed-sources.md                atlasīti sākuma resursi ar uzticamības klasēm
  field-lessons.md               praktiskas atziņas no īstas lietas
  changelog.md                   laidienu vēsture
  photo-search.md                fotogrāfiju atrašana, identificēšana, datēšana un glabāšana
  habsburg-galicia-bukovina.md   Galīcija un Bukovina Hābsburgu laikā un vēlāk
  chechnya-deportation.md        čečenu ģimenes: 1944. gada deportācija, specnometinājumi, vārdi un pārdēvēti ciemi
  germany-forced-labour.md       piespiedu darbinieki Vācijā 1941–1945: Arolsen Archives un Vācijas civilstāvokļa reģistri

  bessarabia-moldova.md          Besarābija, Moldova, Moldāvijas APSR un Dņestras pierobeža
  familysearch-indexes.md       mērķēta pārlūka izpēte, atļautas vietējās kopijas un aptvērums
  familysearch-mcp.md           pievienoti rīki, strukturēta lasīšana, ierobežota rakstīšana un pārbaude
  ww1-search.md                 GWAR personu/vietu meklēšana un avota attēlu atrašana
  gedcom.md                     koku apmaiņa GEDCOM formātā, avoti un pierādījumu stiprums
assets/                          lietas sākotnējie dati, CSV reģistri, gala pārskata veidne,
                                 fotogrāfiju README, izpētes stāvokļa un lasāma PDF veidnes (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py un kopīgi vietējās analīzes moduļi
evals/discovery-and-logic.yaml   aktivizēšanas un spriešanas pārbaudes piemēri
tests/                           vienībtesti (python3 -m unittest discover -s tests)
```

## Atbildīga lietošana

- **Dzimtas vēsture, nevis izsekošana.** Prasme atsakās meklēt dzīvu cilvēku pašreizējās adreses, tālruņus vai kontus un samazina viņu datu apjomu pārskatos.
- **Piekļuves pārbaudes.** Aģents drīkst vienreiz mēģināt atrisināt īstu CAPTCHA ar iekšējā pārlūka parastajiem vadības elementiem, ja tas ir atbalstīts un atļauts. Ja vajadzīga lietotāja rīcība, iespēju robežās atver attiecīgo cilni un norāda URL un vajadzīgo darbību; pierakstās lietotājs pats. Netiek izmantoti ārējie risinātāji, aizsardzības, maksas, ģeogrāfisko vai biežuma ierobežojumu apiešana un noplūdušas datubāzes. Skatiet [pārlūka vadlīnijas](references/browser-and-captcha.md).
- **Jūsu dokumenti vai DNS dati netiek augšupielādēti** trešo pušu pakalpojumos bez nepārprotamas piekrišanas.
- **Sensitīvi atklājumi** (deportācija, represijas, adopcija, DNS pārsteigumi) tiek pasniegti neitrāli un tikai jautājumam vajadzīgajā apjomā.
- **Atļauta sarakste.** Prasme var sūtīt pieprasījumus iestādēm ar pieejamiem rīkiem, kad lietotājs devis atļauju; jau atļautai nosūtīšanai tā atkārtoti nejautā. Pasta konta pievienošana pati par sevi neatļauj sūtīšanu, pielikumus vai maksas pakalpojumus. Pārbaudiet pašreizējo oficiālo kontaktu un kārtību; piekļuves datus un lietas privāto saraksti glabājiet ārpus prasmes repozitorija.

## Ieguldījumi

Jauni avoti ir gaidīti `references/seed-sources.md`. Norādiet pārbaudītu glabātāju, jurisdikciju, kolekciju, izcelsmi, ID, piekļuvi, ierobežojumus un pārbaudes datumu, ja tie zināmi; atzīmējiet trūkstošo, nevis miniet. Piemēros neiekļaujiet personas datus.

Avotu meklēšanas palīgrīki izmanto Python standarta bibliotēku un esošos lietas reģistrus. Palaidiet `python3 -m unittest discover -s tests`, lai ar sintētiskiem datiem pārbaudītu vietējo parsēšanu, GWAR kontrolpunktus, piekļuves kļūmes, nenoskaidrotu aptvērumu un pierādījumu reģistrāciju. FamilySearch atklāšana un mērķēta skatīšana izmanto esošo tiesisko pārlūka sesiju; Python palīgrīki analizē saglabātos fragmentus. Privātos izpētes failus glabājiet ārpus šīs darba kopijas.

## Licence

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Uztur Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
