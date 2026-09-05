## Phase 8: Report & Übergabe

### 8.0 Ethik-Abgleich

Bevor irgendetwas den Kunden erreicht, geht jedes der fünf Artefakte einmal gegen die Tabelle
„Ethik-Abgleich vor der Übergabe" in `references/ETHICS.md`: Headline gegen Regel 4,
About-Text gegen Regel 4 und 7, Content-Skill gegen Regel 1, Kommentar-Skill gegen Regel 2, 5
und 6, Report gegen Regel 3, 4 und 6. Findet der Abgleich etwas, ändere das Artefakt und nicht
den Abgleich. Halte im Report fest, wenn du dabei eine Kundenangabe herausgenommen hast, weil
sie unbelegt war.

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
   - Profil-Audit: 18-Punkte-Checkliste mit Status je Element
   - `ROADMAP`: Kundenspezifisch priorisierte Maßnahmen je Fenster in den Feldern `tag30`, `tag60` und `tag90`, die im Report als Überschriften "Tag 1-30: Quick Wins", "Tag 31-60: Content-Rhythmus" und "Tag 61-90: Sichtbarkeit" erscheinen, dazu `expectedScore` für die Prognose nach 90 Tagen und `handover` für den Übergang in den laufenden Betrieb
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

7. **Profil-Audit** (1 Seite): 18-Punkte-Checkliste als Tabelle mit Status (Vorhanden/Fehlt/Teilweise) und konkreter Maßnahme je Element. Zusammenfassung: X von 18 erfüllt.

8. **Roadmap** (1 Seite): Zeitlich priorisierte Maßnahmen in denselben drei Fenstern wie der SSI-Plan aus Phase 7: Tag 1–30 Quick Wins → Tag 31–60 Content-Rhythmus → Tag 61–90 Sichtbarkeit. Erwarteter Score nach 90 Tagen mit Begründung. Danach endet die Roadmap dieses Skills; der Übergang in den laufenden Betrieb wird benannt und nicht als vierte Phase mitgeplant.

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
