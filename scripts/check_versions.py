# -*- coding: utf-8 -*-
"""Prueft, ob die Skill-Version an allen dokumentierten Stellen uebereinstimmt.

Geprueft werden fuenf Fundstellen: die Ueberschrift und der Versions-Abschnitt
der README, die Ueberschrift und der oberste Changelog-Eintrag in SKILL.md, das
Hero-Badge der Landingpage und der DOCX-Kopfzeilen-String im Report-Template.

Exitcode 0, wenn alle fuenf dieselbe Version nennen. Exitcode 1, wenn sie
auseinanderlaufen oder wenn eine Fundstelle gar nicht mehr gefunden wird. Der
zweite Fall ist Absicht: eine geloeschte oder umformulierte Versionszeile darf
nicht stillschweigend durchgehen.

Die Dokument-Versionen von references/SCORING.md (v2.0) sind bewusst nicht Teil
der Pruefung, sie zaehlen eigenstaendig.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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


def main():
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

    versions = {version for _, _, version in found}
    if len(versions) > 1:
        print(
            "\nFEHLER: Versionsangaben laufen auseinander: "
            + ", ".join(sorted("v" + v for v in versions)),
            file=sys.stderr,
        )
        return 1

    print(f"\nOK: alle {len(found)} Fundstellen nennen v{versions.pop()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
