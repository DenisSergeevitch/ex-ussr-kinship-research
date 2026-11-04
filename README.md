# ex-USSR Kinship Research

![ex-USSR Kinship Research cover](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md) / [日本語](README.ja.md)

**An evidence-first genealogy skill for AI agents (Codex, Claude Code and other Agent Skills runtimes).** It turns an agent into a careful family-history researcher for the former USSR, the Soviet Union and the Russian Empire. The agent reads church books and civil records, military, deportation and repression files, and unindexed archive scans. It keeps every find traceable, separates records from interpretation and says plainly what is proven and what is not.

Coverage includes all 15 former Soviet republics: Russia, Ukraine, Belarus, Moldova, Estonia, Latvia, Lithuania, Georgia, Armenia, Azerbaijan, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan and Uzbekistan. Archives are chosen by the event's historical jurisdiction and current record custodian; a regional example does not replace local research.

The skill's instructions are written in Russian, but **the agent talks to you in your language**: English, Ukrainian, Russian, Polish, German and so on. It quotes sources in their original spelling with a translation, and builds search queries in the languages of the records.

---

## What it does

- **Case intake and scope.** One research question, known facts, who may be alive, what is off-limits.
- **Reproducible registers.** Persons, artifacts, claims, relationships and a full search log (CSV), plus a final report template.
- **Historical jurisdiction model.** It resolves every event to the state, province, district, parish or civil registry *as of the event date*, not today's map.
- **Name-variant matrices.** Pre-reform Russian, Ukrainian, Polish, Romanian, German and Yiddish forms, patronymics, maiden names and transliterations.
- **Source strategy.** Originals first, then official catalogs, indexes, published document collections, and only then trees and forums as leads.
- **Evidence protocol.** Claims get explainable statuses, not percentages: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Copies and mirrors of one record share an `independence_group`, so they never count as independent proof.
- **Identity resolution.** Namesakes stay separate `person_id`s until distinguishing evidence appears: house number, parents, godparents, exact birth date or military unit.
- **Audit script.** It checks referential integrity and flags weak corroboration before you write conclusions. An independence group counts only when a cited artifact belongs to it, so corroboration cannot be declared into existence. It also checks IDs and statuses in the working Markdown report, if present; the agent checks the delivered HTML against the registers. A summary shows what is still uncorroborated or marked illegible.
- **Institutional requests.** Draft and, when authorized, send focused requests to archives, libraries, universities and museums using available email or official web tools. If needed, offer a supported mail integration or a ready-to-send letter. Record the outcome, avoid duplicate sends and treat replies as evidence. See [correspondence guidance](references/correspondence.md).
- **Archive request form.** An anonymized [CANO vital-record request template](assets/cano-vital-record-request.template.docx) preserves the supplied form's layout for an editable case copy. Verify the archive's current form and submission requirements before use.
- **Government services.** Choose an official civil-registration or archive request route, checking eligibility and how the result is delivered ([government portals](references/government-portals.md)).
- **Final report.** A complete HTML report is the default deliverable, with each relationship laid out edge by edge, contradictions, failed searches and concrete next steps. PDF is an optional export only when you explicitly request it.
- **Targeted indexed-record research.** Find relevant FamilySearch books by place or DGS through an existing lawful browser session, view specific records, and retain only evidence fragments permitted by the source. Local helpers search relatives, witnesses and name variants in saved fragments, preserving their context and file checksums. [Workflow and coverage limits](references/familysearch-indexes.md).
- **Connected FamilySearch MCP.** Use a connected server for structured searches, profiles, relatives and sources, and authorized tree changes with explicit scope and read-back. Keep indexed search separate from unindexed scan reading, and check the connector's actual browser, privacy and write capabilities. [Workflow and access limits](references/familysearch-mcp.md).
- **WWI source search.** Search GWAR reports, hospital, award and prisoner-of-war records by person or locality, compare settlement spellings across saved cards to decode a distorted place name, then locate the source image. [Workflow](references/ww1-search.md). Both helpers feed the existing artifact register and search log; they do not establish identities or kinship automatically.

Release history: [changelog](references/changelog.md).

## Install

With Node.js installed, you can use the optional [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

The CLI lets you choose your agent and installs into the current project by default; add `-g` for a personal installation across projects. See its documentation for current Node.js requirements.

Alternatively, clone the repository directly into your agent's skills folder:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (personal skills)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

For a single project, put the folder in `.claude/skills/` inside the repository. Most scripts need only Python 3 and the standard library. The optional `scan_montage.py` helper needs Pillow; `build_pdf.py` needs a Chromium-based browser.

## Use

Describe the family question. The agent works from available information and continues while questions or access requests await a reply. For example:

- *"My great-grandfather was exiled to Kazakhstan in the 1930s. Help me find his parents in church records."*
- *"Here are scans of a marriage certificate and a soldier card. Check whether they are the same person and build the evidence chain."*
- *"Find the parish and the right FamilySearch film for a village in Podolia in the 1890s and read the births for the surname X."*

Keep private case data outside the skill's Git checkout. From the skill folder:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 for every saved artifact
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # check registers before the final report
```

`init_case.py` refuses to create a case inside the skill folder, including with
`--force`. Git ignores common legacy case-folder names as an additional safeguard;
check staged files before contributing, especially if moving an existing case.

The agent prepares a complete HTML report, for example `my-case/report.html`, using `assets/report.template.html` or its existing tools. The default editorial layout puts a family tree in the header, with relationship evidence one click away, readable multilingual system-font fallbacks, and layouts for small screens and print. The tree follows the available evidence; missing relatives do not delay the report. Open it directly in a browser or share the HTML with its local images. Short answers may remain text or Markdown; an explicitly requested format takes precedence. A family-facing report does not imply PDF.

Only when you explicitly request PDF, the agent can export the same HTML:

```bash
python scripts/build_pdf.py --html ~/kinship-cases/my-case/report.html --out ~/kinship-cases/my-case/report.pdf
```

This optional export needs Chrome, Chromium or Edge installed (or `CHROME_PATH`). With `--png-dir` it also renders pages to PNG for review if `pypdfium2` is available. HTML delivery needs no PDF renderer.

For PDF export, use static HTML with local or embedded images. The exporter rejects active HTML and network image sources; source links remain clickable. A failed render preserves any existing output PDF.

## Family trees in GEDCOM

[GEDCOM](https://gedcom.io/specs/) is a standard format for exchanging genealogical data between programs. When you ask the agent to build or export a tree, it prepares a local `.ged` file with source citations and evidence notes. The default is GEDCOM 5.5.1 in UTF-8 for compatibility; use another supported version, such as GEDCOM 7, when you or your chosen program require it.

An existing tree is research input and a set of leads, not proof of its relationships. The agent preserves the original file and keeps unresolved claims, unsupported details, evidence registers and the search log in the case folder. Exports follow the evaluated evidence and do not overwrite your files.

You choose the software. Installing tree applications, configuring MCP connections and automatically synchronizing external trees are outside the skill's scope. See [the GEDCOM workflow](references/gedcom.md).

## Repository layout

```
SKILL.md                         main instructions (workflow, hard rules, language policy)
references/
  source-strategy.md             source hierarchy, query patterns, catalogs, archive requests
  correspondence.md              recipients, mail integration, authorized sending and replies
  government-portals.md          civil-registration services and request delivery routes
  evidence-protocol.md           artifact assessment, statuses, identity resolution, conflicts
  ex-ussr-locale-guide.md        jurisdictions, name variants, calendars, record types by period
  browser-and-captcha.md         browsing, sign-in, one CAPTCHA attempt and hand-off, rate limits
  privacy-and-safety.md          living people, minors, DNA, sensitive findings
  seed-sources.md                curated starting resources with reliability classes
  field-lessons.md               practical lessons from a real case
  changelog.md                   release history
  photo-search.md                finding, identifying, dating and storing photos
  habsburg-galicia-bukovina.md   Galicia and Bukovina under the Habsburgs and after
  chechnya-deportation.md        Chechen families: 1944 deportation, special settlement, names and renamed villages
  germany-forced-labour.md       Forced labourers in Germany 1941-1945: Arolsen Archives and German civil registers

  bessarabia-moldova.md          Bessarabia, Moldova, MASSR and the Dniester borderland
  familysearch-indexes.md       targeted browser research, permitted local snapshots and coverage
  familysearch-mcp.md           connected tools, structured reads, scoped writes and verification
  ww1-search.md                 GWAR WWI person/locality search and source-image locators
  gedcom.md                     portable family-tree exports with sources and evidence notes
assets/                          case intake, CSV registers, final report template,
                                 photos README template, research-state template, HTML report template (report.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py, scan_montage.py (needs Pillow)
                                 and shared local analysis modules
evals/discovery-and-logic.yaml   trigger and reasoning test cases
tests/                           unit tests (python3 -m unittest discover -s tests)
```

## Responsible use

- **Family history, not surveillance.** The skill refuses to look up current addresses, phones or accounts of living people, and it minimizes their data in reports.
- **Access checks.** The agent may try an actual CAPTCHA once through normal controls in its internal browser when supported and allowed. If user action is needed, it opens the relevant tab when possible and provides the URL and required action; sign-ins are done by the user. No external solvers, protection bypass, paywall, geo-block or rate-limit evasion, or leaked databases. See [browser guidance](references/browser-and-captcha.md).
- **No uploads of your documents or DNA data** to third-party services without your explicit consent.
- **Sensitive findings** (deportation, repression, adoption, DNA surprises) are reported neutrally and only as far as the question requires.
- **Authorized correspondence.** The skill can send institutional requests through available tools when the user has authorized them; it does not ask again for an already authorized send. Connecting a mailbox alone does not authorize sending, attachments or paid services. Verify the current official contact and procedure, and keep credentials and private case correspondence outside the skill repository.

## Contributing

New sources are welcome in `references/seed-sources.md`. Record verified owner, jurisdiction, collection, provenance, IDs, access, restrictions and check date where known; mark gaps instead of guessing. Keep personal data out of examples.

Source-search helpers use Python's standard library and the existing case registers. Run `python3 -m unittest discover -s tests` to check local parsing, GWAR checkpoints, access failures, unresolved coverage and evidence registration against synthetic data. FamilySearch discovery and targeted viewing use the existing lawful browser session; its Python helpers analyze saved fragments. Keep private research files outside this checkout.

## License

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Maintained by Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
