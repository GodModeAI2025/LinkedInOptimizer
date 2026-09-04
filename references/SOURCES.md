# Quellen und Datenbasis

**Stand:** 2026-09-04
**Nächste Prüfung:** 2027-03-04 (halbjährlich)
**Geprüft von:** Repo-Wartung, Welle 5

Dieser Skill trifft Aussagen über den LinkedIn-Algorithmus, über Badge-Kriterien und über
Kennzahlen. Diese Datei sagt für jede dieser Aussagen, worauf sie beruht, wann die Quelle
veröffentlicht wurde und wann sie zuletzt abgerufen wurde. Aussagen ohne belegbare Quelle
stehen unter „Zurückgezogen" und sind aus SKILL.md, SCORING.md, README.md, der Landingpage
und dem Report-Template entfernt.

Die Regel für künftige Änderungen: Eine Zahl darf nur dann in den Skill, wenn sie hier eine
Zeile mit URL und Veröffentlichungsdatum bekommt. Wer eine Zahl nicht belegen kann, streicht
die Aussage, statt eine Quelle zu suchen, die ungefähr passt.

`scripts/check_sources.py` prüft bei jedem CI-Lauf, dass jede im Skill verwendete Quellen-ID
hier existiert, dass jede Zeile eine URL und ein Datum trägt und dass das Prüfdatum nach dem
Stand liegt. Gesucht wird nach jedem Vorkommen von `Qn`, gleich in welcher Klammer und welchem
Satzbau, damit eine ausgedachte Belegangabe nicht über eine andere Schreibweise ins Paket kommt.

Die Sperren gegen zurückgezogene Aussagen erzeugt dasselbe Skript aus der Spalte „Sperrmuster"
der Tabelle weiter unten. Jede Zeile trägt ein Muster; es gibt keinen Weg, eine Zeile über die
Tabelle von der Sperre zu befreien. Die Sperren prüfen Schreibweisen, keine Aussagen. Ein frei
formulierter Satz, der eine zurückgezogene Behauptung in neuen Worten aufstellt, fällt ihnen
nicht auf. Für die eine Behauptung, bei der das teuer wäre, steht in `check_sources.py` eine
zweite, engere Prüfung: Ein Absatz, der Collaborative Articles und ein Badge in einem Zug nennt,
muss Q3 zitieren. Das ist eine Schwelle und kein Beweis. Wer die falsche Aussage mit der richtigen
Quellenangabe hinschreibt, kommt weiterhin durch.

---

## Belegte Quellen

| ID | Belegt | Quelle | URL | Veröffentlicht | Abgerufen | Einstufung |
|----|--------|--------|-----|----------------|-----------|------------|
| Q1 | Dwell Time ist ein Ranking-Signal im LinkedIn-Feed. LinkedIn misst, wie lange ein Beitrag betrachtet wird, und nutzt das, weil Klicks und Reaktionen selten und binär sind. | LinkedIn Engineering Blog, „Understanding dwell time to improve LinkedIn feed ranking" | https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time | 2020-05-12 | 2026-09-04 | Primärquelle (Plattformbetreiber) |
| Q2 | LinkedIn setzt für das Feed-Ranking ein eigenes, groß angelegtes Ranking-Modell ein. Die Zusammenfassung nennt Feed-Ranking als einen der Einsatzorte und einen Effekt auf Mitglieds-Sessions. | Borisyuk et al., „LiRank: Industrial Large Scale Ranking Models at LinkedIn", arXiv:2402.06859 | https://arxiv.org/abs/2402.06859 | 2024-02-10 (v2: 2024-08-07) | 2026-09-04 | Primärquelle (Publikation des Betreibers) |
| Q3 | Das goldene Community-Top-Voice-Badge ist zurückgezogen. Es lässt sich seit dem 08.10.2024 nicht mehr über Beiträge zu Collaborative Articles verdienen. | LinkedIn Help, „Community Top Voices (Gold Badge)" | https://www.linkedin.com/help/linkedin/answer/a6245087 | Abrufstand, kein Veröffentlichungsdatum auf der Seite; Wirksamkeit laut Text ab 2024-10-08 | 2026-09-04 | Primärquelle (Plattformbetreiber) |
| Q4 | Das blaue LinkedIn-Top-Voices-Badge wird nur auf Einladung vergeben. Nominierungen prüft LinkedIn quartalsweise. | LinkedIn Help, „LinkedIn Top Voices" | https://www.linkedin.com/help/linkedin/answer/a776208/linkedin-top-voices | Abrufstand, Seite nennt kein Veröffentlichungsdatum | 2026-09-04 | Primärquelle (Plattformbetreiber) |
| Q5 | Der Social Selling Index besteht aus vier Elementen: Professional Brand, Find the Right People, Engage with Insights, Build Relationships. Er ist für alle Mitglieder unter linkedin.com/sales/ssi abrufbar. | LinkedIn Sales Blog, „Get Your Score: LinkedIn Makes the Social Selling Index Available for Everyone" | https://www.linkedin.com/business/sales/blog/modern-selling/get-your-score-linkedin-makes-the-social-selling-index-available-for-everyone | 2015-08-03 | 2026-09-04 | Primärquelle (Plattformbetreiber) |
| Q6 | LinkedIn-Engagement-Raten liegen in Anbieter-Benchmarks branchenabhängig im niedrigen einstelligen Prozentbereich. Die Seite nennt Werte je Branche, aber weder Nenner noch Erhebungszeitraum. | Hootsuite Blog, „Social media benchmarks" | https://blog.hootsuite.com/social-media-benchmarks/ | 2026-04-14 (fortlaufend aktualisiert) | 2026-09-04 | Anbieterstudie |
| Q7 | Der Creator-Mode-Schalter ist entfallen. LinkedIn hat ihn im März 2024 entfernt; Newsletter, LinkedIn Live, Audio Events, Creator-Analytics und der Follow-Link bleiben ohne Schalter verfügbar. | LinkedIn Help, „Updates to Creator Mode" | https://www.linkedin.com/help/linkedin/answer/a5999182 | Abrufstand, Wirksamkeit laut Text ab März 2024 | 2026-09-04 | Primärquelle (Plattformbetreiber) |

### Was diese Quellen ausdrücklich nicht belegen

- **Q1** belegt, dass Dwell Time als Signal genutzt wird. Sie belegt kein Gewicht, keinen
  Prozentwert und keinen Stand 2025 oder 2026. Der Beitrag ist von 2020.
- **Q2** nennt in der Zusammenfassung Feed-Ranking als Einsatzort und einen Effekt auf
  Mitglieds-Sessions. Sie nennt dort weder Dwell Time noch einzelne Ranking-Gewichte.
- **Q5** benennt die vier Säulen. Die verbreitete Aufteilung „4 × 25 Punkte" steht dort nicht.
  Sie stammt aus Anbieter- und Beratungsquellen und wird hier als plausible, aber
  unbestätigte Konvention geführt.
- **Q6** trägt keinen Plattformdurchschnitt für LinkedIn und keine Angabe zum Nenner. Die im
  Repo früher genannten 3,4 % lassen sich damit nicht belegen, siehe unten.

---

## Zurückgezogen

Diese Aussagen standen bis Version 2.3.0 im Skill und sind ohne Ersatz entfernt worden. Der
Grund steht jeweils dabei. Sie kommen nur zurück, wenn jemand eine Quelle mit URL und Datum
beibringt.

Die Spalte **Sperrmuster** ist der maschinenlesbare Teil dieser Tabelle. `scripts/check_sources.py`
baut daraus die Regex, mit der es die ausgelieferten Dateien absucht. Mehrere Muster werden mit
Semikolon getrennt. Geschrieben werden sie so, wie die Aussage früher im Skill stand; das Skript
normalisiert selbst: `3,4` fängt auch `3.4`, `%` fängt auch das ausgeschriebene Prozent, `×` fängt
auch das ASCII-x, Leerzeichen fangen auch `&nbsp;` und den Bindestrich (`Creator Mode` fängt also
auch `Creator-Mode`), Umlaute fangen auch ihre ae-Umschrift, Bindestriche fangen auch die
typografischen Varianten, ein führendes `+` oder `~` ist optional, Groß- und Kleinschreibung ist
egal. Drei Punkte im Muster stehen für eine Lücke von bis zu 40 Zeichen in derselben Zeile:
`Umfragen...~5 %` fängt auch `Umfragen erreichen ~5 %`.

Vier Regeln für neue Zeilen:

1. Jede Prozentangabe und jeder Faktor in der Spalte „Frühere Aussage" muss von einem Sperrmuster
   derselben Zeile getroffen werden. Das prüft `check_sources.py` gegen die Tabelle selbst. Wer
   eine Zahl zurückzieht und die Sperre vergisst, fällt im CI-Lauf auf.
2. Runde Werte wie 5 %, 20 % oder 40 % bekommen ein Kontextwort ins Muster, weil dieselbe Zahl an
   anderer Stelle im Repo legitim vorkommt. Unverwechselbare Werte wie 3,4 % oder 2,5× stehen
   allein.

3. Jede Zeile trägt ein Muster. Es gibt keine Möglichkeit, eine Zeile hier von der Sperre zu
   befreien. Eine frühere Fassung erlaubte dafür `keine:` und eine beliebige Begründung; damit
   ließ sich jede Sperre durch das Ändern einer Tabellenzelle abschalten, auch die gegen den
   Creator Mode. Wenn ein Textverbot an einer Stelle wirklich schaden würde, weil es richtige
   Verneinungen mit treffen würde, gehört die Aussage in `BEHAUPTUNGS_REGELN` in
   `scripts/check_sources.py`. Das ist ein Codediff und keine Tabellenzelle.
4. Mindestens ein Muster der Zeile muss den eigenen Wortlaut in der Spalte „Frühere Aussage"
   treffen. Das prüft `check_sources.py` ebenfalls gegen die Tabelle selbst und erdet die
   Sperre am zurückgezogenen Text. Ohne diese Regel genügte irgendein Wort in der Zelle: die
   Zeile bliebe stehen, der Zähler stimmte, und die Sperre liefe ins Leere. Deshalb trägt die
   Spalte „Frühere Aussage" den Wortlaut, wie er im Skill stand, und nicht nur eine
   Umschreibung. Was offen bleibt: ein Muster lässt sich auf einen Teil des Wortlauts
   verengen, etwa von „Creator Mode" auf „Creator Mode aktiv". Das fällt hier nicht auf,
   steht aber als Änderung in der Tabelle und damit im Diff.

| Frühere Aussage | Stand bis | Warum entfernt | Sperrmuster |
|-----------------|-----------|----------------|-------------|
| „Engagement-Benchmarks: Hootsuite 2025 (3,4 % Plattform-Ø)" (README, Landingpage, Report-Template) | v2.3.0 | Die genannte Quelle führt diesen Wert nicht. Ihre aktuelle Fassung nennt Branchenwerte ohne Nenner und ohne Erhebungszeitraum. Ein Plattformdurchschnitt ohne definierten Nenner ist als Vergleichsmaßstab wertlos. | 3,4 % |
| „Top-performende Formate: Multi-Image 6,6 %, PDF-Karussells 6,1 %, Video (<60s) 5,6 %, Umfragen ~5 %" (SKILL.md Phase 6) | v2.3.0 | Keine prüfbare Primärquelle. Die öffentlich zugänglichen Anbieterstudien nennen für dieselben Formate deutlich abweichende Werte und wechseln sie jährlich. Die Reihenfolge der Formate bleibt als Erfahrungswert stehen, die Prozentwerte nicht. | 6,6 %; 6,1 %; 5,6 %; Umfragen...~5 % |
| „steigert Profilaufrufe um 55 % und eigene Content-Reichweite um 20 %" (SKILL.md Phase 6.2) | v2.3.0 | Keine Quelle auffindbar. Die Empfehlung, täglich substanziell zu kommentieren, bleibt als Erfahrungswert. | 55 %; Content-Reichweite um 20 %; +20 % Content-Reichweite |
| „Kommentare >15 Wörter haben 2,5× mehr algorithmisches Gewicht" (SKILL.md Phase 6.2, SCORING.md) | v2.3.0 | Kein belegbarer Faktor. Dass längere, inhaltliche Kommentare besser wirken als kurze Zustimmung, bleibt als Erfahrungswert; die Zahl 2,5 nicht. | 2,5×; 2,5-fach |
| „Back-to-Back-Posts im selben Format können Performance um 20 % reduzieren" (SCORING.md) | v2.3.0 | Kein Beleg. Die Regel, Formate abzuwechseln, bleibt ohne Prozentwert. | um 20 % reduzieren; minus 20 % |
| „Posts behalten seit 2025 bis zu 5 Tage Sichtbarkeit" (SCORING.md) | v2.3.0 | Weder die Zahl noch das Jahr sind belegbar. | 5 Tage Sichtbarkeit |
| „persönliche Requests (+40 % Akzeptanz)" (SKILL.md Phase 7) | v2.3.0 | Kein Beleg. Die Empfehlung, Kontaktanfragen zu personalisieren, bleibt ohne Prozentwert. | +40 % Akzeptanz |
| Zeile „Engagement-Benchmark 3,6 % / 3,3 % / 3,2 % / 3,2 % / 3,3 %" in der Branchentabelle (SKILL.md) | v2.3.0 | Fünf branchenspezifische Werte auf eine Nachkommastelle, ohne Quelle, ohne Nenner und ohne Erhebungszeitraum. Die übrigen Zeilen der Tabelle sind als Erfahrungswerte gekennzeichnet und bleiben. | 3,6 %; 3,3 %; 3,2 % |
| „Halbjährliche Überprüfung seit Januar 2025" zum Top-Voice-Badge (SKILL.md, README) | v2.3.0 | Falsch. LinkedIn prüft Nominierungen laut Q4 quartalsweise, und das goldene Community-Badge ist laut Q3 seit dem 08.10.2024 zurückgezogen. | Halbjährliche Überprüfung; Halbjährliche Review |
| Rahmung des Punkterasters als „Industrie-Benchmark" (SKILL.md, README, Landingpage) | v2.3.0 | Das Raster in SCORING.md ist ein internes Bewertungsschema dieses Skills. Es gegen einen Branchenwert zu stellen, den es nicht gibt, macht aus einer Setzung eine Messung. | Industrie-Benchmark |
| Rahmung der Punktebänder als „Engagement-Rate-Benchmarks" (SCORING.md) | v2.3.0 | Dieselbe Rahmung eine Ebene tiefer. Die Bänder sind ein Raster, kein erhobener Vergleichswert. | Engagement-Rate-Benchmarks |
| „Dieser Skill ist evidenzbasiert." (SKILL.md, README, Landingpage) | v2.3.0 | Von zehn Kategoriegewichten ist keines gemessen, und die Zahlen in dieser Tabelle mussten zurückgezogen werden. Belegt sind die sieben Aussagen oben, nicht der Skill als Ganzes. Das Muster fasst nur die Selbstbeschreibung: das Wort allein steht in der Branchentabelle in SKILL.md als Tonfall für Healthcare und ist dort in Ordnung. | Skill ist evidenzbasiert; evidenzbasierter Skill |
| Sub-Kriterium „Collaborative Articles" in der Kategorie Top Voice Readiness. Wortlaut bis v2.3.0: „Social Proof + Collaborative Articles" und „Regelmäßige Beiträge zu LinkedIn Collaborative Articles" (SCORING.md), „Collaborative Articles beitragen" (SKILL.md Phase 7) | v2.3.0 | Zahlte auf das goldene Community-Badge ein, das laut Q3 nicht mehr vergeben wird. Der Punkt liegt jetzt bei „Momentum". | Collaborative Articles beitragen; Beiträge zu LinkedIn Collaborative Articles; Social Proof + Collaborative Articles |
| Checklistenpunkt „Creator Mode aktiv" in der Profil-Vollständigkeit (SCORING.md) | v2.3.0 | Den Schalter gibt es laut Q7 seit März 2024 nicht mehr. Ersetzt durch die Nutzung der Creator-Tools, die ohne Schalter verfügbar bleiben. Der Begriff ist gesperrt, mit und ohne Bindestrich; über den entfallenen Schalter wird im Changelog über Q7 geredet, nicht über seinen Namen. | Creator Mode |

---

## Erfahrungswerte ohne Quelle

Diese Angaben sind keine Messwerte und werden im Skill ausdrücklich als Erfahrungswerte aus
der Beratungspraxis geführt. Sie sind nachvollziehbar begründet, aber nicht belegt, und dürfen
nicht als Benchmark gegen ein Kundenprofil gehalten werden:

- Zeichenlängen und Aufbau für Headline und About-Sektion, einschließlich der Grenze von
  220 Zeichen und der Empfehlung, die ersten 60 Zeichen als stärkstes Signal zu behandeln.
- Posting-Frequenz 3 bis 5 Beiträge pro Woche, Postingzeiten, Reaktionsfenster nach dem Post.
- Die Empfehlung, im DACH-Markt auf Emojis in der Headline zu verzichten.
- Die Formatreihenfolge in Phase 6 (Dokument- und Multi-Image-Beiträge vor Text- und
  Link-Beiträgen).
- Die Zielwerte im KPI-Dashboard in SKILL.md Phase 8.3. Das sind selbst gesetzte Ziele, keine
  Branchenwerte.
- Die Punktebänder in `references/SCORING.md`. Sie sind ein internes Bewertungsraster, mit dem
  sich Profile untereinander vergleichen lassen, und kein Industriestandard.

---

## Bekannte Grenze: Nenner der Engagement-Rate

`references/SCORING.md` definiert die Engagement-Rate als Reaktionen geteilt durch Impressions.
`scripts/generate_report.js` kann Impressions nicht erheben, weil LinkedIn sie für fremde
Profile nicht ausweist, und schätzt die Rate deshalb aus der Follower-Zahl. Beide Werte tragen
denselben Namen, meinen aber nicht dasselbe: Der follower-basierte Wert liegt systematisch
höher, weil ein Beitrag in der Regel nur einen Teil der Follower erreicht und zugleich
Nicht-Follower erreichen kann.

Solange das so ist, gilt im Skill:

1. Die Bänder in SCORING.md gelten für den impressions-basierten Wert. Sie werden nicht auf
   den geschätzten Wert angewendet.
2. Der geschätzte Wert wird im Report als geschätzt gekennzeichnet und ausschließlich im
   Zeitverlauf desselben Profils verglichen, nicht gegen ein anderes Profil.
3. Liegen echte Impressions vor, weil es das eigene Profil ist, wird der impressions-basierte
   Wert verwendet und im Report als solcher benannt.

---

## Prüfrhythmus

Halbjährlich, jeweils zum Stand-Datum plus sechs Monate. Zu prüfen ist bei jedem Durchgang:

1. Sind die URLs in der Tabelle noch erreichbar und tragen sie noch dieselbe Aussage?
2. Hat LinkedIn Badge-Kriterien oder das SSI-Modell geändert?
3. Lässt sich eine der zurückgezogenen Zahlen inzwischen belegen?
4. Stand-Datum und nächstes Prüfdatum in dieser Datei hochsetzen, den Changelog in SKILL.md
   ergänzen und die Angabe auf der Landingpage nachziehen.
