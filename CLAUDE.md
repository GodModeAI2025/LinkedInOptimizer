# Projektregeln — LinkedInOptimizer

Diese Datei richtet sich an jeden Agenten, der in diesem Repo arbeitet. Lies sie vor der ersten
Änderung. Was hier steht, gilt, solange der Nutzer nichts anderes sagt.

## Vor jedem Push

Aus dem Wurzelverzeichnis, alle fünf müssen durchlaufen:

```bash
python scripts/check_versions.py
python scripts/check_descriptions.py
python scripts/check_sources.py
python scripts/check_hooks.py
python tests/run_eval.py
python scripts/build_skill_package.py /tmp/probe.skill && unzip -Z1 /tmp/probe.skill
```

Schlägt eine davon fehl, wird nicht gepusht. Die CI fährt dieselben Prüfungen und zusätzlich den
Banner-Lauf und den Paketvergleich.

## Invarianten

**Versionen.** `VERSION` ist die Quelle. Acht Fundstellen sind Kopien: README-Überschrift,
README-Abschnitt „Version", SKILL.md-Überschrift, oberster Eintrag in CHANGELOG.md, beide
Manifeste unter `.claude-plugin/`, das Hero-Badge der Landingpage und die DOCX-Kopfzeile in
`scripts/generate_report.js`. Wer die Version hebt, hebt alle acht und schreibt einen
Changelog-Eintrag.

**Zahlen.** Keine Zahl in den Skill, die in `references/SOURCES.md` keine Zeile hat. Wer eine Zahl
nicht belegen kann, streicht die Aussage, statt eine Quelle zu suchen, die ungefähr passt. Eine
zurückgezogene Aussage kommt nur mit URL und Datum zurück. Die Sperrmuster in SOURCES.md sind
nicht dazu da, umgangen zu werden; sie prüfen Schreibweisen, das Verbot gilt der Aussage.

**Trigger-Beschreibung.** Die `description` im Frontmatter bleibt unter 400 Zeichen, enthält keinen
Geviert- oder Halbgeviertstrich und endet mit dem Abgrenzungssatz, der
`linkedin-community-builder` beim Namen nennt. Ohne ihn kollidieren die Trigger der beiden Skills.

**Struktur.** SKILL.md ist der Router und bleibt kurz: Abgrenzung, Ressourcen, Ablauf, Top Voice,
Branchen, Verifikation, Fehlerbehandlung, Quality Gates. Der Ablauf einer Phase steht in
`references/PHASE-*.md`, nicht hier. Wer eine Phase erweitert, erweitert die Phasendatei.

**Bindungen.** `tests/run_eval.py` hält Listen über mehrere Dateien zusammen: die zehn
Kategorienamen, die 18 Profil-Elemente, die vier gesperrten CTA-Formulierungen, die zehn Achsen der
Wettbewerbsmatrix, die drei Zeitfenster, die Untrusted-Verankerung. Wer eine dieser Listen ändert,
ändert sie überall, oder der Lauf fällt. Das ist der Zweck.

**Erhobener Text.** `references/UNTRUSTED.md` ist die kanonische Regel für alles, was aus einer
LinkedIn-Seite kommt. Neue Schritte, die fremden Text lesen, verweisen darauf, bevor sie ihn lesen.

**Paket.** `scripts/build_skill_package.py` führt eine ausdrückliche Liste. Eine neue Datei, die in
das `.skill`-Archiv gehört, wird dort und in der Paketliste der CI ergänzt. Repo-Werkzeuge,
`.github/`, `.claude-plugin/` und die Landingpage gehören nicht ins Archiv.

**Beispieldaten.** Erfunden, nicht anonymisiert. Ein reales Profil zu erheben und danach zu
verfremden wäre genau die Verarbeitung, die SECURITY.md einschränkt.

## Schwester-Repo

`linkedin-community-builder` liegt in
[LinkedIn-Orchestrator](https://github.com/GodModeAI2025/LinkedIn-Orchestrator). Zwei Dinge sind
über die Repo-Grenze gekoppelt und werden von keinem Skript zusammengehalten:

1. Die Abgrenzungstabelle und die vier Entscheidungsregeln stehen in beiden SKILL.md-Dateien,
   spiegelbildlich. Wer eine Regel ändert, ändert beide.
2. Der Hook-Katalog. Kanonisch dort in `references/HOOKS.md`, hier als Kopie in
   `references/TEMPLATES.md`, weil das Paket offline vollständig sein muss.
   `scripts/check_hooks.py` prüft je Repo die eigene Kopie, nicht den Abgleich.

## Was hier nicht steht

Ob eine Empfehlung im Gespräch befolgt wurde, ob eine Angabe im Kundenprofil stimmt und ob der
Ethik-Abgleich tatsächlich stattgefunden hat, sieht kein Skript in diesem Repo. Die Grenzen jeder
Prüfung stehen im Docstring des jeweiligen Skripts und im letzten Abschnitt der jeweiligen
Referenzdatei.
