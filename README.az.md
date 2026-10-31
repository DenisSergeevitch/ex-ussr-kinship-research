# ex-USSR Kinship Research

![ex-USSR Kinship Research üz qabığı](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Süni intellekt agentləri (Codex, Claude Code və digər Agent Skills mühitləri) üçün sübutları önə çəkən şəcərə araşdırması bacarığı.** O, agenti keçmiş SSRİ, Sovet İttifaqı və Rusiya imperiyası ərazilərində ailə tarixinin diqqətli tədqiqatçısına çevirir. Agent kilsə kitablarını və vətəndaşlıq vəziyyəti aktlarını, hərbi, deportasiya və repressiya işlərini, həmçinin indeksləşdirilməmiş arxiv skanlarını oxuyur. Hər tapıntının mənşəyini izlənə bilən şəkildə saxlayır, qeydləri onların şərhindən ayırır və nəyin sübut edildiyini, nəyin edilmədiyini aydın bildirir.

Əhatə dairəsinə bütün 15 keçmiş sovet respublikası daxildir: Rusiya, Ukrayna, Belarus, Moldova, Estoniya, Latviya, Litva, Gürcüstan, Ermənistan, Azərbaycan, Qazaxıstan, Qırğızıstan, Tacikistan, Türkmənistan və Özbəkistan. Arxivlər hadisənin baş verdiyi dövrdəki inzibati mənsubiyyətə və sənədləri hazırda saxlayan quruma görə seçilir; regional nümunə yerli araşdırmanı əvəz etmir.

Bacarığın təlimatları rusca yazılıb, lakin **agent sizinlə sizin dilinizdə danışır**: ingiliscə, ukraynaca, rusca, polyakca, almanca və s. O, mənbələrdən ilkin yazılışda sitat gətirir, yanında tərcüməsini verir və axtarış sorğularını sənədlərin dillərində qurur.

---

## Nə edir

- **İşin qəbulu və sərhədləri.** Bir tədqiqat sualı, məlum faktlar, kimlərin sağ ola biləcəyi və axtarışa daxil edilməyənlər.
- **Təkrar yoxlanıla bilən reyestrlər.** Şəxslər, artefaktlar, iddialar, qohumluq əlaqələri və tam axtarış jurnalı (CSV), həmçinin yekun hesabat şablonu.
- **Tarixi inzibati mənsubiyyət modeli.** Hər hadisəni bugünkü xəritəyə deyil, *hadisənin baş verdiyi tarixdəki* dövlətə, əyalətə, qəza və ya rayona, kilsə icmasına və ya vətəndaşlıq vəziyyəti aktlarının qeydiyyat orqanına aid edir.
- **Ad variantları matrisləri.** İslahatdan əvvəlki rus yazılışı, ukrayna, polyak, rumın, alman və yidiş formaları, ata adları, qızlıq soyadları və transliterasiyalar.
- **Mənbə strategiyası.** Əvvəlcə orijinallar, sonra rəsmi kataloqlar, indekslər, nəşr edilmiş sənəd topluları və yalnız bundan sonra ipucu kimi şəcərələr və forumlar.
- **Sübut protokolu.** İddialara faiz deyil, izah edilə bilən statuslar verilir: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Eyni qeydin surətləri və güzgü nüsxələri ortaq `independence_group` daşıyır, buna görə heç vaxt müstəqil sübut sayılmır.
- **Şəxsiyyətin müəyyənləşdirilməsi.** Eyni adlı şəxslər fərqləndirici sübut tapılana qədər ayrı `person_id` kimi saxlanılır: ev nömrəsi, valideynlər, xaç valideynləri, dəqiq doğum tarixi və ya hərbi hissə.
- **Audit skripti.** Nəticələr yazılmamışdan əvvəl istinadların bütövlüyünü yoxlayır və zəif təsdiqi qeyd edir. Müstəqillik qrupu yalnız istinad edilən artefakt ona aid olduqda sayılır; sadəcə status təyin etməklə təsdiq yaratmaq mümkün deyil. Yekun hesabatı da yoxlayır: istinad edilən hər ID reyestrlərdə olmalı, hər status isə onlara uyğun gəlməlidir. Xülasə nəyin hələ təsdiqlənmədiyini və ya oxunmaz kimi işarələndiyini göstərir.
- **Qurumlara sorğular.** Mövcud e-poçt və ya rəsmi veb alətləri ilə arxivlərə, kitabxanalara, universitetlərə və muzeylərə məqsədli sorğular hazırlayır və icazə olduqda göndərir. Lazım gəldikdə dəstəklənən poçt inteqrasiyası və ya göndərilməyə hazır məktub təklif edir. Nəticəni qeyd edir, təkrar göndərişlərdən yayınır və cavabları sübut kimi qəbul edir. Baxın: [yazışma üzrə təlimat](references/correspondence.md).
- **Dövlət xidmətləri.** Nəticəni almaq hüququnu və çatdırılma qaydasını yoxlayaraq vətəndaşlıq vəziyyəti aktı və ya arxiv sənədi üçün rəsmi sorğu yolunu seçir ([dövlət portalları](references/government-portals.md)).
- **Yekun hesabat.** Hər qohumluq əlaqəsi ayrı-ayrı halqalarla, ziddiyyətlər, nəticəsiz axtarışlar və konkret növbəti addımlarla təqdim olunur.
- **İndeksləşdirilmiş qeydlərdə məqsədli araşdırma.** Mövcud qanuni brauzer sessiyasında yer və ya DGS əsasında uyğun FamilySearch kitablarını tapır, konkret qeydlərə baxır və yalnız mənbənin icazə verdiyi sübut fraqmentlərini saxlayır. Yerli köməkçi alətlər saxlanmış fraqmentlərdə qohumları, şahidləri və ad variantlarını axtarır, konteksti və faylların yoxlama cəmlərini qoruyur. [İş qaydası və əhatə hədləri](references/familysearch-indexes.md).
- **Qoşulmuş FamilySearch MCP.** Strukturlaşdırılmış axtarış, profillər, qohumlar və mənbələr, eləcə də hüdudları açıq müəyyən edilmiş və təkrar oxuma ilə yoxlanan icazəli şəcərə dəyişiklikləri üçün qoşulmuş serverdən istifadə edir. İndeksləşdirilmiş axtarışı indeksləşdirilməmiş skanların oxunmasından ayırır və konnektorun faktiki brauzer, məxfilik və yazma imkanlarını yoxlayır. [İş qaydası və giriş məhdudiyyətləri](references/familysearch-mcp.md).
- **Birinci Dünya müharibəsinə aid mənbə axtarışı.** GWAR-da şəxsin və ya yaşayış məntəqəsinin adına görə məlumatları, hospital, təltif və hərbi əsir qeydlərini axtarır, təhrif olunmuş yer adını oxumaq üçün saxlanmış kartlarda yaşayış məntəqələrinin yazılışlarını müqayisə edir, sonra mənbə şəklini tapır. [İş qaydası](references/ww1-search.md). Hər iki köməkçi alət mövcud artefakt reyestrini və axtarış jurnalını doldurur; onlar şəxsiyyəti və ya qohumluğu avtomatik müəyyən etmir.

Buraxılış tarixçəsi: [dəyişikliklər jurnalı](references/changelog.md).

<a id="install"></a>

## Quraşdırma

Node.js quraşdırılıbsa, əlavə seçim kimi [Skills CLI](https://github.com/vercel-labs/skills) istifadə edə bilərsiniz:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI agenti seçməyə imkan verir və standart olaraq cari layihəyə quraşdırır; layihələrarası şəxsi quraşdırma üçün `-g` əlavə edin. Node.js üzrə cari tələblər üçün onun sənədlərinə baxın.

Alternativ olaraq repozitoriyanı birbaşa agentinizin bacarıqlar qovluğuna klonlayın:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (şəxsi bacarıqlar)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Tək layihə üçün qovluğu repozitoriyanın daxilində `.claude/skills/` qovluğuna yerləşdirin. Skriptlərə yalnız Python 3 və standart kitabxana lazımdır; `build_pdf.py` əlavə olaraq Chromium əsaslı brauzer tələb edir.

## İstifadə

Ailə ilə bağlı sualı təsvir edin. Agent mövcud məlumatlarla işləyir, suallar və ya giriş sorğuları cavab gözləyərkən araşdırmanı davam etdirir. Məsələn:

- *«Ulu babamı 1930-cu illərdə Qazaxıstana sürgün ediblər. Onun valideynlərini kilsə kitablarında tapmağa kömək et».*
- *«Bunlar nikah şəhadətnaməsinin və əsgər kartının skanlarıdır. Onların eyni şəxsə aid olub-olmadığını yoxla və sübut zənciri qur».*
- *«1890-cı illərdə Podoliyadakı bir kənd üçün kilsə icmasını və uyğun FamilySearch mikrofilmini tap, X soyadı üzrə doğum qeydlərini oxu».*

Şəxsi iş məlumatlarını bacarığın Git iş nüsxəsindən kənarda saxlayın. Bacarıq qovluğundan:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # saxlanmış hər artefakt üçün SHA-256
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # yekun hesabatdan əvvəl reyestrləri yoxlayın
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` bacarıq qovluğu daxilində iş yaratmaqdan imtina edir, hətta
`--force` ilə də. Əlavə qoruma olaraq Git iş qovluqlarının geniş yayılmış köhnə adlarını nəzərə almır;
töhfə verməzdən əvvəl indeksə əlavə edilmiş faylları yoxlayın, xüsusilə mövcud işi köçürürsünüzsə.

`build_pdf.py` üçün Chrome, Chromium və ya Edge quraşdırılmalıdır (və ya `CHROME_PATH` göstərilməlidir). `--png-dir` ilə, `pypdfium2` mövcuddursa, yoxlama üçün səhifələri PNG şəklində də yaradır.

Yerli və ya daxil edilmiş şəkillərlə statik HTML istifadə edin. Aktiv HTML və şəbəkədən yüklənən şəkil mənbələri rədd edilir; mənbə keçidləri kliklənə bilir. Render uğursuz olarsa, mövcud çıxış PDF-i saxlanılır.

## GEDCOM formatında ailə şəcərəsi

[GEDCOM](https://gedcom.io/specs/) (`.ged`) şəcərə məlumatlarının mübadiləsi üçün standart formatdır. Şəcərə qurmaq və ya ixrac etmək istəndikdə agent mənbə istinadları və sübut səviyyəsinə dair qeydlərlə yerli fayl hazırlayır. Uyğunluq üçün standart seçim UTF-8 kodlaşdırmalı GEDCOM 5.5.1-dir; istifadəçi dəstəklənən başqa versiyanı, məsələn GEDCOM 7-ni seçərsə, həmin versiya istifadə olunur.

Mövcud şəcərə ilkin material və axtarış ipucu kimi istifadə olunur, özlüyündə sübut sayılmır. İlkin fayl saxlanılır və üzərinə yazılmır; təsdiqlənməmiş məlumatlar və qeyri-müəyyənlik araşdırma işində qalır. Sübut reyestrləri və axtarış jurnalı nəticələrin əsas uçotu olaraq qalır.

Proqramı istifadəçi seçir. Tətbiqin quraşdırılması, MCP qoşulmasının sazlanması və xarici şəcərə ilə avtomatik sinxronlaşdırma bacarığın əhatəsinə daxil deyil. Ətraflı: [references/gedcom.md](references/gedcom.md).

## Repozitoriyanın quruluşu

```
SKILL.md                         əsas təlimatlar (iş qaydası, məcburi qaydalar, dil siyasəti)
references/
  source-strategy.md             mənbə iyerarxiyası, sorğu nümunələri, kataloqlar, arxiv sorğuları
  correspondence.md              alıcılar, poçt inteqrasiyası, icazəli göndərişlər və cavablar
  government-portals.md          vətəndaşlıq vəziyyəti xidmətləri və nəticənin çatdırılması
  evidence-protocol.md           artefaktların qiymətləndirilməsi, statuslar, şəxsiyyətin müəyyənləşdirilməsi, ziddiyyətlər
  ex-ussr-locale-guide.md        inzibati mənsubiyyət, ad variantları, təqvimlər, dövrə görə qeyd növləri
  browser-and-captcha.md         brauzer, giriş, bir CAPTCHA cəhdi və istifadəçiyə ötürmə, tezlik hədləri
  privacy-and-safety.md          sağ şəxslər, yetkinlik yaşına çatmayanlar, DNT, həssas tapıntılar
  seed-sources.md                etibarlılıq sinifləri ilə seçilmiş başlanğıc mənbələr
  field-lessons.md               real işdən praktik dərslər
  changelog.md                   buraxılış tarixçəsi
  photo-search.md                şəkillərin tapılması, müəyyənləşdirilməsi, tarixləndirilməsi və saxlanması
  habsburg-galicia-bukovina.md   Habsburqlar dövründə və sonra Qalisiya və Bukovina
  chechnya-deportation.md        çeçen ailələri: 1944-cü il deportasiyası, xüsusi məskunlaşma, adlar və adı dəyişdirilmiş kəndlər
  germany-forced-labour.md       Almaniyada məcburi işçilər 1941–1945: Arolsen Archives və alman vətəndaşlıq vəziyyəti reyestrləri

  bessarabia-moldova.md          Bessarabiya, Moldova, Moldova MSSR və Dnestr sərhədyanı əraziləri
  familysearch-indexes.md       məqsədli brauzer araşdırması, icazəli yerli nüsxələr və əhatə
  familysearch-mcp.md           qoşulmuş alətlər, strukturlaşdırılmış oxuma, məhdud yazma və yoxlama
  ww1-search.md                 GWAR-da şəxs/yer axtarışı və mənbə şəkillərinin ünvanları
  gedcom.md                     GEDCOM mübadiləsi: mənbələr, sübut səviyyəsi və araşdırma işi
assets/                          işin qəbulu, CSV reyestrləri, yekun hesabat şablonu,
                                 şəkillər üçün README şablonu, tədqiqat vəziyyəti şablonu, oxunaqlı PDF şablonu (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py və ortaq yerli təhlil modulları
evals/discovery-and-logic.yaml   işə düşmə və məntiq test ssenariləri
tests/                           vahid testləri (python3 -m unittest discover -s tests)
```

## Məsuliyyətli istifadə

- **Ailə tarixi, izləmə deyil.** Bacarıq sağ şəxslərin cari ünvanlarını, telefonlarını və ya hesablarını axtarmaqdan imtina edir və hesabatlarda onların məlumatlarını minimuma endirir.
- **Giriş yoxlamaları.** Dəstəklənirsə və icazə verilirsə, agent daxili brauzerinin adi idarəetmə vasitələri ilə həqiqi CAPTCHA-nı bir dəfə həll etməyə cəhd edə bilər. İstifadəçi hərəkəti lazımdırsa, imkan daxilində uyğun vərəqi açır, URL-i və tələb olunan hərəkəti göstərir; hesaba istifadəçi daxil olur. Xarici həll xidmətlərindən və sızdırılmış bazalardan istifadə edilmir; qoruma tədbirləri, ödənişli giriş məhdudiyyətləri, coğrafi bloklar və sorğu tezliyi hədləri aşılmır. Baxın: [brauzer təlimatı](references/browser-and-captcha.md).
- **Sənədləriniz və ya DNT məlumatlarınız** açıq razılığınız olmadan üçüncü tərəf xidmətlərinə yüklənmir.
- **Həssas tapıntılar** (deportasiya, repressiya, övladlığa götürmə, gözlənilməz DNT nəticələri) neytral və yalnız sualın tələb etdiyi həcmdə təqdim olunur.
- **İcazəli yazışma.** İstifadəçi göndərişə icazə verdikdə bacarıq mövcud alətlərlə qurumlara sorğu göndərə bilər; artıq icazə verilmiş göndəriş üçün yenidən soruşmur. Təkcə poçt qutusunun qoşulması göndərişə, əlavələrə və ya ödənişli xidmətlərə icazə vermir. Cari rəsmi əlaqə məlumatlarını və proseduru yoxlayın; giriş məlumatlarını və işə aid şəxsi yazışmaları bacarığın repozitoriyasından kənarda saxlayın.

## Töhfə vermək

Yeni mənbələr `references/seed-sources.md` faylına əlavə edilə bilər. Məlumdursa, yoxlanmış sahibini, inzibati mənsubiyyətini, kolleksiyanı, mənşəyini, identifikatorlarını, girişi, məhdudiyyətləri və yoxlama tarixini qeyd edin; təxmin etmək əvəzinə boşluqları göstərin. Nümunələrə şəxsi məlumat daxil etməyin.

Mənbə axtarışı köməkçiləri Python-un standart kitabxanasından və mövcud iş reyestrlərindən istifadə edir. Yerli təhlili, GWAR davam nöqtələrini, giriş xətalarını, qeyri-müəyyən əhatəni və sübut qeydiyyatını sintetik məlumatlarla yoxlamaq üçün `python3 -m unittest discover -s tests` işlədin. FamilySearch-də aşkarlama və məqsədli baxış mövcud qanuni brauzer sessiyasından istifadə edir; Python köməkçiləri saxlanmış fraqmentləri təhlil edir. Şəxsi tədqiqat fayllarını bu iş nüsxəsindən kənarda saxlayın.

## Lisenziya

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Layihəni Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)) müşayiət edir.
