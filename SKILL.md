---
name: linkedin-profil-optimierung
description: >
  Professionelle LinkedIn-Profilanalyse mit gewichtetem Scoring (0–100), Headline/About-Optimierung,
  Banner-Erstellung, Content-Strategie und Thought-Leader-Positionierung. Verwende diesen Skill
  immer wenn ein LinkedIn-Profil analysiert, bewertet, optimiert oder für ein Top Voice Badge
  vorbereitet werden soll. Auch bei Anfragen wie "mein LinkedIn verbessern", "Profil-Score",
  "LinkedIn Headline optimieren", "About-Sektion schreiben", "LinkedIn Banner erstellen",
  "Content-Strategie LinkedIn", "SSI verbessern", "Top Voice werden", "LinkedIn Wettbewerbsanalyse",
  oder wenn jemand seinen LinkedIn-Auftritt professionalisieren möchte.
---

# LinkedIn Profil-Optimierung & Thought-Leader Skill v2.2.2

Ein evidenzbasierter 8-Phasen-Workflow zur Analyse und Optimierung von LinkedIn-Profilen. Basiert auf LinkedIn-Algorithmus-Daten 2025/2026, Engagement-Benchmarks und den offiziellen Top Voice Kriterien.

## Ressourcen-Übersicht

Lies die jeweilige Datei, wenn du die Phase erreichst:

| Datei | Inhalt | Wann lesen |
|-------|--------|-----------|
| `references/SCORING.md` | Gewichtete 10-Kategorien-Matrix mit Sub-Kriterien und Benchmarks | Phase 2 (Scoring) |
| `references/TEMPLATES.md` | Vorlagen für Headline, About, Content-Skill, Kommentar-Skill | Phase 4 + 6 |
| `references/BANNER.md` | Technische Banner-Anleitung mit Safe Zones und Viewport-Matrix | Phase 5 |
| `scripts/create_banner.py` | Ausführbares Banner-Skript mit Font-Fallback und Validierung | Phase 5 (ausführen) |
| `scripts/generate_report.js` | DOCX-Report-Template (Node.js, npm-Paket `docx`), als Strukturvorlage nutzen und mit den erhobenen Daten befüllen | Phase 8 (anpassen + ausführen) |

---

## Phase 1: Discovery & Datenerhebung

### 1.0 Datenerhebungsstrategie

LinkedIn blockiert web_fetch (robots.txt). Nutze daher diese Reihenfolge:

1. **Chrome-Plugin (primär)**: Navigiere mit `Claude in Chrome:navigate` zum Profil, lese Daten mit `get_page_text`, `read_page` und `javascript_tool`. Falls der Benutzer eingeloggt ist, sind alle Profildaten sichtbar.
2. **web_search (Ergänzung)**: Für Daten die Chrome nicht liefert (z.B. Profilbild-Qualität, Banner-Details) oder wenn Chrome nicht verfügbar ist.
3. **Manuell (Fallback)**: Wenn weder Chrome noch Suche funktionieren, frage den Kunden nach Screenshot oder PDF-Export und führe das Kontext-Interview (1.2) als Datenbasis durch. Markiere geschätzte Daten.

### 1.1 Profildaten via Chrome extrahieren

Navigiere zum LinkedIn-Profil und erhebe die Daten in drei Schritten:

**Schritt 1 — Hauptprofil** (`/in/username/`):
Nutze `get_page_text` für einen schnellen Überblick, dann `read_page` für die Accessibility-Tree-Struktur. Extrahiere per `javascript_tool`:

```javascript
// Headline (exakter Wortlaut + Zeichenzahl)
const headlineEl = document.querySelector('[class*="text-body-medium"][class*="break-words"]');
const headline = headlineEl?.textContent?.trim();

// About-Sektion (vollständig, inkl. verstecktem Text)
const aboutSection = document.getElementById('about')?.closest('section');
const spans = aboutSection?.querySelectorAll('span[aria-hidden="true"]');
// Laengsten Span nehmen = vollstaendiger Text
// Wenn abgeschnitten: zweite Haelfte mit .substring(800) nachladen

// Featured Section, Creator Mode, Empfehlungen
const hasFeatured = !!document.getElementById('featured');
```

Erfasse systematisch: Name, Headline (Wortlaut + Zeichenzahl), About (vollständiger Text), aktuelle Position + Dauer, alle Positionen, Ausbildung, Zertifikate, Follower-Anzahl, Connections, Empfehlungen (erhalten/erteilt), Skills (Anzahl), Sprachen, Newsletter, Gruppen, Interessen.

**Schritt 2 — Activity-Seite** (`/in/username/recent-activity/all/`):
Navigiere zur Activity-Seite und extrahiere die letzten Posts:

```javascript
// Eindeutige Posts mit Engagement-Daten
const feedItems = document.querySelectorAll('[class*="feed-shared-update-v2"]');
const seen = new Set();
const unique = [];
feedItems.forEach(fi => {
  const socialSection = fi.querySelector('[class*="social-counts"]');
  const socialText = socialSection?.innerText?.trim() || '';
  const txt = fi.innerText;
  const zeit = txt.match(/(\d+\s*(?:Tag|Woche|Monat|Stunde)[en]*\s*[•])/)?.[0] || '';
  if (!zeit) return;
  const key = zeit + '|' + socialText.substring(0, 30);
  if (seen.has(key)) return; // LinkedIn rendert Duplikate
  seen.add(key);
  const reac = socialText.match(/^(\d+)/)?.[1] || '0';
  const komm = socialText.match(/(\d+)\s*Kommentar/)?.[1] || '0';
  unique.push({ time: zeit, reactions: reac, comments: komm });
});
```

Scrolle einmal nach unten (`window.scrollTo(0, document.body.scrollHeight)`) und lese erneut, um weitere Posts zu laden.

**Schritt 3 — Fehlende Daten ergänzen**:
Wenn der About-Text abgeschnitten ist (LinkedIn zeigt nur ~1600 Zeichen im DOM), lies den zweiten Teil mit `.substring(800)` nach. Prüfe, ob ein "mehr anzeigen"-Button existiert und klicke ihn falls nötig.

### 1.2 Kontext-Interview

Stelle dem Kunden diese 10 Fragen:

1. In welcher Nische willst du als Thought Leader wahrgenommen werden? → Topische Fokussierung
2. Wer ist deine Zielgruppe? → Content-Tonalität und Format-Mix
3. Wer sind deine 3–5 Nischen-Konkurrenten? → Wettbewerbsanalyse
4. Welche Bücher, Podcasts, Vorträge willst du hervorheben? → Social Proof maximieren
5. Welche Hashtags nutzt dein Unternehmen? → Corporate-Branding
6. Was ist dein primäres Ziel? (Top Voice, Follower, Lead-Gen, Recruiting) → Strategie-Ausrichtung
7. Welche Themen willst du NICHT bespielen? → Risikomanagement
8. In welcher Sprache postest du primär? → Content-Lokalisierung
9. Wie viel Zeit pro Woche kannst du investieren? → Frequenz dimensionieren
10. Hast du Zugang zu deinem SSI-Score? (linkedin.com/sales/ssi) → Baseline

### 1.3 SSI-Score erheben

Dokumentiere den Social Selling Index (4 Säulen à 25 Punkte, Gesamt 100). Benchmark: SSI >70 = effektiv, >75 = Thought-Leader-Niveau.

---

## Phase 2: Scoring & Gap-Analyse

Lies `references/SCORING.md` für die vollständige Bewertungsmatrix mit Sub-Kriterien.

### 2.1 Profil-Scoring

Bewerte das Profil in 10 gewichteten Kategorien (jede 0–10, multipliziert mit Gewichtungsfaktor):

| Kategorie | Gewicht | Max. Beitrag |
|-----------|---------|-------------|
| Content-Qualität | 15% | 15.0 |
| Engagement & Kommentare | 15% | 15.0 |
| Headline | 12% | 12.0 |
| About-Sektion | 12% | 12.0 |
| Social Proof | 10% | 10.0 |
| Posting-Frequenz | 10% | 10.0 |
| Netzwerk & Follower | 8% | 8.0 |
| Profil-Vollständigkeit | 7% | 7.0 |
| Banner | 6% | 6.0 |
| Top Voice Readiness | 5% | 5.0 |

Dokumentiere für jeden Score die Begründung anhand der Sub-Kriterien aus SCORING.md.

### 2.2 Gap-Analyse

Identifiziere die 3 größten Score-Hebel in einer Prioritäts-Matrix (Impact × Aufwand):
- Quick Wins: Hoher Impact, niedriger Aufwand (z.B. Headline ändern, Featured befüllen)
- Strategische Hebel: Hoher Impact, hoher Aufwand (z.B. Content-Strategie, Newsletter)
- Nice-to-Have: Niedriger Impact, niedriger Aufwand (z.B. Skills ordnen, URL anpassen)

---

## Phase 3: Wettbewerbsanalyse

### 3.1 Nischen-Konkurrenten analysieren

Analysiere 3–5 Konkurrenten anhand: Follower, Post-Frequenz, ø Engagement, Content-Mix, Formate, Nischen-Fokus, Social Proof, Newsletter, Video-Anteil, Top Voice Status, SSI (geschätzt).

### 3.2 Differenzierungs-Strategie

Leite aus der Analyse ab:
- Content-Lücken: Welche Themen/Formate bedient kein Wettbewerber?
- Tonalitäts-Differenzierung: Wie kann sich der Kunde sprachlich absetzen?
- Social-Proof-Vorsprung: Welche Credentials hat nur der Kunde?
- Format-Innovation: Welches Format nutzt keiner der Wettbewerber?

---

## Phase 4: Profil-Optimierung

Lies `references/TEMPLATES.md` Abschnitte 1 + 2 für Headline- und About-Templates.

### 4.1 Headline optimieren

Kernregeln: Max. 220 Zeichen, erste 60 Zeichen = stärkstes Signal, 3–4 SEO-Keywords, keine Emojis im DACH-Markt, Pipe-Separator (|). Liefere immer 3 Varianten mit SEO-Keywords, Zeichenzahl und Vorher/Nachher-Vergleich.

### 4.2 About-Sektion optimieren

Die ersten 270 Zeichen (vor „…mehr") entscheiden über Weiterlesen. Orwell-Prinzipien anwenden: Kein überflüssiger Satz, aktiv statt passiv, konkret statt abstrakt, eigene Bilder statt Klischees. Verbotene Wörter beachten (Liste in TEMPLATES.md).

### 4.3 Quick-Win-Checkliste

Prüfe 15 Profil-Elemente (Profilbild, Banner, Headline, About, Featured, Creator Mode, CTA, URL, Newsletter, Empfehlungen, Skills, Positionen, Publikationen, Collaborative Articles, Video-Content) und erstelle einen Maßnahmenplan.

---

## Phase 5: Banner-Erstellung

Lies `references/BANNER.md` für die vollständige technische Anleitung. Nutze `scripts/create_banner.py` zur Erstellung.

Kritische Regeln im Überblick:
- Format: 1584×396px, PNG, sRGB
- Universell sichere Zone: x=520 bis x=1200, y=30 bis y=350
- Texte als EINEN Block zusammenhalten, nicht über volle Breite verteilen
- Dunkler Hintergrund + weiße Schrift für maximalen Kontrast
- Mindestschriftgrößen: Titel ≥48px, Untertitel ≥22px, Rolle ≥18px, Tags ≥16px

Banner erstellen:
```bash
python scripts/create_banner.py \
  --output banner.png \
  --title1 "Zeile 1" --title2 "Zeile 2" \
  --subtitle "Untertitel" \
  --role "Position @ Unternehmen" \
  --tags "#GenAI  #EnterpriseAI" \
  --strict
```

`--strict` gehört in jeden Aufruf: Ohne die Option meldet das Skript Safe-Zone-Verletzungen nur als Warnung und endet trotzdem mit Exitcode 0, mit der Option endet es mit 1. Ein eigenes Hintergrund-Bild kommt optional über `--background <bild.png>` dazu; fehlt die Option oder der Pfad, entsteht ein Gradient-Hintergrund.

Fehlt NotoSans, greift das Skript auf DejaVuSans zurück. Findet es gar keinen Font mit anwendbarer Größenangabe, sind die gemessenen Textbreiten wertlos; dieser Fall zählt selbst als Verletzung und beendet `--strict` mit 1, statt ein ungeprüftes Banner durchzulassen.

---

## Phase 6: Content-Strategie

Lies `references/TEMPLATES.md` Abschnitte 3 + 4 für Content-Skill und Kommentar-Skill Templates.

### 6.1 Content-Skill erstellen

LinkedIn-Algorithmus 2025/2026 beachten:
- Dwell Time = zentrales Signal → Texte 300–400 Wörter, Story-Struktur
- Comment Quality > Like-Volumen → CTAs die inhaltliche Antworten provozieren
- Save Rate = Qualitätssignal → Frameworks, Listen, Checklisten
- Topische Konsistenz → ≥80% Posts in max. 2 Fokusthemen
- Engagement Bait wird bestraft → Kein „What do you think?", „Agree?"

Top-performende Formate: Multi-Image 6,6%, PDF-Karussells 6,1%, Video (<60s) 5,6%, Umfragen ~5%.

### 6.2 Kommentar-Strategie

Strategisches Kommentieren (5–10/Tag) steigert Profilaufrufe um 55% und eigene Content-Reichweite um 20%. Kommentare >15 Wörter haben 2,5× mehr algorithmisches Gewicht. Identifiziere 15–20 Ziel-Accounts (Top Voices, C-Level, Journalisten, Peers).

### 6.3 Posting-Frequenz und Timing

3–5 Posts/Woche, Mo–Do 8:00–8:30 CET, erste 90 Minuten nach Post aktiv kommentieren. 5–10 qualitative Kommentare/Tag auf fremde Posts. Keine Pause >7 Tage.

---

## Phase 7: SSI-Optimierung

Maßnahmen pro SSI-Säule (je max. 25 Punkte):

1. **Professional Brand**: Profil vollständig, regelmäßig Content, Multimedia, strategische Endorsements
2. **Find the Right People**: 5–10 strategische Connections/Woche, persönliche Requests (+40% Akzeptanz)
3. **Engage with Insights**: Täglich kommentieren, Collaborative Articles beitragen, eigene Standpunkte
4. **Build Relationships**: Inbox pflegen, Kommentare <2h beantworten, Follow-ups, Empfehlungen schreiben

Ziel-SSI nach 90 Tagen: ≥75

---

## Phase 8: Report & Übergabe

### 8.1 DOCX-Report erstellen (Pflicht-Deliverable)

Der Analyse-Report wird immer als professionelles Word-Dokument (.docx) geliefert. Nutze `scripts/generate_report.js` als Strukturvorlage. Lies das Skript, passe die Daten-Konstanten (scoringData, posts, Profilinfos) an den analysierten Kunden an, und führe es aus.

**Vorgehen:**
1. Lies `scripts/generate_report.js` mit dem view-Tool
2. Kopiere es unter dem Namen `generate_report.js` in das Arbeitsverzeichnis
3. Ersetze die Platzhalter-Daten durch die erhobenen Kundendaten:
   - `scoring`-Array: Alle 10 Kategorien mit Roh-Score, Gewichtung, Begründung
   - `posts`-Array: Content-Aktivitäten aus Phase 1 (Schritt 2)
   - Profil-Metadaten: Name, Position, Unternehmen, Standort, Follower, Connections
   - Headline-Varianten: Aus Phase 4.1
   - About-Analyse: Verbotene Wörter, CTA-Bewertung, Hashtag-Status
   - Profil-Audit: 17-Punkte-Checkliste mit Status je Element
   - Roadmap: Kundenspezifisch priorisierte Maßnahmen
4. Passe die letzte Zeile an: der Ausgabepfad steht fest auf `/mnt/user-data/outputs/`. Außerhalb der claude.ai-Sandbox muss dort ein existierendes Verzeichnis stehen.
5. Führe das Skript aus: `node generate_report.js`. Es schreibt den Pfad der erzeugten Datei als `Done: …` nach stdout.
6. Prüfe das Ergebnis: `unzip -l <Ausgabedatei>.docx` muss `word/document.xml` listen, danach die Datei öffnen und die 9 Kapitel durchgehen.

**Report-Struktur (9 Kapitel, alle mit erklärenden Textpassagen):**

1. **Executive Summary** (1 Seite): Gesamtscore mit Bewertungsstufe, Top 3 Stärken mit Erklärung warum sie Stärken sind, Top 3 Hebel mit Erklärung des Score-Impacts, 3 Quick Wins mit konkreter Auswirkung.

2. **Scoring-Details** (1–2 Seiten): Tabelle aller 10 Kategorien (Roh, Gewichtung, gewichtete Punkte, Max, %, Bewertung). Darunter ein erklärender Absatz, der dem Leser zeigt, wie die Tabelle zu lesen ist und was die Farben bedeuten.

3. **Detailanalyse je Kategorie** (3–4 Seiten): Jede der 10 Kategorien wird in einem eigenen Unterkapitel begründet. Jede Begründung nennt konkrete Befunde aus dem Profil — keine generischen Aussagen. Bei niedriger Bewertung: konkreter Verbesserungsvorschlag.

4. **Content-Aktivität** (1 Seite): Tabelle der letzten Posts mit Zeitpunkt, Reaktionen, Kommentaren, geschätzter Engagement-Rate. Darunter Erklärung der Methodik (worauf die Schätzung basiert, was nicht messbar war) und Bewertung der Kennzahlen (Median, Vergleich mit Benchmark).

5. **Headline-Analyse** (1 Seite): Aktuelle Headline mit Bewertung (was funktioniert, was nicht, warum), 3 Optimierungsvorschläge mit Zeichenzahl, ersten 60 Zeichen und Erklärung der jeweiligen Strategie.

6. **About-Sektion-Analyse** (1 Seite): Hook-Bewertung der ersten 270 Zeichen, gefundene verbotene Wörter mit konkreten Ersetzungsvorschlägen und Begründung, CTA-Bewertung mit Alternativvorschlag, fehlende Elemente (Hashtags, Zeichenauslastung).

7. **Profil-Audit** (1 Seite): 17-Punkte-Checkliste als Tabelle mit Status (Vorhanden/Fehlt/Teilweise) und konkreter Maßnahme je Element. Zusammenfassung: X von 17 erfüllt.

8. **Roadmap** (1 Seite): Zeitlich priorisierte Maßnahmen (Woche 1–2 Quick Wins → Monat 2–3 Skalierung → Monat 4–6 Authority Building). Erwarteter Score nach 3 Monaten mit Begründung.

9. **Methodik & Einschränkungen** (1 Seite): Wie die Daten erhoben wurden (Chrome/web_search/manuell), welche Scoring-Methodik verwendet wurde, welche Daten geschätzt oder nicht verfügbar waren. Transparenz schafft Vertrauen.

**Formatierung des DOCX:**
- Arial, 10,5pt Fließtext, Überschriften in Hierarchie (H1 16pt, H2 13pt, H3 11pt)
- Tabellen mit Kopfzeile (dunkel), alternierenden Zeilen, Farbcodierung (Grün ≥70%, Gelb 40–69%, Rot <40%)
- Header mit "LinkedIn Profil-Analyse" + Skill-Version, Footer mit Seitenzahl
- Titelseite mit Name, Position, Score-Box, Datum
- Seitenumbrüche zwischen Hauptkapiteln

### 8.2 A/B-Testing-Framework

Pro Quartal testen: Headline (Nische-First vs Mission), Hook-Typ, Posting-Zeit, Format, CTA-Typ, Hashtag-Anzahl. Testdauer min. 2 Wochen / 6 Posts pro Variante, Median-Vergleich.

### 8.3 KPI-Dashboard

Monatlich tracken: Follower, Profilaufrufe, Engagement-Rate (Ziel >5%), Kommentare/Post (>15), Impressions/Post (>5.000), Save-Rate (>2%), SSI (≥75), Posting-Frequenz (≥3/Woche), Newsletter-Abos.

---

## Top Voice Badge – Anforderungen

Einladungsbasiert durch LinkedIn-Redaktion, halbjährliche Überprüfung seit Januar 2025.

| Kriterium | Messbar machen |
|-----------|---------------|
| Platform Presence | Posting ≥3×/Woche, Kommentare ≥5/Tag, seit ≥6 Monaten |
| Quality & Originality | Keine Reposts, eigene Frameworks, Storytelling |
| Subject Matter Expertise | 80%+ Posts in 1–2 Fokusthemen |
| Safety & Professionalism | Keine kontroversen Inhalte, professioneller Ton |
| Prominence | Bücher, Presse, Awards, Speaker auf Profil |

Verstärker: Newsletter, Video-Content, LinkedIn Live, hohe Save-Rate, externe Presse.

---

## Branchenspezifische Anpassungen

| Parameter | Tech/KI | Energie | Finance | Consulting | Healthcare |
|-----------|---------|---------|---------|------------|------------|
| Engagement-Benchmark | 3,6% | 3,3% | 3,2% | 3,2% | 3,3% |
| Tone of Voice | Pragmatisch | Zukunftsorientiert | Reguliert | Framework-orientiert | Evidenzbasiert |
| Top-Format | Karussell + Code | Text+Bild, Video | Analyse, Charts | Frameworks, Listen | Case Studies |
| Posting-Frequenz | 4–5×/Woche | 3–4×/Woche | 2–3×/Woche | 3–4×/Woche | 2–3×/Woche |

---

## Verifikation

Prüfe vor Übergabe an den Kunden:

**Headline**: Zeichenzahl ≤220, erste 60 Zeichen enthalten Nischen-Keyword, keine Emojis, ≥3 SEO-Keywords, keine verbotenen Wörter, Pipe-Separator.

**About**: Zeichenzahl ≤2.600, erste 270 Zeichen = eigenständiger Hook mit Positionierung, Orwell-Scan gegen verbotene Wörter, CTA vorhanden und konkret, 5–7 Hashtags am Ende, max. 3 Emoji-Typen, kein Absatz >4 Zeilen.

**Banner**: Exakt 1584×396px, <8 MB, alle Textelemente in x=520–1200 / y=30–350, Schriftgrößen eingehalten, WCAG-Kontrast ≥4.5:1.

**Content-Skill**: Alle 10 Hook-Typen mit kundenspezifischen Beispielen, Säulen summieren auf 100%, keine Engagement-Bait-Phrasen.

**Scoring**: Jede Kategorie mit Begründung, gewichtete Summe korrekt berechnet, ≥3 Hebel identifiziert.

**Report**: DOCX erzeugt, als ZIP lesbar (`unzip -l` listet `word/document.xml`), alle 9 Kapitel vorhanden, jede Tabelle und jedes Diagramm hat einen erklärenden Textabsatz darunter, keine Scoring-Kategorie ohne Begründung.

Bei Fehlern: Automatisch korrigieren und erneut prüfen.

---

## Fehlerbehandlung

**LinkedIn blockiert web_fetch/web_search**: Das ist der Normalfall — LinkedIn blockiert robots.txt-basierte Zugriffe. Nutze IMMER das Chrome-Plugin als primäre Datenquelle. Folge der Kaskade aus Phase 1.0: Chrome → web_search → manuell.

**Chrome-Plugin nicht verfügbar**: Wenn der Benutzer kein Chrome-Plugin hat, informiere ihn dass die Datenqualität eingeschränkt ist. Nutze web_search für öffentlich sichtbare Snippets (Name, Headline, Unternehmen, Connections). Frage nach Screenshot oder PDF-Export für den Rest. Markiere alle geschätzten Daten im Report.

**Profil nur eingeschränkt sichtbar** (nicht eingeloggt): Einige Profil-Abschnitte sind ohne LinkedIn-Login nicht sichtbar (About nach 3 Zeilen, Empfehlungen, Skills, detaillierte Positionen). Bitte den Benutzer sich in Chrome bei LinkedIn einzuloggen und starte die Erhebung erneut.

**About-Text abgeschnitten im DOM**: LinkedIn rendert den About-Text in einem `span[aria-hidden="true"]` mit ca. 1600 Zeichen. Wenn abgeschnitten: Lies den zweiten Teil mit `.substring(800)` in einem separaten `javascript_tool`-Aufruf. Falls ein "mehr anzeigen"-Button existiert, klicke ihn vorher.

**Activity-Seite zeigt wenige Posts**: LinkedIn lädt Posts erst beim Scrollen nach (lazy loading). Scrolle mit `window.scrollTo(0, document.body.scrollHeight)`, warte 2 Sekunden, und lese erneut. LinkedIn zeigt Duplikate im DOM — filtere per `Set` auf Basis von Zeitstempel + Social-Counts.

**SSI nicht verfügbar**: Erfordert Zugang zu linkedin.com/sales/ssi. Schätze die 4 Säulen basierend auf beobachtbaren Profil-Signalen. Markiere als "(geschätzt)" im Report.

**Wettbewerber nicht abrufbar**: Minimum 2 Wettbewerber für sinnvolle Matrix. Bei <2: Branchenbenchmarks aus der Tabelle oben verwenden.

**Banner-Erstellung scheitert**: Font-Fallback (DejaVuSans) und Gradient-Fallback sind im Skript eingebaut. Wenn Buchcover nicht in Safe Zone passt: weglassen.

**DOCX-Generierung scheitert**: Prüfe ob das npm-Paket `docx` installiert ist (`npm install -g docx`). Prüfe das Ergebnis mit `unzip -l <Ausgabedatei>.docx`, `word/document.xml` muss enthalten sein. Bei Syntax-Fehlern im Report-Skript: Keine typografischen Anführungszeichen (U+201E, U+201C) in JavaScript-Strings verwenden — nur ASCII-Quotes (`"` und `'`). Umlaute (ä, ö, ü, ß) und andere UTF-8-Zeichen sind dagegen problemlos möglich und sollen immer korrekt geschrieben werden — niemals als ASCII-Umschreibungen (ae, oe, ue, ss).

---

## Quality Gates

| Phase | Gate | Methode |
|-------|------|---------|
| 1. Discovery | Alle Profildaten vollständig | Checkliste |
| 2. Scoring | Jeder Score mit Begründung | Sub-Kriterien aus SCORING.md |
| 3. Wettbewerb | Min. 3 Wettbewerber | Matrix ausgefüllt |
| 4. Profil | Headline in 60-Zeichen-Preview geprüft | Zeichenzahl-Check |
| 5. Banner | Kein Overlap in Safe Zone | Skript-Validierung |
| 6. Content | 3 Test-Posts auf Tonalität geprüft | Template-Check |
| 7. SSI | Baseline dokumentiert | Score notieren |
| 8. Report | Scoring-Delta dokumentiert | Vorher/Nachher |

---

## Changelog

```
v2.2.2 (2026-03-09) – Template anonymisiert
├── generate_report.js: Komplett neu geschrieben mit PROFILE/EXEC/HEADLINE/ABOUT/AUDIT/ROADMAP/LIMITS-Variablen
├── Report-Body ist jetzt 100% generisch — keine Namen, Firmen oder profilspezifischen Texte im Code
├── Alle kundenspezifischen Daten stehen ausschließlich im KUNDENDATEN-Block (Zeile 80-150)
├── Platzhalter-Werte ("Max Mustermann", "[Begründung]") als Vorlage für Anpassung
└── Template von 585 auf 278 Zeilen reduziert (gleiche Report-Struktur, kompakterer Code)

v2.2.1 (2026-03-09) – Korrekte Sonderzeichen
├── generate_report.js: 137 ASCII-Umschreibungen durch echte Umlaute ersetzt (ä, ö, ü, ß)
├── Regel in Fehlerbehandlung: Umlaute immer korrekt, nur typografische Quotes (U+201E) vermeiden
└── SKILL.md Changelog: ASCII-Reste bereinigt

v2.2.0 (2026-03-09) – Chrome-First + DOCX-Pflicht
├── Phase 1: Chrome-Plugin als primaere Datenquelle (navigate, get_page_text, javascript_tool)
├── Phase 1: JS-Snippets für Headline, About, Activity-Scraping dokumentiert
├── Phase 1: Fallback-Kaskade: Chrome → web_search → manuell
├── Phase 8: DOCX-Report als Pflicht-Deliverable (statt PDF)
├── Phase 8: scripts/generate_report.js als Strukturvorlage hinzugefuegt
├── Phase 8: 9-Kapitel-Struktur mit Erklärungspflicht für jede Tabelle/Grafik
├── Fehlerbehandlung: Chrome-spezifische Szenarien (Login, About-Truncation, Lazy Loading, Duplikate)
├── Fehlerbehandlung: DOCX-Generierung (npm docx, typografische Quotes, Validierung)
└── Verifikation: Report-Check auf DOCX-Validierung und Erklärungspflicht angepasst

v2.1.0 (2026-03-09) – Anthropic Skill Standard Compliance
├── Ordnerstruktur: references/, scripts/, assets/ nach Anthropic-Standard
├── SKILL.md auf <500 Zeilen reduziert mit klaren Verweisen auf references/
├── Banner-Code als eigenständiges Skript extrahiert (scripts/create_banner.py)
├── Font-Fallback (DejaVuSans) und Gradient-Fallback eingebaut
├── Frontmatter auf name + description reduziert (Anthropic-Standard)
├── Description trigger-optimiert ("pushy") mit expliziten Trigger-Phrasen
├── Verifikations-Abschnitt hinzugefügt
├── Fehlerbehandlung hinzugefügt
├── BANNER.md Sicherheits-Check-Bug gefixt (falsche Font-Referenz)
├── Claude-Code-Referenzen generalisiert
└── Imperativ-Form konsequenter angewandt

v2.0.0 (2026-02-28)
├── Gewichtetes Scoring-System eingeführt
├── Wettbewerbsanalyse als eigenständige Phase
├── LinkedIn-Algorithmus 2025/2026 Daten
├── SSI-Optimierung als eigene Phase
├── A/B-Testing-Framework
├── KPI-Dashboard
├── Branchenspezifische Anpassungen
├── Quality Gates
└── Top Voice Badge Anforderungen aktualisiert

v1.0.0 (2026-02-28)
└── Erstversion mit 6-Phasen-Workflow
```
