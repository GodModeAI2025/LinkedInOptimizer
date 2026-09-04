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
   Gesucht wird nach jedem Vorkommen von Qn, gleich in welcher Klammer, welcher
   Schreibweise und welchem Satzbau. Ein Fehlalarm in Fliesstext ist billiger als
   eine ausgedachte Belegangabe im ausgelieferten Paket.
4. Die Tabelle der zurueckgezogenen Aussagen ist nicht leer.
5. Keine der zurueckgezogenen Aussagen steht noch irgendwo im Skill. Das ist der
   eigentliche Zweck des Skripts: eine Aussage, die einmal als unbelegt entfernt
   wurde, darf nicht ueber eine spaetere Aenderung zurueckkommen.

Zu 5 gehoert die Bauart der Sperren, denn daran ist eine frueheres Fassung
gescheitert: Sie fuehrte eine handgepflegte Liste woertlicher Schreibweisen neben
der Tabelle. Wer '3.4 %' mit Punkt schrieb, '3,4 Prozent' ausschrieb oder
'3,4&nbsp;%' als HTML-Entity setzte, kam durch, und eine neu zurueckgezogene Zahl
bekam ueberhaupt keine Sperre, solange niemand daran dachte, das Skript
nachzuziehen.

Jetzt steht die Sperre in der Tabelle selbst, in der Spalte 'Sperrmuster', und
das Skript erzeugt daraus die Regex:

* Ziffernfolgen trennen mit [.,], damit 3,4 und 3.4 dasselbe sind.
* Das Prozentzeichen faengt auch das ausgeschriebene Wort.
* Das Multiplikationszeichen faengt auch das ASCII-x.
* Leerraum faengt auch das geschuetzte Leerzeichen und &nbsp;.
* Bindestriche fangen auch die typografischen Varianten.
* Ein fuehrendes + oder ~ ist optional, gross und klein ist egal.
* Vor und hinter Zahlen steht eine Grenze, damit '20 %' nicht in '220 Zeichen'
  anschlaegt.

Und die Tabelle wird gegen sich selbst geprueft: Jede relative Groesse in der
Spalte 'Frühere Aussage', also jede Angabe mit Prozent oder Faktor, muss von
einem Sperrmuster derselben Zeile getroffen werden. Wer eine Zahl zurueckzieht
und keine Sperre dazuschreibt, faellt hier auf und nicht erst dem Kunden.

Was das Skript nicht kann: Es prueft Schreibweisen, keine Aussagen. Fuer die
Zeile zu den Collaborative Articles gibt es deshalb bewusst keine Sperre. Ein
Textverbot auf den Begriff wuerde die richtigen Verneinungen in SKILL.md
mitreissen, die sagen, dass Collaborative Articles auf kein Badge mehr
einzahlen. Gesperrt ist dort stattdessen die Elementliste, und zwar in
tests/run_eval.py. Ein frei formulierter Satz, der die Badge-Behauptung neu
aufstellt, faellt keinem der beiden Schritte auf.

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
# zurueckgezogenen Aussagen nicht mehr vorkommen duerfen. SOURCES.md selbst ist
# nicht dabei, dort stehen die Aussagen absichtlich noch, naemlich in der Liste
# dessen, was entfernt wurde, und in der Spalte mit den Sperrmustern.
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

DATUM = re.compile(r"\d{4}-\d{2}-\d{2}")
QUELLEN_ID = re.compile(r"\bQ\d+\b")

# Relative Groessen: Prozentangaben und Faktoren. Genau diese Klasse von Zahl
# ist im Skill zurueckgezogen worden, und genau fuer sie verlangt das Skript ein
# Sperrmuster. Absolute Angaben wie '15 Wörter' bleiben aussen vor, sie stehen
# in denselben Saetzen, sind aber nicht der zurueckgezogene Teil davon.
QUANTITAET = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|Prozent|×|x\b)")

# Leerraum in einem Sperrmuster faengt auch das geschuetzte Leerzeichen und die
# HTML-Entities dafuer.
LEER = r"(?:\s|&nbsp;|&#160;| )*"
BINDESTRICH = r"[-‐‑‒–]"

# Spalte, in der die Sperrmuster stehen, und das Praefix, mit dem eine Zeile
# ausdruecklich ohne Sperre gefuehrt wird.
SPALTEN_ZURUECK = 4
OHNE_SPERRE = "keine:"


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


def muster_aus_token(token: str) -> str:
    """Baut aus einem Sperrmuster der Tabelle die Regex, die es sperrt.

    Der Token wird so geschrieben, wie die Aussage frueher im Skill stand, also
    zum Beispiel '3,4 %' oder '2,5×' oder '+40 % Akzeptanz'. Die Normalisierung
    macht daraus eine Regex, die auch die naheliegenden Umschreibungen faengt.
    """
    teile = []
    i = 0
    laenge = len(token)
    while i < laenge:
        zeichen = token[i]

        if zeichen.isspace():
            teile.append(LEER)
            while i < laenge and token[i].isspace():
                i += 1
            continue

        if zeichen.isdigit():
            stellen = []
            while i < laenge:
                if token[i].isdigit():
                    stellen.append(re.escape(token[i]))
                    i += 1
                elif token[i] in ".," and i + 1 < laenge and token[i + 1].isdigit():
                    stellen.append("[.,]")
                    i += 1
                else:
                    break
            teile.append(r"(?<![\d.,])" + "".join(stellen) + r"(?!\d)")
            continue

        if zeichen == "%":
            if not teile or teile[-1] != LEER:
                teile.append(LEER)
            teile.append(r"(?:%|Prozent)")
        elif zeichen == "×":
            # Nur das typografische Zeichen gilt als Faktor. Ein ASCII-x im
            # Sperrmuster bleibt ein Buchstabe, sonst wuerde jedes x in einem
            # Wort zur Alternative aufgeblasen.
            if not teile or teile[-1] != LEER:
                teile.append(LEER)
            teile.append(r"[x×]")
        elif zeichen in "+~":
            teile.append(re.escape(zeichen) + "?")
        elif zeichen == "-":
            teile.append(BINDESTRICH)
        else:
            teile.append(re.escape(zeichen))
        i += 1

    return "".join(teile)


def sperren_aus_tabelle(zeilen, fehler):
    """Uebersetzt die Tabelle 'Zurückgezogen' in Sperrmuster.

    Rueckgabe: Liste (kompilierte Regex, Token, Aussage) und die Liste der
    Zeilen, die bewusst ohne Sperre gefuehrt werden.
    """
    sperren = []
    ohne_sperre = []

    for nummer, spalten in enumerate(zeilen, 1):
        if len(spalten) != SPALTEN_ZURUECK:
            fehler.append(
                f"Zurückgezogen, Zeile {nummer}: {len(spalten)} Spalten, erwartet werden "
                f"{SPALTEN_ZURUECK} (Frühere Aussage, Stand bis, Warum entfernt, Sperrmuster)."
            )
            continue

        aussage, _stand, _grund, sperrmuster = spalten
        kurz = aussage if len(aussage) <= 70 else aussage[:67] + "..."

        if not sperrmuster:
            fehler.append(
                f"Zurückgezogen, Zeile {nummer} ({kurz}): die Spalte 'Sperrmuster' ist leer. "
                f"Entweder ein Muster eintragen oder die Zeile mit '{OHNE_SPERRE} <Grund>' "
                "ausdruecklich ohne Sperre fuehren."
            )
            continue

        mengen = list(QUANTITAET.finditer(aussage))

        if sperrmuster.startswith(OHNE_SPERRE):
            grund = sperrmuster[len(OHNE_SPERRE):].strip()
            if not grund:
                fehler.append(
                    f"Zurückgezogen, Zeile {nummer} ({kurz}): '{OHNE_SPERRE}' ohne Begruendung."
                )
            if mengen:
                fehler.append(
                    f"Zurückgezogen, Zeile {nummer} ({kurz}): die Aussage nennt "
                    f"{', '.join(sorted({m.group(0) for m in mengen}))}, dafuer ist "
                    f"'{OHNE_SPERRE}' nicht zulaessig. Eine zurueckgezogene Zahl braucht ein "
                    "Sperrmuster."
                )
            ohne_sperre.append((kurz, grund))
            continue

        zeilen_sperren = []
        for token in [t.strip() for t in sperrmuster.split(";")]:
            if not token:
                continue
            try:
                regex = re.compile(muster_aus_token(token), re.IGNORECASE)
            except re.error as ausnahme:
                fehler.append(
                    f"Zurückgezogen, Zeile {nummer} ({kurz}): das Sperrmuster {token!r} "
                    f"ergibt keine gueltige Regex ({ausnahme})."
                )
                continue
            zeilen_sperren.append((regex, token, kurz))

        if not zeilen_sperren:
            fehler.append(
                f"Zurückgezogen, Zeile {nummer} ({kurz}): kein verwertbares Sperrmuster."
            )
            continue

        # Die Tabelle gegen sich selbst: jede relative Groesse in der Aussage
        # muss von einem Muster derselben Zeile getroffen werden.
        for menge in mengen:
            gedeckt = any(
                treffer.start() <= menge.start() and treffer.end() >= menge.end()
                for regex, _, _ in zeilen_sperren
                for treffer in regex.finditer(aussage)
            )
            if not gedeckt:
                fehler.append(
                    f"Zurückgezogen, Zeile {nummer} ({kurz}): die Angabe "
                    f"{menge.group(0)!r} in der Spalte 'Frühere Aussage' wird von keinem "
                    "Sperrmuster dieser Zeile getroffen. Ohne Muster kommt die Zahl ueber "
                    "die naechste Aenderung zurueck."
                )

        sperren.extend(zeilen_sperren)

    return sperren, ohne_sperre


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
        zurueck = []

    sperren, ohne_sperre = sperren_aus_tabelle(zurueck, fehler)

    zitiert = {}
    for name in GEPRUEFTE_DATEIEN:
        pfad = ROOT / name
        if not pfad.is_file():
            fehler.append(f"{name}: Datei fehlt, die Pruefung kann sie nicht lesen.")
            continue
        inhalt = lies(pfad)

        for treffer in QUELLEN_ID.finditer(inhalt):
            zitiert.setdefault(treffer.group(0), set()).add(name)

        for regex, token, aussage in sperren:
            for treffer in regex.finditer(inhalt):
                nummer = inhalt.count("\n", 0, treffer.start()) + 1
                fehler.append(
                    f"{name}:{nummer}: zurueckgezogene Angabe {treffer.group(0)!r} steht "
                    f"wieder im Skill. Sperrmuster {token!r} aus der Zeile: {aussage}"
                )

    for kennung, dateien in sorted(zitiert.items()):
        if kennung not in ids:
            fehler.append(
                f"{kennung} wird zitiert in {', '.join(sorted(dateien))}, "
                "steht aber nicht in der Quellen-Tabelle."
            )

    print(f"  {len(ids)} Quellen mit URL und Datum: {', '.join(sorted(ids))}")
    print(f"  {len(zurueck)} zurueckgezogene Aussagen dokumentiert")
    print(f"  {len(zitiert)} Quellen-IDs im Skill zitiert")
    print(f"  {len(sperren)} Sperrmuster aus der Tabelle erzeugt und geprueft")
    if ohne_sperre:
        print(f"  {len(ohne_sperre)} Zeilen ausdruecklich ohne Sperre:")
        for kurz, grund in ohne_sperre:
            print(f"    - {kurz}\n      Grund: {grund}")

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
