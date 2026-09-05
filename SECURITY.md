# Sicherheitsrichtlinie

Dieses Repo enthält einen Claude-Skill aus Markdown und zwei Hilfsskripten, keinen laufenden Dienst. Das Hauptrisiko liegt deshalb nicht bei einem Angreifer gegen die Software, sondern bei der Software als Verarbeiter personenbezogener Daten. Dieses Dokument beschreibt, was der Skill technisch tut. Ob eine konkrete Verarbeitung zulässig ist, bewertet es nicht.

## Unterstützte Versionen

Es gibt kein Release und kein Tag. Unterstützt wird ausschließlich der aktuelle Stand von `main`.

| Stand | Unterstützt |
|-------|-------------|
| `main`, aktueller Commit | ja |
| ältere Commits, Forks, lokale Kopien im Skill-Verzeichnis | nein |

Die Versionsangaben im Repo taugen nicht als Referenz: `README.md:1` sagt v2.1, `README.md:43` sagt v2.2.0, `SKILL.md:13` sagt v2.2, der Changelog in `SKILL.md:388` sagt v2.2.2. Auch Zeilenangaben in der Doku stimmen nicht, `SKILL.md:391` verortet den Kundendatenblock von `generate_report.js` auf "Zeile 80-150", tatsächlich steht er auf `:37-149`. Bezieh dich in einer Meldung auf den Commit-SHA.

## Schwachstelle melden

Private Vulnerability Reporting ist für dieses Repo aktiviert. Meldeweg:

https://github.com/GodModeAI2025/LinkedInOptimizer/security/advisories/new

Kein öffentliches Issue für Schwachstellen. Der Issue-Tracker des Repos ist offen, die Regel ist also keine Formalität. Sie gilt auch für Datenschutzbefunde, wenn also im Repo oder in einem generierten Artefakt echte Personendaten auftauchen.

Reaktionszeiten: Eingangsbestätigung innerhalb weniger Tage, inhaltliche Einschätzung innerhalb von zwei Wochen. Eine Einzelperson pflegt das Projekt. Wenn eine Meldung dringend ist, schreib das in den Titel.

## Bedrohungsmodell

**Der Skill als Verarbeiter.** `SKILL.md:37` legt die Datenerhebung auf das Chrome-Plugin fest: `navigate` zum Profil, dann `get_page_text`, `read_page` und `javascript_tool`. Die JS-Snippets in `SKILL.md:48-61` und `SKILL.md:68-86` lesen Headline, About, Featured-Section und die Activity-Seite `/in/username/recent-activity/all/` aus. `SKILL.md:63` listet auf, was systematisch erfasst wird, darunter Ausbildung, Zertifikate, Follower, Connections und Empfehlungen (erhalten/erteilt).

**Wo Dritte ins Spiel kommen.** Phase 1.1 zielt auf das Profil des Kunden, der die Analyse beauftragt hat. Trotzdem landen dort schon fremde Daten: Empfehlungen tragen Namen und Text der Person, die sie geschrieben hat, erteilte Empfehlungen benennen die Empfänger. Die eigentliche Verarbeitung Unbeteiligter steht in Phase 3 (`SKILL.md:146-158`, Kernsatz `:150`), wo drei bis fünf Wettbewerber nach Follower, Post-Frequenz, Engagement, Content-Mix und Social Proof analysiert werden. Genannt werden sie vom Kunden in Interviewfrage 3 (`SKILL.md:99`). Phase 3 nennt keine eigene Datenquelle, es gilt die Kaskade aus Phase 1.0 und der Satz in `SKILL.md:350`, Chrome sei IMMER die primäre Quelle. Dazu Phase 6.2 (`SKILL.md:223`) mit 15 bis 20 Ziel-Accounts (Top Voices, C-Level, Journalisten, Peers). Die zugehörige Vorlage `references/TEMPLATES.md:437-443` hat je Kategorie eine Spalte `[Namen eintragen]`, die Namen gehen also ins Kunden-Deliverable. Keine dieser Personen hat die Verarbeitung angefragt.

**Der Report als Datenträger.** Das Template `scripts/generate_report.js` ist selbst generisch und enthält Platzhalter ("Max Mustermann" in `:37-46`, "[Begründung]" in `:50-59`). Das Risiko ist die befüllte Kopie. Sie setzt den Klarnamen auf die Titelseite (`:177`), dazu Position, Unternehmen, Standort, Profil-URL, Follower und Connections (`:179-189`), sowie die Post-Historie mit geschätzter Engagement-Rate (`:225-230`). Der Ausgabepfad in `:277` ist fest verdrahtet: `/mnt/user-data/outputs/${PROFILE.name}-LinkedIn-Analyse.docx`. Der Name der analysierten Person steht damit im Dateinamen.

**Das Repo als Abflussweg.** `SKILL.md:252` weist an, das Report-Skript ins Arbeitsverzeichnis zu kopieren und den Datenblock `generate_report.js:37-149` mit echten Kundendaten zu füllen. Ist dieses Arbeitsverzeichnis das Skill-Verzeichnis, liegt die gefüllte Kopie neben getrackten Dateien. Es gibt keine `.gitignore`. `README.md:31` verspricht ein Verzeichnis `assets/` für Kundenassets wie Logos und Cover; das Verzeichnis existiert nicht, und nichts schließt es oder `*.docx` vom Commit aus.

**Klassische Angriffsfläche, kurz.** `scripts/create_banner.py` importiert PIL, os, argparse und sys (`:17-20`), nimmt Bildpfade und Texte aus argv (`:235-243`) und schreibt nach `--output` (`:221`). Das Skript öffnet keine Netzwerkverbindung, deserialisiert nichts und startet keine Shell. Ein Robustheitsdetail: `:221` speichert die Datei, die Assertions auf Bildmaße und Dateigröße folgen erst in `:224-226`. Ein zu großes Banner liegt beim Abbruch bereits auf der Platte und wird nicht entfernt. `index.html` ist statisch, ein grep nach `<script`, `<form` und Analytics-Aufrufen liefert nichts. Einzige externe Ressource sind Google Fonts (`index.html:8-9`), die Besucher-IPs erreichen damit Google.

## Vertrauensgrenzen

Als vertrauenswürdig behandelt wird genau eine Sache: die eingeloggte Chrome-Sitzung des Nutzers. Der Skill erbt deren Rechte und sieht, was der Nutzer sieht. Es gibt keine eigene Autorisierung und keine Prüfung pro Profil, ob dieses Profil ausgelesen werden darf.

Damit ist `SKILL.md` selbst privilegierter Inhalt. Der Code in `SKILL.md:48-61` und `SKILL.md:68-86` läuft in der authentifizierten LinkedIn-Sitzung. Ein Pull Request, der diese Snippets ändert, ändert, was mit der Sitzung des Nutzers passiert. Review von Skill-Markdown ist hier Code-Review.

Nicht vertrauenswürdig ist der Seiteninhalt, in zwei Richtungen.

Der Text. `get_page_text` und `read_page` (`SKILL.md:37`, `:46`) holen Text, den Dritte geschrieben haben: fremde Posts, About-Texte, Empfehlungen, in Phase 3 ganze Wettbewerberprofile. Dieser Text geht in den Kontext desselben Modells, das im selben Zug `javascript_tool` auf dem eingeloggten LinkedIn-Tab ausführen darf. Wer Anweisungen in ein LinkedIn-Profil schreibt, schreibt sie in den Kontext dieses Skills. `references/UNTRUSTED.md` markiert diesen Text als Datum und verbietet, ihm zu folgen; die Regel steht in Phase 1.1 und 3.1 vor der Erhebung. Sie ist eine Anweisung an das Modell und kein Riegel im Code.

Die Struktur. Die Selektoren greifen unscharf (`[class*="text-body-medium"]` in `SKILL.md:50`, `[class*="feed-shared-update-v2"]` in `SKILL.md:70`). Ändert LinkedIn das Markup, liefert die Extraktion stillschweigend leere oder falsche Werte, und nichts im Skill schlägt Alarm.

Die Einwilligung endet beim Kunden. Alle anderen Personen, die in den Daten auftauchen, stehen außerhalb dieser Grenze. Seit v2.5.0 gibt es dafür eine Regel, aber weiterhin keinen Mechanismus: `references/ETHICS.md` Regel 6 lässt ein Fremdprofil nur zu, wenn der Kunde es in Phase 1.2, Frage 3 selbst benannt hat oder es ein Ziel-Account der Kommentar-Strategie aus Phase 6.2 ist. Das ist eine Anweisung an das Modell, kein Riegel im Code.

## Bekannte Lücken

1. **Kein Wort zu Datenschutz im Repo.** Ein grep über `SKILL.md`, `references/`, `scripts/`, `README.md` und `index.html` nach Datenschutz, DSGVO, personenbezogen, Einwilligung, Löschung und privacy liefert null Treffer. Dieses Dokument ist der erste Text dazu.
2. **Keine Löschroutine, keine Aufbewahrungsfrist.** Nirgends steht, wann die Profildaten aus Phase 1, die befüllte Kopie von `generate_report.js` und der fertige Report gelöscht werden. Kein Schritt stößt das nach der Übergabe an.
3. **Schutz gegen Anweisungen aus fremden Profilen nur als Regel.** Seit dieser Fassung ist erhobener Seitentext ausdrücklich als Datum gekennzeichnet: `references/UNTRUSTED.md` führt die Regel und fünf Unterregeln, SKILL.md verweist in Phase 1.1 und Phase 3.1 darauf, bevor die erste Erhebung läuft, und `tests/run_eval.py` prüft, dass beide Verweise stehen. Damit ist die Lücke benannt und im Weg, aber nicht geschlossen: es gibt weiterhin keine Trennung zwischen Skill-Anweisung und Profilinhalt auf Werkzeugebene. Dasselbe Modell, das den fremden Text liest, hält im selben Zug `javascript_tool` auf der angemeldeten Sitzung. Geschlossen wäre die Lücke erst durch eine Erhebung ohne Ausführungsrechte.
4. **Kein Hinweis auf die LinkedIn-Nutzungsbedingungen.** `SKILL.md:35` und `SKILL.md:350` halten fest, dass LinkedIn robots.txt-basierte Zugriffe blockiert, und leiten daraus die Chrome-Route ab. Dass es Nutzungsbedingungen zum automatisierten Auslesen gibt, erwähnt das Repo nicht. Wer den Skill einsetzt, muss das selbst prüfen.
5. **Einwilligungsstufe für Dritte nur als Regel, nicht als Schranke.** Bis v2.4.0 benannten Phase 3 und Phase 6.2 Personen, ohne dass ein Schritt gefragt hätte, ob diese Verarbeitung gedeckt ist. Seit v2.5.0 steht die Frage im Text: `references/ETHICS.md` Regel 6 definiert den Anlass, Phase 1.2 Frage 3 hält fest, dass die Nennung durch den Kunden dieser Anlass ist, Phase 3 verweist vor der ersten Erhebung darauf, und `references/COMPETITIVE.md` nennt vier Bedingungen, die ein Profil erfüllen muss, dazu ausdrücklich die Fälle, die nicht aufgenommen werden. Unverändert offen bleibt der wirksame Teil: Es gibt keinen Code, der eine Erhebung verweigern könnte, kein Audit-Log darüber, welche Profile angesehen wurden, und keine Prüfung, ob ein erhobenes Profil die vier Bedingungen tatsächlich erfüllt. `tests/run_eval.py` bindet nur die Listen und Zahlen im Text; das steht so in COMPETITIVE.md unter „Was diese Vorlage nicht leistet".
6. **Beispieldaten sind nicht erfunden.** `TEMPLATES.md:23`, `:35`, `:46` und `:57` nutzen die echte Position und den echten Arbeitgeber des Autors, `TEMPLATES.md:284` einen realen Firmen-Hashtag als Klammerbeispiel, `SCORING.md:44-47` dieselben Angaben als Bewertungsbeispiele. Das sind öffentliche Daten des Autors selbst (`index.html:1120` verlinkt sein Profil), kein Leck fremder Daten. Die Regel gilt trotzdem: Beispieldaten in diesem Repo müssen erfunden sein. Ein Template mit echtem Arbeitgeber lädt dazu ein, in dieselben Felder echte Kundendaten zu setzen, und es gibt keine `.gitignore`, die das auffängt.
7. **Kein `.gitignore`, kein `assets/`.** Siehe Threat Model. Solange beides fehlt, hängt es an der Disziplin des Nutzers, ob Kundendaten im Repo landen.
8. **Ausgabepfad nicht konfigurierbar, keine Anonymisierung.** `generate_report.js:277` verdrahtet `/mnt/user-data/outputs/`. Das Verzeichnis existiert nur in der Claude-Sandbox. Fehlt es, wirft `writeFileSync` in `:278` ENOENT, einen `catch` gibt es nicht, der Fehler landet als unhandled rejection. Ein `--output`-Argument fehlt, ein Modus ohne Klarnamen ebenfalls. Der Report gehört in ein Verzeichnis, das der Kunde kontrolliert, und nach der Übergabe gelöscht. Nicht in dieses Repo, einen Fork oder einen automatisch synchronisierten Ordner.
9. **Der dokumentierte Validierungsschritt läuft nicht.** `SKILL.md:262` und `SKILL.md:366` weisen an, das DOCX mit `python scripts/office/validate.py` zu prüfen, `SKILL.md:342` macht die bestandene Validierung zum Abnahmekriterium vor der Übergabe. Weder die Datei noch das Verzeichnis `scripts/office/` existieren im Repo.
10. **Keine Prüfung der Extraktionsqualität.** Das Repo enthält kein Testverzeichnis und keine Fixtures. Ob die Snippets aus Phase 1.1 noch das lesen, was sie lesen sollen, fällt erst im Report auf, wenn überhaupt.

## Was dieses Projekt nicht leistet

**Keine Rechtsberatung.** Der Skill trifft keine Aussage darüber, ob eine bestimmte Verarbeitung nach DSGVO zulässig ist. Dieses Dokument bewertet ebenso wenig, ob der Weg über die eingeloggte Chrome-Sitzung mit den LinkedIn-Nutzungsbedingungen vereinbar ist. Rechtsgrundlage, Informationspflicht gegenüber den Betroffenen und die Bearbeitung von Betroffenenrechten liegen beim Nutzer.

**Keine Zusicherung zur Datenqualität.** Das Scoring ist eine Heuristik ohne empirische Validierung. Die Engagement-Rate wird aus der Follower-Zahl geschätzt (`generate_report.js:230`), Impressions sind nicht messbar (`:145`), der SSI wird bei fehlendem Zugang geschätzt (`SKILL.md:360`).
