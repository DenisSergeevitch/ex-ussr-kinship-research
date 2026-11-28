# ex-USSR Kinship Research

![ex-USSR Kinship Research kapağı](docs/cover.jpg)

Diller: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md) / [日本語](README.ja.md) / [Türkçe](README.tr.md)

> Bu Türkçe çeviri topluluk tarafından hazırlanmıştır. Bir farklılık olursa İngilizce `README.md` esastır.

**Kanıta dayalı bir soy araştırma becerisi, AI ajanları için (Codex, Claude Code ve diğer Agent Skills ortamları).** Ajanı, eski SSCB'nin, Sovyetler Birliği'nin ve Rus İmparatorluğu'nun topraklarında dikkatli bir aile tarihi araştırmacısına dönüştürür. Ajan kilise defterlerini ve nüfus kayıtlarını, askerlik, sürgün ve baskı dosyalarını ve dizinlenmemiş arşiv taramalarını okur. Her bulguyu izlenebilir tutar, kayıtları yorumdan ayırır ve neyin kanıtlanmış, neyin kanıtlanmamış olduğunu açıkça söyler.

Kapsam, eski 15 Sovyet cumhuriyetinin tamamını içerir: Rusya, Ukrayna, Belarus, Moldova, Estonya, Letonya, Litvanya, Gürcistan, Ermenistan, Azerbaycan, Kazakistan, Kırgızistan, Tacikistan, Türkmenistan ve Özbekistan. Arşivler, olayın tarihsel yargı alanına ve kayıtların bugünkü saklayıcısına göre seçilir; bölgesel bir örnek yerel araştırmanın yerini tutmaz.

Becerinin talimatları Rusça yazılmıştır, ama **ajan sizinle kendi dilinizde konuşur**: İngilizce, Ukraynaca, Rusça, Lehçe, Almanca ve benzeri. Kaynakları özgün yazımıyla alıntılar ve yanına çeviri koyar; arama sorgularını kayıtların dillerinde kurar.

---

## Ne yapar

- **Vaka girişi ve kapsam.** Tek bir araştırma sorusu, bilinen bilgiler, hayatta olabilecek kişiler ve dokunulmayacak konular.
- **Tekrarlanabilir kayıt defterleri.** Kişiler, materyaller, iddialar, ilişkiler ve tam bir arama günlüğü (CSV), artı nihai rapor şablonu.
- **Tarihsel yargı alanı modeli.** Her olayı, bugünkü haritaya göre değil, *olay tarihindeki* devlete, vilayete, ilçeye, cemaate ya da nüfus siciline bağlar.
- **Ad varyantı matrisleri.** Reform öncesi Rusça, Ukraynaca, Lehçe, Romence, Almanca ve Yidiş biçimleri; babaadı, kız soyadı ve transliterasyonlar.
- **Kaynak stratejisi.** Önce özgün kayıtlar, sonra resmi kataloglar, dizinler ve yayımlanmış belge koleksiyonları; ağaçlar ve forumlar ancak son sırada ipucu olarak.
- **Kanıt protokolü.** İddialar yüzde değil, açıklanabilir durumlar alır: `hypothesis`, `single-source`, `corroborated`, `strongly-corroborated`, `contradicted`, `unresolved`. Aynı kaydın kopya ve aynaları bir `independence_group` paylaşır, bu yüzden bağımsız kanıt sayılmazlar.
- **Kimlik çözümü.** Aynı adlı kişiler, ayırt edici kanıt (ev numarası, ebeveynler, vaftiz anne ve babaları, kesin doğum tarihi ya da askerî birlik) çıkana kadar ayrı `person_id`'ler olarak kalır.
- **Denetim betiği.** Referans bütünlüğünü kontrol eder ve sonuç yazmadan önce zayıf teyitleri işaretler. Bir bağımsızlık grubu yalnız atıf yapılan bir materyal o gruba ait olduğunda sayılır; teyit beyanla var edilemez. Varsa çalışma Markdown raporundaki kimlik ve durum kodlarını da kontrol eder; teslim edilen HTML'i ajan kayıt defterlerine karşı denetler. Özet, hâlâ teyitsiz ya da okunamaz işaretli olanları gösterir.
- **Kurumsal talepler.** Arşivlere, kütüphanelere, üniversitelere ve müzelere odaklı talepleri, mevcut e-posta ya da resmi web araçlarıyla taslak olarak hazırlar; yetki verilirse gönderir. Gerekirse desteklenen bir posta entegrasyonu ya da gönderime hazır bir mektup önerir. Sonucu kaydeder, mükerrer gönderimi önler ve yanıtları kanıt olarak değerlendirir. Bkz. [yazışma rehberi](references/correspondence.md).
- **Arşiv talep formu.** Anonimleştirilmiş [CANO doğum/evlilik/ölüm kaydı talep şablonu](assets/cano-vital-record-request.template.docx), verilen formun düzenini korur ve düzenlenebilir bir vaka kopyası verir. Kullanmadan önce arşivin güncel form ve başvuru koşullarını doğrulayın.
- **Devlet hizmetleri.** Resmi nüfus kaydı ya da arşiv başvuru yolunu seçer; uygunluğu ve sonucun nasıl teslim edildiğini kontrol eder ([devlet portalları](references/government-portals.md)).
- **Nihai rapor.** Varsayılan teslim biçimi eksiksiz bir HTML raporudur: her ilişki kenar kenar açıklanır, çelişkiler, başarısız aramalar ve somut sonraki adımlar yer alır. PDF yalnızca açıkça istenirse isteğe bağlı bir çıktıdır.
- **Hedefli dizinlenmiş kayıt araştırması.** Yerleşim yerine ya da DGS'ye göre ilgili FamilySearch defterlerini, mevcut yasal bir tarayıcı oturumu üzerinden bulur, belirli kayıtları görüntüler ve yalnız kaynağın izin verdiği kanıt parçalarını saklar. Yerel yardımcılar, kayıtlı parçalarda akrabaları, tanıkları ve ad varyantlarını arar; bağlamı ve dosya sağlama toplamlarını korur. [İş akışı ve kapsam sınırları](references/familysearch-indexes.md).
- **Yerel tablo dizinleri.** Kullanıcının verdiği CSV ve XLSX tablolarında açık ad varyantlarıyla arama yapar; satırları seçilen alanlara göre gruplayıp gözden geçirmeye sunar. Sonuçlar dosya özetini ve satır konumlarını korur, kimlik ya da akrabalık kurmaz. XLSX desteği için isteğe bağlı `openpyxl` ve `defusedxml` gerekir. [Talimatlar ve sınırlar](references/table-indexes.md).
- **Bağlı FamilySearch MCP.** Bağlı bir sunucu üzerinden yapılandırılmış aramalar, profiller, akrabalar ve kaynaklar; açık kapsam ve geri okuma ile yetkili ağaç değişiklikleri. Dizinli aramayı taranmış ama dizinlenmemiş sayfaların okunmasından ayrı tutun ve bağlayıcının gerçek tarayıcı, gizlilik ve yazma yeteneklerini kontrol edin. [İş akışı ve erişim sınırları](references/familysearch-mcp.md).
- **I. Dünya Savaşı kaynak araması.** GWAR raporlarında, hastane, ödül ve esir kayıtlarında kişi ya da yerleşim yeri üzerinden arama yapar; kaydedilmiş kartlardaki yerleşim adı yazımlarını karşılaştırıp bozulmuş bir yer adını çözmeye çalışır, sonra kaynak görüntüsünü bulur. [İş akışı](references/ww1-search.md). Her iki yardımcı da mevcut materyal kayıt defterine ve arama günlüğüne veri verir; akrabalığı ya da kimliği kendiliğinden kurmazlar.

Sürüm geçmişi: [değişiklik günlüğü](references/changelog.md).

## Kurulum

Node.js kuruluysa, isteğe bağlı [Skills CLI](https://github.com/vercel-labs/skills) ile kurabilirsiniz:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI, kullandığınız ajanı seçmenize izin verir ve varsayılan olarak geçerli projeye kurar; tüm projelerde kişisel kurulum için `-g` ekleyin. Güncel Node.js gereksinimleri için CLI'nin belgelerine bakın.

Alternatif olarak depoyu doğrudan ajanınızın beceri klasörüne klonlayabilirsiniz:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (kişisel beceriler)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

Tek bir proje için klasörü deponun içindeki `.claude/skills/` klasörüne koyun. Betiklerin çoğu yalnız Python 3 ve standart kütüphane ister. İsteğe bağlı `scan_montage.py` yardımcısı Pillow ister; `build_pdf.py` ise Chromium tabanlı bir tarayıcı ister.

## Kullanım

Aile sorunuzu anlatın. Ajan elindeki bilgilerle çalışır ve bir soru ya da erişim talebi yanıt beklerken de devam eder. Örnekler:

- *"Büyük dedem 1930'larda Kazakistan'a sürüldü. Kilise kayıtlarında anne babasını bulmama yardım eder misin?"*
- *"Bir evlilik belgesi ile bir asker kartının taramaları burada. Aynı kişi olup olmadıklarını kontrol edip kanıt zincirini kurar mısın?"*
- *"1890'larda Podolya'daki bir köy için doğru cemaati ve FamilySearch filmini bul; X soyadının doğumlarını oku."*

Özel vaka verilerini skill'in Git kopyasının dışında tutun. Skill klasöründen:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Maria'nın anne babası kimdi?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # kaydedilen her materyal için SHA-256
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # nihai rapordan önce kayıtları denetle
```

`init_case.py`, `--force` ile bile olsa vakayı skill klasörünün içinde oluşturmayı reddeder. Git, yaygın eski vaka klasörü adlarını ek güvenlik olarak yok sayar; özellikle mevcut bir vakayı taşırken katkıdan önce hazırlanmış (stage edilmiş) dosyaları kontrol edin.

Ajan, `assets/report.template.html` şablonunu ya da kendi mevcut araçlarını kullanarak eksiksiz bir HTML raporu hazırlar, örneğin `my-case/report.html`. Varsayılan editoryal düzen, başlıkta bir aile ağacı, her ilişkinin kanıtına tek tıkla erişim, okunabilir çok dilli yedek yazı tipleri ile küçük ekran ve yazdırma düzenleri içerir. Ağaç mevcut kanıtı izler; eksik akrabalar raporu geciktirmez. Raporu doğrudan tarayıcıda açabilir ya da yerel görüntüleriyle birlikte paylaşabilirsiniz. Kısa yanıtlar metin ya da Markdown olarak kalabilir; açıkça istenen bir biçim öncelik taşır. Aile için hazırlanan bir rapor PDF anlamına gelmez.

Yalnızca PDF'i açıkça isterseniz ajan aynı HTML'i dışa aktarabilir:

```bash
python scripts/build_pdf.py --html ~/kinship-cases/my-case/report.html --out ~/kinship-cases/my-case/report.pdf
```

Bu isteğe bağlı dışa aktarım, Chrome, Chromium ya da Edge gerektirir (ya da `CHROME_PATH`). `--png-dir` ile sayfaları gözden geçirme için PNG'ye de çevirir; bunun için `pypdfium2` gerekir. HTML teslimi için PDF oluşturucu gerekmez.

PDF dışa aktarımında yerel ya da gömülü görüntüleri olan statik HTML kullanın. Dışa aktarıcı etkin HTML'i ve ağ görüntü kaynaklarını reddeder; kaynak bağlantıları tıklanabilir kalır. Başarısız bir dönüştürme varsa mevcut PDF çıktısını korur.

## GEDCOM ile aile ağaçları

[GEDCOM](https://gedcom.io/specs/), genealojik verileri programlar arasında taşımak için kullanılan standart bir biçimdir. Ajandan bir ağaç oluşturmasını ya da dışa aktarmasını istediğinizde, kaynak atıfları ve kanıt notları içeren yerel bir `.ged` dosyası hazırlar. Varsayılan, uyumluluk için UTF-8 kodlamalı GEDCOM 5.5.1'dir; siz ya da seçtiğiniz program başka bir sürüm (ör. GEDCOM 7) isterse o kullanılır.

Mevcut bir ağaç araştırma girdisidir ve ilişkileri için bir kanıt değil, bir ipuçları kümesidir. Ajan özgün dosyayı korur; çözülmemiş iddiaları, desteklenmeyen ayrıntıları, kanıt kayıtlarını ve arama günlüğünü vaka klasöründe tutar. Dışa aktarımlar değerlendirilmiş kanıtı izler ve dosyalarınızın üzerine yazmaz.

Yazılımı siz seçersiniz. Ağaç uygulamalarını kurmak, MCP bağlantılarını yapılandırmak ve dış ağaçları otomatik eşitlemek bu skill'in kapsamı dışındadır. Bkz. [GEDCOM iş akışı](references/gedcom.md).

## Depo yapısı

```
SKILL.md                         ana talimatlar (iş akışı, sert kurallar, dil politikası)
references/
  source-strategy.md             kaynak hiyerarşisi, sorgu kalıpları, kataloglar, arşiv talepleri
  correspondence.md              alıcılar, posta entegrasyonu, yetkili gönderim ve yanıtlar
  government-portals.md          nüfus kaydı hizmetleri ve talep teslim yolları
  evidence-protocol.md           materyal değerlendirmesi, durumlar, kimlik çözümü, çelişkiler
  ex-ussr-locale-guide.md        yargı alanları, ad varyantları, takvimler, döneme göre kayıt türleri
  browser-and-captcha.md         tarama, oturum açma, tek CAPTCHA denemesi ve devir, hız sınırları
  privacy-and-safety.md          yaşayan kişiler, küçükler, DNA, hassas bulgular
  seed-sources.md                derecelendirilmiş güvenilirlik sınıflarıyla başlangıç kaynakları
  field-lessons.md               gerçek bir vakadan pratik dersler
  changelog.md                   sürüm geçmişi
  photo-search.md                fotoğrafları bulma, tanımlama, tarihleme ve saklama
  habsburg-galicia-bukovina.md   Habsburg dönemi ve sonrasında Galiçya ve Bukovina
  chechnya-deportation.md        Çeçen aileler: 1944 sürgünü, özel yerleşim, adlar ve yeniden adlandırılan köyler
  germany-forced-labour.md       Almanya'da zorla çalıştırılanlar 1941-1945: Arolsen Archives ve Alman nüfus sicilleri
  bessarabia-moldova.md          Besarabya, Moldova, Moldova Özerk SSC (MASSR) ve Dinyester sınır bölgesi
  familysearch-indexes.md        hedefli tarayıcı araştırması, izin verilen yerel kopyalar ve kapsam
  familysearch-mcp.md            bağlı araçlar, yapılandırılmış okumalar, kapsamı belirlenmiş yazmalar ve doğrulama
  ww1-search.md                  GWAR I. Dünya Savaşı kişi/yerleşim araması ve kaynak görüntüsü konumlayıcıları
  gedcom.md                      kaynak ve kanıt notlu taşınabilir aile ağacı dışa aktarımları
assets/                          vaka girişi, CSV kayıt defterleri, nihai rapor şablonu,
                                 fotoğraf klasörü README şablonu, araştırma durumu şablonu, HTML rapor şablonu (report.template.html)
scripts/                         init_case.py, hash_artifact.py, audit_evidence.py, build_pdf.py
                                 familysearch.py, gwar.py, register_search.py, scan_montage.py (Pillow gerekir)
                                 htr_search.py (tanınmış sayfa metninde bulanık ad araması)
                                 check_gedcom.py (isteğe bağlı GEDCOM denetimi) ve paylaşılan yerel analiz modülleri
evals/discovery-and-logic.yaml   tetikleme ve akıl yürütme test senaryoları
tests/                           birim testleri (python3 -m unittest discover -s tests)
```

## Sorumlu kullanım

- **Aile tarihi, gözetim değil.** Skill, yaşayan kişilerin güncel adres, telefon ya da hesaplarını aramayı reddeder ve raporlarda verilerini en aza indirir.
- **Erişim kontrolleri.** Destekleniyor ve izin veriliyorsa ajan, dahili tarayıcısında normal kontroller üzerinden gerçek bir CAPTCHA'yı bir kez deneyebilir. Kullanıcı işlemi gerekirse ilgili sekmeyi mümkünse açar ve URL ile gerekli işlemi bildirir; oturum açmayı kullanıcı yapar. Harici çözücüler, koruma aşma, ödeme duvarı, coğrafi engel ya da hız sınırı atlatma, sızdırılmış veritabanları kullanılmaz. Bkz. [tarayıcı rehberi](references/browser-and-captcha.md).
- **Belgelerinizin ya da DNA verinizin üçüncü taraf hizmetlere yüklenmesi yok**, açık onayınız olmadan.
- **Hassas bulgular** (sürgün, baskı, evlat edinme, DNA sürprizleri) tarafsız biçimde ve yalnızca sorunun gerektirdiği ölçüde aktarılır.
- **Yetkili yazışma.** Skill, kullanıcı yetki verdiğinde kurumsal talepleri mevcut araçlarla gönderebilir; zaten yetkilendirilmiş bir gönderim için tekrar sormaz. Bir posta kutusunu bağlamak tek başına gönderim, ek dosya ya da ücretli hizmet için yetki vermez. Güncel resmi iletişim bilgisini ve prosedürü doğrulayın; kimlik bilgilerini ve özel vaka yazışmalarını skill deposunun dışında tutun.

## Katkı

Yeni kaynaklar `references/seed-sources.md` dosyasına memnuniyetle eklenir. Biliniyorsa doğrulanmış sahibi, yargı alanı, koleksiyonu, kökenini, kimliklerini, erişimini, kısıtlarını ve kontrol tarihini kaydedin; tahmin etmek yerine boşlukları işaretleyin. Örneklerde kişisel veri kullanmayın.

Okunabilir bir arama günlüğü varsa denetim özeti, arama günlüğünde başvurusu olmayan materyal kimliklerini listeler. Bu listeyi bağlanmamış bulguları kontrol etmek için kullanın. Kullanıcının verdiği materyaller orada görünebilir; bunun için bir işlem gerekmez.

Kaynak arama yardımcıları yalnızca Python'un standart kütüphanesini ve mevcut vaka kayıtlarını kullanır. Yerel ayrıştırmayı, GWAR kontrol noktalarını, erişim hatalarını, çözülmemiş kapsamı ve kanıt kaydını sentetik verilerle denemek için `python3 -m unittest discover -s tests` komutunu çalıştırın. FamilySearch keşfi ve hedefli görüntüleme, mevcut yasal tarayıcı oturumunu kullanır; Python yardımcıları kaydedilmiş parçaları çözümler. Özel araştırma dosyalarını bu kopyanın dışında tutun.

## Lisans

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Bakımcı: Denis Shiryaev ([@DenisSergeevitch](https://github.com/DenisSergeevitch)).

Bu skill'e ilham veren, Claude'un aile tarihi araştırmasında kullanılması üzerine konuşmalar için [Viktor](https://tiulp.in/)'a özel teşekkürler.
