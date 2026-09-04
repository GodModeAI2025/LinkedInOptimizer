# linkedin-profil-optimierung v2.2.2

[![CI](https://github.com/GodModeAI2025/LinkedInOptimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/GodModeAI2025/LinkedInOptimizer/actions/workflows/ci.yml)

Ein Skill zur professionellen Analyse und Optimierung von LinkedIn-Profilen. Entwickelt für Berater, Agenturen und Freelancer, die Kunden strategisch als Thought Leader positionieren und auf das LinkedIn Top Voice Badge vorbereiten.

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
| PDF-Report | 10–15 Seiten mit Radar-Charts und 12-Monats-Roadmap |

## Ordnerstruktur

```
LinkedInOptimizer/
├── SKILL.md               # Hauptworkflow (8 Phasen)
├── index.html             # Landingpage (GitHub Pages, Quelle ist der Repo-Root)
├── scripts/
│   ├── create_banner.py   # Banner-Generator mit Safe-Zone-Validierung
│   ├── check_versions.py  # Vergleicht die Versionsangaben in README, SKILL.md, index.html, Report-Template
│   └── generate_report.js # DOCX-Report-Template (Node.js, npm-Paket docx)
├── references/
│   ├── SCORING.md         # Gewichtete Bewertungsmatrix mit Sub-Kriterien und Benchmarks
│   ├── TEMPLATES.md       # Vorlagen für Headline, About, Content, Kommentare
│   └── BANNER.md          # Technische Banner-Anleitung mit Viewport-Matrix
└── .github/workflows/
    └── ci.yml             # Syntax-, Banner- und Versionsprüfung
```

## Datenbasis

- LinkedIn-Algorithmus 2025/2026 (Dwell Time, Comment Quality, Topische Konsistenz)
- Engagement-Benchmarks: Hootsuite 2025 (3,4% Plattform-Ø)
- Top Voice Kriterien: Halbjährliche Review seit Januar 2025
- SSI-Framework: 4 Säulen × 25 Punkte, Ziel ≥75

## Version

Aktuelle Version: v2.2.2. Was sich je Version geändert hat, steht im Changelog in [SKILL.md](SKILL.md#changelog).
