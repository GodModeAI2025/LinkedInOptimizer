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
  Abgrenzung: Dieser Skill macht die einmalige Ist-Analyse und liefert die Profil-Artefakte.
  Geht es um den laufenden Betrieb, also Wochenroutine, Content-Kalender, Community-Aufbau,
  Analytics-Auswertung oder Monetarisierung, ist linkedin-community-builder zuständig.
---

# LinkedIn Profil-Optimierung & Thought-Leader Skill v2.3.0

Ein 8-Phasen-Workflow zur Analyse und Optimierung von LinkedIn-Profilen. Was daran belegt ist und was nicht, steht in `references/SOURCES.md`: belegte Quellen mit URL und Datum, zurückgezogene Zahlen und die Angaben, die ausdrücklich Erfahrungswerte aus der Beratungspraxis sind. Bewerte kein Kundenprofil gegen eine Zahl, die dort nicht steht.

## Abgrenzung zum Schwester-Skill

Es gibt einen zweiten LinkedIn-Skill derselben Herkunft: `linkedin-community-builder`
(Repo [LinkedIn-Orchestrator](https://github.com/GodModeAI2025/LinkedIn-Orchestrator)). Beide
reagieren auf dieselben Formulierungen, unter anderem „Profil optimieren", „Profil verbessern",
„Personal Branding", „Content-Strategie" und „Top Voice". Ohne Regel muss das Modell raten. Die
Regel steht hier.

| | linkedin-profil-optimierung (dieser Skill) | linkedin-community-builder |
|--|--|--|
| Aufgabe | Einmalige Ist-Analyse und Profil-Artefakte | Laufender Betrieb über Wochen und Monate |
| Ergebnis | Score, Headline, About, Banner, Wettbewerbsmatrix, SSI-Plan, DOCX-Report | Wochensystem, Content-Kalender, Community-Aufbau, Analytics, Monetarisierung |
| Zeitform | Bestandsaufnahme mit Übergabe am Ende | Zustandsgesteuert, läuft weiter |
| Werkzeuge | Chrome-Plugin, Banner-Skript, Report-Template | Rein konversationell |

Entscheidungsregel bei überlappenden Anfragen:

1. Geht es darum, wie das Profil dasteht, was es wert ist, wie Headline, About, Banner oder
   Report aussehen sollen: dieser Skill.
2. Geht es darum, was diese Woche gepostet wird, warum die Reichweite nicht wächst, wie eine
   Community oder ein Newsletter aufgebaut wird oder wie sich das monetarisieren lässt:
   `linkedin-community-builder`. Verweise darauf und arbeite die Frage nicht selbst ab.
3. Kommt beides in einer Anfrage vor, beginne hier. Eine Content-Strategie ohne Ist-Analyse
   optimiert auf ein Profil, das sich gleich ändert. Nach der Übergabe in Phase 8 verweise
   ausdrücklich auf den Schwester-Skill für den Betrieb.
4. „Top Voice" kommt in beiden vor und meint zweierlei: hier die Messung der Reife und der
   Maßnahmenplan, dort die wöchentliche Umsetzung. Kläre im Zweifel mit einer Rückfrage, welche
   der beiden Seiten gemeint ist.

Der Content-Skill und der Kommentar-Skill aus Phase 6 sind Vorlagen, die einmal erstellt und
übergeben werden. Sie ersetzen nicht die laufende Redaktionsarbeit.

---

## Ressourcen-Übersicht

Lies die jeweilige Datei, wenn du die Phase erreichst:

| Datei | Inhalt | Wann lesen |
|-------|--------|-----------|
| `references/SCORING.md` | Gewichtete 10-Kategorien-Matrix mit Sub-Kriterien und Bewertungsraster | Phase 2 (Scoring) |
| `references/TEMPLATES.md` | Vorlagen für Headline, About, Content-Skill, Kommentar-Skill | Phase 4 + 6 |
| `references/BANNER.md` | Technische Banner-Anleitung mit Safe Zones und Viewport-Matrix | Phase 5 |
| `references/SOURCES.md` | Quellen mit Datum, zurückgezogene Zahlen, Erfahrungswerte, Prüfrhythmus | Vor jeder Zahl im Report |
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

Dokumentiere den Social Selling Index. LinkedIn benennt vier Säulen (Q5 in `references/SOURCES.md`); die Aufteilung in je 25 Punkte bis 100 bestätigt LinkedIn nicht und ist als Konvention zu kennzeichnen. Zielmarken dieses Skills, keine Branchenwerte: SSI über 70 gilt als effektiv, über 75 als Thought-Leader-Niveau.

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

`scripts/create_banner.py` braucht Pillow ab 10.1. Fehlt es, endet der Aufruf mit `ModuleNotFoundError: No module named 'PIL'`. Installiere die Abhängigkeit vorher mit `pip install -r requirements.txt` im Skill-Verzeichnis, also dort, wo diese SKILL.md und requirements.txt nebeneinander liegen.

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

Algorithmische Leitplanken, mit Beleglage in `references/SOURCES.md`:
- Dwell Time = zentrales Signal → Texte 300–400 Wörter, Story-Struktur
- Comment Quality > Like-Volumen → CTAs die inhaltliche Antworten provozieren
- Save Rate = Qualitätssignal → Frameworks, Listen, Checklisten
- Topische Konsistenz → ≥80% Posts in max. 2 Fokusthemen
- Engagement Bait wird bestraft → Kein „What do you think?", „Agree?"

Formate nach Wirkung, als Reihenfolge und ohne Prozentwerte: Dokument- und Multi-Image-Beiträge vor Video, Video vor reinem Text und Link-Beiträgen. Das ist ein Erfahrungswert (`references/SOURCES.md`). Die früher hier genannten Prozentwerte je Format sind zurückgezogen, weil sich keine prüfbare Quelle dafür findet. Nenne im Report keine Format-Prozentwerte.

### 6.2 Kommentar-Strategie

Strategisches Kommentieren (5–10/Tag) auf fremden Beiträgen zahlt auf Sichtbarkeit und Profilaufrufe ein. Kommentare über 15 Wörter mit eigener Perspektive wirken besser als kurze Zustimmung. Beides ist Erfahrungswert. Die früher hier genannten Prozentfaktoren sind zurückgezogen, die Liste steht in `references/SOURCES.md`. Identifiziere 15–20 Ziel-Accounts (Top Voices, C-Level, Journalisten, Peers).

### 6.3 Posting-Frequenz und Timing

3–5 Posts/Woche, Mo–Do 8:00–8:30 CET, erste 90 Minuten nach Post aktiv kommentieren. 5–10 qualitative Kommentare/Tag auf fremde Posts. Keine Pause >7 Tage.

---

## Phase 7: SSI-Optimierung

LinkedIn benennt vier SSI-Säulen (Q5 in `references/SOURCES.md`). Die verbreitete Aufteilung in je 25 Punkte bestätigt LinkedIn dort nicht; behandle sie als Konvention, nicht als Tatsache.

Maßnahmen pro SSI-Säule:

1. **Professional Brand**: Profil vollständig, regelmäßig Content, Multimedia, strategische Endorsements
2. **Find the Right People**: 5–10 strategische Connections/Woche, Kontaktanfragen immer mit persönlicher Nachricht (Erfahrungswert, die frühere Prozentangabe zur Annahmequote ist zurückgezogen)
3. **Engage with Insights**: Täglich kommentieren, eigene Standpunkte. Beiträge zu Collaborative Articles zahlen nicht mehr auf ein Badge ein (Q3), sie bleiben nur als Sichtbarkeitskanal sinnvoll.
4. **Build Relationships**: Inbox pflegen, Kommentare <2h beantworten, Follow-ups, Empfehlungen schreiben

Ziel-SSI nach 90 Tagen: ≥75

---

## Phase 8: Report & Übergabe

### 8.1 DOCX-Report erstellen (Pflicht-Deliverable)

Der Analyse-Report wird immer als professionelles Word-Dokument (.docx) geliefert. Nutze `scripts/generate_report.js` als Strukturvorlage. Lies das Skript, passe die Daten-Konstanten (scoringData, posts, Profilinfos) an den analysierten Kunden an, und führe es aus.

**Vorgehen:**
1. Lies `scripts/generate_report.js` mit dem view-Tool
2. Kopiere es unter dem Namen `generate_report.js` in das Arbeitsverzeichnis und installiere dort das Paket `docx` mit `npm install docx`
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

4. **Content-Aktivität** (1 Seite): Tabelle der letzten Posts mit Zeitpunkt, Reaktionen, Kommentaren, geschätzter Engagement-Rate. Darunter Erklärung der Methodik (worauf die Schätzung basiert, was nicht messbar war) und Bewertung der Kennzahlen (Median, Vergleich mit dem Bewertungsraster in `references/SCORING.md`, sofern der Nenner passt).

5. **Headline-Analyse** (1 Seite): Aktuelle Headline mit Bewertung (was funktioniert, was nicht, warum), 3 Optimierungsvorschläge mit Zeichenzahl, ersten 60 Zeichen und Erklärung der jeweiligen Strategie.

6. **About-Sektion-Analyse** (1 Seite): Hook-Bewertung der ersten 270 Zeichen, gefundene verbotene Wörter mit konkreten Ersetzungsvorschlägen und Begründung, CTA-Bewertung mit Alternativvorschlag, fehlende Elemente (Hashtags, Zeichenauslastung).

7. **Profil-Audit** (1 Seite): 17-Punkte-Checkliste als Tabelle mit Status (Vorhanden/Fehlt/Teilweise) und konkreter Maßnahme je Element. Zusammenfassung: X von 17 erfüllt.

8. **Roadmap** (1 Seite): Zeitlich priorisierte Maßnahmen (Woche 1–2 Quick Wins → Woche 3–4 Content-Start → Monat 2–3 Skalierung → Monat 4–6 Authority Building). Erwarteter Score nach 3 Monaten mit Begründung.

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

Monatlich tracken: Follower, Profilaufrufe, Engagement-Rate, Kommentare/Post, Impressions/Post, Save-Rate, SSI, Posting-Frequenz, Newsletter-Abos.

Die Zielwerte dazu (Engagement-Rate >5 %, Kommentare/Post >15, Impressions/Post >5.000, Save-Rate >2 %, SSI ≥75, Posting-Frequenz ≥3/Woche) sind selbst gesetzte Ziele, keine Branchenwerte. Kennzeichne sie im Report so und vergleiche sie nur mit dem Vormonat desselben Profils.

---

## Top Voice Badge – Anforderungen

Das blaue Top-Voices-Badge vergibt LinkedIn nur auf Einladung. Nominierungen (auch Selbstnominierungen) prüft LinkedIn quartalsweise (Q4 in `references/SOURCES.md`). Das goldene Community-Top-Voice-Badge über Collaborative Articles ist seit dem 08.10.2024 zurückgezogen und lässt sich nicht mehr verdienen (Q3).

Die folgende Tabelle ist kein Kriterienkatalog von LinkedIn, sondern die Übersetzung der öffentlich genannten Anforderungen in beobachtbare Größen. Behandle sie als Arbeitsraster.

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

Die folgenden Zeilen sind Erfahrungswerte, keine erhobenen Branchenkennzahlen. Die früher hier geführte Zeile mit branchenspezifischen Engagement-Benchmarks ist zurückgezogen, weil sich weder Nenner noch Erhebung belegen ließen (`references/SOURCES.md`).

| Parameter | Tech/KI | Energie | Finance | Consulting | Healthcare |
|-----------|---------|---------|---------|------------|------------|
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

**Report**: DOCX erzeugt, als ZIP lesbar (`unzip -l` listet `word/document.xml`), alle 9 Kapitel vorhanden, jede Tabelle hat einen erklärenden Textabsatz darunter, keine Scoring-Kategorie ohne Begründung.

Bei Fehlern: Automatisch korrigieren und erneut prüfen.

---

## Fehlerbehandlung

**LinkedIn blockiert web_fetch/web_search**: Das ist der Normalfall — LinkedIn blockiert robots.txt-basierte Zugriffe. Nutze IMMER das Chrome-Plugin als primäre Datenquelle. Folge der Kaskade aus Phase 1.0: Chrome → web_search → manuell.

**Chrome-Plugin nicht verfügbar**: Wenn der Benutzer kein Chrome-Plugin hat, informiere ihn dass die Datenqualität eingeschränkt ist. Nutze web_search für öffentlich sichtbare Snippets (Name, Headline, Unternehmen, Connections). Frage nach Screenshot oder PDF-Export für den Rest. Markiere alle geschätzten Daten im Report.

**Profil nur eingeschränkt sichtbar** (nicht eingeloggt): Einige Profil-Abschnitte sind ohne LinkedIn-Login nicht sichtbar (About nach 3 Zeilen, Empfehlungen, Skills, detaillierte Positionen). Bitte den Benutzer sich in Chrome bei LinkedIn einzuloggen und starte die Erhebung erneut.

**About-Text abgeschnitten im DOM**: LinkedIn rendert den About-Text in einem `span[aria-hidden="true"]` mit ca. 1600 Zeichen. Wenn abgeschnitten: Lies den zweiten Teil mit `.substring(800)` in einem separaten `javascript_tool`-Aufruf. Falls ein "mehr anzeigen"-Button existiert, klicke ihn vorher.

**Activity-Seite zeigt wenige Posts**: LinkedIn lädt Posts erst beim Scrollen nach (lazy loading). Scrolle mit `window.scrollTo(0, document.body.scrollHeight)`, warte 2 Sekunden, und lese erneut. LinkedIn zeigt Duplikate im DOM — filtere per `Set` auf Basis von Zeitstempel + Social-Counts.

**SSI nicht verfügbar**: Erfordert Zugang zu linkedin.com/sales/ssi. Schätze die 4 Säulen basierend auf beobachtbaren Profil-Signalen. Markiere als "(geschätzt)" im Report.

**Wettbewerber nicht abrufbar**: Das Quality Gate für Phase 3 verlangt 3 Wettbewerber. Sind nur 2 erreichbar, erstelle die Matrix mit 2 und vermerke die Abweichung im Report. Bei <2: Branchenbenchmarks aus der Tabelle oben verwenden.

**Banner-Erstellung scheitert**: Bei `ModuleNotFoundError: No module named 'PIL'` fehlt Pillow. Hole `pip install -r requirements.txt` im Skill-Verzeichnis nach; die Datei liegt neben dieser SKILL.md und begründet dort die Untergrenze 10.1. Font-Fallback (DejaVuSans) und Gradient-Fallback sind im Skript eingebaut. Wenn Buchcover nicht in Safe Zone passt: weglassen.

**DOCX-Generierung scheitert**: Prüfe ob das npm-Paket `docx` im Arbeitsverzeichnis installiert ist (`npm install docx`). Eine globale Installation reicht nicht: `require("docx")` durchsucht nur die node_modules-Ordner oberhalb des Skripts, nicht das globale npm-Verzeichnis. Prüfe das Ergebnis mit `unzip -l <Ausgabedatei>.docx`, `word/document.xml` muss enthalten sein. Bei Syntax-Fehlern im Report-Skript: Keine typografischen Anführungszeichen (U+201E, U+201C) in JavaScript-Strings verwenden — nur ASCII-Quotes (`"` und `'`). Umlaute (ä, ö, ü, ß) und andere UTF-8-Zeichen sind dagegen problemlos möglich und sollen immer korrekt geschrieben werden — niemals als ASCII-Umschreibungen (ae, oe, ue, ss).

---

## Quality Gates

| Phase | Gate | Methode |
|-------|------|---------|
| 1. Discovery | Alle Profildaten vollständig | Checkliste |
| 2. Scoring | Jeder Score mit Begründung | Sub-Kriterien aus SCORING.md |
| 3. Wettbewerb | Min. 3 Wettbewerber, Ausnahme siehe Fehlerbehandlung | Matrix ausgefüllt |
| 4. Profil | Headline in 60-Zeichen-Preview geprüft | Zeichenzahl-Check |
| 5. Banner | Kein Overlap in Safe Zone | Skript-Validierung |
| 6. Content | 3 Test-Posts auf Tonalität geprüft | Template-Check |
| 7. SSI | Baseline dokumentiert | Score notieren |
| 8. Report | Scoring-Delta dokumentiert | Vorher/Nachher |

---

## Changelog

```
v2.3.0 (2026-09-04) – Erstes Release, Banner-Skript repariert
├── create_banner.py: --background ist optional, ohne Hintergrundbild entsteht ein Gradient
├── create_banner.py: die angeforderte Schriftgröße wirkt jetzt auch auf den PIL-Ersatz-Font
├── create_banner.py: Safe-Zone-Verletzungen werden zurückgegeben, --strict endet dann mit Exitcode 1
├── create_banner.py: ein Font ohne anwendbare Größenangabe zählt selbst als Verletzung
├── Beispieldaten in den Templates ersetzen die vorher enthaltenen realen Profildaten
├── requirements.txt ergänzt: Pillow ab 10.1, dazu der Hinweis auf das npm-Paket docx
├── scripts/build_skill_package.py baut linkedin-optimizer.skill reproduzierbar und ohne Netz
├── Release-Workflow hängt dieses Artefakt an ein Tag v*
├── CI prüft Syntax, Banner-Verhalten, Versionsangaben und den Inhalt des Artefakts
├── VERSION ist die Quelle der Versionsnummer, check_versions.py prüft die Kopien dagegen
└── README und Landingpage: Grenzen, Roadmap und Installationsweg an den Stand angepasst

v2.2.2 (2026-03-09) – Template anonymisiert
├── generate_report.js: Komplett neu geschrieben mit PROFILE/EXEC/HEADLINE/ABOUT/AUDIT/ROADMAP/LIMITS-Variablen
├── Report-Body ist jetzt 100% generisch — keine Namen, Firmen oder profilspezifischen Texte im Code
├── Alle kundenspezifischen Daten stehen ausschließlich im KUNDENDATEN-Block (PROFILE bis LIMITS, Zeile 32-149)
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
├── Ordnerstruktur: references/ und scripts/ nach Anthropic-Standard
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
