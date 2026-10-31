# ex-USSR Kinship Research

![ex-USSR Kinship Research のカバー画像](docs/cover.jpg)

Languages: [English](README.md) / [Русский](README.ru.md) / [Беларуская](README.be.md) / [Қазақша](README.kk.md) / [Українська](README.uk.md) / [Polski](README.pl.md) / [Deutsch](README.de.md) / [Română](README.ro.md) / [Eesti](README.et.md) / [Latviešu](README.lv.md) / [Lietuvių](README.lt.md) / [ქართული](README.ka.md) / [Հայերեն](README.hy.md) / [Azərbaycanca](README.az.md) / [Кыргызча](README.ky.md) / [Тоҷикӣ](README.tg.md) / [Türkmençe](README.tk.md) / [O‘zbekcha](README.uz.md) / [日本語](README.ja.md)

**AI エージェント（Codex、Claude Code、その他の Agent Skills ランタイム）向けの、エビデンスを最優先する系譜調査スキルです。** エージェントを、旧ソ連、ソビエト連邦、ロシア帝国を対象とする慎重な家族史の研究者に変えます。エージェントは教会の記録簿や戸籍記録、軍事・強制移住・弾圧に関するファイル、索引化されていないアーカイブのスキャン画像を読み解きます。あらゆる発見を追跡可能な状態に保ち、記録と解釈を区別し、何が証明済みで何が未証明なのかをはっきりと伝えます。

対象範囲には旧ソ連の 15 共和国すべてが含まれます: ロシア、ウクライナ、ベラルーシ、モルドバ、エストニア、ラトビア、リトアニア、ジョージア、アルメニア、アゼルバイジャン、カザフスタン、キルギス、タジキスタン、トルクメニスタン、ウズベキスタン。アーカイブは、その出来事の歴史的な管轄と記録の現在の保管者に基づいて選ばれます。地域ごとの例だけで、その地域に即した調査を代替できるわけではありません。

スキルの指示はロシア語で書かれていますが、**エージェントはあなたの言語で対話します**: 英語、ウクライナ語、ロシア語、ポーランド語、ドイツ語などです。出典は原文の綴りのまま翻訳を添えて引用し、検索クエリは記録の言語で組み立てます。

---

## できること

- **案件の受付と範囲設定。** 1 つの調査課題、既知の事実、存命の可能性がある人物、調査対象外の事項を整理します。
- **再現可能な登録簿。** 人物、資料、主張、関係、そして完全な検索ログ（CSV）に加え、最終報告書のテンプレートを用意します。
- **歴史的な管轄モデル。** すべての出来事を、現在の地図ではなく*その出来事の日付時点*の国家、県、郡、教区、または戸籍登録機関に割り当てます。
- **名前の表記揺れのマトリクス。** 改革前のロシア語、ウクライナ語、ポーランド語、ルーマニア語、ドイツ語、イディッシュ語の表記、父称、旧姓、翻字を扱います。
- **情報源の戦略。** まず原本、次に公式の目録、索引、刊行された史料集を調べ、家系図やフォーラムは最後に手がかりとしてのみ使います。
- **エビデンスのプロトコル。** 主張にはパーセンテージではなく、説明可能なステータスが付きます: `hypothesis`、`single-source`、`corroborated`、`strongly-corroborated`、`contradicted`、`unresolved`。1 つの記録のコピーやミラーは同じ `independence_group` を共有するため、独立した証拠として数えられることはありません。
- **同一人物の判定。** 同名の人物は、家屋番号、両親、代父母、正確な生年月日、所属部隊といった区別できる証拠が現れるまで、別々の `person_id` のままにします。
- **監査スクリプト。** 結論を書く前に参照整合性をチェックし、裏付けの弱い箇所を指摘します。独立グループは、引用された資料がそのグループに属している場合にのみ数えられるため、裏付けを宣言だけで作り出すことはできません。作業用の Markdown 報告書がある場合は、その ID とステータスもチェックします。納品する HTML は、エージェントが登録簿と照合して確認します。サマリーには、まだ裏付けのないものや判読不能とされたものが表示されます。
- **機関への問い合わせ。** 利用可能なメールや公式の Web ツールを使い、アーカイブ、図書館、大学、博物館への的を絞った問い合わせを作成し、許可されている場合は送信します。必要に応じて、対応しているメール連携か、すぐに送れる状態の書簡を提案します。結果を記録し、重複した送信を避け、返信を証拠として扱います。[やり取りに関するガイダンス](references/correspondence.md)を参照してください。
- **アーカイブへの請求フォーム。** 匿名化された [CANO の人口動態記録請求テンプレート](assets/cano-vital-record-request.template.docx)は、提供されたフォームのレイアウトを保ったまま、編集可能な案件用のコピーを作れます。使用前に、アーカイブの現行のフォームと提出要件を確認してください。
- **行政サービス。** 公式の戸籍登録やアーカイブへの請求ルートを選び、申請資格と結果の受け取り方法を確認します（[行政ポータル](references/government-portals.md)）。
- **最終報告書。** 完全な HTML 報告書がデフォルトの成果物です。各関係をひとつずつ示し、矛盾点、成果のなかった検索、具体的な次のステップを記載します。PDF は、明示的に依頼された場合にのみ出力するオプションのエクスポートです。
- **索引付き記録の的を絞った調査。** 既存の正当なブラウザーセッションを通じて、場所や DGS から関連する FamilySearch の記録簿を探し、特定の記録を閲覧し、その情報源が許可する範囲の証拠の断片だけを保存します。ローカルのヘルパーは、保存した断片の中から親族、証人、名前の表記揺れを検索し、その文脈とファイルのチェックサムを保持します。[ワークフローと対象範囲の制限](references/familysearch-indexes.md)。
- **接続済みの FamilySearch MCP。** 接続されたサーバーを使って、構造化された検索、プロフィール、親族、情報源を扱い、明示的な範囲指定と読み戻しによる確認のもとで、許可された家系図の変更を行います。索引付きの検索と、索引のないスキャン画像の読み取りは区別し、コネクターの実際のブラウザー、プライバシー、書き込みの機能を確認してください。[ワークフローとアクセスの制限](references/familysearch-mcp.md)。
- **第一次世界大戦の情報源の検索。** GWAR の報告書、病院、叙勲、捕虜の記録を人物または地域で検索し、保存したカード間で集落名の綴りを比較して歪んだ地名を解読し、そのうえで情報源の画像を特定します。[ワークフロー](references/ww1-search.md)。どちらのヘルパーも既存の資料登録簿と検索ログに情報を追加しますが、同一人物や親族関係を自動的に確定することはありません。

リリース履歴: [変更履歴](references/changelog.md)。

## インストール

Node.js がインストールされていれば、オプションの [Skills CLI](https://github.com/vercel-labs/skills) を使用できます:

```bash
npx skills add https://github.com/DenisSergeevitch/ex-ussr-kinship-research
```

CLI ではエージェントを選択でき、デフォルトでは現在のプロジェクトにインストールされます。プロジェクトをまたいで使う個人用のインストールにするには `-g` を追加してください。現在の Node.js の要件については、CLI のドキュメントを参照してください。

または、リポジトリをエージェントのスキルフォルダーに直接クローンします:

```bash
# Codex
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.codex/skills/ex-ussr-kinship-research

# Claude Code (personal skills)
git clone https://github.com/DenisSergeevitch/ex-ussr-kinship-research ~/.claude/skills/ex-ussr-kinship-research
```

単一のプロジェクトで使う場合は、リポジトリ内の `.claude/skills/` にフォルダーを置いてください。ほとんどのスクリプトに必要なのは Python 3 と標準ライブラリだけです。オプションの `scan_montage.py` ヘルパーには Pillow が、`build_pdf.py` には Chromium ベースのブラウザーが必要です。

## 使い方

家族に関する疑問を説明してください。エージェントは利用可能な情報をもとに作業し、質問やアクセスの依頼への返答を待つ間も作業を続けます。例:

- *「私の曽祖父は 1930 年代にカザフスタンへ流刑になりました。教会の記録から彼の両親を探すのを手伝ってください。」*
- *「婚姻証明書と兵士カードのスキャン画像です。同一人物かどうかを確認し、証拠の連鎖を組み立ててください。」*
- *「1890 年代のポドリアにある村の教区と、該当する FamilySearch のフィルムを見つけ、姓 X の出生記録を読んでください。」*

個人的な案件のデータは、スキルの Git チェックアウトの外に置いてください。スキルのフォルダーから実行します:

```bash
python scripts/init_case.py --case-dir ~/kinship-cases/my-case --research-question "Who were Maria's parents?" --subject-label "Maria"
python scripts/hash_artifact.py ~/kinship-cases/my-case/scans/marriage-1902.jpg   # SHA-256 for every saved artifact
python scripts/audit_evidence.py --case-dir ~/kinship-cases/my-case             # check registers before the final report
```

`init_case.py` は、`--force` を指定した場合でも、スキルのフォルダー内に案件を作成することを拒否します。
追加の安全策として、Git はよく使われる旧来の案件フォルダー名を無視します。
コントリビュートする前、特に既存の案件を移動する場合は、ステージされたファイルを確認してください。

エージェントは、`assets/report.template.html` または既存のツールを使って、`my-case/report.html` のような完全な HTML 報告書を作成します。デフォルトの編集レイアウトでは、ヘッダーに家系図を配置し、関係の証拠にはワンクリックでたどり着けます。多言語に対応した読みやすいシステムフォントのフォールバックと、小さな画面や印刷向けのレイアウトも備えています。家系図は利用可能な証拠に基づいて作られ、欠けている親族がいても報告書は遅れません。ブラウザーで直接開くか、ローカルの画像と一緒に HTML を共有してください。短い回答はテキストや Markdown のままの場合があります。明示的に依頼された形式が優先されます。家族向けの報告書だからといって PDF になるわけではありません。

PDF を明示的に依頼された場合に限り、エージェントは同じ HTML をエクスポートできます:

```bash
python scripts/build_pdf.py --html ~/kinship-cases/my-case/report.html --out ~/kinship-cases/my-case/report.pdf
```

このオプションのエクスポートには、Chrome、Chromium、または Edge のインストール（または `CHROME_PATH`）が必要です。`--png-dir` を指定すると、`pypdfium2` が利用できる場合は確認用にページを PNG としてもレンダリングします。HTML での納品には PDF のレンダラーは不要です。

PDF のエクスポートには、ローカルまたは埋め込みの画像を使った静的な HTML を使用してください。エクスポーターはアクティブな HTML やネットワーク上の画像ソースを拒否します。情報源へのリンクはクリック可能なまま残ります。レンダリングに失敗した場合、既存の出力 PDF は保持されます。

## GEDCOM による家系図

[GEDCOM](https://gedcom.io/specs/) は、プログラム間で系譜データを交換するための標準形式です。エージェントに家系図の作成やエクスポートを依頼すると、出典の引用と証拠に関するメモ付きのローカルの `.ged` ファイルを作成します。互換性のため、デフォルトは UTF-8 の GEDCOM 5.5.1 です。あなたや選択したプログラムが必要とする場合は、GEDCOM 7 など、対応している別のバージョンを使用してください。

既存の家系図は調査の入力であり手がかりの集まりであって、その関係を証明するものではありません。エージェントは元のファイルを保持し、未解決の主張、裏付けのない詳細、証拠の登録簿、検索ログを案件フォルダーに残します。エクスポートは評価済みの証拠に従い、あなたのファイルを上書きすることはありません。

ソフトウェアはあなたが選びます。家系図アプリのインストール、MCP 接続の設定、外部の家系図との自動同期は、このスキルの範囲外です。[GEDCOM のワークフロー](references/gedcom.md)を参照してください。

## リポジトリの構成

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

## 責任ある利用

- **監視ではなく家族史のために。** このスキルは、存命の人物の現住所、電話番号、アカウントの調査を拒否し、報告書に含まれる彼らのデータを最小限に抑えます。
- **アクセスのチェック。** エージェントは、対応していて許可されている場合、内部ブラウザーの通常のコントロールを通じて実際の CAPTCHA に一度だけ挑戦することがあります。ユーザーの操作が必要な場合は、可能であれば該当するタブを開き、URL と必要な操作を伝えます。サインインはユーザーが行います。外部のソルバー、保護の回避、ペイウォール・地域制限・レート制限の回避、流出したデータベースは使用しません。[ブラウザーに関するガイダンス](references/browser-and-captcha.md)を参照してください。
- **あなたの書類や DNA データを**、明示的な同意なしに第三者のサービスへ**アップロードすることはありません**。
- **センシティブな発見**（強制移住、弾圧、養子縁組、DNA による予期せぬ事実）は、中立的に、かつ質問に必要な範囲でのみ報告します。
- **許可されたやり取り。** ユーザーが許可した場合、このスキルは利用可能なツールを通じて機関への問い合わせを送信できます。すでに許可された送信について改めて確認することはありません。メールボックスを接続しただけでは、送信、添付ファイル、有料サービスの利用は許可されません。現在の公式の連絡先と手続きを確認し、認証情報や個人的な案件のやり取りはスキルのリポジトリの外に置いてください。

## コントリビュート

新しい情報源は `references/seed-sources.md` への追加を歓迎します。判明している場合は、確認済みの所有者、管轄、コレクション、来歴、ID、アクセス、制限、確認日を記録してください。推測するのではなく、不明な点はそのように明記してください。例には個人データを含めないでください。

情報源検索のヘルパーは、Python の標準ライブラリと既存の案件の登録簿を使用します。`python3 -m unittest discover -s tests` を実行すると、ローカルでのパース、GWAR のチェックポイント、アクセスの失敗、未解決の対象範囲、証拠の登録を、合成データに対してチェックできます。FamilySearch での探索と的を絞った閲覧には既存の正当なブラウザーセッションを使用し、その Python のヘルパーは保存された断片を分析します。個人的な調査ファイルはこのチェックアウトの外に置いてください。

## ライセンス

[MIT](LICENSE) © 2026 Denis Shiryaev.

---

Denis Shiryaev（[@DenisSergeevitch](https://github.com/DenisSergeevitch)）がメンテナンスしています。
