# Changelog

Versionsgeschichte des Skills `linkedin-profil-optimierung`. Die aktuelle Version steht in
`VERSION` und in der Überschrift von `SKILL.md`.

```
v2.6.0 (2026-09-05) – Router statt Monolith, Untrusted-Regel, kuerzerer Trigger
├── SKILL.md war 588 Zeilen lang und wurde bei jedem Treffer vollstaendig geladen; jetzt 190 Zeilen Router mit Ablauftabelle
├── Die acht Phasen liegen in references/PHASE-1-discovery.md bis PHASE-8-report.md, Wortlaut unveraendert, und werden gelesen, wenn die Phase dran ist
├── Der Changelog steht in CHANGELOG.md statt in SKILL.md; check_versions.py prueft dort den obersten Eintrag
├── references/UNTRUSTED.md: erhobener Seitentext ist Daten, nie Anweisung, verankert in Phase 1.1 und 3.1; schliesst die Benennung von SECURITY.md Luecke 3
├── Die description im Frontmatter von 898 auf 394 Zeichen, mit Abgrenzungssatz zum Schwester-Skill; scripts/check_descriptions.py prueft Laenge, Strichzeichen und Abgrenzung
├── tests/run_eval.py prueft den Skill-Text aus Router und Phasendateien zusammen und bindet zusaetzlich die Untrusted-Regel
└── SECURITY.md: Zeilenangaben durch Datei- und Abschnittsangaben ersetzt, Luecke 9 als erledigt vermerkt
```

```
v2.5.0 (2026-09-05) – Ethik, Wettbewerbsvorlage, ein Zeitraster
├── references/ETHICS.md: acht Leitplanken mit Begründung, dazu der Satz, was der Skill ablehnt, auch wenn der Kunde es verlangt
├── Die Engagement-Bait-Regel ist nicht mehr als Algorithmus-Regel begründet, sondern als Haltung; die Strafe ist der Nebeneffekt
├── Die gesperrten CTA-Formulierungen liefen unter vier verschiedenen Längen, jetzt an allen vier Stellen dieselben vier
├── Ethik-Abgleich als Phase 8.0, als Zeile in der Verifikation und als Quality Gate
├── references/COMPETITIVE.md: Auswahlregel, zehn Achsen mit Herkunft und Grenze, Ausgabeformat mit Erhebungsdatum
├── Der Widerspruch zwischen Gate und Fehlerpfad ist aufgelöst, es gilt 3; unter 3 ist das Gate nicht bestanden und die Matrix als unvollständig gekennzeichnet
├── Der geschätzte SSI eines Wettbewerbers entfällt, er ist nur für das eigene Konto ablesbar; damit zehn Achsen statt elf
├── Ein Zeitraster statt drei: Tag 1–30, 31–60, 61–90 in Phase 7, in Kapitel 8 des Reports, im Report-Template, in README und auf der Landingpage
├── Phase 7 trägt je Fenster eine Hypothese, eine Messgröße und den Messweg, mit dem Vorbehalt für fehlenden SSI-Zugang
├── Die Spalte „Erwarteter Zeithorizont bis Top Voice" in SCORING.md ist als Prognose gekennzeichnet und steht als Erfahrungswert in SOURCES.md
└── run_eval.py bindet CTA-Liste, Achsen, Mindestzahl und Zeitfenster und weist die abgelösten Wortlaute zurück

v2.4.0 (2026-09-04) – Beleglage, Eval-Set, Abgrenzung
├── references/SOURCES.md: sieben Quellen mit URL, Veröffentlichungs- und Abrufdatum, dazu je Quelle, was sie nicht belegt
├── Elf unbelegte Zahlen ohne Ersatz entfernt, darunter der Plattformdurchschnitt der Engagement-Rate und die Werte je Postformat
├── Sachfehler korrigiert: das goldene Community-Top-Voice-Badge ist seit dem 08.10.2024 zurückgezogen (Q3), Nominierungen prüft LinkedIn quartalsweise (Q4)
├── Sub-Kriterium Collaborative Articles entfällt, der Punkt liegt bei Momentum; der laut Q7 entfallene Schalter ist durch die Creator-Tools ersetzt
├── SCORING.md: Nenner der Engagement-Rate geklärt, das Raster gilt für den impressions-basierten Wert
├── Die zehn Kategorien heißen an allen vier Stellen gleich, generate_report.js zog vier Kurznamen nach
├── tests/: drei frei erfundene Profil-Fixtures, erwartete Score-Bänder und tests/run_eval.py
├── scripts/check_sources.py hält zurückgezogene Aussagen aus dem Skill heraus; die Sperren entstehen aus der Sperrmuster-Spalte in SOURCES.md, nicht aus einer Handliste daneben
├── Quellen-IDs werden in jeder Schreibweise geprüft, nicht nur in runden Klammern
├── Die Checkliste in SCORING.md Abschnitt 9 ist die Quelle der 18 Profil-Elemente; SKILL.md Phase 4.3 nannte 15, die Deliverables-Beschreibung 17, die Audit-Tabelle im Report 17
├── Audit-Tabelle im Report: 18 Elemente statt 17, Video-Content gehört zur Content-Aktivität und nicht zur Profil-Vollständigkeit
├── Landingpage: aus "Live Demo" wird "Beispiel-Dialog", jede Zahl stammt aus tests/fixtures/profile_mid.json, und run_eval.py bindet diesen Wortlaut
├── Abgrenzung zu linkedin-community-builder in SKILL.md, README und auf der Landingpage, inklusive Trigger-Regel
├── Sperrmuster fangen jetzt auch die Bindestrich-Schreibweise, die ae-Umschrift von Umlauten und ein Kontextwort mit Abstand zur Zahl
├── Die Ausnahme, mit der sich eine Sperre über die Tabellenzelle „keine:" abschalten ließ, ist wieder entfernt; die Zeile zu Collaborative Articles trägt die Schreibweisen aus v2.3.0
├── Jedes Sperrmuster muss den eigenen Wortlaut in der Spalte „Frühere Aussage" treffen, sonst fällt die Zeile im CI-Lauf auf
├── Neue Belegpflicht in check_sources.py: ein Absatz, der Collaborative Articles und ein Badge in einem Zug nennt, muss Q3 zitieren
└── CI fährt Beleglage und Eval-Set mit

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
