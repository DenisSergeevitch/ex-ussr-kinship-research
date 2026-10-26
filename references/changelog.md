# Release history

## Unreleased

- End each piece of work with a short, anonymised “notes on the skill” block for the user: unclear or conflicting guidance, working sources and techniques missing from the references, and rules that would have prevented errors; issues or PRs only with the user’s consent.

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
