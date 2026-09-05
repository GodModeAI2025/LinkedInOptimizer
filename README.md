# linkedin-profil-optimierung v2.5.0

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
| Wettbewerbsanalyse | Positionierungsmatrix auf zehn Achsen gegen 3–5 Nischen-Konkurrenten, Erhebungsrahmen in references/COMPETITIVE.md |
| Optimierte Headline | 3 Varianten mit SEO-Score, Zeichenzahl und Begründung |
| Optimierter About-Text | Orwell-inspiriert, strategische Hashtags, starker CTA |
| Banner | 1584×396px mit Safe-Zone-Validierung |
| Content Skill | Personalisierter Posting-Skill mit 10 Hook-Typen |
| Kommentar Skill | 5 Kommentar-Typen, 15–20 Ziel-Accounts |
| SSI-Aktionsplan | Social Selling Index Optimierung über 4 Säulen, aufgeteilt auf Tag 1–30, 31–60 und 61–90, je mit Hypothese und Messweg |
| DOCX-Report | Word-Dokument mit 9 Kapiteln, Scoring-Tabellen und 30/60/90-Tage-Roadmap |

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
│   ├── check_sources.py        # Prüft SOURCES.md und sperrt zurückgezogene Aussagen
│   ├── build_skill_package.py  # Baut linkedin-optimizer.skill, reproduzierbar und offline
│   └── generate_report.js      # DOCX-Report-Template (Node.js, npm-Paket docx)
├── references/
│   ├── SCORING.md              # Gewichtete Bewertungsmatrix mit Sub-Kriterien und Bewertungsraster
│   ├── SOURCES.md              # Quellen mit Datum, zurückgezogene Zahlen, Prüfrhythmus
│   ├── ETHICS.md               # Ethische Leitplanken, gesperrte CTA-Formulierungen, Ethik-Abgleich
│   ├── COMPETITIVE.md          # Erhebungsrahmen der Wettbewerbsanalyse: Auswahlregel, zehn Achsen, Ausgabe
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

## Verhältnis zum Schwester-Skill

Neben diesem Skill gibt es [LinkedIn-Orchestrator](https://github.com/GodModeAI2025/LinkedIn-Orchestrator) mit dem Skill `linkedin-community-builder`. Die beiden bleiben getrennt, weil sie verschiedene Aufgaben haben.

| | linkedin-profil-optimierung (dieses Repo) | linkedin-community-builder |
|--|--|--|
| Aufgabe | Einmalige Ist-Analyse und Profil-Artefakte | Laufender Betrieb über Wochen und Monate |
| Ergebnis | Score, Headline, About, Banner, Wettbewerbsmatrix, SSI-Plan, DOCX-Report | Wochensystem, Content-Kalender, Community, Analytics, Monetarisierung |
| Zeitform | Bestandsaufnahme mit Übergabe am Ende | Zustandsgesteuert, läuft weiter |
| Werkzeuge | Chrome-Plugin, Banner-Skript, Report-Template | Rein konversationell |

Beide reagieren heute auf dieselben Formulierungen: „Profil optimieren", „Profil verbessern", „Personal Branding", „Content-Strategie", „Top Voice". Das ist kein Schönheitsfehler, sondern führt dazu, dass Claude bei solchen Sätzen zwischen zwei Skills wählen muss. Die Auflösung steht im Abschnitt [Abgrenzung zum Schwester-Skill](SKILL.md#abgrenzung-zum-schwester-skill) in SKILL.md: Ist-Analyse und Artefakte hier, laufender Betrieb dort, bei beidem zuerst hier und danach Übergabe.

Der Orchestrator führt seinerseits eine Abgrenzungstabelle, beschreibt diesen Skill darin aber nur in einer Zeile und ohne Trigger-Regel. Die Gegenrichtung dort nachzuziehen ist ein eigener Vorgang in jenem Repo.

## Was dieser Skill nicht tut

Der Skill positioniert Menschen öffentlich, unter ihrem Klarnamen. Deshalb schreibt er keine
Behauptung ins Profil, die der Kunde nicht belegen kann, und er baut keine Reichweite, die nicht
aus dem Interesse echter Leser entsteht. Das gilt auch dann, wenn ein Kunde ausdrücklich etwas
anderes beauftragt.

Abgelehnt wird: erfundene Titel, Rollen, Auszeichnungen oder Kundenzahlen; gekaufte Follower,
Reaktionen und Kommentare; Pods und abgesprochene Kommentar-Runden; Automatisierung von
Kontaktanfragen, Kommentaren oder Nachrichten; Fremdprofile über den Anlass hinaus.

Die Regeln stehen mit ihrer Begründung in [references/ETHICS.md](references/ETHICS.md), der
Abgleich vor der Übergabe in SKILL.md Phase 8.0. Was davon geprüft wird und was nicht, steht in
ETHICS.md unter „Was diese Seite nicht leistet": `tests/run_eval.py` bindet die gesperrten
CTA-Formulierungen an vier Fundstellen und prüft, dass der Abgleich in SKILL.md verankert ist.
Ob eine Angabe im Profil stimmt, ob der Kunde den Text gelesen hat und ob sich jemand im
Gespräch über eine Regel hinwegsetzt, sieht kein Skript.

## Datenbasis

Jede Zahl im Skill hat in [references/SOURCES.md](references/SOURCES.md) entweder eine Zeile mit Quelle, URL, Veröffentlichungs- und Abrufdatum, oder sie steht dort unter „Zurückgezogen“ und ist aus dem Skill entfernt. Stand: 04.09.2026, nächste Prüfung: 04.03.2027.

Belegt:

- Dwell Time ist ein Ranking-Signal im Feed (LinkedIn Engineering Blog, 12.05.2020).
- Das blaue Top-Voices-Badge wird nur auf Einladung vergeben, Nominierungen prüft LinkedIn quartalsweise (LinkedIn Help).
- Das goldene Community-Top-Voice-Badge ist seit dem 08.10.2024 zurückgezogen (LinkedIn Help).
- Der SSI besteht aus vier Säulen (LinkedIn Sales Blog, 03.08.2015). Die Aufteilung in je 25 Punkte bestätigt LinkedIn nicht.

Zurückgezogen, weil nicht belegbar: der genannte Plattformdurchschnitt der Engagement-Rate, die Engagement-Prozentwerte je Postformat, die Wirkungsfaktoren für Kommentieren und Kontaktanfragen, die Angabe zur Sichtbarkeitsdauer eines Beitrags, die branchenspezifische Benchmark-Zeile, die Rahmung des Punkterasters als Branchen-Benchmark und die Selbstbeschreibung des Skills als evidenzbasiert. Die vollständige Liste mit Begründung steht in SOURCES.md.

`scripts/check_sources.py` baut die Sperren gegen diese Aussagen aus der Spalte „Sperrmuster“ derselben Tabelle und läuft in der CI. Es prüft Schreibweisen, keine Aussagen. Ein Muster fängt die Zahl mit Komma und mit Punkt, das Prozentzeichen und das ausgeschriebene Wort, das geschützte Leerzeichen als HTML-Entity und das ASCII-x als Faktorzeichen. Ein frei formulierter Satz, der dieselbe Behauptung ohne die gesperrte Schreibweise aufstellt, fällt nicht auf. Jede Zeile der Tabelle trägt ein Muster; eine Zeile lässt sich über die Tabelle nicht von der Sperre befreien. Für die Behauptung, bei der ein reines Textverbot die richtigen Verneinungen im Skill mit treffen würde, kommt eine zweite Prüfung dazu: Ein Absatz, der „Collaborative Articles“ und ein Badge in einem Zug nennt, muss Q3 zitieren. Das hält einen neu formulierten Satz auf, der die Badge-Behauptung ohne Quelle wieder aufstellt. Wer die falsche Aussage mit der richtigen Quellenangabe hinschreibt, kommt weiterhin durch.

## Scoring

Die zehn Kategorien, ihre Gewichte und die Begründung je Gewicht stehen in [references/SCORING.md](references/SCORING.md#gewichtung). Dort liegt auch das [Engagement-Rate-Bewertungsraster](references/SCORING.md#engagement-rate-bewertungsraster) samt Berechnungsformel und die [Score-Interpretation](references/SCORING.md#score-interpretation), die einen Gesamtscore in einen Zeithorizont bis Top Voice übersetzt.

## Tests

```bash
python tests/run_eval.py
```

Der Runner liest das Gewichtsmodell aus `references/SCORING.md` und prüft damit drei erfundene
Profil-Fixtures gegen erwartete Score-Bänder. Er stellt außerdem sicher, dass die zehn Kategorien
in SCORING.md, SKILL.md, auf der Landingpage und in `scripts/generate_report.js` wortgleich
heißen, dass die 18 Profil-Elemente aus der Checkliste in SCORING.md in derselben Reihenfolge in
SKILL.md Phase 4.3 und in der Audit-Tabelle des Report-Generators stehen, dass die Zahlen der
Scoring-Engine auf der Landingpage aus `tests/fixtures/profile_mid.json` stammen und dass die
Landingpage den Dialog als Beispiel ausweist und die Fixture dazu nennt.

Seit v2.5.0 kommen drei Bindungen dazu: die vier gesperrten CTA-Formulierungen aus
`references/ETHICS.md` stehen vollständig an allen vier Stellen, die dieselbe Liste führen; die
zehn Achsen der Wettbewerbsmatrix stehen in `references/COMPETITIVE.md` und in SKILL.md Phase 3.1
in derselben Reihenfolge, und die Mindestzahl der Wettbewerber lautet überall gleich; der
Maßnahmenplan läuft an allen vier Stellen über Tag 1–30, 31–60 und 61–90, und die abgelösten
Horizonte dürfen nicht danebenstehen. Alle drei prüfen Schreibweisen und Listen. Was sie nicht
sehen, steht in den beiden Referenzdateien jeweils im letzten Abschnitt.

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

Aktuelle Version: v2.5.0. Was sich je Version geändert hat, steht im Changelog in [SKILL.md](SKILL.md#changelog).
