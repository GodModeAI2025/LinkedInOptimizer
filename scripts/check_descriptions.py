# -*- coding: utf-8 -*-
"""Prueft das Frontmatter des Skills gegen die Regeln fuer Trigger-Beschreibungen.

Die description im Frontmatter ist der Text, an dem das Modell entscheidet, ob
es diesen Skill laedt. Zwei Skills derselben Herkunft reagieren auf dieselben
Formulierungen (Profil optimieren, Personal Branding, Content-Strategie, Top
Voice). Ohne eine Abgrenzung in der description muss das Modell raten.

Geprueft werden vier Dinge:

1. name stimmt mit dem erwarteten Skill-Namen ueberein.
2. Die description ist hoechstens MAX_CHARS Zeichen lang, zusammengefaltet auf
   eine Zeile gemessen. Laengere Beschreibungen verwaessern den Treffer.
3. Die description enthaelt keinen Geviert- oder Halbgeviertstrich. Beide
   ueberleben die Weitergabe an manche Runtimes nicht unveraendert.
4. Die description nennt den Schwester-Skill in einem Abgrenzungssatz, also
   sowohl "Nicht fuer" als auch den Namen des anderen Skills. Fehlt der Satz,
   kollidieren die Trigger wieder.

Exitcode 0, wenn alle vier zutreffen. Exitcode 1 sonst, mit einer Zeile je
Verstoss. Was hier nicht geprueft wird: ob die genannten Trigger die richtigen
sind und ob die Abgrenzung inhaltlich stimmt. Das Skript liest Schreibweisen,
keine Bedeutung.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_FILE = ROOT / "SKILL.md"
EXPECTED_NAME = "linkedin-profil-optimierung"
SIBLING = "linkedin-community-builder"
MAX_CHARS = 400

DASHES = {"—": "Geviertstrich", "–": "Halbgeviertstrich"}


def frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---", text, re.S)
    if not match:
        return None
    return match.group(1)


def field(block, key):
    """Liest ein Feld, auch in der gefalteten Schreibweise mit >."""
    match = re.search(
        r"^" + key + r":\s*(?:>[-+]?|\|[-+]?)?[ \t]*\n?((?:.|\n)*?)(?=^\w[\w-]*:|\Z)",
        block,
        re.M,
    )
    if not match:
        return None
    raw = match.group(1)
    return " ".join(line.strip() for line in raw.strip().splitlines() if line.strip())


def main():
    problems = []

    if not SKILL_FILE.exists():
        print("FEHLER: %s fehlt" % SKILL_FILE.relative_to(ROOT))
        return 1

    text = SKILL_FILE.read_text(encoding="utf-8")
    block = frontmatter(text)
    if block is None:
        print("FEHLER: %s hat kein Frontmatter" % SKILL_FILE.relative_to(ROOT))
        return 1

    name = field(block, "name")
    if name != EXPECTED_NAME:
        problems.append("name ist %r, erwartet %r" % (name, EXPECTED_NAME))

    description = field(block, "description")
    if not description:
        problems.append("description fehlt")
        description = ""

    if len(description) > MAX_CHARS:
        problems.append(
            "description ist %d Zeichen lang, erlaubt sind %d"
            % (len(description), MAX_CHARS)
        )

    for char, label in DASHES.items():
        if char in description:
            problems.append("description enthaelt einen %s" % label)

    if SIBLING not in description:
        problems.append(
            "description nennt den Schwester-Skill %r nicht" % SIBLING
        )
    if "Nicht f" not in description:
        problems.append(
            "description hat keinen Abgrenzungssatz, erwartet wird \"Nicht fuer ..., dafuer %s\""
            % SIBLING
        )

    if problems:
        for problem in problems:
            print("FEHLER: %s" % problem)
        return 1

    print(
        "OK: %s, description %d von %d Zeichen, Abgrenzung zu %s vorhanden"
        % (EXPECTED_NAME, len(description), MAX_CHARS, SIBLING)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
