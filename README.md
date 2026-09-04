# linkedin-profil-optimierung v2.3.0

[![CI](https://github.com/GodModeAI2025/LinkedInOptimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/GodModeAI2025/LinkedInOptimizer/actions/workflows/ci.yml)

Ein Skill zur professionellen Analyse und Optimierung von LinkedIn-Profilen. Entwickelt für Berater, Agenturen und Freelancer, die Kunden strategisch als Thought Leader positionieren und auf das LinkedIn Top Voice Badge vorbereiten.

## Installation

Das Release-Artefakt heißt `linkedin-optimizer.skill` und liegt am jeweils letzten Release:

```bash
curl -LO https://github.com/GodModeAI2025/LinkedInOptimizer/releases/latest/download/linkedin-optimizer.skill
```

Die Datei entweder in Claude Chat ziehen oder lokal auspacken:

```bash
unzip linkedin-optimizer.skill -d /path/to/skills/user/linkedin-profil-optimierung/
```

Im Archiv liegen SKILL.md, `references/`, `scripts/create_banner.py`, `scripts/generate_report.js`, LICENSE und requirements.txt. Landingpage, Workflows und die Repo-Werkzeuge `check_versions.py` und `build_skill_package.py` sind nicht enthalten.

Aus einem Klon lässt sich dasselbe Archiv selbst bauen, ohne Netz und ohne GitHub:

```bash
python scripts/build_skill_package.py dist/linkedin-optimizer.skill
```

Das Skript setzt feste Zeitstempel und eine feste Reihenfolge und speichert unkomprimiert. Zwei Läufe liefern dieselben Bytes, auch auf verschiedenen Rechnern.

`scripts/create_banner.py` braucht Pillow ab 10.1: `pip install -r requirements.txt`. `scripts/generate_report.js` braucht das npm-Paket `docx`.

## Deliverables

| Deliverable | Beschreibung |
|-------------|-------------|
| Gewichteter Profil-Score | 10-Kategorie-Bewertung (0–100) mit Industrie-Benchmarks |
| Wettbewerbsanalyse | Positionierungsmatrix vs. 3–5 Nischen-Konkurrenten |
| Optimierte Headline | 3 Varianten mit SEO-Score, Zeichenzahl und Begründung |
| Optimierter About-Text | Orwell-inspiriert, strategische Hashtags, starker CTA |
| Banner | 1584×396px mit Safe-Zone-Validierung |
| Content Skill | Personalisierter Posting-Skill mit 10 Hook-Typen |
| Kommentar Skill | 5 Kommentar-Typen, 15–20 Ziel-Accounts |
| SSI-Aktionsplan | Social Selling Index Optimierung (4 Säulen) |
| DOCX-Report | Word-Dokument mit 9 Kapiteln, Scoring-Tabellen und Roadmap bis Monat 6 |

## Ordnerstruktur

```
LinkedInOptimizer/
├── README.md                   # Diese Übersicht
├── SKILL.md                    # Hauptworkflow (8 Phasen)
├── VERSION                     # Quelle der Versionsnummer, alles andere ist Kopie
├── requirements.txt            # Pillow-Untergrenze für create_banner.py
├── LICENSE                     # MIT-Lizenz
├── index.html                  # Landingpage (GitHub Pages, Quelle ist der Repo-Root)
├── scripts/
│   ├── create_banner.py        # Banner-Generator mit Safe-Zone-Validierung
│   ├── check_versions.py       # Prüft die Versionsangaben gegen VERSION
│   ├── build_skill_package.py  # Baut linkedin-optimizer.skill, reproduzierbar und offline
│   └── generate_report.js      # DOCX-Report-Template (Node.js, npm-Paket docx)
├── references/
│   ├── SCORING.md              # Gewichtete Bewertungsmatrix mit Sub-Kriterien und Benchmarks
│   ├── TEMPLATES.md            # Vorlagen für Headline, About, Content, Kommentare
│   └── BANNER.md               # Technische Banner-Anleitung mit Viewport-Matrix
└── .github/workflows/
    ├── ci.yml                  # Syntax-, Banner-, Versions- und Paketprüfung
    └── release.yml             # Hängt das Artefakt an ein Tag v*
```

## Datenbasis

- LinkedIn-Algorithmus 2025/2026 (Dwell Time, Comment Quality, Topische Konsistenz)
- Engagement-Benchmarks: Hootsuite 2025 (3,4% Plattform-Ø)
- Top Voice Kriterien: Halbjährliche Review seit Januar 2025
- SSI-Framework: 4 Säulen × 25 Punkte, Ziel ≥75

## Scoring

Die zehn Kategorien, ihre Gewichte und die Begründung je Gewicht stehen in [references/SCORING.md](references/SCORING.md#gewichtung). Dort liegen auch die [Engagement-Rate-Benchmarks](references/SCORING.md#engagement-rate-benchmarks-2025) samt Berechnungsformel und die [Score-Interpretation](references/SCORING.md#score-interpretation), die einen Gesamtscore in einen Zeithorizont bis Top Voice übersetzt.

## Grenzen

- LinkedIn blockiert web_fetch und web_search über robots.txt. Ohne das Chrome-Plugin bleibt die manuelle Eingabe, und die Datenqualität sinkt entsprechend.
- Impressions sind öffentlich nicht sichtbar. `scripts/generate_report.js` schätzt die Engagement-Rate deshalb aus der Follower-Zahl, während die Benchmark-Tabelle in SCORING.md Impressions als Nenner voraussetzt. Der geschätzte Wert liegt systematisch höher als der Benchmark-Wert, beide sind nicht direkt vergleichbar.
- Der DOCX-Report enthält keine Diagramme. Radar-Chart und Balkendiagramm sind in SCORING.md als Darstellungsform beschrieben, das Report-Template erzeugt sie nicht.
- Der Ausgabepfad in `scripts/generate_report.js` steht fest auf `/mnt/user-data/outputs/`, also auf die Sandbox von claude.ai. Für einen lokalen Lauf muss die letzte Zeile angepasst werden.
- Der SSI lässt sich nur mit Zugang zu linkedin.com/sales/ssi ablesen. Ohne Zugang wird er aus Profil-Signalen geschätzt und ist im Report als geschätzt zu kennzeichnen.
- `scripts/create_banner.py` braucht Pillow ab 10.1. Ältere Versionen wenden die angeforderte Schriftgröße nicht auf den Ersatz-Font an; die Safe-Zone-Messung ist dann nicht belastbar, und `--strict` bricht ab.
- requirements.txt nennt für Pillow nur eine Untergrenze, keinen Pin. Für das npm-Paket `docx` gibt es weiterhin keine package.json, seine Version ist damit offen.

## Roadmap

Offene Punkte, ohne Termin:

- package.json für `docx`, dazu gepinnte Versionen statt der Untergrenze in requirements.txt.
- Ausgabepfad des Report-Templates konfigurierbar machen, statt ihn auf die claude.ai-Sandbox zu verdrahten.
- Quellenangaben für die Engagement-Benchmarks in SCORING.md, dazu die Klärung, welcher Nenner gilt.
- Fehlerfälle Rate Limit beziehungsweise LinkedIn-Checkpoint und geänderte DOM-Struktur in der Fehlerbehandlung ergänzen.
- Testfälle für das Scoring mit erwarteten Score-Bändern.

## Version

Die Versionsnummer steht in der Datei `VERSION`. README, SKILL.md, Landingpage und Report-Template führen sie als Kopie; `scripts/check_versions.py` vergleicht sie bei jedem Push gegen `VERSION` und schlägt bei Abweichung fehl. Der Release-Workflow prüft zusätzlich, dass der Tagname zu `VERSION` passt.

Aktuelle Version: v2.3.0. Was sich je Version geändert hat, steht im Changelog in [SKILL.md](SKILL.md#changelog).
