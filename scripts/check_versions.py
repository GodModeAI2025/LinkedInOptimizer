# -*- coding: utf-8 -*-
"""Prueft, ob die Skill-Version an allen dokumentierten Stellen uebereinstimmt.

Die Quelle ist die Datei VERSION im Repo-Wurzelverzeichnis. Sie enthaelt eine
Zeile mit der Versionsnummer ohne fuehrendes v. Alles andere ist eine Kopie,
die hier gegen die Quelle geprueft wird.

Geprueft werden sechs Fundstellen: die Ueberschrift und der Versions-Abschnitt
der README, die Ueberschrift und der oberste Changelog-Eintrag in SKILL.md, das
Hero-Badge der Landingpage und der DOCX-Kopfzeilen-String im Report-Template.

Exitcode 0, wenn alle sechs die Version aus VERSION nennen. Exitcode 1, wenn
eine davon abweicht oder wenn eine Fundstelle gar nicht mehr gefunden wird. Der
zweite Fall ist Absicht: eine geloeschte oder umformulierte Versionszeile darf
nicht stillschweigend durchgehen.

Mit --expect X muss zusaetzlich VERSION selbst X sein. Der Release-Workflow
uebergibt dort den Tagnamen ohne v, damit ein Tag, der nicht zum Repo passt,
kein Release erzeugt.

Die Dokument-Versionen von references/SCORING.md (v2.0) sind bewusst nicht Teil
der Pruefung, sie zaehlen eigenstaendig.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION_FILE = ROOT / "VERSION"

VERSION = r"(\d+\.\d+\.\d+)"

CHECKS = [
    (
        "README.md",
        "Ueberschrift",
        re.compile(r"^# linkedin-profil-optimierung v" + VERSION + r"\s*$", re.M),
    ),
    (
        "README.md",
        "Abschnitt Version",
        re.compile(r"^Aktuelle Version: v" + VERSION + r"\b", re.M),
    ),
    (
        "SKILL.md",
        "Ueberschrift",
        re.compile(r"^# LinkedIn Profil-Optimierung .* Skill v" + VERSION + r"\s*$", re.M),
    ),
    (
        "SKILL.md",
        "oberster Changelog-Eintrag",
        re.compile(r"## Changelog\s*\n+```\s*\nv" + VERSION + r" \("),
    ),
    (
        "index.html",
        "Hero-Badge",
        re.compile(r"v" + VERSION + r" &middot; Claude Cowork Skill|v" + VERSION + r" · Claude Cowork Skill"),
    ),
    (
        "scripts/generate_report.js",
        "DOCX-Kopfzeile",
        re.compile(r'"linkedin-profil-optimierung v' + VERSION + r'"'),
    ),
]


def read_source_version():
    """Liest die Versionsnummer aus VERSION. None, wenn das nicht geht."""
    if not VERSION_FILE.exists():
        print("FEHLER: VERSION fehlt im Repo-Wurzelverzeichnis.", file=sys.stderr)
        return None
    raw = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", raw):
        print(
            f"FEHLER: VERSION enthaelt keine Versionsnummer der Form 1.2.3: {raw!r}",
            file=sys.stderr,
        )
        return None
    return raw


def main():
    parser = argparse.ArgumentParser(
        description="Prueft die Versionsangaben gegen die Datei VERSION."
    )
    parser.add_argument(
        "--expect",
        metavar="X",
        help="Verlangt zusaetzlich, dass VERSION genau X ist (ohne fuehrendes v).",
    )
    args = parser.parse_args()

    source = read_source_version()
    if source is None:
        return 1

    print(f"  v{source:<8} VERSION (Quelle)")

    if args.expect is not None:
        expected = args.expect.lstrip("v")
        if expected != source:
            print(
                f"\nFEHLER: erwartet wurde v{expected}, VERSION nennt v{source}.",
                file=sys.stderr,
            )
            return 1

    found = []
    missing = []

    for rel_path, label, pattern in CHECKS:
        path = ROOT / rel_path
        if not path.exists():
            missing.append(f"{rel_path} ({label}): Datei fehlt")
            continue
        match = pattern.search(path.read_text(encoding="utf-8"))
        if match is None:
            missing.append(f"{rel_path} ({label}): Versionsangabe nicht gefunden")
            continue
        version = next(g for g in match.groups() if g)
        found.append((rel_path, label, version))

    for rel_path, label, version in found:
        print(f"  v{version:<8} {rel_path} ({label})")

    if missing:
        print("\nFEHLER: Versionsangaben nicht auffindbar:", file=sys.stderr)
        for entry in missing:
            print(f"  - {entry}", file=sys.stderr)
        return 1

    abweichend = [
        f"{rel_path} ({label}): v{version}"
        for rel_path, label, version in found
        if version != source
    ]
    if abweichend:
        print(
            f"\nFEHLER: Fundstellen weichen von VERSION (v{source}) ab:",
            file=sys.stderr,
        )
        for entry in abweichend:
            print(f"  - {entry}", file=sys.stderr)
        return 1

    print(f"\nOK: VERSION und alle {len(found)} Fundstellen nennen v{source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
