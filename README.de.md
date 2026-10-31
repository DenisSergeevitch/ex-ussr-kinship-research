# ex-USSR Kinship Research

![Titelbild von ex-USSR Kinship Research](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Eine genealogische Fähigkeit für KI-Agenten (Codex, Claude Code und andere Agent-Skills-Laufzeitumgebungen), bei der Belege an erster Stelle stehen.** Sie macht einen Agenten zum sorgfältigen Erforscher der Familiengeschichte in der ehemaligen UdSSR, der Sowjetunion und dem Russischen Reich. Der Agent liest Kirchenbücher und Personenstandsregister, Militär-, Deportations- und Repressionsakten sowie nicht indexierte Archivscans. Er hält die Herkunft jedes Fundes nachvollziehbar fest, trennt Aufzeichnungen von ihrer Deutung und sagt klar, was bewiesen ist und was nicht.

Der Umfang schließt alle 15 ehemaligen Sowjetrepubliken ein: Russland, die Ukraine, Belarus, Moldau, Estland, Lettland, Litauen, Georgien, Armenien, Aserbaidschan, Kasachstan, Kirgisistan, Tadschikistan, Turkmenistan und Usbekistan. Archive werden nach der historischen Zuständigkeit des Ereignisses und der heutigen verwahrenden Stelle ausgewählt; ein regionales Beispiel ersetzt keine örtliche Recherche.

Die Anweisungen der Fähigkeit sind auf Russisch verfasst, aber **der Agent spricht mit Ihnen in Ihrer Sprache**: Englisch, Ukrainisch, Russisch, Polnisch, Deutsch und so weiter. Er zitiert Quellen in ihrer ursprünglichen Schreibweise mit Übersetzung und formuliert Suchanfragen in den Sprachen der Unterlagen.

---

## Was sie leistet

- **Aufnahme und Abgrenzung des Falls.** Eine Forschungsfrage, bekannte Fakten, möglicherweise noch lebende Personen und die Grenzen der Recherche.
- **Reproduzierbare Register.** Personen, Artefakte, Aussagen, Beziehungen und ein vollständiges Suchprotokoll (CSV) sowie eine Vorlage für den Abschlussbericht.
- **Modell historischer Zuständigkeiten.** Jedes Ereignis wird dem Staat, der Provinz, dem Bezirk, der Pfarrei oder dem Standesamt *zum Zeitpunkt des Ereignisses* zugeordnet, nicht nach der heutigen Landkarte.
- **Matrizen mit Namensvarianten.** Russische Formen vor der Rechtschreibreform, ukrainische, polnische, rumänische, deutsche und jiddische Formen, Vatersnamen, Geburtsnamen und Transliteration.
- **Quellenstrategie.** Zuerst Originale, dann amtliche Kataloge, Indizes und veröffentlichte Dokumentensammlungen; Stammbäume und Foren dienen erst danach als Hinweise.
- **Belegprotokoll.** Aussagen erhalten erklärbare Statuswerte statt Prozentangaben: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Kopien und Spiegelungen desselben Eintrags teilen sich eine `independence_group` und zählen deshalb niemals als unabhängige Belege.
- **Identitätsklärung.** Namensgleiche Personen behalten getrennte `person_id`s, bis unterscheidende Belege vorliegen: Hausnummer, Eltern, Taufpaten, genaues Geburtsdatum oder militärische Einheit.
- **Prüfskript.** Es prüft die referenzielle Integrität und weist vor dem Verfassen von Schlussfolgerungen auf schwache Bestätigung hin. Eine Unabhängigkeitsgruppe zählt nur, wenn ein zitiertes Artefakt zu ihr gehört; eine Bestätigung lässt sich also nicht durch bloße Statusvergabe erzeugen. Auch der Abschlussbericht wird geprüft: Jede zitierte ID muss in den Registern existieren und jeder Status mit ihnen übereinstimmen. Eine Übersicht zeigt, was noch unbestätigt oder als unleserlich markiert ist.
- **Anfragen an Einrichtungen.** Es entwirft gezielte Anfragen an Archive, Bibliotheken, Universitäten und Museen und versendet sie bei entsprechender Autorisierung über verfügbare E-Mail- oder offizielle Webwerkzeuge. Bei Bedarf bietet es eine unterstützte E-Mail-Integration oder einen versandfertigen Brief an. Es hält das Ergebnis fest, vermeidet doppelte Sendungen und behandelt Antworten als Belege. Siehe die [Hinweise zur Korrespondenz](references/correspondence.md).
- **Behördliche Dienste.** Es wählt einen offiziellen Weg für Personenstands- oder Archivanfragen und prüft die Berechtigung sowie die Zustellung des Ergebnisses ([Behördenportale](references/government-portals.md)).
- **Abschlussbericht.** Jede Verwandtschaftsbeziehung wird Glied für Glied dargestellt, mit Widersprüchen, erfolglosen Suchen und konkreten nächsten Schritten.
- **Gezielte Recherche in indexierten Aufzeichnungen.** Es findet passende FamilySearch-Bücher nach Ort oder DGS über eine bestehende rechtmäßige Browsersitzung, sieht bestimmte Einträge ein und bewahrt nur die von der Quelle erlaubten Belegfragmente auf. Lokale Hilfsprogramme suchen Verwandte, Zeugen und Namensvarianten in gespeicherten Fragmenten und erhalten dabei deren Kontext und Dateiprüfsummen. [Arbeitsablauf und Grenzen der Abdeckung](references/familysearch-indexes.md).
- **Verbundenes FamilySearch MCP.** Ein verbundener Server wird für strukturierte Suchen, Profile, Verwandte und Quellen sowie autorisierte Änderungen am Stammbaum mit ausdrücklich festgelegtem Umfang und anschließender Kontrolle durch erneutes Lesen verwendet. Indexsuche und das Lesen nicht indexierter Scans bleiben getrennt; die tatsächlichen Browser-, Datenschutz- und Schreibmöglichkeiten des Konnektors werden geprüft. [Arbeitsablauf und Zugriffsgrenzen](references/familysearch-mcp.md).
- **Quellensuche zum Ersten Weltkrieg.** Es durchsucht GWAR-Meldungen, Lazarett-, Auszeichnungs- und Kriegsgefangenenunterlagen nach Person oder Ort, vergleicht Ortsnamenschreibungen auf gespeicherten Karten, um einen entstellten Ortsnamen zu entziffern, und ermittelt anschließend das Quellenbild. [Arbeitsablauf](references/ww1-search.md). Beide Hilfsprogramme speisen das bestehende Artefaktregister und Suchprotokoll; sie stellen Identität oder Verwandtschaft nicht automatisch fest.

Versionsgeschichte: [Änderungsprotokoll](references/changelog.md).

<a id="install"></a>

## Installation

Wenn Node.js installiert ist, können Sie die optionale [Skills CLI](https://github.com/vercel-labs/skills) verwenden:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

Mit der CLI wählen Sie Ihren Agenten aus; standardmäßig installiert sie die Fähigkeit im aktuellen Projekt. Fügen Sie `-g` für eine persönliche, projektübergreifende Installation hinzu. Die aktuellen Node.js-Anforderungen finden Sie in ihrer Dokumentation.

Alternativ klonen Sie das Repository direkt in den Skills-Ordner Ihres Agenten:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (persönliche Fähigkeiten)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Für ein einzelnes Projekt legen Sie den Ordner innerhalb des Repositorys unter `.claude/skills/` ab. Die Skripte benötigen nur Python 3 und die Standardbibliothek; `build_pdf.py` braucht zusätzlich einen Chromium-basierten Browser.

## Verwendung

Beschreiben Sie die Familienfrage. Der Agent arbeitet mit den verfügbaren Informationen und forscht weiter, während Fragen oder Zugriffsanfragen auf eine Antwort warten. Zum Beispiel:

- *„Mein Urgroßvater wurde in den 1930er-Jahren nach Kasachstan verbannt. Hilf mir, seine Eltern in Kirchenbüchern zu finden.“*
- *„Hier sind Scans einer Heiratsurkunde und einer Soldatenkarte. Prüfe, ob sie dieselbe Person betreffen, und baue die Belegkette auf.“*
- *„Finde die Pfarrei und den richtigen FamilySearch-Film für ein Dorf in Podolien in den 1890er-Jahren und lies die Geburtseinträge zum Nachnamen X.“*

Bewahren Sie private Falldaten außerhalb der Git-Arbeitskopie der Fähigkeit auf. Aus dem Skills-Ordner:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 für jedes gespeicherte Artefakt
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # Register vor dem Abschlussbericht prüfen
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` verweigert das Anlegen eines Falls innerhalb des Skills-Ordners, auch mit
`--force`. Git ignoriert häufige ältere Namen von Fallordnern als zusätzliche Absicherung;
prüfen Sie vor einem Beitrag die zum Commit vorgemerkten Dateien, besonders beim Verschieben eines bestehenden Falls.

`build_pdf.py` benötigt ein installiertes Chrome, Chromium oder Edge (oder `CHROME_PATH`). Mit `--png-dir` rendert es zusätzlich Seiten als PNG zur Kontrolle, sofern `pypdfium2` verfügbar ist.

Verwenden Sie statisches HTML mit lokalen oder eingebetteten Bildern. Aktives HTML und Bildquellen aus dem Netz werden abgewiesen; Quellenverweise bleiben anklickbar. Bei fehlgeschlagener Ausgabe bleibt eine vorhandene Ausgabe-PDF erhalten.

## Stammbaum in GEDCOM

[GEDCOM](https://gedcom.io/specs/) ist ein Standardformat zum Austausch genealogischer Daten (`.ged`). Auf Wunsch, einen Stammbaum zu erstellen oder zu exportieren, erzeugt der Agent eine lokale Datei mit Quellen und Anmerkungen zur Beleglage. Für die Kompatibilität verwendet er standardmäßig GEDCOM 5.5.1 in UTF-8; nennt der Nutzer eine andere unterstützte Version, etwa GEDCOM 7, verwendet er diese.

Ein vorhandener Stammbaum ist Ausgangsmaterial und liefert Recherchehinweise; er beweist keine Verwandtschaft. Das Original bleibt erhalten, die Datei des Nutzers wird nicht überschrieben. Unbelegte Angaben, Widersprüche und Unsicherheiten bleiben im Fall dokumentiert. Die Belegregister und das Suchprotokoll bleiben die Grundlage der Schlussfolgerungen. Die Regeln für Import und Export stehen in [references/gedcom.md](references/gedcom.md).

Die Stammbaumsoftware wählt der Nutzer. Die Installation von Anwendungen, die MCP-Einrichtung und die automatische Synchronisierung mit einem externen Stammbaum liegen außerhalb des Umfangs dieser Fähigkeit.

## Aufbau des Repositorys

```
SKILL.md                         Hauptanweisungen (Arbeitsablauf, verbindliche Regeln, Sprachrichtlinie)
references/
  source-strategy.md             Quellenhierarchie, Suchmuster, Kataloge, Archivanfragen
  correspondence.md              Empfänger, E-Mail-Integration, autorisiertes Senden und Antworten
  government-portals.md          Personenstandsdienste und Zustellwege
  evidence-protocol.md           Artefaktbewertung, Statuswerte, Identitätsklärung, Konflikte
  ex-ussr-locale-guide.md        Zuständigkeiten, Namensvarianten, Kalender, Aufzeichnungstypen nach Zeitraum
  browser-and-captcha.md         Browser, Anmeldung, ein CAPTCHA-Versuch und Übergabe, Zugriffslimits
  privacy-and-safety.md          lebende Personen, Minderjährige, DNA, sensible Erkenntnisse
  seed-sources.md                ausgewählte Ausgangsquellen mit Verlässlichkeitsklassen
  field-lessons.md               praktische Erkenntnisse aus einem realen Fall
  changelog.md                   Versionsgeschichte
  photo-search.md                Fotos finden, identifizieren, datieren und aufbewahren
  habsburg-galicia-bukovina.md   Galizien und Bukowina unter den Habsburgern und danach
  chechnya-deportation.md        tschetschenische Familien: Deportation 1944, Sondersiedlungen, Namen und umbenannte Dörfer
  germany-forced-labour.md       Zwangsarbeiter in Deutschland 1941–1945: Arolsen Archives und deutsche Personenstandsregister

  bessarabia-moldova.md          Bessarabien, Moldau, Moldauische ASSR und Dnister-Grenzgebiet
  familysearch-indexes.md       gezielte Browserrecherche, erlaubte lokale Kopien und Abdeckung
  familysearch-mcp.md           verbundene Werkzeuge, strukturierte Lesezugriffe, begrenztes Schreiben und Kontrolle
  ww1-search.md                 GWAR-Personen-/Ortssuche und Fundstellen der Quellenbilder
  gedcom.md                     Stammbaumaustausch in GEDCOM, Quellen und Beleglage
assets/                          Fallaufnahme, CSV-Register, Abschlussberichtsvorlage,
                                 Foto-README-Vorlage, Forschungsstandsvorlage, lesbare PDF-Vorlage (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py und gemeinsame lokale Analysemodule
evals/discovery-and-logic.yaml   Testfälle für Aktivierung und Schlussfolgerungen
tests/                           Unit-Tests (python3 -m unittest discover -s tests)
```

## Verantwortungsvoller Einsatz

- **Familiengeschichte, keine Überwachung.** Die Fähigkeit verweigert die Suche nach aktuellen Adressen, Telefonnummern oder Konten lebender Personen und beschränkt deren Daten in Berichten auf das Nötigste.
- **Zugriffsprüfungen.** Der Agent darf eine tatsächliche CAPTCHA einmal mit den normalen Bedienelementen seines internen Browsers versuchen, sofern unterstützt und erlaubt. Wenn der Nutzer handeln muss, öffnet er nach Möglichkeit den passenden Tab und nennt die URL sowie den nötigen Schritt; Anmeldungen übernimmt der Nutzer. Keine externen Lösungsdienste, kein Umgehen von Schutzmaßnahmen, Bezahlschranken, Geosperren oder Anfragelimits und keine geleakten Datenbanken. Siehe die [Browserhinweise](references/browser-and-captcha.md).
- **Kein Hochladen Ihrer Dokumente oder DNA-Daten** bei Drittdiensten ohne Ihre ausdrückliche Zustimmung.
- **Sensible Erkenntnisse** (Deportation, Repression, Adoption, überraschende DNA-Ergebnisse) werden neutral und nur so weit mitgeteilt, wie es die Frage erfordert.
- **Autorisierte Korrespondenz.** Die Fähigkeit kann über verfügbare Werkzeuge Anfragen an Einrichtungen versenden, wenn der Nutzer dies autorisiert hat; eine bereits autorisierte Sendung wird nicht erneut abgefragt. Allein die Verbindung eines Postfachs autorisiert weder Sendungen noch Anhänge oder kostenpflichtige Dienste. Prüfen Sie die aktuellen offiziellen Kontaktdaten und Verfahren und bewahren Sie Zugangsdaten sowie private Fallkorrespondenz außerhalb des Skills-Repositorys auf.

## Mitwirken

Neue Quellen sind in `references/seed-sources.md` willkommen. Halten Sie den überprüften Betreiber, die Zuständigkeit, Sammlung, Herkunft, IDs, Zugang, Einschränkungen und das Prüfdatum fest, soweit bekannt; kennzeichnen Sie Lücken, statt zu raten. Verwenden Sie keine personenbezogenen Daten in Beispielen.

Die Hilfsprogramme zur Quellensuche verwenden die Python-Standardbibliothek und die bestehenden Fallregister. Führen Sie `python3 -m unittest discover -s tests` aus, um lokales Parsing, GWAR-Fortsetzungspunkte, Zugriffsfehler, ungeklärte Abdeckung und Belegregistrierung anhand synthetischer Daten zu prüfen. FamilySearch-Recherche und gezieltes Einsehen nutzen die bestehende rechtmäßige Browsersitzung; die Python-Hilfsprogramme analysieren gespeicherte Fragmente. Bewahren Sie private Forschungsdateien außerhalb dieser Arbeitskopie auf.

## Lizenz

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Betreut von Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
