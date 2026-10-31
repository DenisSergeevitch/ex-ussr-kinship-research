# ex-USSR Kinship Research

![ex-USSR Kinship Research muqovasi](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md)

**Sun’iy intellekt agentlari uchun dalilga ustuvorlik beruvchi genealogiya ko‘nikmasi (Codex, Claude Code va boshqa Agent Skills muhitlari).** U agentni sobiq SSSR, Sovet Ittifoqi va Rossiya imperiyasi hududidagi oila tarixini sinchiklab o‘rganuvchi tadqiqotchiga aylantiradi. Agent cherkov kitoblari va fuqarolik holati qaydlarini, harbiy, surgun va qatag‘on hujjatlarini, shuningdek indekslanmagan arxiv skanlarini o‘qiydi. Har bir topilmaning manbasini kuzatish imkonini saqlaydi, qaydni uning talqinidan ajratadi va nima isbotlanganini, nima isbotlanmaganini aniq aytadi.

Qamrov barcha 15 sobiq sovet respublikasini o‘z ichiga oladi: Rossiya, Ukraina, Belarus, Moldova, Estoniya, Latviya, Litva, Gruziya, Armaniston, Ozarbayjon, Qozog‘iston, Qirg‘iziston, Tojikiston, Turkmaniston va O‘zbekiston. Arxivlar voqea paytidagi tarixiy yurisdiksiya va hujjatlarni hozir saqlayotgan muassasaga qarab tanlanadi; mintaqaviy misol mahalliy tadqiqot o‘rnini bosa olmaydi.

Ko‘nikma yo‘riqnomasi rus tilida yozilgan, biroq **agent siz bilan o‘z tilingizda gaplashadi**: inglizcha, ukraincha, ruscha, polyakcha, nemischa va hokazo. U manbalardan iqtiboslarni asl imlosida tarjimasi bilan beradi, qidiruv so‘rovlarini esa hujjatlar tilida tuzadi.

---

## Nimalar qiladi

- **Ishni boshlash va doirasini belgilash.** Bitta tadqiqot savoli, ma’lum faktlar, kim tirik bo‘lishi mumkinligi va ruxsat etilmagan harakatlar.
- **Qayta tekshiriladigan reyestrlar.** Shaxslar, artefaktlar, da’volar, qarindoshlik aloqalari va to‘liq qidiruv jurnali (CSV), shuningdek yakuniy hisobot andozasi.
- **Tarixiy yurisdiksiya modeli.** Har bir voqeani bugungi xarita bo‘yicha emas, *voqea sanasidagi* davlat, viloyat, tuman, cherkov qavmi yoki fuqarolik holatini qayd etish idorasiga bog‘laydi.
- **Ism variantlari matritsalari.** Islohotdan oldingi ruscha, ukraincha, polyakcha, rumincha, nemischa va idishcha shakllar, otasining ismi, turmushga chiqishdan oldingi familiya va transliteratsiyalar.
- **Manba strategiyasi.** Avval asl nusxalar, so‘ng rasmiy kataloglar, indekslar, nashr etilgan hujjat to‘plamlari; shajaralar va forumlar faqat undan keyin qidiruvga yo‘nalish beruvchi ma’lumot sifatida qo‘llanadi.
- **Dalil protokoli.** Da’volarga foiz emas, izohlash mumkin bo‘lgan holatlar beriladi: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Bitta qaydning nusxalari va ko‘zgulari bir xil `independence_group` guruhiga kiradi, shuning uchun ular hech qachon mustaqil dalil sanalmaydi.
- **Shaxsni aniqlash.** Uy raqami, ota-onasi, cho‘qintirishdagi tutingan ota-onasi, aniq tug‘ilgan sana yoki harbiy qism kabi farqlovchi dalil topilmaguncha adashlar alohida `person_id` bilan saqlanadi.
- **Audit skripti.** Xulosa yozishdan oldin havolalar yaxlitligini tekshiradi va zaif tasdiqlangan ma’lumotni belgilaydi. Mustaqillik guruhi faqat havola qilingan artefakt unga kirganida hisoblanadi; tasdiqni shunchaki e’lon qilib yaratib bo‘lmaydi. Yakuniy hisobot ham tekshiriladi: undagi har bir ID reyestrlarda bo‘lishi va har bir holat ularga mos kelishi kerak. Umumlashtirishda nimalar hali tasdiqlanmagani yoki o‘qilmaydigan deb belgilanganini ko‘rsatadi.
- **Muassasalarga so‘rovlar.** Mavjud elektron pochta yoki rasmiy veb-vositalar orqali arxivlar, kutubxonalar, universitetlar va muzeylarga aniq so‘rovlar tayyorlaydi va ruxsat bo‘lganda yuboradi. Zarur bo‘lsa qo‘llab-quvvatlanadigan pochta integratsiyasi yoki yuborishga tayyor xatni taklif etadi. Natijani qayd qiladi, takroriy yuborishni oldini oladi va javoblarni dalil sifatida ko‘radi. [Yozishmalar bo‘yicha yo‘riqnomaga](references/correspondence.md) qarang.
- **Davlat xizmatlari.** Murojaat qilish huquqi va natija qanday yetkazilishini tekshirib, fuqarolik holati qaydi yoki arxiv so‘rovining rasmiy yo‘lini tanlaydi ([davlat portallari](references/government-portals.md)).
- **Yakuniy hisobot.** Har bir qarindoshlik aloqasi bo‘g‘inma-bo‘g‘in, ziddiyatlar, natijasiz qidiruvlar va keyingi aniq qadamlar bilan ko‘rsatiladi.
- **Indekslangan qaydlarni maqsadli tadqiq qilish.** Mavjud qonuniy brauzer seansi orqali joy yoki DGS bo‘yicha tegishli FamilySearch kitoblarini topadi, aniq qaydlarni ko‘radi va faqat manba ruxsat etgan dalil parchalarini saqlaydi. Mahalliy yordamchi vositalar saqlangan parchalardan qarindoshlar, guvohlar va ism variantlarini qidirib, ularning konteksti va fayl nazorat yig‘indilarini saqlaydi. [Ish jarayoni va qamrov chegaralari](references/familysearch-indexes.md).
- **Ulangan FamilySearch MCP.** Ulangan serverni tuzilmali qidiruvlar, profillar, qarindoshlar, manbalar va doirasi aniq belgilangan, qayta o‘qib tekshiriladigan ruxsatli shajara o‘zgarishlari uchun ishlatadi. Indekslangan qidiruvni indekslanmagan skanlarni o‘qishdan alohida saqlaydi, konnektorning brauzer, maxfiylik va yozish bo‘yicha haqiqiy imkoniyatlarini tekshiradi. [Ish jarayoni va kirish chegaralari](references/familysearch-mcp.md).
- **Birinchi jahon urushi manbalarini qidirish.** GWAR xabarlari, kasalxona, mukofot va harbiy asirlar qaydlarini shaxs yoki joy bo‘yicha qidiradi; buzib yozilgan joy nomini aniqlash uchun saqlangan kartochkalardagi aholi punkti nomlari imlosini solishtiradi, keyin manbaning asl tasvirini topadi. [Ish jarayoni](references/ww1-search.md). Ikkala yordamchi vosita mavjud artefakt reyestri va qidiruv jurnaliga ma’lumot beradi; ular shaxs yoki qarindoshlikni avtomatik aniqlamaydi.

Chiqarilishlar tarixi: [o‘zgarishlar jurnali](references/changelog.md).

<a id="install"></a>
## O‘rnatish

Node.js o‘rnatilgan bo‘lsa, ixtiyoriy [Skills CLI](https://github.com/vercel-labs/skills) vositasidan foydalanishingiz mumkin:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI agentingizni tanlash imkonini beradi va odatda joriy loyihaga o‘rnatadi; loyihalar bo‘ylab shaxsiy o‘rnatish uchun `-g` qo‘shing. Node.js uchun joriy talablarni uning hujjatlaridan ko‘ring.

Yoki repozitoriyni to‘g‘ridan-to‘g‘ri agentingizning ko‘nikmalar papkasiga klonlang:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (shaxsiy ko‘nikmalar)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Bitta loyiha uchun papkani repozitoriy ichidagi `.claude/skills/` ga joylashtiring. Skriptlarga faqat Python 3 va standart kutubxona kerak; `build_pdf.py` ga Chromium asosidagi brauzer ham zarur.

## Foydalanish

Oilaga oid savolingizni tavsiflang. Agent mavjud ma’lumot bilan ishlaydi va savollar yoki kirish so‘rovlariga javob kutilayotganida ham tadqiqotni davom ettiradi. Masalan:

- *«Bobomning otasi 1930-yillarda Qozog‘istonga surgun qilingan. Uning ota-onasini cherkov qaydlaridan topishga yordam ber.»*
- *«Mana nikoh guvohnomasi va askar kartochkasi skanlari. Ular bir shaxsga tegishlimi, tekshir va dalillar zanjirini tuz.»*
- *«1890-yillardagi Podoliya qishlog‘i uchun cherkov qavmi va kerakli FamilySearch filmini top, X familiyasi bo‘yicha tug‘ilish qaydlarini o‘qi.»*

Shaxsiy ish ma’lumotlarini ko‘nikmaning Git ishchi nusxasidan tashqarida saqlang. Ko‘nikma papkasidan:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # har bir saqlangan artefakt uchun SHA-256
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # yakuniy hisobotdan oldin reyestrlarni tekshirish
python scripts/build_pdf.py --html ~/kinship-cases/my-case/pdf-source/report.html --out ~/kinship-cases/my-case/report.pdf
```

`init_case.py` ko‘nikma papkasi ichida, hatto `--force` bilan ham, ish yaratishni rad etadi. Qo‘shimcha himoya sifatida Git eski ish papkalarining keng tarqalgan nomlarini e’tiborsiz qoldiradi; hissa qo‘shishdan avval, ayniqsa mavjud ishni ko‘chirayotganda, indeksga qo‘shilgan fayllarni tekshiring.

`build_pdf.py` uchun Chrome, Chromium yoki Edge o‘rnatilgan bo‘lishi kerak (yoki `CHROME_PATH` ko‘rsatiladi). Agar `pypdfium2` mavjud bo‘lsa, `--png-dir` sahifalarni ko‘rib chiqish uchun PNG ko‘rinishida ham chiqaradi.

Mahalliy yoki ichiga joylangan rasmlari bor statik HTML ishlating. Faol HTML va tarmoqdan olinadigan rasm manbalari rad etiladi; manba havolalari bosiladigan bo‘lib qoladi. Render muvaffaqiyatsiz bo‘lsa, oldingi chiqish PDF fayli saqlanadi.

## GEDCOM formatidagi oilaviy shajara

[GEDCOM](https://gedcom.io/specs/) (`.ged`) genealogik ma’lumot almashishning standart formatidir. Shajara tuzish yoki eksport qilish so‘ralsa, agent manba havolalari va dalil darajasiga oid izohlar bilan mahalliy fayl tayyorlaydi. Moslik uchun odatiy tanlov — UTF-8 kodlashidagi GEDCOM 5.5.1; foydalanuvchi qo‘llab-quvvatlanadigan boshqa versiyani, masalan GEDCOM 7-ni tanlasa, shu versiya ishlatiladi.

Mavjud shajara boshlang‘ich material va qidiruv uchun yo‘l-yo‘riq sifatida olinadi, o‘z-o‘zidan dalil hisoblanmaydi. Asl fayl saqlanadi va uning ustiga yozilmaydi; tasdiqlanmagan ma’lumotlar va noaniqlik tadqiqot ishida qoladi. Dalillar reyestrlari va qidiruv jurnali xulosalarning asosiy qaydi bo‘lib qoladi.

Dasturni foydalanuvchi tanlaydi. Ilovani o‘rnatish, MCP ulanishini sozlash va tashqi shajara bilan avtomatik sinxronlash ko‘nikma doirasiga kirmaydi. Batafsil: [references/gedcom.md](references/gedcom.md).

## Repozitoriy tuzilishi

```
SKILL.md                         asosiy ko‘rsatmalar (ish jarayoni, qat’iy qoidalar, til siyosati)
references/
  source-strategy.md             manba ierarxiyasi, so‘rov andozalari, kataloglar, arxiv so‘rovlari
  correspondence.md              oluvchilar, pochta integratsiyasi, ruxsatli yuborish va javoblar
  government-portals.md          fuqarolik qaydi xizmatlari va so‘rov natijasini yetkazish yo‘llari
  evidence-protocol.md           artefakt baholash, holatlar, shaxsni aniqlash, ziddiyatlar
  ex-ussr-locale-guide.md        yurisdiksiyalar, ism variantlari, taqvimlar, davrga qarab qayd turlari
  browser-and-captcha.md         brauzer, kirish, bir CAPTCHA urinishi va foydalanuvchiga topshirish, tezlik cheklovlari
  privacy-and-safety.md          tirik odamlar, voyaga yetmaganlar, DNK, nozik topilmalar
  seed-sources.md                ishonchlilik sinflari bilan tanlangan boshlang‘ich manbalar
  field-lessons.md               haqiqiy ishdan amaliy saboqlar
  changelog.md                   chiqarilishlar tarixi
  photo-search.md                rasmlarni topish, aniqlash, sanasini belgilash va saqlash
  habsburg-galicia-bukovina.md   Gabsburglar davrida va undan keyingi Galitsiya va Bukovina
  chechnya-deportation.md        chechen oilalari: 1944-yilgi deportatsiya, maxsus manzilgoh, ismlar va nomi o‘zgargan qishloqlar
  germany-forced-labour.md       Germaniyada majburiy mehnat, 1941–1945: Arolsen Archives va nemis fuqarolik qaydlari

  bessarabia-moldova.md          Bessarabiya, Moldova, Moldova ASSR va Dnestr chegara hududi
  familysearch-indexes.md       brauzerda maqsadli tadqiqot, ruxsatli mahalliy nusxalar va qamrov
  familysearch-mcp.md           ulangan vositalar, tuzilmali o‘qish, cheklangan yozish va tekshirish
  ww1-search.md                 GWARda shaxs/joy qidiruvi va manba tasviri manzillari
  gedcom.md                     GEDCOM almashinuvi: manbalar, dalil darajasi va tadqiqot ishi
assets/                          boshlang‘ich ma’lumotlar, CSV reyestrlar, yakuniy hisobot andozasi,
                                 rasmlar README andozasi, tadqiqot holati, o‘qishga qulay PDF andozasi (report-pdf.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py va umumiy mahalliy tahlil modullari
evals/discovery-and-logic.yaml   ishga tushish va mantiqiy fikrlash sinovlari
tests/                           birlik testlari (python3 -m unittest discover -s tests)
```

## Mas’uliyatli foydalanish

- **Kuzatuv emas, oila tarixi.** Ko‘nikma tirik odamlarning hozirgi manzili, telefoni yoki akkauntlarini qidirishni rad etadi va hisobotlarda ularning ma’lumotlarini kamaytiradi.
- **Kirishni tekshirish.** Qo‘llab-quvvatlansa va ruxsat etilgan bo‘lsa, agent ichki brauzerning odatiy boshqaruvlari orqali haqiqiy CAPTCHA-ni bir marta bajarib ko‘rishi mumkin. Foydalanuvchi harakati kerak bo‘lsa, imkon qadar tegishli varaqni ochib, URL va zarur harakatni beradi; akkauntga foydalanuvchining o‘zi kiradi. Tashqi yechish xizmatlari, himoya, to‘lov to‘sig‘i, geografik blok yoki so‘rov tezligi chegaralarini aylanib o‘tish va sizib chiqqan bazalar ishlatilmaydi. [Brauzer yo‘riqnomasiga](references/browser-and-captcha.md) qarang.
- **Aniq roziligingizsiz hujjatlaringiz yoki DNK ma’lumotlaringiz uchinchi tomon xizmatlariga yuklanmaydi.**
- **Nozik topilmalar** (deportatsiya, qatag‘on, farzandlikka olish, kutilmagan DNK natijalari) xolis va faqat savol talab qilgan darajada bayon etiladi.
- **Ruxsatli yozishmalar.** Foydalanuvchi ruxsat berganida ko‘nikma mavjud vositalar orqali muassasalarga so‘rov yuborishi mumkin; avval ruxsat etilgan yuborish uchun yana so‘ramaydi. Faqat pochta qutisini ulash yuborishga, biriktirmalarga yoki pulli xizmatlarga ruxsat bermaydi. Hozirgi rasmiy aloqa va tartibni tekshiring; kirish ma’lumotlari hamda shaxsiy ish yozishmalarini ko‘nikma repozitoriysidan tashqarida saqlang.

## Hissa qo‘shish

Yangi manbalar `references/seed-sources.md` fayliga qabul qilinadi. Ma’lum bo‘lsa, tekshirilgan egasi, yurisdiksiya, to‘plam, kelib chiqishi, IDlar, kirish, cheklovlar va tekshirilgan sanani yozing; bo‘shliqlarni taxmin bilan to‘ldirmay belgilang. Misollarga shaxsiy ma’lumot kiritmang.

Manba qidirish yordamchilari Python standart kutubxonasi va mavjud ish reyestrlaridan foydalanadi. Mahalliy tahlil, GWAR nazorat nuqtalari, kirish xatolari, aniqlanmagan qamrov va sun’iy ma’lumotlar asosida dalil qaydini tekshirish uchun `python3 -m unittest discover -s tests` ni bajaring. FamilySearchdan topish va maqsadli ko‘rish mavjud qonuniy brauzer seansidan foydalanadi; Python yordamchilari saqlangan parchalarni tahlil qiladi. Shaxsiy tadqiqot fayllarini bu ishchi nusxadan tashqarida saqlang.

## Litsenziya

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Loyiha yurituvchisi: Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).
