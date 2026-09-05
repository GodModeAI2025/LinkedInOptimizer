# -*- coding: utf-8 -*-
"""Baut das Release-Artefakt linkedin-optimizer.skill.

Verwendung:
    python scripts/build_skill_package.py dist/linkedin-optimizer.skill
    python scripts/build_skill_package.py --print-name

Das Skript laeuft ohne Netz und ohne GitHub. Es packt genau die Dateien, die
der Skill zur Laufzeit braucht, dazu LICENSE und requirements.txt. Alles
andere im Repo bleibt draussen: .git, .github, index.html, die Caches und die
Werkzeug-Skripte check_versions.py, check_sources.py und build_skill_package.py,
die nur im Repo-Kontext einen Sinn haben.

Das Archiv ist ein ZIP mit den Dateien auf oberster Ebene, also SKILL.md,
references/ und scripts/ direkt an der Wurzel. Genau diese Form erwartet
Claude beim Hochladen einer .skill-Datei.

Reproduzierbarkeit: alle Eintraege bekommen denselben festen Zeitstempel
(1980-01-01, die frueheste Zeit, die das ZIP-Format kennt), dieselben
Dateirechte und dieselbe Reihenfolge. Gespeichert wird unkomprimiert
(ZIP_STORED), damit das Ergebnis nicht von der zlib-Version der jeweiligen
Maschine abhaengt. Zwei Laeufe liefern dieselben Bytes, auch auf
unterschiedlichen Rechnern.
"""

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Der Dateiname ist Teil des dokumentierten Installationswegs:
# https://github.com/GodModeAI2025/LinkedInOptimizer/releases/latest/download/linkedin-optimizer.skill
# README, index.html und die Workflows lesen ihn ueber --print-name, damit er
# nicht an mehreren Stellen abweichen kann.
ARTIFACT_NAME = "linkedin-optimizer.skill"

# Inhalt des Artefakts, bewusst als Positivliste. Was hier nicht steht, ist
# nicht im Paket.
CONTENTS = [
    "SKILL.md",
    "LICENSE",
    "requirements.txt",
    "references/BANNER.md",
    "references/COMPETITIVE.md",
    "references/ETHICS.md",
    "references/SCORING.md",
    "references/SOURCES.md",
    "references/TEMPLATES.md",
    "references/UNTRUSTED.md",
    "scripts/create_banner.py",
    "scripts/generate_report.js",
]

# 1980-01-01 00:00:00, der Nullpunkt des ZIP-Zeitformats.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def build(output: Path) -> int:
    missing = [name for name in CONTENTS if not (ROOT / name).is_file()]
    if missing:
        print("FEHLER: Dateien fehlen im Repo:", file=sys.stderr)
        for name in missing:
            print(f"  - {name}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(CONTENTS):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3  # Unix, unabhaengig vom Betriebssystem
            info.external_attr = 0o644 << 16
            archive.writestr(info, (ROOT / name).read_bytes())

    data = output.read_bytes()
    print(f"Artefakt: {output}")
    print(f"Groesse:  {len(data)} Bytes")
    print(f"SHA256:   {hashlib.sha256(data).hexdigest()}")
    print("Inhalt:")
    for name in sorted(CONTENTS):
        print(f"  {name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Baut das Skill-Paket als reproduzierbares ZIP."
    )
    parser.add_argument(
        "output",
        nargs="?",
        help=f"Ausgabepfad, ueblicherweise .../{ARTIFACT_NAME}",
    )
    parser.add_argument(
        "--print-name",
        action="store_true",
        help="Gibt nur den dokumentierten Dateinamen aus und beendet sich.",
    )
    args = parser.parse_args()

    if args.print_name:
        print(ARTIFACT_NAME)
        return 0

    if not args.output:
        parser.error("Ausgabepfad fehlt (oder --print-name verwenden)")

    return build(Path(args.output))


if __name__ == "__main__":
    sys.exit(main())
