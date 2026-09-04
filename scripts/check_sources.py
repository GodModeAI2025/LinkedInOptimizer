# -*- coding: utf-8 -*-
"""Prueft die Beleglage in references/SOURCES.md.

Der Skill nennt Zahlen ueber den LinkedIn-Algorithmus, ueber Badge-Kriterien und
ueber Kennzahlen. SOURCES.md ist die Quelle der Wahrheit dafuer, welche dieser
Zahlen belegt sind, welche zurueckgezogen wurden und welche ausdruecklich
Erfahrungswerte sind. Dieses Skript haelt die Datei und den Rest des Repos
zusammen.

Geprueft wird:

1. SOURCES.md hat ein Stand-Datum und ein Datum fuer die naechste Pruefung,
   beide im Format JJJJ-MM-TT, und die naechste Pruefung liegt nach dem Stand.
2. Jede Zeile der Quellen-Tabelle hat eine ID der Form Qn, eine http(s)-URL und
   ein Abrufdatum im Format JJJJ-MM-TT.
3. Jede Quellen-ID, die anderswo im Repo zitiert wird, existiert in der Tabelle.
4. Die Tabelle der zurueckgezogenen Aussagen ist nicht leer.
5. Keine der zurueckgezogenen Zahlen steht noch irgendwo im Skill. Das ist der
   eigentliche Zweck des Skripts: eine Zahl, die einmal als unbelegt entfernt
   wurde, darf nicht ueber eine spaetere Aenderung zurueckkommen.

Exitcode 0, wenn alles zutrifft, sonst 1. Ist das Pruefdatum ueberschritten,
gibt es eine Warnung, aber keinen Fehler: eine abgelaufene Pruefung soll
sichtbar sein, aber nicht den Build eines unbeteiligten Beitrags blockieren.
"""

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "references" / "SOURCES.md"

# Dateien, in denen Quellen-IDs zitiert werden duerfen und in denen die
# zurueckgezogenen Zahlen nicht mehr vorkommen duerfen. SOURCES.md selbst ist
# nicht dabei, dort stehen die Zahlen absichtlich noch, naemlich in der Liste
# dessen, was entfernt wurde.
GEPRUEFTE_DATEIEN = [
    "SKILL.md",
    "README.md",
    "index.html",
    "references/SCORING.md",
    "references/TEMPLATES.md",
    "references/BANNER.md",
    "scripts/generate_report.js",
    "scripts/create_banner.py",
]

# Zurueckgezogene Zahlen. Links das Suchmuster, rechts die Begruendung, die im
# Fehlerfall ausgegeben wird. Die Muster sind bewusst eng gefasst, damit sie
# keine unbeteiligte Prozentangabe treffen.
VERBOTEN = [
    (r"3,4\s?%", "Plattformdurchschnitt 3,4 % Engagement-Rate, Quelle fuehrt den Wert nicht"),
    (r"6,6\s?%", "Formatwert Multi-Image 6,6 %, keine pruefbare Quelle"),
    (r"6,1\s?%", "Formatwert PDF-Karussell 6,1 %, keine pruefbare Quelle"),
    (r"5,6\s?%", "Formatwert Video 5,6 %, keine pruefbare Quelle"),
    (r"3,6\s?%", "branchenspezifischer Engagement-Benchmark 3,6 %, keine Quelle"),
    (r"um 55\s?%", "Profilaufrufe plus 55 %, keine Quelle"),
    (r"\+\s?55\s?%", "Profilaufrufe plus 55 %, keine Quelle"),
    (r"\+\s?40\s?%\s?Akzeptanz", "Annahmequote plus 40 %, keine Quelle"),
    (r"2,5×\s?mehr", "Kommentargewicht Faktor 2,5, keine Quelle"),
    (r"[Hh]albjährliche (Review|Überprüfung)",
     "halbjaehrliche Top-Voice-Review, LinkedIn prueft Nominierungen quartalsweise"),
    (r"bis zu 5 Tage Sichtbarkeit", "5 Tage Sichtbarkeit seit 2025, keine Quelle"),
    (r"um 20\s?% reduzieren", "Back-to-Back minus 20 %, keine Quelle"),
]

DATUM = re.compile(r"\d{4}-\d{2}-\d{2}")


def lies(pfad: Path) -> str:
    return pfad.read_text(encoding="utf-8")


def datum(text: str):
    treffer = DATUM.search(text)
    if not treffer:
        return None
    try:
        return dt.date.fromisoformat(treffer.group(0))
    except ValueError:
        return None


def tabellenzeilen(text: str, ueberschrift: str):
    """Gibt die Datenzeilen der ersten Markdown-Tabelle unter einer Ueberschrift."""
    start = text.find(ueberschrift)
    if start == -1:
        return None
    rest = text[start + len(ueberschrift):]
    naechste = rest.find("\n## ")
    if naechste != -1:
        rest = rest[:naechste]
    zeilen = []
    for zeile in rest.splitlines():
        zeile = zeile.strip()
        if not zeile.startswith("|"):
            continue
        if set(zeile) <= set("|-: "):
            continue
        spalten = [s.strip() for s in zeile.strip("|").split("|")]
        if spalten and spalten[0] in ("ID", "Frühere Aussage"):
            continue
        zeilen.append(spalten)
    return zeilen


def main() -> int:
    fehler = []

    if not SOURCES.is_file():
        print("FEHLER: references/SOURCES.md fehlt.", file=sys.stderr)
        return 1

    text = lies(SOURCES)

    stand = None
    naechste = None
    for zeile in text.splitlines():
        if zeile.startswith("**Stand:**"):
            stand = datum(zeile)
        elif zeile.startswith("**Nächste Prüfung:**"):
            naechste = datum(zeile)

    if stand is None:
        fehler.append("Zeile '**Stand:**' mit Datum JJJJ-MM-TT fehlt.")
    if naechste is None:
        fehler.append("Zeile '**Nächste Prüfung:**' mit Datum JJJJ-MM-TT fehlt.")
    if stand and naechste and naechste <= stand:
        fehler.append(
            f"Naechste Pruefung ({naechste}) liegt nicht nach dem Stand ({stand})."
        )

    quellen = tabellenzeilen(text, "## Belegte Quellen")
    if not quellen:
        fehler.append("Tabelle unter '## Belegte Quellen' fehlt oder ist leer.")
        quellen = []

    ids = set()
    for spalten in quellen:
        kennung = spalten[0]
        if not re.fullmatch(r"Q\d+", kennung):
            fehler.append(f"Quellen-ID nicht in der Form Qn: {kennung!r}")
            continue
        ids.add(kennung)
        zeile = " | ".join(spalten)
        if "http://" not in zeile and "https://" not in zeile:
            fehler.append(f"{kennung}: keine URL in der Zeile.")
        if not DATUM.search(zeile):
            fehler.append(f"{kennung}: kein Datum im Format JJJJ-MM-TT in der Zeile.")

    zurueck = tabellenzeilen(text, "## Zurückgezogen")
    if not zurueck:
        fehler.append("Tabelle unter '## Zurückgezogen' fehlt oder ist leer.")

    zitiert = {}
    for name in GEPRUEFTE_DATEIEN:
        pfad = ROOT / name
        if not pfad.is_file():
            fehler.append(f"{name}: Datei fehlt, die Pruefung kann sie nicht lesen.")
            continue
        inhalt = lies(pfad)

        for treffer in re.finditer(r"\((Q\d+)(?: in [^)]*)?\)", inhalt):
            zitiert.setdefault(treffer.group(1), set()).add(name)

        for muster, grund in VERBOTEN:
            for treffer in re.finditer(muster, inhalt):
                nummer = inhalt.count("\n", 0, treffer.start()) + 1
                fehler.append(
                    f"{name}:{nummer}: zurueckgezogene Angabe {treffer.group(0)!r} "
                    f"steht wieder im Skill ({grund})."
                )

    for kennung, dateien in sorted(zitiert.items()):
        if kennung not in ids:
            fehler.append(
                f"{kennung} wird zitiert in {', '.join(sorted(dateien))}, "
                "steht aber nicht in der Quellen-Tabelle."
            )

    print(f"  {len(ids)} Quellen mit URL und Datum: {', '.join(sorted(ids))}")
    print(f"  {len(zurueck or [])} zurueckgezogene Aussagen dokumentiert")
    print(f"  {len(zitiert)} Quellen-IDs im Skill zitiert")
    print(f"  {len(VERBOTEN)} Muster gegen die Rueckkehr entfernter Zahlen geprueft")

    if fehler:
        print("\nFEHLER:", file=sys.stderr)
        for eintrag in fehler:
            print(f"  - {eintrag}", file=sys.stderr)
        return 1

    if naechste and dt.date.today() > naechste:
        print(
            f"\nWARNUNG: Die Datenbasis war zum {naechste} zur Pruefung faellig. "
            "Quellen nachschlagen und Stand hochsetzen."
        )

    print(f"\nOK: Beleglage vollstaendig, Stand {stand}, naechste Pruefung {naechste}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
