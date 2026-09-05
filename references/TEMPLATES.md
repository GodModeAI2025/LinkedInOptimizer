# LinkedIn Optimierung – Templates & Prompt-Engineering v2.0

Dieses Dokument enthält Templates für alle Deliverables des Optimierungs-Workflows. Jedes Template ist so formuliert, dass Claude es direkt anwenden kann – mit klaren Variablen, Regeln und Qualitätskriterien.

---

## 1. Headline-Templates

### 1.1 Template A: Nische-First (empfohlen für Thought Leader)

```
[Nische/Mission] | [Position @ Unternehmen] | [Expertise-Keywords] | [Rollen]
```

**Variablen**:
- `[Nische/Mission]`: Max. 60 Zeichen. Muss die Kernexpertise auf den Punkt bringen.
- `[Position @ Unternehmen]`: Offizieller Titel. „@" statt „bei" spart Zeichen.
- `[Expertise-Keywords]`: 2–4 SEO-relevante Begriffe, kommagetrennt.
- `[Rollen]`: Autor, Speaker, Podcast-Host, Berater – nur wenn zutreffend.

**Beispiel**:
```
Künstliche Intelligenz in der Logistik | Head of Digital Platforms @ Musterwerke AG | GenAI, Agents, Enterprise AI | Podcast-Host
```
Zeichenzahl: 129 | Erste 60 Zeichen: „Künstliche Intelligenz in der Logistik | Head of Digital Pla…"

### 1.2 Template B: Position-First (für Corporate-Fokus)

```
[Position] @ [Unternehmen] | [Nische] | [Keywords] | [Differentiator]
```

**Beispiel**:
```
Head of Digital Platforms @ Musterwerke AG | KI-Agenten im Enterprise | GenAI, AI Strategy | Autor von 6 Fachbüchern
```

### 1.3 Template C: Mission-Statement (für starke persönliche Marke)

```
[Was ich tue/glaube] | [Position @ Unternehmen] | [Rollen] | [Social Proof Signal]
```

**Beispiel**:
```
Ich baue Brücken zwischen KI-Hype und Enterprise-Realität | Head of Digital Platforms @ Musterwerke AG | Autor & Podcast-Host
```

### 1.4 Template D: Autor/Speaker-First (für Personen mit starkem Social Proof)

```
[Autor von X Büchern zu Nische] | [Position @ Unternehmen] | [Keywords] | [Podcast/Medium]
```

**Beispiel**:
```
Autor von 6 KI-Büchern | Head of Digital Platforms @ Musterwerke AG | GenAI, Agents, Enterprise AI | Fachmedien-Autor
```

### Headline-Checkliste

```
QUALITÄTSKRITERIEN:
□ Max. 220 Zeichen (LinkedIn-Limit)
□ Erste 60 Zeichen = stärkste Botschaft (sichtbar in Suche, Kommentaren, Feed-Preview)
□ 3–4 SEO-Keywords enthalten, die Zielgruppe aktiv sucht
□ Position + Unternehmen erkennbar
□ Keine Emojis (DACH-Markt: wirkt unprofessionell in Headline)
□ Rollen wie Autor/Speaker/Podcast-Host erwähnt (wenn vorhanden)
□ Pipe-Separator (|) für Gliederung – keine Punkte oder Kommas als Trenner
□ Keine Floskeln („Passionate about…", „Helping companies…")
□ Kein „Open to Work" in der Headline (dafür gibt es den LinkedIn-Rahmen)
```

### Prompt für Headline-Generierung

```
Du bist ein LinkedIn-SEO-Experte. Erstelle 3 Headline-Varianten für folgendes Profil:

PROFILDATEN:
- Name: {name}
- Position: {position}
- Unternehmen: {unternehmen}
- Nische: {nische}
- Rollen: {rollen} (z.B. Autor, Speaker, Podcast-Host)
- Keywords: {keywords} (die wichtigsten 5 Suchbegriffe der Zielgruppe)
- Social Proof: {social_proof} (Bücher, Awards, Presse)

REGELN:
1. Max. 220 Zeichen pro Variante
2. Erste 60 Zeichen = stärkstes Statement
3. 3–4 Keywords aus der Liste einbauen
4. Keine Emojis
5. Pipe-Separator (|) als Trenner
6. DACH-Markt: professionell, sachlich, keine Anglizismen außer etablierte Fachbegriffe

AUSGABE:
Für jede Variante:
- Headline-Text
- Zeichenzahl
- Erste 60 Zeichen (Abschnitt bei „…")
- SEO-Keywords markiert [fett]
- Begründung (2 Sätze)
```

---

## 2. About-Sektion Templates

### 2.1 Template: Thought Leader mit Büchern (empfohlen für Autoren)

```
Seit [X] Jahren [was du tust] – heute als [Position] bei [Unternehmen]. Mein Fokus: [Nische/Mission in einem Satz].

Was mich antreibt:
[Klare These/Position – 2–3 Sätze. Eigene Meinung. Kein Marketing-Speak. Was glaubst du? Wofür stehst du? Was siehst du anders als andere?]

Was ich tue:
→ [Tätigkeit 1 – konkret, mit Unternehmenskontext und Impact]
→ [Tätigkeit 2 – zeigt Expertise, nicht nur Funktion]
→ [Tätigkeit 3 – zeigt Reichweite oder Verantwortung]
→ [Tätigkeit 4 – Nebenrolle: Autor/Speaker/Berater mit Zahl]

Meine Bücher (Auswahl):
📖 [Buch 1] – [Kurzinfo, ggf. Seitenzahl oder Besonderheit]
📖 [Buch 2] – [Kurzinfo]
📖 [Buch 3] – [Kurzinfo]
📖 [Buch 4] – [Kurzinfo]
📖 [Buch 5] – [Kurzinfo]
[Optional: „+ [X] weitere Fach- und Sachbücher zu [Thema]"]
[Optional: „Rezensiert bei [Publikation]"]

Was du hier findest:
[Wertversprechen in 2–3 Sätzen. Was bekommt jemand, der dir folgt? Konkretes Wissen, keine Versprechungen. Was teilst du? Was teilst du NICHT?]

Meine Themen:
▪ [Thema 1 – Kernthema mit Kontext]
▪ [Thema 2 – Zweites Standbein]
▪ [Thema 3 – Schnittstelle/Brücke zwischen Welten]
▪ [Thema 4 – Übergeordnetes Thema]

Auszeichnungen:
▪ [Award 1 – Jahr]
▪ [Zertifikat 1 – Aussteller]

Podcast-Host:
🎙 [Podcast 1 – Kurzbeschreibung]
🎙 [Podcast 2 – Kurzbeschreibung]

[Rollen-Zusammenfassung: 1 Satz, der alle Rollen zusammenfasst] | [Abschluss/Qualifikation]

[CTA – z.B.: Schreib mir, wenn du über [Thema] sprechen willst. Oder folge mir für [konkretes Wertversprechen].]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5 #Unternehmens-Hashtag
```

### 2.2 Template: Thought Leader ohne Bücher

```
[Wer bin ich – 2–3 Sätze. Kontext + Erfahrung + aktueller Fokus. Erste 270 Zeichen = Hook.]

Was mich antreibt:
[Klare These/Position – 2–3 Sätze.]

Was ich tue:
→ [Tätigkeit 1]
→ [Tätigkeit 2]
→ [Tätigkeit 3]
→ [Tätigkeit 4]

Was du hier findest:
[Wertversprechen]

Meine Themen:
▪ [Thema 1]
▪ [Thema 2]
▪ [Thema 3]
▪ [Thema 4]

Auszeichnungen:
▪ [Award/Zertifikat 1]
▪ [Award/Zertifikat 2]

[Rollen-Zusammenfassung] | [Abschluss]

[CTA]

#Hashtags
```

### 2.3 Template: C-Level / Management

```
[Verantwortungsbereich] bei [Unternehmen] – [Branche]. [Zahl]+ Jahre Erfahrung in [Bereich].

Mein Fokus:
→ [Strategisches Thema 1 – mit konkretem Kontext]
→ [Strategisches Thema 2 – mit messbarem Impact]
→ [Team/Bereich, den du leitest – Größe/Scope]

Was ich hier teile:
[Perspektive auf Branche/Trends – keine PR, sondern echte Einblicke. Was sieht man als Entscheider, was andere nicht sehen?]

Hintergrund:
▪ [Karriere-Highlight 1 – mit Zahl]
▪ [Karriere-Highlight 2 – mit Impact]
▪ [Karriere-Highlight 3 – mit Reputation]

[CTA]

#Hashtags
```

### Stilregeln für alle Templates

```
ERLAUBT:
✓ Kurze Sätze (max. 20 Wörter)
✓ Aktive Verben („Ich leite", „Ich entwickle", „Ich schreibe")
✓ Konkrete Zahlen („14 Bücher", „20 Jahre", „14.000 Follower")
✓ Eigene Meinungen/Thesen
✓ Aufzählungszeichen: → und ▪
✓ Emojis: Nur 📖 für Bücher und 🎙 für Podcasts (maximal)
✓ Max. 2.600 Zeichen (LinkedIn-Limit)

VERBOTEN:
✗ „Leidenschaftlich", „mit Herzblut", „ganzheitlich", „Synergien"
✗ „Ich helfe [Zielgruppe] dabei, [Ergebnis] zu erreichen" (zu generisch)
✗ „Excited to share", „Ich freue mich, mitteilen zu dürfen"
✗ „Mehrwert stiften", „End-to-End", „Ecosystem"
✗ Passive Formulierungen („Es wurde erreicht")
✗ Mehr als 3 verschiedene Emoji-Typen
✗ Hashtags mitten im Text (nur am Ende)
✗ Absätze länger als 4 Zeilen
✗ Über-Erklärung: Wenn es offensichtlich ist, nicht ausschreiben
```

### Qualitätsprüfung About

```
PRÜFPROTOKOLL:
1. Erste 270 Zeichen (vor „…mehr") kopieren → Würde ICH auf „mehr" klicken?
2. Orwell-Test: Jeden Satz einzeln lesen → „Kann ich den streichen?" → Ja = raus
3. Floskeln-Scan: Jedes Adjektiv prüfen → Kann es durch ein konkretes Beispiel ersetzt werden?
4. Zeichenzahl prüfen: ≤2.600 (LinkedIn-Limit)
5. Hashtag-Check: 5–7 Hashtags, inklusive Unternehmens-Hashtag
6. CTA-Check: Ist die Handlungsaufforderung konkret? (nicht „Let's connect")
7. Social-Proof-Check: Sind Bücher/Awards/Zahlen prominent platziert?
```

---

## 3. Content-Skill Template

Erstelle für jeden Kunden einen personalisierten Content-Skill:

```markdown
# LinkedIn Content Skill – [KUNDENNAME]

## IDENTITÄT
- Name: [Vollständiger Name]
- Position: [Aktuelle Position]
- Unternehmen: [Arbeitgeber]
- Nische: [Spezifische Nische – so eng wie möglich, z.B. nicht „KI" sondern „KI-Agenten im Enterprise"]
- Tonalität: [z.B. „Klar, direkt, keine Floskeln. Orwell-inspiriert. Praxis vor Theorie."]
- Sprache: [DE / EN / beides + Regeln für Code-Switching]

## LINKEDIN-ALGORITHMUS-REGELN
Arbeitsregeln dieses Skills. Belegt ist davon Punkt 1 (Dwell Time als Ranking-Signal, LinkedIn Engineering Blog vom 12.05.2020), der Rest ist Erfahrungswert. Beleglage je Aussage: `SOURCES.md`. Beachte bei JEDEM Post:
1. Dwell Time ist das wichtigste Signal → Texte 300–400 Wörter, strukturiert, Story-Format
2. Comment Quality > Like-Anzahl → CTAs die inhaltliche Antworten provozieren
3. Save Rate ist Qualitätssignal → Frameworks, Listen, Checklisten einfügen
4. Topische Konsistenz → ≥80% Posts in den definierten Fokusthemen
5. Erste 90 Minuten = Golden Hour → Beste Posting-Zeit einhalten
6. Content Completion > Länge → Karussells: 9 Slides max, Videos: <60 Sekunden
7. Kein Engagement-Bait → Kein „What do you think?", „Agree?", „Thoughts?", „Tag someone" (Quelle der Liste und Begründung: `ETHICS.md`)
8. Format-Variation → Nie 2× hintereinander dasselbe Format

## POST-FORMAT
- Zeichenzahl: 1.000–1.500 (Sweet Spot für Dwell Time, 300–400 Wörter)
- Absätze: Max. 3 Zeilen pro Absatz (mobil-optimiert, größerer Bildschirmanteil)
- Zeilenumbrüche: Großzügig einsetzen (Whitespace = Lesbarkeit = Dwell Time)
- Hashtags: [3–5 strategische] am Ende des Posts
- Pflicht-Hashtag: [z.B. #WIRsindMusterwerke]
- Emojis: Max. 3, nur als Aufzählungszeichen oder Akzente

## HOOK-TYPEN (10 Varianten)

Diese zehn Typen stehen in zwei Repos. Kanonisch sind sie im Schwester-Repo
[LinkedIn-Orchestrator](https://github.com/GodModeAI2025/LinkedIn-Orchestrator) unter
`LinkedIn-Orchestrator/references/HOOKS.md`; hier stehen sie als Kopie, weil das Skill-Paket offline vollständig sein
muss und keine Datei aus dem anderen Repo lesen kann. Bindende Fläche sind die zehn Namen und ihre
Reihenfolge, `scripts/check_hooks.py` prüft sie. Wer hier einen Typ ändert, zieht ihn dort nach;
diese Kopplung sieht kein Skript.

Jeder Post beginnt mit einem Hook in den ersten 2 Zeilen. Variiere systematisch:

### 1. PROVOKANTE THESE
„[Konventionelle Weisheit] ist falsch. Und die meisten haben es noch nicht gemerkt."
→ Funktioniert für: Meinungsposts, Gegen-den-Strom-Positionierung

### 2. PERSÖNLICHE GESCHICHTE
„Letzte Woche hat mich [Person/Situation] etwas gefragt, das mich nicht losgelassen hat."
→ Funktioniert für: Erfahrungs-Posts, Behind-the-Scenes

### 3. ZAHLEN-HOOK
„[Konkrete Zahl]% der [Zielgruppe] machen bei [Thema] denselben Fehler."
→ Funktioniert für: Daten-getriebene Posts, Benchmarks
→ Nur mit einer Zahl, die du belegen kannst. Siehe `references/SOURCES.md`.

### 4. GEGEN-DEN-STROM
„Unpopuläre Meinung: [Mainstream-Position] schadet mehr als sie nützt."
→ Funktioniert für: Polarisierende Meinungsposts (sparsam einsetzen: 1×/Monat)

### 5. KONTEXT-FRAGE
„Wenn du morgen [realistisches Szenario] umsetzen müsstest – wo würdest du anfangen?"
→ Funktioniert für: Praxis-Posts mit CTA

### 6. BREAKING-NEWS-ANALYSE
„[Aktuelle Nachricht] – Drei Dinge, die die meisten dabei übersehen."
→ Funktioniert für: Aktualitäts-Posts, Einordnung

### 7. LEHRE AUS FEHLER
„Ich habe [konkreten Fehler] gemacht. Hier ist, was ich daraus gelernt habe."
→ Funktioniert für: Authentizitäts-Posts, Vertrauensaufbau

### 8. FRAMEWORK / LISTE
„[Zahl] Prinzipien für [Thema], die ich in [X] Jahren gelernt habe:"
→ Funktioniert für: Content, der gespeichert wird

### 9. BEOBACHTUNG
„Mir fällt ein Muster auf: [Trend/Beobachtung]. Und kaum jemand spricht darüber."
→ Funktioniert für: Trend-Analyse, Thought Leadership

### 10. MICRO-CASE-STUDY
„Wir haben [Maßnahme] eingeführt. Das Ergebnis nach [Zeitraum]:"
→ Funktioniert für: Praxis-Beweise, Social Proof

## CONTENT-SÄULEN
- [Säule 1 – 50–60%]: [Kernthema – z.B. „KI im Enterprise: Agents, GenAI, Strategie"]
- [Säule 2 – 20–25%]: [Nebenthema – z.B. „Energiewende & Digitalisierung"]
- [Säule 3 – 10–15%]: [Persönliches – z.B. „Learnings als Führungskraft, Bücher, Podcasts"]
- [Säule 4 – 5–10%]:  [Polarisierend – z.B. „Hype vs. Realität, unpopuläre Meinungen"]

## STIL-REGELN (ORWELL-PRINZIPIEN)
1. Jeder Satz hat genau einen Zweck. Keinen Satz, den man streichen könnte.
2. Kurze Wörter statt langer. „nutzen" statt „utilisieren".
3. Aktiv statt Passiv. „Wir haben X eingeführt" statt „X wurde eingeführt".
4. Eigene Bilder und Vergleiche statt Klischees.
5. Keine Füllwörter: „grundsätzlich", „eigentlich", „sozusagen", „gewissermaßen".
6. Kontext vor Behauptung: Erst das Problem, dann die Meinung.
7. Zahlen und Beispiele statt Adjektive.

## VERBOTENE WÖRTER UND PHRASEN
[Individuell anpassen pro Kunde]
- „leidenschaftlich" / „mit Herzblut"
- „ganzheitlich" / „Synergien" / „auf Augenhöhe"
- „Gamechanger" / „disruptiv" (ohne konkreten Kontext)
- „ich freue mich, mitteilen zu dürfen" / „excited to share"
- „Mehrwert stiften"
- „Food for thought"
- „Let that sink in"
- „Agree?" / „Thoughts?" / „What do you think?" / „Tag someone" (gesperrte CTA-Formulierungen, vollständige Liste mit Begründung in `ETHICS.md`)

## SAVE-OPTIMIERUNG
Posts so formulieren, dass Leser sie speichern wollen:
- Listen und Frameworks → höchste Save-Rate aller Formate
- Checklisten und How-To-Schritte → „Speicher dir das für dein nächstes [Projekt]"
- Vorher/Nachher-Vergleiche mit konkreten Zahlen
- Templates und Vorlagen zum Nachmachen
- „Diese 5 Fragen stelle ich mir bei jeder [Entscheidung]:"

## CTA-VARIANTEN (Engagement-Bait-frei)
Jeder Post endet mit einem CTA. Variiere (KEINE generischen Fragen). Was ein brauchbarer CTA
von einem Bait unterscheidet, steht in `ETHICS.md`: Die Frage muss eine Antwort haben wollen.
- „Welche Erfahrung hast du mit [konkretem Aspekt] gemacht?"
- „Welchen der [X] Punkte würdest du ergänzen?"
- „Speicher dir das für dein nächstes [konkretes Szenario]."
- „Ich bin gespannt: Setzt ihr [konkretes Tool/Methode] schon ein?"
- „Teile das mit jemandem, der gerade [konkretes Problem] löst."
- „Folge mir für [konkretes Thema]-Praxis aus dem Enterprise-Alltag."

## POST-FREQUENZ & TIMING
- Frequenz: [3–5]× pro Woche
- Timing: [Mo/Di/Mi/Do 8:00–8:30 CET] (DACH-Markt: vor Arbeitsbeginn)
- Golden Hour: Erste 90 Minuten nach Veröffentlichung: aktiv kommentieren, auf alle Antworten reagieren
- Freitag: Optional, niedrigere Reichweite
- Wochenende: Nur für persönliche/polarisierende Posts (weniger Konkurrenz, aber weniger Impressions)
- 1× pro Woche: Kommentar-Marathon (20+ Kommentare auf relevante Posts in 30 Min.)

## FORMAT-ROTATION (4-Wochen-Kalender)

| Woche | Mo | Mi | Fr |
|-------|----|----|-----|
| 1 | Text+Bild (Hook 1–3) | Karussell (Framework) | Video <60s |
| 2 | Text+Bild (Hook 6–7) | Umfrage | Text+Bild (Hook 8) |
| 3 | Karussell (Case Study) | Text+Bild (Hook 4–5) | Video <60s |
| 4 | Text+Bild (Hook 9–10) | Karussell (Checkliste) | Persönlicher Post |
```

---

## 4. Kommentar-Skill Template

```markdown
# LinkedIn Kommentar-Skill – [KUNDENNAME]

## WARUM KOMMENTIEREN NEBEN DEM POSTEN ZÄHLT
- Ein Kommentar erscheint im Netzwerk der kommentierten Person, ein eigener Post nur im eigenen
- Substanzielle Kommentare fallen auf, kurze Zustimmung nicht
- LinkedIn erkennt „Pod-Behavior": Nicht immer bei denselben Accounts kommentieren
- Die Wirkung ist ein Erfahrungswert. Frühere Prozentangaben an dieser Stelle sind zurückgezogen, siehe `SOURCES.md`

## REGELN
- Länge: 15–50 Wörter (Sweet Spot: 20–30 Wörter, Erfahrungswert)
- Sprache: [Sprache des Originalposts / DE als Default im DACH-Raum]
- Immer Mehrwert: eigene Erfahrung, neue Perspektive oder kluge Frage
- Kein Pod-Verhalten: Nicht jeden Tag bei denselben 5 Accounts kommentieren. Eine abgesprochene
  Kommentar-Runde ist nach `ETHICS.md` Regel 2 ausgeschlossen, unabhängig davon, ob LinkedIn sie erkennt
- Nie: „Toller Beitrag!", „Danke fürs Teilen!", „100% Zustimmung!", „So true!"
- Immer: Bezug zum konkreten Inhalt des Posts herstellen

## KOMMENTAR-TYPEN

### Typ 1: ERFAHRUNGS-KOMMENTAR (häufigster Typ: 40%)
„Deckt sich mit meiner Erfahrung bei [konkreter Kontext]. Wir haben dabei [konkretes Learning] gelernt."
→ Zeigt: Du hast Praxiswissen. Positioniert dich als Experte.

### Typ 2: ERGÄNZUNGS-KOMMENTAR (20%)
„Guter Punkt. Ergänzend: [Aspekt] spielt hier eine unterschätzte Rolle, besonders wenn [Kontext]."
→ Zeigt: Du denkst weiter als der Autor. Bringt neuen Wert.

### Typ 3: FRAGE-KOMMENTAR (15%)
„Spannend. Wie geht ihr mit [spezifische Herausforderung] um, wenn [konkrete Bedingung]?"
→ Zeigt: Du verstehst die Komplexität. Öffnet Dialog.

### Typ 4: GEGENPOSITION (15%)
„Sehe ich differenzierter. In der Praxis zeigt sich eher [Gegenargument], weil [konkrete Begründung]."
→ Zeigt: Du hast eine eigene Meinung. WICHTIG: Respektvoll, nie herablassend.

### Typ 5: KONTEXT-KOMMENTAR (10%)
„Wichtiger Kontext dazu: [Fakt/Studie/Erfahrung], der das Bild vervollständigt."
→ Zeigt: Du bringst Tiefe. Positioniert dich als Wissensgeber.

## ZIEL-ACCOUNTS
Identifiziere und pflege 15–20 strategische Accounts:

| Kategorie | Anzahl | Beispiel |
|-----------|--------|---------|
| Top Voices / Influencer der Nische | 5–7 | [Namen eintragen] |
| C-Level der Zielkunden | 3–5 | [Namen eintragen] |
| Journalisten / Medien der Nische | 2–3 | [Namen eintragen] |
| Peers / Gleichgesinnte Experten | 3–5 | [Namen eintragen] |
| Aufstrebende Stimmen (gegenseitiger Support) | 2–3 | [Namen eintragen] |

Regelmäßig auf deren Posts kommentieren → Als Experte in deren Community sichtbar werden.
ABER: Nicht jeden Tag bei denselben Accounts. Rotation über die Woche.

## KOMMENTAR-FREQUENZ
- Min. 5 substanzielle Kommentare pro Tag auf fremde Posts
- 1× pro Woche: „Kommentar-Marathon" (20+ Kommentare in 30 Min.)
- Alle Antworten auf eigene Kommentare IMMER beantworten (Dialog-Signal)
- Alle Kommentare unter eigenen Posts innerhalb von 2 Stunden beantworten (Golden Hour)
- Best Practice: 15 Min. morgens + 15 Min. mittags + 15 Min. abends = 45 Min./Tag
```

---

## 5. Newsletter-Template (LinkedIn Newsletter)

```markdown
# Newsletter-Strategie für [KUNDENNAME]

## GRUNDDATEN
- Titel: [Kurz, merkbar, Nische im Titel, z.B. „KI im Enterprise – Weekly"]
- Frequenz: [Wöchentlich oder 2× pro Monat]
- Sprache: [DE / EN]
- Zielgruppe: [Wer soll abonnieren?]

## WARUM NEWSLETTER?
- LinkedIn-Newsletter signalisiert Platform Investment (Top Voice-Verstärker)
- Abonnenten werden bei jeder Ausgabe per Push benachrichtigt
- Newsletter-Posts haben überdurchschnittliche Reichweite
- Baut E-Mail-ähnliche Audience auf (LinkedIn-native)

## STRUKTUR PRO AUSGABE (800–1.200 Wörter)
1. [Hook/Einleitung]: Aktueller Anlass oder überraschende These (3–5 Sätze)
2. [Hauptteil]: Deep Dive in ein Thema der Woche (500–700 Wörter)
3. [Praxis-Takeaway]: 3–5 konkrete Handlungsempfehlungen
4. [Kurznotizen]: 2–3 Links/News der Woche mit 1-Satz-Einordnung
5. [CTA]: Frage an die Leser oder Hinweis auf nächste Ausgabe

## THEMEN-ROTATION
Jeden Monat:
- Woche 1: Deep Dive (Kernthema)
- Woche 2: Praxis-Report (Case Study / Erfahrungsbericht)
- Woche 3: Trend-Analyse (was verändert sich in der Nische?)
- Woche 4: Meinungsstück (Position beziehen)
```

---

## 6. Featured Section – Empfohlene Bestückung

```
PRIORITÄT 1 (immer):
1. Meistgelesener/erfolgreichster Post (Screenshot oder Link)
2. Wichtigstes Buch / Publikation (Link zu BoD/Amazon)
3. Newsletter (Abo-Link)

PRIORITÄT 2 (wenn vorhanden):
4. Podcast-Episode (Highlight-Folge)
5. Keynote / Vortrag (Video oder Slides)
6. Presse-Artikel (heise, iX, etc.)

MAXIMUM: 5–6 Items. Weniger ist mehr.
Reihenfolge: Stärkstes Signal zuerst.
```
