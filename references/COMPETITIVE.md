# Wettbewerbsanalyse

Vorlage für Phase 3. Bis v2.4.0 war dieser Schritt eine Beschreibung in Prosa und ein einmaliger
Prompt: elf Achsen in einem Satz, kein Erhebungsweg, kein Ausgabeformat, keine Regel dafür, wer
überhaupt als Wettbewerber zählt. Zwei Durchläufe desselben Kunden konnten deshalb nichts
gemeinsam haben. Diese Datei legt beides fest, damit ein zweiter Durchlauf denselben Schnitt
zeigt wie der erste.

Wiederholbar heißt hier: gleicher Erhebungsrahmen, gleiche Achsen, gleiches Ausgabeformat, mit
Datum. Dieser Skill fährt den Schritt einmal, als Teil der Bestandsaufnahme. Wer ihn im Betrieb
regelmäßig wiederholen will, ist bei `linkedin-community-builder` richtig; die Matrix aus diesem
Lauf ist dann der erste Messpunkt.

Vor jeder Erhebung gilt [ETHICS.md](ETHICS.md) Regel 6: Fremdprofile nur mit Anlass, nur was
ohne Login und ohne Kontaktanfrage sichtbar ist, keine Speicherung über den Report hinaus,
bewertet wird der öffentliche Auftritt und nicht die Person.

## Wer als Wettbewerber zählt

Ein Wettbewerber im Sinne dieser Analyse erfüllt alle vier Bedingungen:

1. Der Kunde hat ihn in Phase 1.2, Frage 3 selbst benannt. Der Anlass nach ETHICS.md Regel 6
   entsteht durch diese Nennung und durch nichts anderes.
2. Er bespielt dieselbe Nische, nicht nur dieselbe Branche. Ein Vorstand, der einmal im Quartal
   ein Unternehmensthema postet, ist kein Wettbewerber um dieselbe Aufmerksamkeit.
3. Sein Profil ist ohne Login sichtbar, und er hat in den letzten drei Monaten gepostet. Ohne
   Aktivität gibt es nichts zu vergleichen.
4. Er ist eine Person, keine Unternehmensseite. Unternehmensseiten folgen anderen Regeln für
   Reichweite und Profil-Elemente; sie in dieselbe Matrix zu schreiben, vergleicht Ungleiches.

Nimm 3 bis 5. Unter 3 greift die Regel im Abschnitt „Wenn die Mindestzahl nicht erreicht wird".
Über 5 wird die Matrix breit und die Ableitung in Phase 3.2 beliebig.

Ausdrücklich nicht aufgenommen werden: Profile, die dem Kunden nur aufgefallen sind; Profile,
die er beobachten lassen möchte; Profile aus seinem direkten Arbeitsumfeld, mit denen er nicht
um dieselbe Sichtbarkeit konkurriert.

## Die zehn Achsen

Für jeden Wettbewerber wird auf diesen zehn Achsen erhoben, in dieser Reihenfolge. Die
Reihenfolge steht auch in SKILL.md Phase 3.1; `tests/run_eval.py` hält beide Listen gegeneinander.

| Achse | Woher | Was sie zeigt | Grenze |
|-------|-------|---------------|--------|
| Follower | Profilkopf | Größe der erreichbaren Basis | Sagt nichts über Aktivität oder Aufmerksamkeit |
| Post-Frequenz | Activity-Seite, letzte 30 Tage, Beiträge gezählt | Rhythmus und Verbindlichkeit | Urlaub oder Kampagne verzerrt einen 30-Tage-Ausschnitt |
| Median-Engagement je Beitrag | Reaktionen und Kommentare der letzten 10 Beiträge, Median | Resonanz je Beitrag, robust gegen einen Ausreißer | Follower-basiert, nicht impressions-basiert. Der Wert ist nicht mit dem Raster in SCORING.md vergleichbar (siehe SOURCES.md, „Bekannte Grenze") |
| Content-Mix | Letzte 10 Beiträge nach Thema sortiert | Worüber der Wettbewerber tatsächlich spricht | Zehn Beiträge sind eine Stichprobe, keine Redaktionslinie |
| Formate | Letzte 10 Beiträge nach Format sortiert | Welche Formate er beherrscht und welche nicht | Ein Format kann fehlen, weil es nicht passt, nicht weil er es nicht kann |
| Nischen-Fokus | Anteil der Beiträge im Kernthema, aus Content-Mix | Ob er als Experte für eine Sache lesbar ist | Braucht eine vorher definierte Nische, sonst ist der Anteil beliebig |
| Social Proof | Profil: Publikationen, Auszeichnungen, Featured, Empfehlungen | Woran ein Leser seine Autorität festmacht | Nur was im Profil steht; ein ungepflegtes Profil unterschätzt die Person |
| Newsletter | Profil und Beiträge | Ob er eine Zielgruppe direkt erreicht, am Feed vorbei | Abonnentenzahl ist nur sichtbar, wenn er sie selbst zeigt |
| Video-Anteil | Aus Formate | Ob er ein Format bedient, das Aufwand kostet | Ein hoher Anteil sagt nichts über die Wirkung |
| Top-Voice-Status | Profilkopf, Badge sichtbar oder nicht | Ob LinkedIn ihn bereits ausgezeichnet hat | Nur ein Ja oder Nein, kein Maß für Reife |

Der SSI eines Wettbewerbers gehört nicht in diese Matrix. Er ist nur für das eigene Konto unter
linkedin.com/sales/ssi ablesbar. Ein geschätzter Fremd-SSI wäre eine erfundene Zahl in einem
Kundendokument und fällt unter ETHICS.md Regel 4.

## Ausgabe

Der Schritt liefert genau ein Artefakt: die Wettbewerbsmatrix, als eigenständiges Dokument zur
Übergabe. Sie bekommt kein eigenes Kapitel im DOCX-Report; der hat neun Kapitel, und die bleiben.

Kopf des Artefakts, ohne den zwei Läufe nicht vergleichbar sind:

- Erhebungsdatum
- Name des Kunden und seine Nische in einem Satz
- Die Wettbewerber mit Profil-URL, in der Reihenfolge, in der der Kunde sie genannt hat
- Der Hinweis, dass alle Werte aus öffentlich sichtbaren Profilen stammen und wann sie erhoben
  wurden
- Ob die Mindestzahl erreicht wurde

Danach die Matrix: zehn Zeilen für die zehn Achsen, eine Spalte je Wettbewerber, eine Spalte für
den Kunden selbst. Der Kunde steht in derselben Tabelle, sonst ist die Ableitung in Phase 3.2 ein
Bauchgefühl.

Darunter die vier Ableitungen aus Phase 3.2, je zwei bis vier Sätze, jede mit dem Verweis auf die
Zeile der Matrix, aus der sie stammt:

1. Content-Lücken: Welches Thema bedient keiner der Wettbewerber?
2. Tonalitäts-Differenzierung: Wo kann sich der Kunde sprachlich absetzen?
3. Social-Proof-Vorsprung: Welche Credentials hat nur der Kunde?
4. Format-Innovation: Welches Format nutzt keiner?

Im Report wird die Matrix in Kapitel 9 als verwendete Quelle genannt, mit Erhebungsdatum und der
Zahl der einbezogenen Wettbewerber.

## Wenn die Mindestzahl nicht erreicht wird

Das Quality Gate für Phase 3 verlangt 3 Wettbewerber. Bis v2.4.0 stand daneben in der
Fehlerbehandlung ein zweiter Wert: „Minimum 2 Wettbewerber für sinnvolle Matrix", dazu der
Hinweis, bei weniger als 2 auf die Tabelle der branchenspezifischen Anpassungen auszuweichen.
Das war kein Gate, sondern zwei Zahlen und ein Ausweg. Der Ausweg war zusätzlich falsch adressiert:
jene Tabelle enthält Erfahrungswerte zu Tonalität, Format und Frequenz je Branche, sie enthält
keine Wettbewerber und kann eine Wettbewerbsanalyse nicht ersetzen.

Es gilt eine Zahl: 3. Werden weniger erreicht, dann gilt:

1. Das Gate für Phase 3 ist nicht bestanden. Das wird so vermerkt, nicht umformuliert.
2. Die Matrix wird trotzdem erstellt und übergeben, mit den erreichten Wettbewerbern, und im Kopf
   als unvollständig gekennzeichnet.
3. Die vier Ableitungen aus Phase 3.2 werden nicht aus ihr abgeleitet. Aus zwei Profilen lässt
   sich keine Lücke im Feld zeigen, sondern nur eine Beobachtung an zwei Profilen.
4. Kapitel 9 des Reports nennt die Zahl der einbezogenen Wettbewerber und dass die
   Differenzierungs-Strategie deshalb ohne die Matrix entstanden ist.

Der häufigste Grund für weniger als 3 ist kein technischer, sondern der: Der Kunde hat in Phase
1.2, Frage 3 keine 3 genannt. Frag nach, bevor du die Erhebung startest.

## Was diese Vorlage nicht leistet

`tests/run_eval.py` prüft, dass die zehn Achsen hier und in SKILL.md Phase 3.1 in derselben
Reihenfolge stehen, dass die Mindestzahl 3 in SKILL.md an beiden Stellen und hier gleich lautet,
und dass die alte zweite Zahl nirgends zurückkommt. Das sind Listen und Zahlen im Text.

Nicht geprüft wird:

- ob eine Erhebung überhaupt stattgefunden hat
- ob die eingetragenen Werte stimmen; sie sind von Hand aus einem Browser abgelesen
- ob die genannten Profile die Bedingungen im Abschnitt „Wer als Wettbewerber zählt" erfüllen
- ob jemand die Matrix ohne Anlass nach ETHICS.md Regel 6 mit weiteren Profilen füllt
- ob die vier Ableitungen tatsächlich aus der Matrix stammen oder daneben entstanden sind
