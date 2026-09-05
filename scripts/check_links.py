# -*- coding: utf-8 -*-
"""Prueft, dass jeder Verweis im Repo auf eine Datei zeigt, die es gibt.

Drei Gruppen mit drei verschiedenen Bezugspunkten:

1. **Backtick-Pfade im Skill-Text.** Der Skill nennt Dateien in Backticks, etwa
   `references/SOURCES.md`. Geprueft werden nur Pfade mit Verzeichnisanteil;
   ein blosser Dateiname wie `SOURCES.md` ist die uebliche Kurzform fuer eine
   Nachbardatei und wird nicht geprueft. Aufgeloest wird erst relativ zur
   Datei, die den Verweis traegt, dann relativ zum Skill-Verzeichnis. Ein Pfad
   mit .. faellt immer auf: Claude laedt den Skill aus seinem eigenen Ordner,
   und was darueber liegt, gibt es im installierten Plugin nicht.

2. **Markdown-Links in der Doku.** README, CLAUDE.md und die uebrigen Dateien
   im Wurzelverzeichnis verlinken mit [Text](pfad). Diese Pfade sind relativ
   zum Repo-Wurzelverzeichnis, denn dort liest sie GitHub.

3. **Verweise im ausgelieferten Archiv**, wo es eines gibt. Wer nur das
   .skill-Archiv hat, hat keine Repo-Werkzeuge; ein Verweis dorthin ist fuer
   ihn tot. Repo-Werkzeuge werden deshalb mit dem Repo-Namen davor genannt.

Geprueft wird die Existenz der Datei. Nicht geprueft wird, ob der Verweis
inhaltlich passt, ob ein Anker existiert und ob eine externe URL erreichbar ist.

Exitcode 0, wenn alle Verweise aufloesen. Exitcode 1 sonst, mit Datei und Zeile
je Verstoss.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "."
SKILL_DATEIEN = sorted(SKILL_ROOT.rglob("*.md"))
DOKU_DATEIEN = [ROOT / name for name in ["README.md", "CLAUDE.md", "CHANGELOG.md", "SECURITY.md"]]
PAKET_SKRIPT = ROOT / "scripts" / "build_skill_package.py"

# Ein Pfad in Backticks mit mindestens einem Verzeichnisanteil.
BACKTICK = re.compile(r"`([A-Za-z0-9._][A-Za-z0-9._-]*(?:/[A-Za-z0-9._-]+)+\.(?:md|py|js|json|yml|html))`")

# Pfade, die absichtlich aus dem Repo herausfuehren: das Schwester-Repo.
FREMDE_REPOS = ("LinkedInOptimizer/", "LinkedIn-Orchestrator/")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#][^)]*?)\)")


def verweise(pfad):
    """(Zeilennummer, Pfad) je Backtick-Verweis mit Verzeichnisanteil."""
    for nummer, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        for ziel in BACKTICK.findall(zeile):
            if not ziel.startswith(FREMDE_REPOS):
                yield nummer, ziel


def pruefe_skill(fehler):
    for pfad in SKILL_DATEIEN:
        for nummer, ziel in verweise(pfad):
            if ".." in Path(ziel).parts:
                fehler.append(
                    "%s:%d: `%s` fuehrt mit .. aus dem Skill-Verzeichnis heraus. "
                    "Im installierten Plugin gibt es dort nichts."
                    % (pfad.relative_to(ROOT), nummer, ziel)
                )
                continue
            if (pfad.parent / ziel).exists() or (SKILL_ROOT / ziel).exists():
                continue
            fehler.append(
                "%s:%d: `%s` loest weder neben der Datei noch im Skill-Verzeichnis auf. "
                "Im installierten Plugin ist das ein toter Verweis."
                % (pfad.relative_to(ROOT), nummer, ziel)
            )


def pruefe_doku(fehler):
    for pfad in DOKU_DATEIEN:
        if not pfad.exists():
            fehler.append("%s fehlt" % pfad.name)
            continue
        for nummer, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
            for ziel in MD_LINK.findall(zeile):
                ziel = ziel.split("#", 1)[0].strip()
                if not ziel or "://" in ziel or ziel.startswith("mailto:"):
                    continue
                if not (ROOT / ziel).exists():
                    fehler.append(
                        "%s:%d: der Link auf %s zeigt ins Leere."
                        % (pfad.relative_to(ROOT), nummer, ziel)
                    )


def pruefe_paket(fehler):
    """Verweise innerhalb des .skill-Archivs, gegen dessen Dateiliste."""
    if not PAKET_SKRIPT.exists():
        return
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_skill_package", PAKET_SKRIPT)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    im_paket = set(modul.CONTENTS)

    for rel in sorted(im_paket):
        if not rel.endswith(".md"):
            continue
        pfad = ROOT / rel
        eigener_ordner = str(Path(rel).parent)
        for nummer, ziel in verweise(pfad):
            kandidaten = {ziel}
            if eigener_ordner not in (".", ""):
                kandidaten.add("%s/%s" % (eigener_ordner, ziel))
            if kandidaten & im_paket:
                continue
            fehler.append(
                "%s:%d: `%s` liegt nicht im .skill-Archiv. Wer nur das Archiv hat, "
                "findet die Datei nicht. Repo-Werkzeuge mit dem Repo-Namen davor nennen."
                % (rel, nummer, ziel)
            )


def main() -> int:
    fehler = []
    pruefe_skill(fehler)
    pruefe_doku(fehler)
    pruefe_paket(fehler)

    if fehler:
        print("FEHLER:", file=sys.stderr)
        for eintrag in fehler:
            print("  - %s" % eintrag, file=sys.stderr)
        return 1

    print("OK: %d Skill-Dateien, %d Doku-Dateien%s, alle Verweise loesen auf"
          % (len(SKILL_DATEIEN), len(DOKU_DATEIEN),
             " und das .skill-Archiv" if PAKET_SKRIPT.exists() else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
