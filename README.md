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

Im Archiv liegen SKILL.md, `references/` einschließlich SOURCES.md, `scripts/create_banner.py`, `scripts/generate_report.js`, LICENSE und requirements.txt. Landingpage, Workflows und die Repo-Werkzeuge `check_versions.py`, `check_sources.py` und `build_skill_package.py` sind nicht enthalten.

Aus einem Klon lässt sich dasselbe Archiv selbst bauen, ohne Netz und ohne GitHub:

```bash
python scripts/build_skill_package.py dist/linkedin-optimizer.skill
```

Das Skript setzt feste Zeitstempel und eine feste Reihenfolge und speichert unkomprimiert. Zwei Läufe liefern dieselben Bytes, auch auf verschiedenen Rechnern.

`scripts/create_banner.py` braucht Pillow ab 10.1: `pip install -r requirements.txt`. `scripts/generate_report.js` braucht das npm-Paket `docx`.

## Deliverables

| Deliverable | Beschreibung |
|-------------|-------------|
| Gewichteter Profil-Score | 10-Kategorie-Bewertung (0–100) nach dem Raster in references/SCORING.md |
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
│   ├── check_sources.py        # Prüft SOURCES.md und die Rückkehr entfernter Zahlen
│   ├── build_skill_package.py  # Baut linkedin-optimizer.skill, reproduzierbar und offline
│   └── generate_report.js      # DOCX-Report-Template (Node.js, npm-Paket docx)
├── references/
│   ├── SCORING.md              # Gewichtete Bewertungsmatrix mit Sub-Kriterien und Bewertungsraster
│   ├── SOURCES.md              # Quellen mit Datum, zurückgezogene Zahlen, Prüfrhythmus
│   ├── TEMPLATES.md            # Vorlagen für Headline, About, Content, Kommentare
│   └── BANNER.md               # Technische Banner-Anleitung mit Viewport-Matrix
├── tests/
│   ├── fixtures/               # Drei frei erfundene Profile als JSON
│   ├── expected/               # Erwartete Score-Bänder je Fixture
│   └── run_eval.py             # Eval-Runner, prüft Matrix, Namen und Bänder
└── .github/workflows/
    ├── ci.yml                  # Syntax-, Banner-, Versions-, Quellen- und Paketprüfung
    └── release.yml             # Hängt das Artefakt an ein Tag v*
```

## Datenbasis

Jede Zahl im Skill hat in [references/SOURCES.md](references/SOURCES.md) entweder eine Zeile mit Quelle, URL, Veröffentlichungs- und Abrufdatum, oder sie steht dort unter „Zurückgezogen“ und ist aus dem Skill entfernt. Stand: 04.09.2026, nächste Prüfung: 04.03.2027.

Belegt:

- Dwell Time ist ein Ranking-Signal im Feed (LinkedIn Engineering Blog, 12.05.2020).
- Das blaue Top-Voices-Badge wird nur auf Einladung vergeben, Nominierungen prüft LinkedIn quartalsweise (LinkedIn Help).
- Das goldene Community-Top-Voice-Badge ist seit dem 08.10.2024 zurückgezogen (LinkedIn Help).
- Der SSI besteht aus vier Säulen (LinkedIn Sales Blog, 03.08.2015). Die Aufteilung in je 25 Punkte bestätigt LinkedIn nicht.

Zurückgezogen, weil nicht belegbar: der genannte Plattformdurchschnitt der Engagement-Rate, die Engagement-Prozentwerte je Postformat, die Wirkungsfaktoren für Kommentieren und Kontaktanfragen, die Angabe zur Sichtbarkeitsdauer eines Beitrags und die branchenspezifische Benchmark-Zeile. Die vollständige Liste mit Zahl und Begründung steht in SOURCES.md.

## Scoring

Die zehn Kategorien, ihre Gewichte und die Begründung je Gewicht stehen in [references/SCORING.md](references/SCORING.md#gewichtung). Dort liegt auch das [Engagement-Rate-Bewertungsraster](references/SCORING.md#engagement-rate-bewertungsraster) samt Berechnungsformel und die [Score-Interpretation](references/SCORING.md#score-interpretation), die einen Gesamtscore in einen Zeithorizont bis Top Voice übersetzt.

## Tests

```bash
python tests/run_eval.py
```

Der Runner liest das Gewichtsmodell aus `references/SCORING.md` und prüft damit drei erfundene
Profil-Fixtures gegen erwartete Score-Bänder. Er stellt außerdem sicher, dass die zehn Kategorien
in SCORING.md, SKILL.md, auf der Landingpage und in `scripts/generate_report.js` wortgleich
heißen, und dass die Zahlen der Scoring-Engine auf der Landingpage aus
`tests/fixtures/profile_mid.json` stammen.

Die Fixtures sind frei erfunden, nicht anonymisiert. Ein reales Profil zu erheben und danach zu
verfremden wäre genau die Datenverarbeitung, die SECURITY.md einschränkt.

Ein echter Lauf lässt sich gegen dieselben Bänder prüfen:

```bash
python tests/run_eval.py --fixture profile_mid --result lauf.json
```

## Grenzen

- Es gibt kein Vorher-Nachher. Das Rechenbeispiel auf der Landingpage und in `references/SCORING.md` ist ein erfundenes Profil aus `tests/fixtures/`, keine Messung. Ein belastbares Vorher-Nachher braucht zwei datierte Messungen desselben Profils im Abstand von 60 bis 90 Tagen.
- LinkedIn blockiert web_fetch und web_search über robots.txt. Ohne das Chrome-Plugin bleibt die manuelle Eingabe, und die Datenqualität sinkt entsprechend.
- Impressions sind öffentlich nicht sichtbar. `scripts/generate_report.js` schätzt die Engagement-Rate deshalb aus der Follower-Zahl, während das Bewertungsraster in SCORING.md Impressions als Nenner voraussetzt. Der geschätzte Wert liegt systematisch höher, beide sind nicht direkt vergleichbar.
- Der DOCX-Report enthält keine Diagramme. Radar-Chart und Balkendiagramm sind in SCORING.md als Darstellungsform beschrieben, das Report-Template erzeugt sie nicht.
- Der Ausgabepfad in `scripts/generate_report.js` steht fest auf `/mnt/user-data/outputs/`, also auf die Sandbox von claude.ai. Für einen lokalen Lauf muss die letzte Zeile angepasst werden.
- Der SSI lässt sich nur mit Zugang zu linkedin.com/sales/ssi ablesen. Ohne Zugang wird er aus Profil-Signalen geschätzt und ist im Report als geschätzt zu kennzeichnen.
- `scripts/create_banner.py` braucht Pillow ab 10.1. Ältere Versionen wenden die angeforderte Schriftgröße nicht auf den Ersatz-Font an; die Safe-Zone-Messung ist dann nicht belastbar, und `--strict` bricht ab.
- requirements.txt nennt für Pillow nur eine Untergrenze, keinen Pin. Für das npm-Paket `docx` gibt es weiterhin keine package.json, seine Version ist damit offen.

## Roadmap

Offene Punkte, ohne Termin:

- package.json für `docx`, dazu gepinnte Versionen statt der Untergrenze in requirements.txt.
- Ausgabepfad des Report-Templates konfigurierbar machen, statt ihn auf die claude.ai-Sandbox zu verdrahten.
- Fehlerfälle Rate Limit beziehungsweise LinkedIn-Checkpoint und geänderte DOM-Struktur in der Fehlerbehandlung ergänzen.

## Version

Die Versionsnummer steht in der Datei `VERSION`. README, SKILL.md, Landingpage und Report-Template führen sie als Kopie; `scripts/check_versions.py` vergleicht sie bei jedem Push gegen `VERSION` und schlägt bei Abweichung fehl. Der Release-Workflow prüft zusätzlich, dass der Tagname zu `VERSION` passt.

Aktuelle Version: v2.3.0. Was sich je Version geändert hat, steht im Changelog in [SKILL.md](SKILL.md#changelog).
