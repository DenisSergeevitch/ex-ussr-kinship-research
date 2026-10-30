# Release history

## 1.26.0 — 2026-10-29

- Add two qualified holdings-discovery catalogs for the 1897 census and distinguish them from published statistics and personal records. Separate Soviet census guidance, verify catalog leads against archival inventories, and retain uncertainty when an inventory is unavailable or a locality is absent from a catalog. Add an attributed RGIA inventory 11 route for settlement and population summaries without assuming that names are present ([#87](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/87)).

## 1.25.0 — 2026-10-29

- Refine Perm and Bashkortostan source navigation with attributed contributor observations, correct the Basharchive project attribution, and distinguish routing diagnostics from demonstrated geographic restrictions. Explain restoring an allowed direct connection through the user's existing client without relying on another site's IP display ([#78](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/78), [#79](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/79)).
- Clarify the evidence needed to assign a distant DNA match to a parental side; a sibling's non-match or absent X segment alone does not establish that side. Keep unproven surname links as hypotheses without requiring one particular evidence route ([#80](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/80)).
- Add an optional local column-strip montage helper for reviewing saved scan series with Pillow. Preserve source images and existing output, reject ambiguous frame numbers and empty crops, and verify candidates against full records; retain existing image tools as alternatives ([#81](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/81)).
- Refine requests for unnamed children and revision-list coverage split by estate, institution or owner. Add an editable anonymized CANO request specimen, with archive-specific requirements checked through the existing correspondence workflow ([#82](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/82), [#83](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/83)).
- Add the FNP probate index as a qualified death-record lead, distinguishing notarial districts from established residence, exact-name behavior from broader matching, and contributor observations from verified form guidance ([#84](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/84)).
- Add Soviet maternal-award records as a route to family information, with original regulations and an archive finding aid; distinguish qualifying children from complete family composition or biological relationships ([#85](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/85)).

## 1.24.0 — 2026-10-29

- Add Rootera as a qualified 1897 census index route and explain how to handle reported placeholders in locked fields. Keep the support explanation attributed and dated, leave closed fields unknown, verify accessible data against archival originals, and correct earlier interpretations without losing the observation history. Distinguish published Latgale coverage from complete coverage of Latvia ([#76](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/76)).

## 1.23.0 — 2026-10-29

- Add adaptable institutional request scenarios for event records, known files, household records, additional civil-register details and departmental files. Reuse existing authorization, access and negative-result guidance without requiring exhaustive searches before a useful request. Plan child-to-parent record searches from established facts, account for varying household-record fields, and distinguish migration petitions from completed moves ([#74](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/74)).

## 1.22.0 — 2026-10-29

- Adopt an editorial HTML report design after comparing three alternatives. Put an evidence-qualified family tree in the header, link relationships to their supporting records, and adapt it to the known family without inventing relatives. Improve reading hierarchy, keyboard navigation, small-screen tables and print layout; keep evidence-label explanations in print. Use multilingual system-font fallbacks and preserve original alphabets without remote font downloads. Keep photos and thematic sections optional and PDF export explicit.

## 1.21.0 — 2026-10-29

- Make a complete HTML report the default final deliverable; generate PDF only when the user explicitly requests it, reusing the HTML. A report for relatives does not imply PDF. Reuse the existing report template under its format-neutral name, add a screen layout, clarify the audit script's Markdown scope, and keep useful partial results independent of PDF tooling. Add a reasoning scenario for the default HTML report and retain explicit PDF-request coverage.

## 1.20.0 — 2026-10-29

- Replace the app-specific family-tree integration with portable local GEDCOM exports, using 5.5.1 UTF-8 by default or the version required by the user or chosen software. Preserve source citations, evidence status, original files and the existing case registers; leave application choice, MCP setup and automatic external-tree synchronization outside the skill. Replace the integration scenarios with focused GEDCOM cases and retain the canonical tree-import guidance.
- Update the English README and all 17 translations for the GEDCOM workflow, and remove the translation-status and monthly-maintenance notices from localized READMEs.

## 1.19.0 — 2026-10-28

- Add a language bar below the README cover and complete README translations in Russian, Belarusian, Kazakh, Ukrainian, Polish, German, Romanian, Estonian, Latvian, Lithuanian, Georgian, Armenian, Azerbaijani, Kyrgyz, Tajik, Turkmen and Uzbek. Keep installation commands and reference links usable in every language; label translations as monthly maintainer-reviewed snapshots.

## 1.18.0 — 2026-10-28

- Add a focused forced-labour and displaced-person research route through Arolsen, German civil registers and local and Soviet records. Link current official Hessen catalogue guidance, qualify contributor observations, date formats, coverage, fees and access; reuse existing name, identity, evidence and correspondence protocols without exhaustive-search or manual-only gates ([#69](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/69)).

## 1.17.0 — 2026-10-28

- Add Vyatka archive, church-periodical and regional-library discovery routes; distinguish independent access checks from contributor observations and retain per-file provenance, rights and coverage limits. Check directory sections and index coverage before drawing negative conclusions about employment ([#67](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/67)).

- Distinguish completed accessible checks from routes awaiting user action in research conclusions; reuse the existing access hand-off guidance and record actual blockers without inferring a need to install certificates from a TLS error. Add a focused reasoning scenario ([#68](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/68)).

## 1.16.0 — 2026-10-28

- Add focused DNA-evidence guidance for platform copies, related matches, measured observations versus inferred ancestry, segment and ethnicity-estimate limits, and private task-authorized account work. Reuse claim-level independence, existing statuses, artifact categories and privacy/correspondence rules; qualify locality and endogamy clues and cite the provider's method descriptions ([#66](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/66)).

## 1.15.0 — 2026-10-28

- Report register rows with fewer CSV fields than their header before missing values are normalized, identifying the row and field counts so truncated or misaligned evidence can be corrected. Preserve explicit empty cells and unknown optional values; add a synthetic regression for a short artifact row ([#65](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/65)).

## 1.14.0 — 2026-10-28

- Use a suitable connected FamilySearch MCP for structured reads and task-authorized tree changes; preserve the selected destination, actual filters and scope, evidence provenance, privacy and read-back after ambiguous writes. Keep browser research available and avoid requiring a particular server or browser-session extraction ([#63](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/63)).

- Add GWAR prisoner-of-war cards through `--kind pows`, include them in the default selection, preserve direct card locators and document how to resume older checkpoints. Add a synthetic CLI regression for explicit POW selection and the expanded default query ([#64](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/64)).
- Add qualified source routes for Moscow archive requests, Volga German personal books, Voronezh digital access, Moscow Oblast burial records, Odesa archival collections and German consular registers. Consolidate existing Voronezh navigation, distinguish official descriptions from contributor observations, and omit private-case details and unsupported negative coverage claims.

## 1.13.0 — 2026-10-28

- Refine targeted reading of machine-recognised metric books: choose useful pre-reform name variants, open truncated case titles, distinguish parish sections and pages without recognised text, and preserve viewer captures as screenshots. Keep full-volume reading optional and qualify contributor access observations ([#62](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/62)).
- Add the Danish Red Cross POW route at Rigsarkivet, distinguishing the approximately dated Russian-prisoner card index (1915–1918), Russian-prisoner lists (1917–1918) and German-prisoner lists (1915); record the limited surviving sample boxes and list packet. Verify document provenance, keep identity candidates separate and centralise paid-order conditions in the existing correspondence guide.
- Check historical civil-registration jurisdictions and present-day custodians when later boundary changes move village records between regional archives.
- Treat unverified search-result loading as incomplete coverage using existing statuses; an empty HTML table does not establish an absent record or a JavaScript failure.
- Keep confidence consistent between family-report summaries and the main text; adapt narrative, plans and reader checks to the task without requiring a second reader or extra deliverables. Add six reasoning scenarios for these distinctions.

## 1.12.0 — 2026-10-28

- Add official civil-registration request starting points and distinguish online filing from remote delivery; reuse existing correspondence tracking and verify each service's current conditions. Refine targeted reading of ZAGS alphabetic indexes and contextual reading of difficult scan fragments with existing image tools ([#60](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/60)).
- Expand source navigation for libraries, historic maps, repression records, Finland, Baltic and Polish collections and emigrant records; update moved addresses. Qualify contributor access observations, preserve record provenance and source dependence, and consolidate Commons discovery into the existing archival-copy guidance ([#61](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/61)).
- Use a connected Arca family tree as research material and write evaluated results with source citations and evidence marks, without repeated approval for ordinary operations. Respect the user's project and output choice, connection permissions and existing private-file rules; preserve user records and keep registers and pending work in the case folder ([#59](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/59), [#58](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/58)).

## 1.11.0 — 2026-10-28

- Preserve the original settlement, volost, uyezd and gubernia when registering new GWAR leads, retaining source snapshots and deduplication; correct the official CDIAK domain ([#55](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/55)).
- Add the third-party RGADA Search index with metadata/PDF search modes, inventory provenance and bounded negative-result guidance ([#56](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/56), [#54](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/54)).
- Add Velikiya Opisi volunteer inventories and document indexes, with result-type and coverage filters, archival verification and claim-level source dependence ([#57](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/57)).

## 1.10.0 — 2026-10-27

- Add the official DAKhMO metric-book catalog and the Ukrainian Wikisource archive directory; distinguish catalog holdings, volunteer navigation and individual scan provenance, rights and access ([#52](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/52)).

- Refine targeted WWI locality/name searches, historical place and parish checks, OBD filter diagnostics, timed archive access and request-channel guidance. Keep contributor access observations qualified, use canonical locale guidance and avoid mandatory bulk searches. Preserve GWAR report/hospital card locators and allow the three source CLIs to run in isolated Python mode ([#50](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/50)).
- Keep Cyrillic CLI output and error messages readable when Windows agents capture legacy-encoded pipes; share UTF-8 stream setup through the existing common helper and decode captured test output explicitly ([#51](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/51)).

## 1.9.0 — 2026-10-27

- Add targeted urban-directory and education-list research, qualified OCR and name-frequency clues, and flexible record routes for a child/parent name mismatch; keep private case details out of examples and record actual source-access limits ([#48](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/48)).
- Add the optional Skills CLI installation route, explaining project and personal scope while retaining direct installation ([#41](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/41)).
- Add a Bessarabia/Moldova research route with historical jurisdictions, Romanian name variants and ANA fond 211 inventory navigation; verify parish, volume structure, calendar and coverage for each document ([#43](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/43)).
- Add verified ANA certificate-request guidance and FamilySearch Moldova collection descriptions, distinguishing public catalog access from image access and contributor observations from confirmed coverage.
- Compare distorted place names against selected records of the same historical jurisdiction and contemporary settlement lists; preserve candidates and assess independence through the existing evidence protocol ([#44](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/44)).
- Add offline `gwar.py places` to group saved settlement spellings and rank possible readings without identifying places automatically. Preserve record namespaces, conflicting snapshots and input evidence; keep settlement names containing administrative-unit letter sequences.
- Choose evidence-led name and patronymic combinations when a search mode requires exact matches; keep variants as hypotheses without requiring exhaustive permutations.
- Add targeted Chechnya deportation and special-settlement research routes, name and locality clues, and current archive-request starting points; keep field observations qualified, assess copies per record, and check surviving collections before concluding that a file was lost ([#45](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/45)).
- Add the official Altai State Archive index for the 1917 agricultural and urban census, distinguish index entries from household forms and document their dependence, incomplete coverage and dated service conditions; select forms by the research question ([#46](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/46)).
- Keep long scan reading resumable with small batches, compact delegated results where available and progress within the user's existing budget ([#40](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/40)).
- Correct overgeneralizations about house numbers, name/kinship formulas, surname clusters and OBD personnel coverage; quarantine the reported unsafe former memorial domain and qualify unavailable-source observations ([#42](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/42)).

- Register manually described source leads through the existing local helper with resource-scoped snapshots, unknown provenance and optional coverage; add an optional resumable-plan template, a malformed-CSV diagnostic and a warning for found searches lacking artifact links ([#47](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/47)).

## 1.8.0 — 2026-10-27

- Add targeted discovery routes for Zhnivo, Belarus’s SODD NAF archival catalog and hryc.by, preserving source provenance, access limits and verification against original documents ([#39](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/39)).
- Refine Geneteka territory, parish, parent and pair searches, event-year and recent-index filters, and record-type coverage checks.
- Add six reasoning scenarios for Belarusian and Ukrainian source selection, participant roles, OCR context and unavailable originals.

## 1.7.0 — 2026-10-26

- Add targeted use of public funeral-agency burial catalogs to locate historical gravestones, with task-relevant private evidence, claim-based source dependence and a verified general catalog link ([#37](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/37)).
- Offer compact, prioritised next checks when useful for a progress report or hand-off, explaining their purpose, access, executor, known costs and dependencies; adapt the format to the task and use existing coordination guidance for parallel work ([#36](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/36)).
- Add targeted FamilySearch discovery guidance and local name searches across saved evidence fragments, including principal names without an optional participant list, relatives, witnesses and name variants ([#28](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/28)).
- Record observed index states and unresolved coverage, with source context and file checksums.
- Add bounded GWAR WWI person/locality searches with checkpoints, source-image locators and evidence-preserving registration; distinguish the volost field from the settlement field.
- Deduplicate unchanged source snapshots without creating persons, claims, relationships or independence assessments; keep the existing evidence protocol and case registers.

## 1.6.0 — 2026-10-26

- Coordinate parallel register changes and archive processing with existing tools, preserving current edits and distinguishing preparation, import and verification ([#31](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/31)).

- Support user-authorized institutional requests through existing mail integrations or official channels, with precise sending states and reply provenance ([#30](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/30)).

- Assess information dependence for each material claim rather than equating a shared institution with shared evidence ([#29](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/29)).

- Limit marginal-note conclusions to the administrative action and parties actually named, preserving uncertainty about life status and request dates ([#27](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/27)).

- Check saved-search scope and proposed archive-locator corrections against actual coverage, dates and catalog context ([#24](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/24)).

- Distinguish rows, acts, people and event dates when reconciling register numbering and totals ([#23](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/23)).

- Verify scan identity, extent and content, preserve distinct source photographs, and avoid treating faint pages or unusable text layers as negative evidence ([#22](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/22)).

- Clarify manuscript reading, crop provenance and the distinction between repeated transcription and independent evidence ([#20](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/pull/20)).
- Explain how to import existing GEDCOM/JSON trees into the current research workflow as traceable leads, preserving original files, external IDs, separate candidates and living-person privacy without requiring a dedicated converter ([#25](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/25)).
- Continue searches beyond an expected parish using explicit coverage, evidence-led locality choices and qualified indirect time bounds; distinguish absence from death and preserve chronology conflicts ([#26](https://github.com/DenisSergeevitch/ex-ussr-kinship-research/issues/26)).
- Allow one CAPTCHA attempt through normal controls in the agent’s internal browser when supported and permitted; open the affected tabs when user verification or login is needed, while other research continues.

## 1.5.0 — 2026-10-25

- Incorporate PR #17's gravestone-to-military-family route and Soviet civilian employment, awards and evacuation research, with regional examples and separate identity and relationship conclusions.
- Consolidate access and collection-coverage guidance in existing references; distinguish digitization from availability, contributor observations from verified policies, and dependent copies from independent evidence.
- Add official archive starting points for the Caucasus and Central Asia, make coverage of all 15 former Soviet republics explicit, and use «страны Балтии» in Russian documentation.

## 1.4.0 — 2026-10-25

- Autonomous, resumable research continues while questions, logins or access requests await a reply. Intake asks only what materials are already available and reuses supplied information.
- Routine public historical searches, permitted evidence downloads and local processing need no repeated per-file approval. Sources and query variants are chosen for the question rather than an exhaustive checklist.
- Reports and templates adapt to available evidence. Partial findings remain useful; PDF is optional, and ordinary English words and archive identifiers no longer block PDF generation.
- Evidence audit normalizes independence-group labels, checks direct evidence and provenance on the same artifact, and flags contradictory evidence and invalid person references. Existing research cases are reused.
- Private cases stay outside the skill checkout; source links and FamilySearch source categories are clarified. Release history lives here instead of expanding the README.
- Available skill updates are offered to the user without pausing research; no custom updater is required.

## 1.3.0

General rules for a complete first pass, photo search and a readable PDF for the family. They were prompted by a real case (a WWII officer), where a family memorial page with a certified service-record extract and photos turned up only after the report was "done", but they apply to any line: peasant, urban, repressed, emigrant or Jewish families, and women's lines.

- **Ask the family first.** Before searching, the agent asks once whether relatives have researched this person before, which trees and pages the family keeps (FamilySearch, Geni, MyHeritage, VGD forum threads, and memorial bases that fit the case: Immortal Regiment, Bessmertny Barak, Posledny Adres, Yad Vashem testimonies) and who holds documents, letters, albums and family records. The answer goes to `prior_family_research` in the intake.
- **Coverage checklists.** `references/source-strategy.md` section 12 has checklists for church books, revision lists and censuses, civil registration after 1918, repression and deportation, evacuation, POWs and Ostarbeiter, emigration, Jewish communities and military service. Every item must be closed in `search-log.csv` as `found`, `not-found`, `blocked` or `skipped` before the report. A rich first database no longer ends the search.
- **Name variants in every database.** е/ё, -ев/-ов, female forms, maiden and married surnames, Polish, Yiddish, German and Romanian spellings, church and everyday first names.
- **Site-internal search for family and memorial pages.** An empty web search does not cover a site's internal database; the agent uses the site's own search when available.
- **Grade materials, not websites.** A scan of an original on a family page is an `image-of-original` artifact with its own provenance; the page's text is family testimony.
- **Photos in the main pass.** `references/photo-search.md`: where to look (documents, albums, family pages, school and workplace groups, gravestones, files that may contain photos), identification by caption and provenance only (no face recognition), dating by studio stamps and mounts or by uniform as a hypothesis, maximum available resolution, `not-found` limited to the sources actually checked, a `photos/` folder with a README (`assets/photos-readme.template.md`). `init_case.py` now creates `photos/`.
- **Readable PDF for the family.** `assets/report-pdf.template.html` and `scripts/build_pdf.py`: a clean A4 layout with plain-language reliability labels instead of internal statuses. Required sections: summary, the person and their family, a "how we are related" chain with a label on every parent–child link, timeline, documents, contradictions, where we searched without result, next steps and sources. Optional blocks: places and jurisdictions, military service with awards, repression and rehabilitation, migration and emigration, photos and document scans. The script refuses to build if internal IDs, English statuses or unfilled placeholders remain in the visible text, then prints via headless Chrome, Chromium or Edge.
- **Military database notes** (field lessons): award sheets have higher commanders' resolutions on the reverse side; 1944–1957 long-service awards are distinguished from combat awards by the decree title.

## 1.2.0

The seed catalog previously leaned heavily on Russia; this release expands coverage of the other claimed jurisdictions; archive coverage and current access still need checking for each case:

- **Central imperial/Soviet archives of Russia:** RGIA (St. Petersburg), RGADA, RGVIA, RGAVMF, GARF, plus digitized provincial address-calendars (Presidential Library).
- **Ukraine and Belarus:** CDIAL (Lviv), CDIAK (Kyiv), Ukraine's national archives portal, and the National Historical Archive of Belarus (Minsk).
- **Moldova:** Bessarabian metric books 1820–1924 at the National Archives, with online certificate requests (the domain changed to `arhiva.gov.md`).
- **The Baltics:** Latvia's Raduraksti (church books, revision lists, 1935 census), Lithuania's ePaveldas, Estonia's Saaga.
- **Poland and the Habsburg layer:** Szukajwarchiwach, Geneteka (volunteer index covering Polish, Lithuanian, Belarusian and western-Ukrainian parishes), AGAD (historical eastern-territory collections), Matricula Online, Mapire (Habsburg cadastral and military maps), Kriegsarchiv and successor-state archives (military personnel records; custody and survival depend on period and origin).
- **Jewish families of the region:** JewishGen, JRI-Poland, Yad Vashem, Routes to Roots Foundation (which archive holds which town's surviving records).

New reference **`references/habsburg-galicia-bukovina.md`**: the jurisdiction chain 1772–1945, Austrian-era metric books and consistorial copies, calendar verification by confession, period, and individual register (a 12- or 13-day discrepancy is a hypothesis to investigate), Habsburg conscription records, Galician land cadastres (Josephine and Franciscan records — household and landholding evidence that helps disambiguate namesakes), and a storage map for each record type. New eval cases cover the Galician jurisdiction chain and the 13-day date conflict.

## 1.1.0

Version 1.1.0 adds `references/field-lessons.md`, distilled from a real multi-week research case. Personal data from that case is not included.

- **Unindexed scans.** Most ex-USSR church books on FamilySearch are images only. The file shows how to find the right film (including archive-reference-to-film mapping), map it, skim the key column and zoom on candidates. It also covers what to log.
- **Reading cues that link records.**
  - An exact birth date in a marriage register can match a baptism day for day.
  - House numbers persist for decades.
  - Stillbirths are listed among births.
  - Patronymic formulas: Ukrainian possessive forms, Romanian *fiul lui / n.*, Church Slavonic, German.
  - Clerk name swaps, such as Grigorie and Gheorghe.
- **Marginal annotations.** Later Soviet-era notes on old registers show when a certificate was issued, which is evidence that the person or their family was alive and requesting documents.
- **Repression and deportation records.**
  - Published document collections and their typical contents.
  - How rehabilitation books group people.
  - How to read a "basis" column such as a 25-year sentence.
  - Why a family is linked to a deportation operation, not to the local incident used to justify it.
  - How to draft an archive request.
- **Military databases.** WWII loss records (survivors are absent), "surname nests" built from birthplace clusters, and which portals put up CAPTCHAs. Austro-Hungarian WWI casualty lists help for Galicia and Bukovina.
- **Places that no longer exist.** Liquidated hamlets, redrawn districts, and the difference between "born in" and "grew up in". Also archives in occupied or war-damaged areas.
- **Family materials as sources.** Passports, oral-history recordings with timestamps, and the user's own notes, all tagged by source type.
- **Browser technique.** Deep-zoom tile crops, composite column views for fast skimming, keeping long jobs in their own tab, polite crawling and retries.
- **Knowing when to stop.** When public sources are exhausted, the agent says so once, prepares questions for living relatives and request drafts for archives, and does not invent or loop.

Also in 1.1.0:

- The agent replies in the user's language; the intake template defaults to `requested_output_language: auto`.
- The skill description is bilingual, so it triggers for English-speaking users too.
- **CAPTCHAs are handed to a human.** The agent never solves or bypasses them, and the user signs in to sites themselves.
- More seed sources, each with a reliability class and role.
- New eval cases: language matching, unindexed scans, house-number identity, birthplace conflicts, exhausted sources, repression lists.
