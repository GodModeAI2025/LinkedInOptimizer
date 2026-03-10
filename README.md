# linkedin-profil-optimierung v2.1

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
linkedin-profil-skill-2/
├── SKILL.md              # Hauptworkflow (8 Phasen, <500 Zeilen)
├── scripts/
│   ├── create_banner.py  # Banner-Generator mit Safe-Zone-Validierung
│   └── generate_report.js # DOCX-Report-Template (Node.js/docx-js)
├── references/
│   ├── SCORING.md        # Gewichtete Bewertungsmatrix mit Sub-Kriterien
│   ├── TEMPLATES.md      # Vorlagen für Headline, About, Content, Kommentare
│   └── BANNER.md         # Technische Banner-Anleitung mit Viewport-Matrix
└── assets/               # (Platzhalter für Kundenassets wie Logos, Covers)
```

## Datenbasis

- LinkedIn-Algorithmus 2025/2026 (Dwell Time, Comment Quality, Topische Konsistenz)
- Engagement-Benchmarks: Hootsuite 2025 (3,4% Plattform-Ø)
- Top Voice Kriterien: Halbjährliche Review seit Januar 2025
- SSI-Framework: 4 Säulen × 25 Punkte, Ziel ≥75

## Version

v2.2.0 – Chrome-First Datenerhebung, DOCX als Pflicht-Deliverable, Report-Template in scripts/.
