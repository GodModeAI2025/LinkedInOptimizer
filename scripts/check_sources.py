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
* Leerraum faengt auch das geschuetzte Leerzeichen, &nbsp; und den Bindestrich,
  damit 'Creator Mode' auch 'Creator-Mode' und 'CreatorMode' faengt.
* Umlaute fangen auch ihre ae-Umschrift. Die Skripte im Repo schreiben Umlaute
  aus, und generate_report.js wird mitgeprueft.
* Bindestriche fangen auch die typografischen Varianten.
* Ein fuehrendes + oder ~ ist optional, gross und klein ist egal.
* Drei Punkte im Muster stehen fuer eine Luecke von bis zu 40 Zeichen in
  derselben Zeile. Damit haengt ein Kontextwort nicht daran, dass es direkt vor
  der Zahl steht: 'Umfragen...~5 %' faengt auch 'Umfragen erreichen ~5 %'.
* Vor und hinter Zahlen steht eine Grenze, damit '20 %' nicht in '220 Zeichen'
  anschlaegt.

Und die Tabelle wird gegen sich selbst geprueft, zweifach:

* Jede relative Groesse in der Spalte 'Frühere Aussage', also jede Angabe mit
  Prozent oder Faktor, muss von einem Sperrmuster derselben Zeile getroffen
  werden. Wer eine Zahl zurueckzieht und keine Sperre dazuschreibt, faellt hier
  auf und nicht erst dem Kunden.
* Mindestens ein Muster jeder Zeile muss den eigenen Wortlaut in der Spalte
  'Frühere Aussage' treffen. Das erdet die Sperre am zurueckgezogenen Text.
  Ohne diese Pruefung genuegte irgendein Wort in der Zelle: die Zeile blieb
  stehen, der Zaehler stimmte, und die Sperre lief ins Leere.

Was bleibt: ein Muster laesst sich auf einen Teil des Wortlauts verengen, etwa
von 'Creator Mode' auf 'Creator Mode aktiv'. Das faellt hier nicht auf, steht
aber als Aenderung in der Tabelle und damit im Diff.

Eine Zeile ohne Sperrmuster gibt es nicht. Eine frueher hier eingebaute
Ausnahme, mit der sich eine Zeile ueber das Wort 'keine:' und eine beliebige
Begruendung von der Sperre befreien liess, ist wieder entfernt: sie haette
jede Sperre ohne Codeaenderung abschaltbar gemacht, und der Zaehler in der
Ausgabe waere der einzige Hinweis darauf gewesen. Wer eine Sperre fuer schaedlich
haelt, aendert das Muster, nicht den Schalter.

Was das Skript nicht kann: Es prueft Schreibweisen, keine Aussagen. Ein frei
formulierter Satz, der eine zurueckgezogene Behauptung in neuen Worten
aufstellt, faellt ihm nicht auf. Fuer die eine Behauptung, an der das teuer
waere, steht deshalb unten eine zweite, engere Pruefung: BEHAUPTUNGS_REGELN
verlangt, dass ein Absatz, der Collaborative Articles und ein Badge in einem Zug
nennt, Q3 zitiert. Das ist kein Beweis, sondern eine Schwelle. Wer die falsche
Aussage mit der richtigen Quellenangabe hinschreibt, kommt weiter durch.

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
    "references/ETHICS.md",
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

# Leerraum in einem Sperrmuster faengt auch das geschuetzte Leerzeichen, die
# HTML-Entities dafuer und den Bindestrich. Der Bindestrich gehoert dazu, weil
# 'Creator-Mode' sonst an der Sperre 'Creator Mode' vorbeigeht und der
# zurueckgezogene Schalter ueber die Schreibweise zurueckkommt.
BINDESTRICH = r"[-‐‑‒–]"
LEER = r"(?:\s|&nbsp;|&#160;| |" + BINDESTRICH + r")*"

# Umlaute in einem Sperrmuster fangen auch ihre ae-Umschrift. Die Skripte im
# Repo schreiben Umlaute aus, und scripts/generate_report.js steht mit auf der
# Liste der geprueften Dateien.
UMLAUTE = {
    "ä": r"(?:ä|ae)",
    "ö": r"(?:ö|oe)",
    "ü": r"(?:ü|ue)",
    "ß": r"(?:ß|ss)",
}

# Drei Punkte in einem Sperrmuster: eine Luecke von bis zu 40 Zeichen in
# derselben Zeile. Damit muss ein Kontextwort nicht unmittelbar vor der Zahl
# stehen.
LUECKE = r"[^\n]{0,40}?"
LUECKE_TOKEN = "..."

# Spalte, in der die Sperrmuster stehen. Eine Zeile ohne Muster gibt es nicht;
# die frueher hier gefuehrte Ausnahme 'keine:' ist entfernt, siehe Docstring.
SPALTEN_ZURUECK = 4
ABGESCHALTET = re.compile(r"^\s*keine\s*:", re.IGNORECASE)

# Behauptungen, die sich nicht ueber eine Schreibweise sperren lassen, weil das
# Textverbot die richtigen Verneinungen mit treffen wuerde. Statt eines Verbots
# steht hier eine Belegpflicht: Nennt ein Absatz beide Begriffe in einem Zug,
# muss er die Quelle zitieren, die die Sache klaert. Diese Liste steht bewusst
# im Code und nicht in der Tabelle. Sie ist keine Sperrliste von Schreibweisen,
# sondern eine Regel; und wer sie lockert, hinterlaesst einen Diff im Skript
# statt einer geaenderten Tabellenzelle.
BEHAUPTUNGS_REGELN = [
    {
        "name": "Collaborative Articles und Badge",
        "erster": re.compile(r"Collaborative" + LEER + r"Articles", re.IGNORECASE),
        "zweiter": re.compile(r"Badge", re.IGNORECASE),
        "beleg": re.compile(r"\bQ3\b"),
        "hinweis": (
            "Ein Absatz, der Collaborative Articles und ein Badge in einem Zug nennt, "
            "muss Q3 zitieren. Q3 belegt, dass das goldene Community-Top-Voice-Badge "
            "seit dem 08.10.2024 nicht mehr ueber Collaborative Articles zu verdienen "
            "ist. Die Pruefung ersetzt kein Lesen: eine falsche Aussage mit richtiger "
            "Quellenangabe kommt durch."
        ),
    },
]


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

        if token.startswith(LUECKE_TOKEN, i):
            teile.append(LUECKE)
            i += len(LUECKE_TOKEN)
            continue

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
        elif zeichen.lower() in UMLAUTE:
            teile.append(UMLAUTE[zeichen.lower()])
        else:
            teile.append(re.escape(zeichen))
        i += 1

    return "".join(teile)


def sperren_aus_tabelle(zeilen, fehler):
    """Uebersetzt die Tabelle 'Zurückgezogen' in Sperrmuster.

    Rueckgabe: Liste (kompilierte Regex, Token, Aussage). Jede Zeile muss ein
    Muster tragen. Es gibt keinen Weg, eine Zeile ueber die Tabelle von der
    Sperre zu befreien.
    """
    sperren = []

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
                "Jede zurueckgezogene Aussage braucht mindestens ein Muster."
            )
            continue

        if ABGESCHALTET.match(sperrmuster):
            fehler.append(
                f"Zurückgezogen, Zeile {nummer} ({kurz}): die Spalte 'Sperrmuster' schaltet "
                "die Sperre ab. Das ist nicht vorgesehen. Eine Zeile ohne Muster gibt es "
                "nicht; wenn ein Textverbot hier schaedlich waere, gehoert die Aussage in "
                "BEHAUPTUNGS_REGELN in scripts/check_sources.py und damit in einen "
                "Codediff, nicht in eine Tabellenzelle."
            )
            continue

        mengen = list(QUANTITAET.finditer(aussage))

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

        # Erdung: mindestens ein Muster der Zeile muss den eigenen Wortlaut in
        # der Spalte 'Frühere Aussage' treffen. Ohne das laesst sich eine Sperre
        # aushebeln, indem jemand ein beliebiges anderes Wort in die Zelle
        # schreibt: die Zeile bleibt stehen, der Zaehler stimmt, und die Sperre
        # greift ins Leere. Genau dieser Weg stand offen, solange nur geprueft
        # wurde, ob ueberhaupt etwas in der Zelle steht.
        if not any(regex.search(aussage) for regex, _, _ in zeilen_sperren):
            fehler.append(
                f"Zurückgezogen, Zeile {nummer} ({kurz}): kein Sperrmuster dieser Zeile "
                "trifft die eigene Spalte 'Frühere Aussage'. Ein Muster, das nicht einmal "
                "den zurueckgezogenen Wortlaut faengt, sperrt nichts. Entweder das Muster "
                "korrigieren oder in der Spalte 'Frühere Aussage' den Wortlaut eintragen, "
                "wie er im Skill stand."
            )

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

    return sperren


def absaetze(text: str):
    """Absaetze eines Textes als (Startzeile, Text), getrennt an Leerzeilen."""
    gesammelt = []
    start = 1
    for nummer, zeile in enumerate(text.split("\n"), 1):
        if zeile.strip():
            if not gesammelt:
                start = nummer
            gesammelt.append(zeile)
        elif gesammelt:
            yield start, "\n".join(gesammelt)
            gesammelt = []
    if gesammelt:
        yield start, "\n".join(gesammelt)


def pruefe_behauptungen(name: str, inhalt: str, fehler):
    """Belegpflicht fuer Behauptungen, die sich nicht sperren lassen."""
    for regel in BEHAUPTUNGS_REGELN:
        for zeile, absatz in absaetze(inhalt):
            if not regel["erster"].search(absatz):
                continue
            if not regel["zweiter"].search(absatz):
                continue
            if regel["beleg"].search(absatz):
                continue
            fehler.append(
                f"{name}:{zeile}: der Absatz faellt unter die Regel "
                f"{regel['name']!r}, nennt aber keine Quelle. {regel['hinweis']}"
            )


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

    sperren = sperren_aus_tabelle(zurueck, fehler)

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

        pruefe_behauptungen(name, inhalt, fehler)

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
    print(f"  {len(BEHAUPTUNGS_REGELN)} Behauptungsregel(n) mit Belegpflicht geprueft:")
    for regel in BEHAUPTUNGS_REGELN:
        print(f"    - {regel['name']}")

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
