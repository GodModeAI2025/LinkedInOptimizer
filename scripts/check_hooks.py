# -*- coding: utf-8 -*-
"""Prueft, dass der Hook-Katalog dieses Repos die zehn kanonischen Namen fuehrt.

Der Katalog steht in zwei Repos: kanonisch in LinkedIn-Orchestrator unter
references/HOOKS.md, als Kopie in LinkedInOptimizer unter
references/TEMPLATES.md. Die Kopie ist noetig, weil das Skill-Paket des
Optimizers offline vollstaendig sein muss und keine Datei aus dem anderen Repo
lesen kann.

Bindende Flaeche sind die zehn Namen und ihre Reihenfolge. Dieses Skript prueft
sie gegen die Liste unten. Es prueft, was in diesem Repo steht; ob das andere
Repo nachgezogen wurde, sieht es nicht. Die Kopplung ueber Repo-Grenzen bleibt
Handarbeit und steht als solche in beiden Dateien.

Exitcode 0, wenn die Namen in dieser Reihenfolge stehen. Exitcode 1 sonst.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KATALOG = ROOT / "references/TEMPLATES.md"
UEBERSCHRIFT = re.compile(r"^### \d+\. (.+)$", re.M)

NAMEN = [
    "PROVOKANTE THESE",
    "PERSÖNLICHE GESCHICHTE",
    "ZAHLEN-HOOK",
    "GEGEN-DEN-STROM",
    "KONTEXT-FRAGE",
    "BREAKING-NEWS-ANALYSE",
    "LEHRE AUS FEHLER",
    "FRAMEWORK / LISTE",
    "BEOBACHTUNG",
    "MICRO-CASE-STUDY",
]


def main() -> int:
    if not KATALOG.exists():
        print("FEHLER: %s fehlt" % KATALOG.name, file=sys.stderr)
        return 1

    gefunden = [t.strip() for t in UEBERSCHRIFT.findall(KATALOG.read_text(encoding="utf-8"))]

    if gefunden == NAMEN:
        print("OK: %s fuehrt die zehn Hook-Typen in der kanonischen Reihenfolge"
              % KATALOG.relative_to(ROOT))
        return 0

    print("FEHLER: der Hook-Katalog weicht ab.", file=sys.stderr)
    print("  erwartet: %s" % ", ".join(NAMEN), file=sys.stderr)
    print("  gefunden: %s" % (", ".join(gefunden) if gefunden else "nichts"), file=sys.stderr)
    print("  Der Katalog steht in beiden Repos. Wer einen Typ aendert, zieht ihn dort nach.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
