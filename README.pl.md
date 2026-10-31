# ex-USSR Kinship Research

![Okładka ex-USSR Kinship Research](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Umiejętność genealogiczna dla agentów AI (Codex, Claude Code i innych środowisk Agent Skills), która stawia dowody na pierwszym miejscu.** Zamienia agenta w uważnego badacza historii rodzinnej na terenach byłego ZSRR, Związku Radzieckiego i Imperium Rosyjskiego. Agent czyta księgi kościelne i akta stanu cywilnego, dokumentację wojskową, deportacyjną i represyjną oraz nieindeksowane skany archiwalne. Zachowuje pochodzenie każdego znaleziska, oddziela zapisy od interpretacji i jasno mówi, co zostało udowodnione, a co nie.

Zakres obejmuje wszystkie 15 byłych republik radzieckich: Rosję, Ukrainę, Białoruś, Mołdawię, Estonię, Łotwę, Litwę, Gruzję, Armenię, Azerbejdżan, Kazachstan, Kirgistan, Tadżykistan, Turkmenistan i Uzbekistan. Archiwa dobierane są według historycznej jurysdykcji zdarzenia i obecnego dysponenta dokumentów; przykład regionalny nie zastępuje badań lokalnych.

Instrukcje umiejętności napisano po rosyjsku, ale **agent rozmawia z Tobą w Twoim języku**: po angielsku, ukraińsku, rosyjsku, polsku, niemiecku itd. Cytuje źródła w oryginalnej pisowni wraz z tłumaczeniem i tworzy zapytania w językach dokumentów.

---

## Co potrafi

- **Przyjęcie materiałów i określenie zakresu.** Jedno pytanie badawcze, znane fakty, osoby, które mogą żyć, i granice poszukiwań.
- **Odtwarzalne rejestry.** Osoby, artefakty, twierdzenia, relacje i pełny dziennik wyszukiwania (CSV), a także szablon raportu końcowego.
- **Model historycznych jurysdykcji.** Każde zdarzenie przypisuje do państwa, guberni, powiatu, parafii lub urzędu stanu cywilnego *na dzień zdarzenia*, a nie według dzisiejszej mapy.
- **Macierze wariantów imion i nazwisk.** Rosyjskie formy sprzed reformy pisowni, formy ukraińskie, polskie, rumuńskie, niemieckie i jidysz, patronimika, nazwiska panieńskie i transliteracje.
- **Strategia źródeł.** Najpierw oryginały, potem oficjalne katalogi, indeksy, opublikowane zbiory dokumentów, a dopiero na końcu drzewa i fora jako wskazówki.
- **Protokół dowodowy.** Twierdzenia otrzymują zrozumiałe statusy zamiast procentów: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Kopie i lustrzane wersje jednego zapisu mają wspólną `independence_group`, więc nigdy nie liczą się jako niezależne dowody.
- **Ustalanie tożsamości.** Osoby o tych samych imionach i nazwiskach zachowują osobne `person_id`, dopóki nie pojawi się dowód rozróżniający: numer domu, rodzice, chrzestni, dokładna data urodzenia lub jednostka wojskowa.
- **Skrypt audytu.** Sprawdza integralność odwołań i sygnalizuje słabe potwierdzenie przed napisaniem wniosków. Grupa niezależności liczy się tylko wtedy, gdy należy do niej cytowany artefakt, więc samo zadeklarowanie statusu nie tworzy potwierdzenia. Sprawdza również raport końcowy: każdy cytowany ID musi istnieć w rejestrach, a każdy status musi być z nimi zgodny. Podsumowanie pokazuje, co nadal nie ma potwierdzenia lub jest oznaczone jako nieczytelne.
- **Zapytania do instytucji.** Przygotowuje i, po uzyskaniu upoważnienia, wysyła precyzyjne zapytania do archiwów, bibliotek, uniwersytetów i muzeów przez dostępną pocztę lub oficjalne narzędzia internetowe. W razie potrzeby proponuje obsługiwaną integrację pocztową lub gotowy list. Zapisuje wynik, unika ponownego wysyłania i traktuje odpowiedzi jako materiał dowodowy. Zobacz [wskazówki dotyczące korespondencji](references/correspondence.md).
- **Usługi publiczne.** Wybiera oficjalną drogę zamówienia dokumentów stanu cywilnego lub archiwalnych, sprawdzając uprawnienia i sposób dostarczenia wyniku ([portale administracji](references/government-portals.md)).
- **Raport końcowy.** Każdą relację rodzinną przedstawia ogniwo po ogniwie, ze sprzecznościami, bezskutecznymi poszukiwaniami i konkretnymi następnymi krokami.
- **Ukierunkowane badanie indeksowanych zapisów.** Znajduje odpowiednie księgi FamilySearch według miejsca lub DGS w istniejącej, zgodnej z zasadami sesji przeglądarki, przegląda konkretne zapisy i zachowuje wyłącznie fragmenty dowodowe dozwolone przez źródło. Lokalne narzędzia wyszukują krewnych, świadków i warianty nazwisk w zapisanych fragmentach, zachowując kontekst i sumy kontrolne plików. [Przebieg pracy i granice pokrycia](references/familysearch-indexes.md).
- **Podłączony FamilySearch MCP.** Korzysta z podłączonego serwera do uporządkowanego wyszukiwania, profili, krewnych i źródeł oraz upoważnionych zmian drzewa o jasno określonym zakresie, potwierdzanych ponownym odczytem. Oddziela wyszukiwanie indeksowane od czytania nieindeksowanych skanów i sprawdza rzeczywiste możliwości konektora dotyczące przeglądarki, prywatności i zapisu. [Przebieg pracy i ograniczenia dostępu](references/familysearch-mcp.md).
- **Wyszukiwanie źródeł z I wojny światowej.** Wyszukuje w GWAR meldunki, dokumenty szpitalne, odznaczeniowe i jenieckie według osoby lub miejscowości, porównuje pisownię nazw miejscowości na zapisanych kartach, aby odczytać zniekształconą nazwę, a następnie odnajduje obraz źródłowy. [Przebieg pracy](references/ww1-search.md). Oba narzędzia zasilają istniejący rejestr artefaktów i dziennik wyszukiwania; nie ustalają automatycznie tożsamości ani pokrewieństwa.

Historia wydań: [dziennik zmian](references/changelog.md).

<a id="install"></a>

## Instalacja

Jeśli masz zainstalowany Node.js, możesz użyć opcjonalnego [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI pozwala wybrać agenta i domyślnie instaluje umiejętność w bieżącym projekcie; dodaj `-g`, aby zainstalować ją do osobistego użytku we wszystkich projektach. Aktualne wymagania dotyczące Node.js znajdziesz w jego dokumentacji.

Możesz też sklonować repozytorium bezpośrednio do folderu umiejętności swojego agenta:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (umiejętności osobiste)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Dla pojedynczego projektu umieść folder w `.claude/skills/` wewnątrz repozytorium. Skrypty potrzebują tylko Pythona 3 i biblioteki standardowej; `build_pdf.py` wymaga również przeglądarki opartej na Chromium.

## Użycie

Opisz pytanie dotyczące rodziny. Agent pracuje na dostępnych informacjach i kontynuuje badania, gdy pytania lub prośby o dostęp czekają na odpowiedź. Na przykład:

- *„Mojego pradziadka zesłano do Kazachstanu w latach 30. XX wieku. Pomóż znaleźć jego rodziców w księgach kościelnych”.*
- *„Oto skany aktu małżeństwa i karty żołnierza. Sprawdź, czy dotyczą tej samej osoby, i zbuduj łańcuch dowodowy”.*
- *„Znajdź parafię i właściwy mikrofilm FamilySearch dla wsi na Podolu w latach 90. XIX wieku i odczytaj urodzenia dla nazwiska X”.*

Prywatne dane sprawy przechowuj poza kopią Git umiejętności. Z folderu umiejętności:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 każdego zapisanego artefaktu
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # sprawdzenie rejestrów przed raportem końcowym
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` odmawia utworzenia sprawy wewnątrz folderu umiejętności, również z
`--force`. Git ignoruje popularne dawne nazwy folderów spraw jako dodatkowe zabezpieczenie;
przed przekazaniem zmian sprawdź pliki w indeksie, szczególnie przy przenoszeniu istniejącej sprawy.

`build_pdf.py` wymaga zainstalowanego Chrome, Chromium lub Edge (albo `CHROME_PATH`). Opcja `--png-dir` dodatkowo renderuje strony do PNG na potrzeby przeglądu, jeśli dostępny jest `pypdfium2`.

Używaj statycznego HTML z lokalnymi lub osadzonymi obrazami. Aktywny HTML i sieciowe źródła obrazów są odrzucane; odnośniki do źródeł pozostają klikalne. Nieudane renderowanie zachowuje istniejący wynikowy PDF.

## Drzewo rodzinne w GEDCOM

[GEDCOM](https://gedcom.io/specs/) to standardowy format wymiany danych genealogicznych (`.ged`). Na prośbę o zbudowanie lub wyeksportowanie drzewa agent tworzy lokalny plik ze źródłami i uwagami o sile dowodów. Domyślnie używa GEDCOM 5.5.1 w UTF-8 dla zgodności; jeśli użytkownik wskaże inną obsługiwaną wersję, na przykład GEDCOM 7, używa jej.

Istniejące drzewo jest materiałem wyjściowym i zbiorem wskazówek, a nie dowodem pokrewieństwa. Oryginał zostaje zachowany; plik użytkownika nie jest nadpisywany. Niepotwierdzone informacje, sprzeczności i niepewność pozostają w sprawie. Rejestry dowodów i dziennik poszukiwań pozostają podstawą wniosków. Zasady importu i eksportu opisano w [references/gedcom.md](references/gedcom.md).

Program do drzewa wybiera użytkownik. Instalacja aplikacji, konfiguracja MCP i automatyczna synchronizacja z zewnętrznym drzewem wykraczają poza zakres umiejętności.

## Układ repozytorium

```
SKILL.md                         główne instrukcje (przebieg pracy, twarde zasady, polityka językowa)
references/
  source-strategy.md             hierarchia źródeł, zapytania, katalogi, wnioski archiwalne
  correspondence.md              odbiorcy, integracja pocztowa, upoważnione wysyłki i odpowiedzi
  government-portals.md          usługi stanu cywilnego i sposoby dostarczania wyników
  evidence-protocol.md           ocena artefaktów, statusy, tożsamość, konflikty
  ex-ussr-locale-guide.md        jurysdykcje, warianty nazwisk, kalendarze, typy zapisów według okresów
  browser-and-captcha.md         przeglądarka, logowanie, jedna próba CAPTCHA i przekazanie użytkownikowi, limity
  privacy-and-safety.md          osoby żyjące, małoletni, DNA, wrażliwe odkrycia
  seed-sources.md                wybrane źródła początkowe z klasami wiarygodności
  field-lessons.md               praktyczne wnioski z rzeczywistej sprawy
  changelog.md                   historia wydań
  photo-search.md                znajdowanie, identyfikacja, datowanie i przechowywanie zdjęć
  habsburg-galicia-bukovina.md   Galicja i Bukowina za Habsburgów i później
  chechnya-deportation.md        rodziny czeczeńskie: deportacja w 1944 r., osiedla specjalne, imiona i przemianowane wsie
  germany-forced-labour.md       robotnicy przymusowi w Niemczech 1941–1945: Arolsen Archives i niemieckie rejestry stanu cywilnego

  bessarabia-moldova.md          Besarabia, Mołdawia, Mołdawska ASRR i pogranicze Dniestru
  familysearch-indexes.md       ukierunkowane badanie w przeglądarce, dozwolone lokalne kopie i pokrycie
  familysearch-mcp.md           podłączone narzędzia, odczyt strukturalny, zapis o określonym zakresie i weryfikacja
  ww1-search.md                 wyszukiwanie GWAR według osoby/miejscowości i lokalizatory obrazów źródłowych
  gedcom.md                     wymiana drzew w GEDCOM, źródła i siła dowodów
assets/                          przyjęcie materiałów, rejestry CSV, szablon raportu końcowego,
                                 szablon README zdjęć, stanu badań i czytelnego PDF (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py i wspólne lokalne moduły analizy
evals/discovery-and-logic.yaml   scenariusze testowe aktywacji i rozumowania
tests/                           testy jednostkowe (python3 -m unittest discover -s tests)
```

## Odpowiedzialne korzystanie

- **Historia rodzinna, nie inwigilacja.** Umiejętność odmawia wyszukiwania aktualnych adresów, telefonów lub kont osób żyjących i minimalizuje ich dane w raportach.
- **Sprawdzanie dostępu.** Agent może raz spróbować rozwiązać rzeczywistą CAPTCHA zwykłymi narzędziami swojej wewnętrznej przeglądarki, jeśli jest to obsługiwane i dozwolone. Gdy potrzebne jest działanie użytkownika, w miarę możliwości otwiera odpowiednią kartę oraz podaje URL i wymagane działanie; loguje się użytkownik. Bez zewnętrznych usług rozwiązywania i baz z wycieków; bez obchodzenia zabezpieczeń, płatnych ograniczeń dostępu, blokad geograficznych lub limitów zapytań. Zobacz [wskazówki dotyczące przeglądarki](references/browser-and-captcha.md).
- **Bez przesyłania Twoich dokumentów ani danych DNA** do usług zewnętrznych bez Twojej wyraźnej zgody.
- **Wrażliwe odkrycia** (deportacja, represje, adopcja, niespodziewane wyniki DNA) są przedstawiane neutralnie i tylko w zakresie potrzebnym do odpowiedzi na pytanie.
- **Upoważniona korespondencja.** Umiejętność może wysyłać zapytania do instytucji dostępnymi narzędziami, gdy użytkownik upoważnił ją do wysyłki; nie pyta ponownie o już udzielone upoważnienie. Samo podłączenie skrzynki nie upoważnia do wysyłania, załączników ani płatnych usług. Sprawdź aktualny oficjalny kontakt i procedurę, a dane uwierzytelniające i prywatną korespondencję dotyczącą sprawy przechowuj poza repozytorium umiejętności.

## Współtworzenie

Nowe źródła są mile widziane w `references/seed-sources.md`. Zapisz zweryfikowanego właściciela, jurysdykcję, kolekcję, pochodzenie, identyfikatory, dostęp, ograniczenia i datę sprawdzenia, jeśli są znane; zaznaczaj braki zamiast zgadywać. Nie umieszczaj danych osobowych w przykładach.

Narzędzia wyszukiwania źródeł używają standardowej biblioteki Pythona i istniejących rejestrów sprawy. Uruchom `python3 -m unittest discover -s tests`, aby sprawdzić lokalne parsowanie, punkty kontrolne GWAR, błędy dostępu, nieustalone pokrycie i rejestrowanie dowodów na danych syntetycznych. Wyszukiwanie i ukierunkowany podgląd FamilySearch korzystają z istniejącej, zgodnej z zasadami sesji przeglądarki; narzędzia Pythona analizują zapisane fragmenty. Prywatne pliki badawcze przechowuj poza tą kopią repozytorium.

## Licencja

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Projekt utrzymuje Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
