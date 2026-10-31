# ex-USSR Kinship Research

![ex-USSR Kinship Research sahypasynyň baş suraty](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Emeli aň agentleri üçin subutnamany ileri tutýan nesilşynaslyk başarnygy (Codex, Claude Code we beýleki Agent Skills gurşawlary).** Ol agenti öňki SSSR, Sowet Soýuzy we Russiýa imperiýasy boýunça maşgala taryhyny ünsli öwrenýän gözlegçä öwürýär. Agent buthana kitaplaryny we raýat ýagdaýynyň ýazgylaryny, harby, sürgün we repressiýa resminamalaryny, şeýle hem indekslenmedik arhiw skanlaryny okaýar. Her tapyndynyň gelip çykyşyny yzarlap bolýan görnüşde saklaýar, ýazgyny onuň düşündirişinden aýyrýar we nämäniň subut edilendigini, nämäniň edilmändigini açyk aýdýar.

Iş çägi öňki 15 sowet respublikasynyň hemmesini öz içine alýar: Russiýa, Ukraina, Belarus, Moldowa, Estoniýa, Latwiýa, Litwa, Gruziýa, Ermenistan, Azerbaýjan, Gazagystan, Gyrgyzystan, Täjigistan, Türkmenistan we Özbegistan. Arhiwler wakanyň bolan döwründäki taryhy dolandyryş degişliligine we ýazgylary häzir saklaýan edara görä saýlanýar; sebitleýin mysal ýerli gözlegiň ornuny tutmaýar.

Başarnygyň görkezmeleri rusça ýazylan, ýöne **agent siziň bilen öz diliňizde gürleşýär**: iňlisçe, ukrainçe, rusça, polýakça, nemesçe we ş.m. Çeşmelerden parçalary asyl ýazylyşynda terjimesi bilen getirýär we gözleg talaplaryny ýazgylaryň dilinde düzýär.

---

## Näme edýär

- **Gözleg işini başlamak we çägini kesgitlemek.** Bir gözleg soragy, belli maglumatlar, kimiň diri bolmagy mümkin we rugsat edilmeýän hereketler.
- **Gaýtadan barlap bolýan sanawlar.** Adamlar, artefaktlar, tassyklamalar, garyndaşlyk baglanyşyklary we doly gözleg gündeligi (CSV), şeýle hem jemleýji hasabatyň nusgasy.
- **Taryhy dolandyryş degişliligi modeli.** Her wakany häzirki karta däl-de, *wakanyň bolan senesindäki* döwlete, welaýata, etraba, buthana jemagatyna ýa-da raýat ýagdaýyny bellige alyş edarasyna degişli edýär.
- **At görnüşleriniň tablisalary.** Özgertmeden öňki rusça, ukrainçe, polýakça, rumynça, nemesçe we ýidişçe görnüşler, atasynyň ady, durmuşa çykmazdan öňki familiýa we transliterasiýalar.
- **Çeşme strategiýasy.** Ilki asyl nusgalar, soň resmi kataloglar, indeksler, neşir edilen resminama ýygyndylary; diňe şondan soň şejereler we forumlar gözleg ugruny görkezýän maglumat hökmünde ulanylýar.
- **Subutnama düzgüni.** Tassyklamalara göterim däl-de, düşündirip bolýan ýagdaýlar berilýär: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Bir ýazgynyň göçürmeleri we aýna nusgalary umumy `independence_group` toparyna girýär, şonuň üçin olar hiç wagt garaşsyz subutnama hasaplanmaýar.
- **Şahsyýeti anyklamak.** Jaý belgisi, ene-atasy, çokundyrma ene-atalary, takyk doglan senesi ýa-da harby bölümi ýaly tapawutlandyryjy subutnama tapylýança atdaşlar aýratyn `person_id` bilen saklanýar.
- **Audit skripti.** Netije ýazylmazdan öň salgylanmalaryň bitewiligini barlaýar we gowşak tassyklamalary belleýär. Garaşsyzlyk topary diňe salgylanylýan artefakt şol topara degişli bolsa hasaba alynýar; tassyklamany diňe yglan etmek bilen döretmek bolmaýar. Jemleýji hasabaty hem barlaýar: getirilen her ID sanawlarda bolmaly we her ýagdaý olara gabat gelmeli. Jemleme nämäniň entek tassyklanmandygyny ýa-da okap bolmaýan diýlip bellenendigini görkezýär.
- **Edaralara ýüz tutmak.** Elýeterli e-poçta ýa-da resmi web gurallary bilen arhiwlere, kitaphanalara, uniwersitetlere we muzeýlere anyk talaplary taýýarlaýar hem-de rugsat bolanda iberýär. Gerek bolsa goldanylýan poçta birikmesini ýa-da ibermäge taýýar haty hödürleýär. Netijäni ýazýar, gaýtadan iberilmeginiň öňüni alýar we jogaplary subutnama hökmünde kabul edýär. [Hat alyşmak boýunça görkezmä](references/correspondence.md) serediň.
- **Döwlet hyzmatlary.** Ýüz tutmaga hukugy we netijäniň nähili gowşuryljakdygyny barlap, raýat ýagdaýyny bellige alyş ýa-da arhiw talaby üçin resmi ýoly saýlaýar ([döwlet portallary](references/government-portals.md)).
- **Jemleýji hasabat.** Her garyndaşlyk baglanyşygy aýratyn baglar boýunça, gapma-garşylyklar, netijesiz gözlegler we indiki anyk ädimler bilen görkezilýär.
- **Indekslenen ýazgylary maksatly öwrenmek.** Öňden bar bolan kanuny brauzer sessiýasy arkaly ýer ýa-da DGS boýunça degişli FamilySearch kitaplaryny tapýar, anyk ýazgylary görýär we diňe çeşmäniň rugsat berýän subutnama parçalaryny saklaýar. Ýerli kömekçi gurallar saklanan parçalardan garyndaşlary, şaýatlary we at görnüşlerini gözleýär, olaryň kontekstini we faýllaryň barlag jemlerini saklaýar. [Iş tertibi we gurşawyň çäkleri](references/familysearch-indexes.md).
- **Birikdirilen FamilySearch MCP.** Birikdirilen serweri gurluşly gözlegler, profiller, garyndaşlar, çeşmeler we anyk çäkleri bellenen, soňundan gaýtadan okap barlanylýan, rugsat berlen şejere üýtgeşmeleri üçin ulanýar. Indekslenen gözlegi indekslenmedik skanlary okamakdan aýry saklaýar we birikdirijiniň brauzer, gizlinlik hem-de ýazmak boýunça hakyky mümkinçiliklerini barlaýar. [Iş tertibi we elýeterlilik çäkleri](references/familysearch-mcp.md).
- **Birinji jahan urşunyň çeşmelerini gözlemek.** GWAR habarlaryny, hassahana, sylag we harby ýesir ýazgylaryny adam ýa-da ýer boýunça gözleýär; ýoýlan ýer adyny çözmek üçin saklanan kartoçkalardaky ilatly ýer atlarynyň ýazylyşyny deňeşdirýär, soň çeşmäniň asyl suratyny tapýar. [Iş tertibi](references/ww1-search.md). Iki kömekçi gural hem bar bolan artefakt sanawyna we gözleg gündeligine maglumat goşýar; şahsyýeti ýa-da garyndaşlygy awtomatik kesgitlemeýär.

Goýberilişleriň taryhy: [üýtgeşmeler gündeligi](references/changelog.md).

<a id="install"></a>
## Gurmak

Node.js gurnalan bolsa, goşmaça [Skills CLI](https://github.com/vercel-labs/skills) guralyny ulanyp bilersiňiz:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI agentiňizi saýlamaga mümkinçilik berýär we adaty ýagdaýda häzirki taslama gurýar; ähli taslamalarda şahsy ulanmak üçin `-g` goşuň. Node.js boýunça häzirki talaplary onuň resminamalaryndan görüň.

Ýa-da repozitoriýany göni agentiňiziň başarnyklar bukjasyna klonlaň:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (şahsy başarnyklar)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Bir taslama üçin bukjany repozitoriýanyň içindäki `.claude/skills/` ýerine goýuň. Skriptlere diňe Python 3 we standart kitaphana gerek; `build_pdf.py` üçin Chromium esasly brauzer hem zerur.

## Ulanmak

Maşgala barada gözleg soragyňyzy beýan ediň. Agent elýeterli maglumatlardan ugur alyp işleýär we soraglara ýa-da giriş talaplaryna jogap garaşylýarka hem gözlegi dowam etdirýär. Mysal üçin:

- *«Atamyň kakasy 1930-njy ýyllarda Gazagystana sürgün edilipdir. Onuň ene-atasyny buthana ýazgylaryndan tapmaga kömek et.»*
- *«Ine, nika şahadatnamasynyň we esger kartoçkasynyň skanlary. Olaryň şol bir adama degişlidigini barla we subutnama zynjyryny düz.»*
- *«1890-njy ýyllarda Podoliýadaky bir oba üçin buthana jemagatyny we dogry FamilySearch filmini tap, X familiýasy boýunça dogluş ýazgylaryny oka.»*

Şahsy gözleg işiniň maglumatlaryny başarnygyň Git iş nusgasyndan daşarda saklaň. Başarnyk bukjasyndan:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # her saklanan artefakt üçin SHA-256
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # jemleýji hasabatdan öň sanawlary barlamak
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` başarnyk bukjasynyň içinde, hatda `--force` bilen hem, gözleg işini döretmegi ret edýär. Goşmaça gorag hökmünde Git öňki iş bukjalarynyň giňden ulanylýan atlaryny äsgermeýär; goşant goşmazdan öň, esasan hem bar işi göçüreniňizde, indekse goşulan faýllary barlaň.

`build_pdf.py` üçin Chrome, Chromium ýa-da Edge gurnalan bolmaly (ýa-da `CHROME_PATH` görkezilmeli). `pypdfium2` elýeterli bolsa, `--png-dir` sahypalary gözden geçirmek üçin PNG görnüşinde hem çykarýar.

Ýerli ýa-da içine ýerleşdirilen suratlary bolan statik HTML ulanyň. Işjeň HTML we tordan alynýan surat çeşmeleri kabul edilmeýär; çeşme baglanyşyklary basylýan görnüşde galýar. Render şowsuz bolsa, öňki netijäniň PDF faýly saklanýar.

## GEDCOM görnüşindäki maşgala şejeresi

[GEDCOM](https://gedcom.io/specs/) (`.ged`) nesilşynaslyk maglumatlaryny alyşmagyň standart görnüşidir. Şejere düzmek ýa-da eksport etmek soralanda, agent çeşme salgylary we subutnama derejesi barada bellikler bilen ýerli faýl taýýarlaýar. Gabat gelmek üçin deslapky saýlaw UTF-8 kodlamasyndaky GEDCOM 5.5.1-dir; ulanyjy goldanylýan başga wersiýany, mysal üçin GEDCOM 7-ni saýlasa, şol ulanylýar.

Bar bolan şejere başlangyç material we gözleg üçin ugur hökmünde ulanylýar, öz-özünden subutnama hasaplanmaýar. Asyl faýl saklanýar we üstünden ýazylmaýar; tassyklanmadyk maglumatlar we näbellilik gözleg işinde galýar. Subutnama sanawlary we gözleg gündeligi netijeleriň esasy hasaby bolup galýar.

Programmany ulanyjy saýlaýar. Programmany gurmak, MCP birikmesini sazlamak we daşarky şejere bilen awtomatik sinhronlamak başarnygyň çägine girmeýär. Giňişleýin: [references/gedcom.md](references/gedcom.md).

## Repozitoriýanyň gurluşy

```
SKILL.md                         esasy görkezmeler (iş tertibi, berk düzgünler, dil syýasaty)
references/
  source-strategy.md             çeşme iýerarhiýasy, talap nusgalary, kataloglar, arhiw talaplary
  correspondence.md              alyjylar, poçta birikmesi, rugsat berlen iberiş we jogaplar
  government-portals.md          raýat bellige alyş hyzmatlary we talap netijesini gowşurmak
  evidence-protocol.md           artefakt bahasy, ýagdaýlar, şahsyýeti anyklamak, gapma-garşylyklar
  ex-ussr-locale-guide.md        dolandyryş degişliligi, at görnüşleri, senenamalar, döwür boýunça ýazgylar
  browser-and-captcha.md         brauzer, giriş, bir CAPTCHA synanyşygy we ulanyja geçirmek, tizlik çäkleri
  privacy-and-safety.md          diri adamlar, kämillik ýaşyna ýetmedikler, DNK, duýgur tapyndylar
  seed-sources.md                ygtybarlylyk toparlary bilen saýlanan başlangyç çeşmeler
  field-lessons.md               hakyky gözleg işinden amaly sapaklar
  changelog.md                   goýberilişleriň taryhy
  photo-search.md                suratlary tapmak, tanamak, senesini kesgitlemek we saklamak
  habsburg-galicia-bukovina.md   Habsburglar döwründäki we soňraky Galisiýa hem Bukowina
  chechnya-deportation.md        çeçen maşgalalary: 1944-nji ýyldaky sürgün, ýörite mesgen, atlar we ady üýtgedilen obalar
  germany-forced-labour.md       Germaniýada mejbury zähmet, 1941–1945: Arolsen Archives we nemes raýat ýazgylary

  bessarabia-moldova.md          Bessarabiýa, Moldowa, Moldowa ASSR-i we Dnestr serhet sebiti
  familysearch-indexes.md       brauzerde maksatly gözleg, rugsatly ýerli nusgalar we gurşaw
  familysearch-mcp.md           birikdirilen gurallar, gurluşly okamak, çäklendirilen ýazmak we barlag
  ww1-search.md                 GWAR-da adam/ýer gözlegi we çeşme suratynyň ýerleşişi
  gedcom.md                     GEDCOM alyşmagy: çeşmeler, subutnama derejesi we gözleg işi
assets/                          başlangyç maglumatlar, CSV sanawlary, jemleýji hasabat nusgasy,
                                 suratlar üçin README, gözleg ýagdaýy, düşnükli PDF nusgasy (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py we umumy ýerli seljeriş modullary
evals/discovery-and-logic.yaml   işjeňleşme we pikir ýöretme synaglary
tests/                           modul synaglary (python3 -m unittest discover -s tests)
```

## Jogapkärçilikli ulanmak

- **Gözegçilik däl, maşgala taryhy.** Başarnyk diri adamlaryň häzirki salgylaryny, telefonlaryny ýa-da hasaplaryny gözlemegi ret edýär we hasabatlarda olaryň maglumatlaryny mümkin boldugyça azaldýar.
- **Giriş barlaglary.** Goldanylýan we rugsat berilýän bolsa, agent içerki brauzeriň adaty dolandyryş serişdeleri bilen hakyky CAPTCHA-ny bir gezek synap biler. Ulanyjynyň hereketi gerek bolsa, mümkin bolanda degişli goýmaçany açýar we URL-i hem-de zerur hereketi berýär; hasaba ulanyjynyň özi girýär. Daşarky çözüji hyzmatlar, goragy, töleg diwaryny, geografik bloklamany ýa-da talap tizliginiň çäklerini aýlanyp geçmek we syzdyrylan maglumat bazalary ulanylmaýar. [Brauzer görkezmesine](references/browser-and-captcha.md) serediň.
- **Açyk razylygyňyz bolmazdan resminamalaryňyz ýa-da DNK maglumatlaryňyz üçünji tarap hyzmatlaryna ýüklenmeýär.**
- **Duýgur tapyndylar** (sürgün, repressiýa, ogullyga almak, garaşylmadyk DNK netijeleri) bitarap we diňe soragyň talap edýän möçberinde beýan edilýär.
- **Rugsat berlen hat alyşmak.** Ulanyjy rugsat beren bolsa, başarnyk elýeterli gurallar bilen edaralara talap iberip biler; öňden rugsat edilen iberiş üçin gaýtadan soramaýar. Diňe poçta gutusyny birikdirmek hat ibermäge, goşundylara ýa-da tölegli hyzmatlara rugsat bermeýär. Häzirki resmi aragatnaşygy we tertibi barlaň, giriş maglumatlaryny we şahsy gözleg hatlaryny başarnygyň repozitoriýasyndan daşarda saklaň.

## Goşant goşmak

Täze çeşmeleri `references/seed-sources.md` faýlyna goşup bilersiňiz. Belli bolsa barlanan eýesini, dolandyryş degişliligini, ýygyndysyny, gelip çykyşyny, ID-lerini, elýeterliligini, çäklendirmelerini we barlag senesini ýazyň; boşluklary çaklama bilen doldurman belläň. Mysallara şahsy maglumatlary goşmaň.

Çeşme gözleginiň kömekçi gurallary Python-yň standart kitaphanasyny we bar bolan gözleg sanawlaryny ulanýar. Ýerli seljermäni, GWAR dowam nokatlaryny, giriş şowsuzlyklaryny, anyklanmadyk gurşawy we emeli maglumatlar bilen subutnama bellige alnyşyny barlamak üçin `python3 -m unittest discover -s tests` işlediň. FamilySearch-de tapmak we maksatly seretmek öňden bar bolan kanuny brauzer sessiýasyny ulanýar; Python kömekçileri saklanan parçalary seljerýär. Şahsy gözleg faýllaryny bu iş nusgasyndan daşarda saklaň.

## Ygtyýarnama

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Taslamany ýörediji: Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
