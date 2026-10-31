# ex-USSR Kinship Research

![Coperta ex-USSR Kinship Research](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Un skill de genealogie bazat pe dovezi pentru agenți AI (Codex, Claude Code și alte medii Agent Skills).** Transformă agentul într-un cercetător atent al istoriei familiei din fostul spațiu sovietic, Uniunea Sovietică și Imperiul Rus. Agentul citește registre parohiale și de stare civilă, dosare militare, de deportare și represiune, precum și scanări de arhivă neindexate. Păstrează proveniența fiecărei descoperiri, separă documentele de interpretare și spune clar ce este demonstrat și ce nu.

Acoperă toate cele 15 foste republici sovietice: Rusia, Ucraina, Belarus, Moldova, Estonia, Letonia, Lituania, Georgia, Armenia, Azerbaidjan, Kazahstan, Kârgâzstan, Tadjikistan, Turkmenistan și Uzbekistan. Arhivele sunt alese după jurisdicția istorică a evenimentului și deținătorul actual al documentelor; un exemplu regional nu înlocuiește cercetarea locală.

Instrucțiunile skill-ului sunt scrise în rusă, dar **agentul vă vorbește în limba dumneavoastră**: engleză, ucraineană, rusă, poloneză, germană și altele. Citează sursele cu grafia originală și o traducere, iar interogările sunt formulate în limbile documentelor.

---

## Ce face

- **Preluarea și delimitarea cazului.** O întrebare de cercetare, faptele cunoscute, cine ar putea fi în viață și limitele cercetării.
- **Registre reproductibile.** Persoane, artefacte, afirmații, relații și un jurnal complet de căutare (CSV), plus un șablon pentru raportul final.
- **Modelul jurisdicției istorice.** Atribuie fiecare eveniment statului, provinciei, districtului, parohiei sau oficiului de stare civilă *de la data evenimentului*, nu hărții de astăzi.
- **Matrice ale variantelor de nume.** Forme rusești prereformă, ucrainene, poloneze, românești, germane și idiș, patronimice, nume de fată și transliterări.
- **Strategia surselor.** Mai întâi originale, apoi cataloage oficiale, indexuri și colecții de documente publicate; arborii și forumurile servesc abia apoi ca piste.
- **Protocolul dovezilor.** Afirmațiile primesc stări explicabile, nu procente: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Copiile și oglinzile aceluiași document au același `independence_group` și nu sunt niciodată dovezi independente.
- **Identificarea persoanelor.** Omonimii păstrează `person_id` distincte până apar dovezi care îi diferențiază: numărul casei, părinții, nașii, data exactă a nașterii sau unitatea militară.
- **Scriptul de audit.** Verifică integritatea referințelor și semnalează coroborarea slabă înainte de concluzii. Un grup de independență contează numai dacă îi aparține un artefact citat; coroborarea nu poate fi creată prin simpla declarare. Verifică și raportul final: fiecare ID citat trebuie să existe în registre, iar fiecare stare trebuie să corespundă acestora. Rezumatul arată ce rămâne necoroborat sau ilizibil.
- **Cereri către instituții.** Pregătește și, cu autorizare, trimite cereri precise arhivelor, bibliotecilor, universităților și muzeelor prin e-mailul disponibil sau instrumentele web oficiale. La nevoie propune o integrare de e-mail acceptată sau o scrisoare gata de trimis. Înregistrează rezultatul, evită trimiterile duplicate și tratează răspunsurile ca dovezi. Consultați [ghidul de corespondență](references/correspondence.md).
- **Servicii publice.** Alege o cale oficială pentru solicitări de stare civilă sau de arhivă, verificând eligibilitatea și modalitatea de livrare ([portaluri guvernamentale](references/government-portals.md)).
- **Raportul final.** Prezintă fiecare relație legătură cu legătură, cu contradicții, căutări nereușite și pași următori concreți.
- **Cercetare țintită a documentelor indexate.** Găsește registre FamilySearch după localitate sau DGS printr-o sesiune de browser legală existentă, consultă înregistrări specifice și păstrează numai fragmentele de dovezi permise de sursă. Instrumentele locale caută rude, martori și variante de nume în fragmentele salvate, păstrând contextul și sumele de control. [Flux de lucru și limite de acoperire](references/familysearch-indexes.md).
- **FamilySearch MCP conectat.** Folosește serverul conectat pentru căutări structurate, profiluri, rude și surse, precum și pentru modificări autorizate ale arborelui, cu limite explicite și verificare prin recitire. Separă căutarea în indexuri de citirea scanărilor neindexate și verifică funcțiile reale ale conectorului privind browserul, confidențialitatea și scrierea. [Flux de lucru și limite de acces](references/familysearch-mcp.md).
- **Căutarea surselor din Primul Război Mondial.** Caută rapoarte GWAR, documente de spital, decorații și prizonieri de război după persoană sau localitate; compară grafiile așezărilor din fișele salvate pentru a descifra un toponim deformat, apoi găsește imaginea sursei. [Flux de lucru](references/ww1-search.md). Ambele instrumente alimentează registrul de artefacte și jurnalul de căutare existente; nu stabilesc automat identitatea sau rudenia.

Istoricul versiunilor: [jurnalul modificărilor](references/changelog.md).

<a id="install"></a>

## Instalare

Cu Node.js instalat, puteți folosi opțional [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI vă permite să alegeți agentul și instalează implicit în proiectul curent; adăugați `-g` pentru o instalare personală disponibilă în toate proiectele. Consultați documentația sa pentru cerințele Node.js actuale.

Alternativ, clonați depozitul direct în directorul de skill-uri al agentului:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (skill-uri personale)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Pentru un singur proiect, puneți directorul în `.claude/skills/` din depozit. Scripturile necesită numai Python 3 și biblioteca standard; `build_pdf.py` necesită și un browser bazat pe Chromium.

## Utilizare

Descrieți întrebarea despre familie. Agentul folosește informațiile disponibile și continuă cât timp întrebările sau cererile de acces așteaptă răspuns. De exemplu:

- *„Străbunicul meu a fost exilat în Kazahstan în anii 1930. Ajută-mă să-i găsesc părinții în registrele parohiale.”*
- *„Iată scanările unui certificat de căsătorie și ale unei fișe militare. Verifică dacă se referă la aceeași persoană și construiește lanțul de dovezi.”*
- *„Găsește parohia și microfilmul FamilySearch potrivit pentru un sat din Podolia din anii 1890 și citește nașterile pentru numele X.”*

Păstrați datele private ale cazului în afara copiei Git a skill-ului. Din directorul skill-ului:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 pentru fiecare artefact salvat
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # verificarea registrelor înaintea raportului final
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` refuză crearea unui caz în directorul skill-ului, inclusiv cu `--force`. Ca protecție suplimentară, Git ignoră denumirile uzuale ale vechilor directoare de caz; verificați fișierele pregătite pentru commit înainte de contribuții, mai ales când mutați un caz existent.

`build_pdf.py` necesită Chrome, Chromium sau Edge instalat (ori `CHROME_PATH`). Cu `--png-dir`, redă și paginile în PNG pentru verificare dacă este disponibil `pypdfium2`.

Folosiți HTML static cu imagini locale sau încorporate. HTML-ul activ și sursele de imagini din rețea sunt respinse; legăturile către surse rămân accesibile. Dacă randarea eșuează, PDF-ul existent este păstrat.

## Arbore genealogic în GEDCOM

[GEDCOM](https://gedcom.io/specs/) este un format standard de schimb al datelor genealogice (`.ged`). La cererea de a construi sau exporta un arbore, agentul creează un fișier local cu surse și note privind susținerea prin dovezi. Pentru compatibilitate, folosește implicit GEDCOM 5.5.1 în UTF-8; dacă utilizatorul indică o altă versiune acceptată, de exemplu GEDCOM 7, o folosește pe aceea.

Un arbore existent este material inițial și oferă indicii de cercetare, nu dovada rudeniei. Originalul este păstrat; fișierul utilizatorului nu este suprascris. Informațiile neconfirmate, contradicțiile și incertitudinile rămân în dosar. Registrele de dovezi și jurnalul de căutare rămân baza concluziilor. Regulile de import și export sunt în [references/gedcom.md](references/gedcom.md).

Utilizatorul alege programul pentru arbore. Instalarea aplicațiilor, configurarea MCP și sincronizarea automată cu un arbore extern nu fac parte din domeniul acestei abilități.

## Structura depozitului

```
SKILL.md                         instrucțiuni principale (flux, reguli obligatorii, politica lingvistică)
references/
  source-strategy.md             ierarhia surselor, modele de interogări, cataloage, cereri de arhivă
  correspondence.md              destinatari, integrare e-mail, trimiteri autorizate și răspunsuri
  government-portals.md          servicii de stare civilă și modalități de livrare
  evidence-protocol.md           evaluarea artefactelor, stări, identificarea persoanelor, conflicte
  ex-ussr-locale-guide.md        jurisdicții, variante de nume, calendare, tipuri de documente pe perioade
  browser-and-captcha.md         navigare, autentificare, o încercare CAPTCHA și predare către utilizator, limite de frecvență
  privacy-and-safety.md          persoane în viață, minori, ADN, descoperiri sensibile
  seed-sources.md                resurse inițiale selectate, cu clase de fiabilitate
  field-lessons.md               lecții practice dintr-un caz real
  changelog.md                   istoricul versiunilor
  photo-search.md                căutarea, identificarea, datarea și stocarea fotografiilor
  habsburg-galicia-bukovina.md   Galiția și Bucovina în perioada habsburgică și ulterior
  chechnya-deportation.md        familii cecene: deportarea din 1944, colonii speciale, nume și sate redenumite
  germany-forced-labour.md       muncitori forțați în Germania 1941–1945: Arolsen Archives și registre civile germane

  bessarabia-moldova.md          Basarabia, Moldova, RASSM și zona de frontieră a Nistrului
  familysearch-indexes.md       cercetare țintită în browser, copii locale permise și acoperire
  familysearch-mcp.md           instrumente conectate, citiri structurate, scrieri delimitate și verificare
  ww1-search.md                 căutări GWAR după persoană/localitate și localizarea imaginilor-sursă
  gedcom.md                     schimb de arbori în GEDCOM, surse și susținerea prin dovezi
assets/                          preluarea cazului, registre CSV, șablon de raport final,
                                 șablon README pentru fotografii, stare de cercetare, PDF lizibil (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py și module comune de analiză locală
evals/discovery-and-logic.yaml   cazuri de testare pentru declanșare și raționament
tests/                           teste unitare (python3 -m unittest discover -s tests)
```

## Utilizare responsabilă

- **Istoria familiei, nu supraveghere.** Skill-ul refuză căutarea adreselor, numerelor de telefon sau conturilor actuale ale persoanelor în viață și le minimizează datele în rapoarte.
- **Verificarea accesului.** Agentul poate încerca o CAPTCHA reală o singură dată, prin controalele normale ale browserului intern, dacă este posibil și permis. Dacă este nevoie de acțiunea utilizatorului, deschide fila relevantă când poate și furnizează adresa și acțiunea necesară; autentificarea o face utilizatorul. Fără servicii externe de rezolvare, eludarea protecțiilor, a plății, a restricțiilor geografice ori de frecvență sau baze de date scurse. Consultați [ghidul pentru browser](references/browser-and-captcha.md).
- **Nu încarcă documentele sau datele ADN** în servicii terțe fără consimțământul dumneavoastră explicit.
- **Descoperirile sensibile** (deportare, represiune, adopție, surprize ADN) sunt prezentate neutru și numai în măsura necesară întrebării.
- **Corespondență autorizată.** Skill-ul poate trimite cereri instituțiilor prin instrumentele disponibile când utilizatorul le-a autorizat; nu cere din nou permisiunea pentru o trimitere deja autorizată. Simpla conectare a unei căsuțe de e-mail nu autorizează trimiteri, atașamente sau servicii plătite. Verificați datele oficiale de contact și procedura actuală; păstrați acreditările și corespondența privată în afara depozitului skill-ului.

## Contribuții

Sursele noi sunt binevenite în `references/seed-sources.md`. Înregistrați, unde sunt cunoscute și verificate, deținătorul, jurisdicția, colecția, proveniența, ID-urile, accesul, restricțiile și data verificării; marcați lipsurile în loc să ghiciți. Nu includeți date personale în exemple.

Instrumentele de căutare folosesc biblioteca standard Python și registrele existente ale cazului. Rulați `python3 -m unittest discover -s tests` pentru verificarea parsării locale, a punctelor de reluare GWAR, erorilor de acces, acoperirii neclarificate și înregistrării dovezilor pe date sintetice. Descoperirea și consultarea țintită FamilySearch folosesc sesiunea legală de browser existentă; instrumentele Python analizează fragmentele salvate. Păstrați fișierele private de cercetare în afara acestei copii Git.

## Licență

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Întreținut de Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
