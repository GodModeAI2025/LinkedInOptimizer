# -*- coding: utf-8 -*-
"""Eval-Runner fuer die Scoring-Matrix.

Verwendung:
    python tests/run_eval.py                      # alle Fixtures und alle Pruefungen
    python tests/run_eval.py --fixture profile_mid
    python tests/run_eval.py --result lauf.json --fixture profile_mid

Ohne --result prueft der Runner den Referenzlauf, der im Fixture mitliegt. Mit
--result prueft er das Ergebnis eines echten Laufs gegen dieselben Baender. Die
Ergebnisdatei ist ein JSON-Objekt mit einem Feld "kategorien" (Kategoriename auf
Rohscore 0 bis 10) und optional "gesamt".

Was geprueft wird:

1. Die Gewichtstabelle in references/SCORING.md ist die Quelle der Wahrheit.
   Zehn Kategorien, Gewichte in Summe 100 Prozent.
2. Dieselben zehn Namen stehen wortgleich in der Gewichtstabelle von SKILL.md,
   in den Balken der Landingpage und in den cat-Feldern von
   scripts/generate_report.js, dort zusaetzlich mit passendem Gewicht und
   passendem Maximalbeitrag. Das war der Befund aus dem Audit: dieselben zehn
   Kategorien liefen unter drei verschiedenen Benennungen.
3. references/SCORING.md hat je Kategorie einen eigenen Abschnitt.
4. Je Fixture: der Referenzlauf nennt genau die zehn Kategorien, alle Rohscores
   liegen zwischen 0 und 10, der gewichtete Gesamtscore ist aus den Rohscores
   nachgerechnet und liegt im erwarteten Band, und jeder Einzelscore liegt in
   seinem Band.
5. Drei Kategorien sind mechanisch aus den Fixture-Daten ableitbar und werden
   nicht geglaubt, sondern nachgerechnet: Posting-Frequenz aus Posts pro Woche,
   Netzwerk & Follower aus der Follower-Zahl, Profil-Vollstaendigkeit aus den
   18 Haken der Checkliste. Die Umrechnung haengt an den Tabellen in SCORING.md;
   aendern sich deren Zeilen, faellt der Runner mit einem Hinweis aus, statt
   still eine veraltete Umrechnung weiterzuverwenden.
6. Die Zahlen der Scoring-Engine auf der Landingpage sind identisch mit dem
   Referenzlauf von profile_mid. Damit hat jeder Wert auf der Seite eine
   committete Quelldatei.
7. Die Pflicht-Deliverables aus den Erwartungsdateien stehen in der
   Deliverables-Tabelle der README.
8. Die Checkliste in SCORING.md Abschnitt 9 ist die Quelle der Wahrheit fuer die
   geprueften Profil-Elemente. Ihre Kurznamen stehen in derselben Reihenfolge in
   der Audit-Tabelle von scripts/generate_report.js und in der Aufzaehlung in
   SKILL.md Phase 4.3, und die Stueckzahl stimmt an allen vier Stellen: dazu
   gehoert die Beschreibung der Deliverables in SKILL.md, die sonst weiter eine
   eigene Zahl fuehrt. Das war der Befund aus der Abnahme: dieselbe Liste lief
   unter drei Laengen (15, 17, 18) und trug in zweien davon noch die Elemente
   'Creator Mode' und 'Collaborative Articles', die laut Q3 und Q7 in SOURCES.md
   hinfaellig sind.
   Diese Pruefung bindet die Listen aneinander. Sie prueft Namen, Reihenfolge und
   Stueckzahl, nicht den Fliesstext drumherum: ein Satz wie 'Collaborative
   Articles bringen das goldene Badge' faellt ihr nicht auf. Dafuer ist
   scripts/check_sources.py zustaendig, das fuer genau diesen Absatz eine
   Quellenangabe verlangt.
9. Die Landingpage bezeichnet den Dialog als Beispiel und nennt die Fixture, aus
   der seine Zahlen stammen. pruefe_landing bindet die Zahlen, diese Pruefung
   bindet die Aussage, dass sie nicht gemessen sind.
10. Die gesperrten CTA-Formulierungen aus references/ETHICS.md stehen
   vollstaendig an allen vier Stellen, die dieselbe Liste noch einmal fuehren,
   und SKILL.md verankert den Ethik-Abgleich in der Ressourcen-Uebersicht, in
   Phase 8, in der Verifikation und in den Quality Gates. Das prueft
   Schreibweisen und Verweise; was es nicht sieht, steht in ETHICS.md unter
   "Was diese Seite nicht leistet".
11. Die zehn Achsen der Wettbewerbsmatrix stehen in references/COMPETITIVE.md
   und in SKILL.md Phase 3.1 in derselben Reihenfolge, und die Mindestzahl der
   Wettbewerber lautet an allen drei Stellen gleich. Der frueher daneben
   stehende zweite Wert darf nicht zurueckkommen.
12. Der Massnahmenplan laeuft an allen vier Stellen ueber dieselben drei
   Zeitfenster, und keiner der drei abgeloesten Horizonte steht mehr daneben.
   Der Changelog in SKILL.md ist davon ausgenommen, dort werden die alten
   Wortlaute genannt.

Die Fixtures sind frei erfunden. Es sind keine anonymisierten Echtprofile: ein
Echtprofil zu erheben und danach zu verfremden waere genau die Datenverarbeitung,
die SECURITY.md einschraenken soll.

Die Engagement-Rate in den Fixtures ist follower-basiert und traegt den Hinweis
mit. Sie wird bewusst nicht als Kriterium fuer Content-Qualitaet oder Engagement
verwendet, weil das Bewertungsraster in SCORING.md den impressions-basierten
Wert meint.

Exitcode 0, wenn alles zutrifft, sonst 1.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
EXPECTED = ROOT / "tests" / "expected"

# Erwarteter Wortlaut der Frequenz-Spalte in der Bewertungstabelle von
# SCORING.md Abschnitt 5, dazu die Untergrenze in Posts pro Woche, mit der der
# Runner rechnet. Steht in der Tabelle etwas anderes, ist die Umrechnung hier
# veraltet und muss nachgezogen werden.
FREQUENZ_ZEILEN = [
    ("<1×/Monat", 0.0),
    ("1–2×/Monat", 0.25),
    ("1×/Woche", 0.75),
    ("2–3×/Woche", 1.75),
    ("3–5×/Woche", 3.0),
]

# Dasselbe fuer die Follower-Spalte in Abschnitt 8.
FOLLOWER_ZEILEN = [
    ("<500", 0),
    ("500–2.000", 500),
    ("2.000–5.000", 2000),
    ("5.000–15.000", 5000),
    (">15.000 ODER Wachstum >500/Monat", 15000),
]


class Fehler(Exception):
    pass


# Der Skill-Text verteilt sich seit v2.6.0 auf die Router-Datei SKILL.md und die
# acht Phasendateien unter references/. Die Bindungen unten pruefen ihn als
# Ganzes: eine Liste, die in Phase 4.3 steht, ist dieselbe Liste, egal in
# welcher Datei sie liegt. In den Pfadlisten steht dafuer SKILL_TEXT; die
# Fehlermeldung nennt dann beide Orte, damit klar ist, wo zu suchen ist.
#
# SKILL_TEXT steht nur dort, wo eine Fundstelle bewusst in irgendeiner
# Skill-Datei liegen darf. Anker, die zur Struktur gehoeren, also die
# Ressourcen-Uebersicht, die Verifikation und die Quality Gates im Router oder
# der Ethik-Abgleich in Phase 8, nennen ihre Datei. Sonst waere die Aussage
# "das steht im Router" durch einen Treffer in einer Phasendatei erfuellt.
SKILL_TEXT = "SKILL.md + references/PHASE-*.md"


def skill_dateien():
    return [ROOT / "SKILL.md"] + sorted((ROOT / "references").glob("PHASE-*.md"))


def lies_skill() -> str:
    return "\n".join(lies(pfad) for pfad in skill_dateien())


def lies_pfad(rel_pfad: str) -> str:
    return lies_skill() if rel_pfad == SKILL_TEXT else lies(ROOT / rel_pfad)


def lies(pfad: Path) -> str:
    return pfad.read_text(encoding="utf-8")


def tabelle(text: str, ueberschrift: str, spalten: int, unter: str = None):
    """Datenzeilen der ersten Markdown-Tabelle unter einer Ueberschrift.

    Mit `unter` wird innerhalb des Abschnitts erst noch bis zu einer
    Unterueberschrift vorgespult. Das ist noetig, weil die Kategorie-Abschnitte
    in SCORING.md zuerst die Sub-Kriterien und danach die Bewertungsstufen
    fuehren.
    """
    start = text.find(ueberschrift)
    if start == -1:
        raise Fehler(f"Ueberschrift {ueberschrift!r} nicht gefunden.")
    if unter is not None:
        weiter = text.find(unter, start + len(ueberschrift))
        if weiter == -1:
            raise Fehler(f"{unter!r} nicht unter {ueberschrift!r} gefunden.")
        start = weiter

    zeilen = text[start:].splitlines()
    kopf = None
    for i in range(len(zeilen) - 1):
        eins, zwei = zeilen[i].strip(), zeilen[i + 1].strip()
        if eins.startswith("|") and zwei.startswith("|") and set(zwei) <= set("|-: "):
            kopf = i
            break
    if kopf is None:
        raise Fehler(f"Keine Tabelle unter {unter or ueberschrift!r} gefunden.")

    daten = []
    for zeile in zeilen[kopf + 2:]:
        blank = zeile.strip()
        if not blank.startswith("|"):
            break
        felder = [f.strip() for f in blank.strip("|").split("|")]
        if len(felder) != spalten:
            raise Fehler(
                f"Tabelle unter {unter or ueberschrift!r}: Zeile hat {len(felder)} Spalten, "
                f"erwartet sind {spalten}: {blank!r}"
            )
        daten.append(felder)
    return daten


def gewichte_aus_scoring(scoring: str):
    zeilen = tabelle(scoring, "### Gewichtung", 3)
    modell = {}
    for name, gewicht, _ in zeilen:
        treffer = re.fullmatch(r"(\d+)%", gewicht)
        if not treffer:
            raise Fehler(f"Gewicht nicht lesbar: {name} -> {gewicht!r}")
        modell[name] = int(treffer.group(1))
    if len(modell) != 10:
        raise Fehler(f"Erwartet werden 10 Kategorien, gefunden {len(modell)}.")
    if sum(modell.values()) != 100:
        raise Fehler(f"Die Gewichte summieren auf {sum(modell.values())}%, nicht auf 100%.")
    return modell


def score_baender(zeilen, spalte: int):
    """Liest Zeilen der Form '0–2' in der ersten Spalte und einen Text daneben."""
    ergebnis = []
    for felder in zeilen:
        treffer = re.fullmatch(r"(\d+)–(\d+)", felder[0])
        if not treffer:
            continue
        ergebnis.append(((int(treffer.group(1)), int(treffer.group(2))), felder[spalte]))
    return ergebnis


def band_fuer_frequenz(scoring: str, posts_pro_woche: float):
    zeilen = score_baender(tabelle(scoring, "## 5. POSTING-FREQUENZ", 3, "### Bewertungsstufen"), 1)
    if len(zeilen) != len(FREQUENZ_ZEILEN):
        raise Fehler("Die Bewertungstabelle der Posting-Frequenz hat nicht mehr fuenf Stufen.")
    treffer = None
    for (band, text), (erwartet, untergrenze) in zip(zeilen, FREQUENZ_ZEILEN):
        if text != erwartet:
            raise Fehler(
                f"Posting-Frequenz: SCORING.md nennt {text!r}, der Runner rechnet mit "
                f"{erwartet!r}. Umrechnung in tests/run_eval.py nachziehen."
            )
        if posts_pro_woche >= untergrenze:
            treffer = band
    return treffer


def band_fuer_follower(scoring: str, follower: int, wachstum: int):
    zeilen = score_baender(tabelle(scoring, "## 8. NETZWERK & FOLLOWER", 3, "### Bewertungsstufen"), 1)
    if len(zeilen) != len(FOLLOWER_ZEILEN):
        raise Fehler("Die Bewertungstabelle Netzwerk & Follower hat nicht mehr fuenf Stufen.")
    treffer = None
    for (band, text), (erwartet, untergrenze) in zip(zeilen, FOLLOWER_ZEILEN):
        if text != erwartet:
            raise Fehler(
                f"Netzwerk & Follower: SCORING.md nennt {text!r}, der Runner rechnet mit "
                f"{erwartet!r}. Umrechnung in tests/run_eval.py nachziehen."
            )
        if follower >= untergrenze:
            treffer = band
    if wachstum > 500:
        treffer = zeilen[-1][0]
    return treffer


def band_fuer_vollstaendigkeit(scoring: str, haken: int):
    zeilen = score_baender(tabelle(scoring, "## 9. PROFIL-VOLLSTÄNDIGKEIT", 2, "### Bewertungsstufen"), 1)
    if len(zeilen) != 5:
        raise Fehler("Die Bewertungstabelle Profil-Vollstaendigkeit hat nicht mehr fuenf Stufen.")
    for band, text in zeilen:
        zahlen = [int(z) for z in re.findall(r"\d+", text)]
        if text.startswith("≤"):
            if haken <= zahlen[0]:
                return band
        elif len(zahlen) >= 2:
            if zahlen[0] <= haken <= zahlen[1]:
                return band
    raise Fehler(f"Kein Band fuer {haken} von 18 Haken gefunden.")


def checkliste(scoring: str):
    punkte = [z.strip()[1:].strip() for z in scoring.splitlines() if z.strip().startswith("□")]
    if len(punkte) != 18:
        raise Fehler(f"Die Vollstaendigkeits-Checkliste hat {len(punkte)} Punkte, erwartet sind 18.")
    for punkt in punkte:
        if " (" not in punkt or not punkt.endswith(")"):
            raise Fehler(
                f"Checklistenpunkt {punkt!r} hat nicht die Form 'Kurzname (Kriterium)'. "
                "Ohne die Klammer laesst sich kein Kurzname ableiten, und die Bindung an "
                "die Audit-Tabelle und an SKILL.md faellt aus."
            )
    return punkte


def profil_elemente(scoring: str):
    """Die Kurznamen der Checkliste, also alles vor der ersten Klammer."""
    return [punkt.split(" (", 1)[0].strip() for punkt in checkliste(scoring)]


def elemente_aus_report(js: str):
    """Die Elementspalte der AUDIT-Tabelle in scripts/generate_report.js."""
    treffer = re.search(r"const AUDIT = \[(.*?)\n\];", js, re.S)
    if treffer is None:
        raise Fehler("scripts/generate_report.js: die AUDIT-Tabelle ist nicht lesbar.")
    return re.findall(r'\[\s*"[^"]*",\s*"([^"]*)"', treffer.group(1))


def elemente_aus_skill(skill: str):
    """Die Aufzaehlung in SKILL.md Phase 4.3, dazu die dort genannte Stueckzahl."""
    treffer = re.search(r"Prüfe die (\d+) Profil-Elemente[^(]*\(([^)]*)\)", skill)
    if treffer is None:
        raise Fehler(
            "SKILL.md Phase 4.3: der Satz 'Prüfe die N Profil-Elemente (...)' ist nicht lesbar."
        )
    return int(treffer.group(1)), [n.strip() for n in treffer.group(2).split(",")]


def namen_aus_skill(skill: str):
    return [name for name, _, _ in tabelle(skill, "| Kategorie | Gewicht | Max. Beitrag |", 3)]


def namen_aus_landing(seite: str):
    return [html.unescape(t) for t in re.findall(r'<span class="label">(.*?)</span>', seite)]


def kategorien_aus_report(js: str):
    muster = re.compile(
        r'\{\s*cat:\s*"([^"]+)",\s*raw:\s*([\d.]+),\s*w:\s*([\d.]+),'
        r'\s*weighted:\s*([\d.]+),\s*max:\s*([\d.]+)'
    )
    return [
        {"cat": m.group(1), "raw": float(m.group(2)), "w": float(m.group(3)),
         "weighted": float(m.group(4)), "max": float(m.group(5))}
        for m in muster.finditer(js)
    ]


def landing_werte(seite: str):
    """Kategoriename, Rohscore und Balkenbreite je Zeile der Scoring-Engine."""
    muster = re.compile(
        r'<span class="label">(.*?)</span>\s*'
        r'<div class="bar-bg"><div class="bar-fill" style="width:(\d+)%"></div></div>\s*'
        r'<span class="val">(\d+)/10</span>',
        re.S,
    )
    return [
        (html.unescape(m.group(1)), int(m.group(2)), int(m.group(3)))
        for m in muster.finditer(seite)
    ]


def deliverables_aus_readme(readme: str):
    return [name for name, _ in tabelle(readme, "## Deliverables", 2)]


def pruefe_quellen(fehler, scoring, skill, seite, js, modell):
    namen = list(modell)

    skill_namen = namen_aus_skill(skill)
    if skill_namen != namen:
        fehler.append(
            "SKILL.md nennt andere Kategorien als SCORING.md:\n"
            f"    SCORING.md: {namen}\n    SKILL.md:   {skill_namen}"
        )

    landing_namen = [n.rsplit(" (", 1)[0] for n in namen_aus_landing(seite)]
    if sorted(landing_namen) != sorted(namen):
        fehler.append(
            "Die Landingpage nennt andere Kategorien als SCORING.md:\n"
            f"    SCORING.md:   {sorted(namen)}\n    index.html:   {sorted(landing_namen)}"
        )

    report = kategorien_aus_report(js)
    report_namen = [e["cat"] for e in report]
    if sorted(report_namen) != sorted(namen):
        fehler.append(
            "scripts/generate_report.js nennt andere Kategorien als SCORING.md:\n"
            f"    SCORING.md:          {sorted(namen)}\n"
            f"    generate_report.js:  {sorted(report_namen)}"
        )
    else:
        for eintrag in report:
            prozent = modell[eintrag["cat"]]
            if round(eintrag["w"] * 10, 6) != prozent:
                fehler.append(
                    f"generate_report.js: {eintrag['cat']} hat w={eintrag['w']}, "
                    f"SCORING.md nennt {prozent}%."
                )
            if eintrag["max"] != prozent:
                fehler.append(
                    f"generate_report.js: {eintrag['cat']} hat max={eintrag['max']}, "
                    f"SCORING.md nennt {prozent}%."
                )

    for name in namen:
        if f". {name.upper()} (Gewicht: {modell[name]}%)" not in scoring:
            fehler.append(
                f"references/SCORING.md hat keinen Abschnitt "
                f"'## n. {name.upper()} (Gewicht: {modell[name]}%)'."
            )


def pruefe_profil_elemente(fehler, scoring, skill, js):
    """Haelt die drei Listen der geprueften Profil-Elemente aneinander.

    Quelle der Wahrheit ist die Checkliste in SCORING.md Abschnitt 9. Die
    Audit-Tabelle im Report und die Aufzaehlung in SKILL.md Phase 4.3 muessen
    dieselben Kurznamen in derselben Reihenfolge fuehren.
    """
    try:
        elemente = profil_elemente(scoring)
    except Fehler as ausnahme:
        fehler.append(str(ausnahme))
        return

    try:
        report = elemente_aus_report(js)
    except Fehler as ausnahme:
        fehler.append(str(ausnahme))
        report = None
    if report is not None and report != elemente:
        fehler.append(
            "Die Audit-Tabelle in scripts/generate_report.js nennt andere Profil-Elemente "
            "als die Checkliste in references/SCORING.md:\n"
            f"    SCORING.md:          {elemente}\n"
            f"    generate_report.js:  {report}"
        )

    try:
        anzahl, aus_skill = elemente_aus_skill(skill)
    except Fehler as ausnahme:
        fehler.append(str(ausnahme))
        aus_skill, anzahl = None, None
    if aus_skill is not None and aus_skill != elemente:
        fehler.append(
            "SKILL.md Phase 4.3 nennt andere Profil-Elemente als die Checkliste in "
            "references/SCORING.md:\n"
            f"    SCORING.md: {elemente}\n"
            f"    SKILL.md:   {aus_skill}"
        )
    if anzahl is not None and anzahl != len(elemente):
        fehler.append(
            f"SKILL.md Phase 4.3 spricht von {anzahl} Profil-Elementen, die Checkliste in "
            f"references/SCORING.md hat {len(elemente)}."
        )

    # Die beiden Stellen im Report, die die Stueckzahl im Klartext nennen. Ohne
    # sie stuende im Kundendokument weiter eine Zahl, die niemand nachzieht.
    for satz in (f"[X von {len(elemente)} Elementen", f'p("{len(elemente)} Elemente geprüft.'):
        if satz not in js:
            fehler.append(
                f"scripts/generate_report.js nennt {satz!r} nicht. Die Stueckzahl im Report "
                f"muss auf {len(elemente)} stehen, so viele Elemente hat die Checkliste."
            )

    # Dieselbe Stueckzahl steht in SKILL.md noch einmal in der Beschreibung der
    # Deliverables, und zwar zweimal: in Phase 7 und in der Kurzliste davor.
    # Genau die blieb bei der letzten Aenderung auf 17 stehen, waehrend Phase 4.3
    # und die Audit-Tabelle schon auf 18 waren. Geprueft wird deshalb nicht nur,
    # ob die Zahl vorkommt, sondern dass keine abweichende dasteht.
    for muster, wo in (
        (r"(\d+)-Punkte-Checkliste", "N-Punkte-Checkliste"),
        (r"X von (\d+) erfüllt", "X von N erfüllt"),
    ):
        treffer = re.findall(muster, skill)
        if not treffer:
            fehler.append(
                f"SKILL.md enthaelt die Stelle {wo!r} nicht mehr. Sie bindet die Stueckzahl "
                "der Profil-Elemente an die Checkliste und darf nicht ersatzlos verschwinden."
            )
            continue
        abweichend = sorted({z for z in treffer if int(z) != len(elemente)})
        if abweichend:
            fehler.append(
                f"SKILL.md nennt an der Stelle {wo!r} die Zahl(en) "
                f"{', '.join(abweichend)}, die Checkliste in references/SCORING.md hat "
                f"{len(elemente)} Elemente."
            )


def pruefe_fixture(fehler, scoring, modell, name, ergebnis=None):
    fixture = json.loads(lies(FIXTURES / f"{name}.json"))
    erwartet = json.loads(lies(EXPECTED / f"{name}.json"))
    lauf = ergebnis if ergebnis is not None else fixture["referenzlauf"]
    kategorien = lauf["kategorien"]
    kennung = f"{name}"

    if set(kategorien) != set(modell):
        fehlend = sorted(set(modell) - set(kategorien))
        zuviel = sorted(set(kategorien) - set(modell))
        fehler.append(f"{kennung}: Kategorien passen nicht. Fehlt: {fehlend}. Zuviel: {zuviel}.")
        return None

    gesamt = 0.0
    for kategorie, wert in kategorien.items():
        if not isinstance(wert, int) or not 0 <= wert <= 10:
            fehler.append(f"{kennung}: {kategorie} hat den Wert {wert!r}, erlaubt sind 0 bis 10.")
            continue
        gesamt += wert * modell[kategorie] / 10
        unten, oben = erwartet["baender"][kategorie]
        if not unten <= wert <= oben:
            fehler.append(
                f"{kennung}: {kategorie} liegt bei {wert}, erwartet war {unten} bis {oben}."
            )
    gesamt = round(gesamt, 1)

    gemeldet = lauf.get("gesamt")
    if gemeldet is not None and round(float(gemeldet), 1) != gesamt:
        fehler.append(
            f"{kennung}: gemeldeter Gesamtscore {gemeldet}, aus den Rohscores "
            f"nachgerechnet ergibt sich {gesamt}."
        )

    unten, oben = erwartet["gesamt"]
    if not unten <= gesamt <= oben:
        fehler.append(f"{kennung}: Gesamtscore {gesamt}, erwartet war {unten} bis {oben}.")

    if ergebnis is None:
        profil = fixture["profil"]

        soll = checkliste(scoring)
        if list(profil["vollstaendigkeit"]) != soll:
            fehler.append(
                f"{kennung}: die Checkliste im Fixture passt nicht mehr zu SCORING.md. "
                "Punkte in tests/fixtures nachziehen."
            )
        else:
            haken = sum(1 for wert in profil["vollstaendigkeit"].values() if wert)
            band = band_fuer_vollstaendigkeit(scoring, haken)
            wert = kategorien["Profil-Vollständigkeit"]
            if not band[0] <= wert <= band[1]:
                fehler.append(
                    f"{kennung}: {haken} von 18 Haken ergeben nach SCORING.md {band[0]} bis "
                    f"{band[1]} Punkte, der Referenzlauf nennt {wert}."
                )

        band = band_fuer_frequenz(scoring, profil["posting"]["posts_pro_woche"])
        wert = kategorien["Posting-Frequenz"]
        if band is None or not band[0] <= wert <= band[1]:
            fehler.append(
                f"{kennung}: {profil['posting']['posts_pro_woche']} Posts/Woche ergeben nach "
                f"SCORING.md {band}, der Referenzlauf nennt {wert}."
            )

        band = band_fuer_follower(
            scoring, profil["netzwerk"]["follower"], profil["netzwerk"]["wachstum_pro_monat"]
        )
        wert = kategorien["Netzwerk & Follower"]
        if band is None or not band[0] <= wert <= band[1]:
            fehler.append(
                f"{kennung}: {profil['netzwerk']['follower']} Follower ergeben nach "
                f"SCORING.md {band}, der Referenzlauf nennt {wert}."
            )

        if profil["kennzahlen"]["impressions"] is not None:
            fehler.append(
                f"{kennung}: das Fixture nennt Impressions. Fuer fremde Profile sind sie nicht "
                "sichtbar, das Feld gehoert auf null."
            )
        if "engagement_rate_follower_basis" not in profil["kennzahlen"]:
            fehler.append(
                f"{kennung}: die Engagement-Rate muss den Nenner im Feldnamen tragen "
                "(engagement_rate_follower_basis)."
            )
        if "erfunden" not in fixture.get("herkunft", ""):
            fehler.append(f"{kennung}: das Feld herkunft muss die Fixture als erfunden ausweisen.")

    return gesamt


def pruefe_landing(fehler, seite):
    fixture = json.loads(lies(FIXTURES / "profile_mid.json"))
    referenz = fixture["referenzlauf"]
    zeilen = landing_werte(seite)
    if len(zeilen) != 10:
        fehler.append(f"Die Scoring-Engine auf der Landingpage hat {len(zeilen)} Zeilen, erwartet sind 10.")
        return
    for label, breite, wert in zeilen:
        name = label.rsplit(" (", 1)[0]
        soll = referenz["kategorien"].get(name)
        if soll is None:
            continue
        if wert != soll:
            fehler.append(
                f"index.html: {name} zeigt {wert}/10, tests/fixtures/profile_mid.json nennt {soll}."
            )
        if breite != wert * 10:
            fehler.append(
                f"index.html: der Balken von {name} steht auf {breite}%, der Wert ist {wert}/10."
            )
    treffer = re.search(r'<span class="number">(\d+)</span>', seite)
    if not treffer:
        fehler.append("index.html: der Gesamtscore-Ring ist nicht lesbar.")
    elif int(treffer.group(1)) != round(referenz["gesamt"]):
        fehler.append(
            f"index.html: der Ring zeigt {treffer.group(1)}, profile_mid ergibt "
            f"{referenz['gesamt']}."
        )

    # Der nachgestellte Dialog nennt dieselben Zahlen noch einmal. Auch die
    # muessen aus dem Fixture stammen, sonst steht auf der Seite wieder ein
    # zweites, nicht nachrechenbares Zahlenbild.
    dialog = re.search(r'Profil-Score: <strong>(\d+)/100</strong>(.*?)</div>', seite, re.S)
    if not dialog:
        fehler.append("index.html: der Beispiel-Dialog ist nicht lesbar.")
    else:
        if int(dialog.group(1)) != round(referenz["gesamt"]):
            fehler.append(
                f"index.html: der Beispiel-Dialog nennt {dialog.group(1)}/100, profile_mid "
                f"ergibt {referenz['gesamt']}."
            )
        for name, wert in re.findall(r"([A-ZÄÖÜ][\wÄÖÜäöüß&; -]*?) (\d+)/10", dialog.group(2)):
            name = html.unescape(name).strip()
            soll = referenz["kategorien"].get(name)
            if soll is None:
                fehler.append(
                    f"index.html: der Beispiel-Dialog nennt die Kategorie {name!r}, die es im "
                    "Gewichtsmodell nicht gibt."
                )
            elif int(wert) != soll:
                fehler.append(
                    f"index.html: der Beispiel-Dialog nennt {name} mit {wert}/10, "
                    f"profile_mid nennt {soll}."
                )


# Was auf der Landingpage stehen muss, damit der Dialog nicht als Messung
# durchgeht, und warum. Die Zahlen im Dialog bindet pruefe_landing an die
# Fixture; diese Liste bindet die Aussage, dass sie nicht gemessen sind. Ohne
# sie liesse sich 'Beispiel-Dialog' wieder in 'Live Demo' aendern, ohne dass ein
# Pruefschritt anschlaegt.
LANDING_EHRLICHKEIT = [
    ('<div class="section-label">Beispiel-Dialog</div>',
     "Die Ueberschrift des Dialogs muss ihn als Beispiel ausweisen."),
    ('<div class="chat-status">Nachgestellter Dialog &middot; Werte aus '
     'tests/fixtures/profile_mid.json</div>',
     "Die Statuszeile muss den Dialog als nachgestellt ausweisen und die Fixture nennen."),
    ("Der Dialog rechts ist nachgestellt.",
     "Der Fliesstext muss sagen, dass der Dialog nachgestellt ist."),
    ("hinterlegt als tests/fixtures/profile_mid.json, kein gemessenes Profil",
     "Der Fliesstext muss die Fixture nennen und sagen, dass sie kein gemessenes Profil ist."),
]


def pruefe_landing_ehrlichkeit(fehler, seite):
    for satz, grund in LANDING_EHRLICHKEIT:
        if satz not in seite:
            fehler.append(f"index.html: {grund} Erwartet wird der Wortlaut {satz!r}.")


# Fundstellen der gesperrten CTA-Formulierungen. Die Quelle ist die Tabelle
# "Gesperrte CTA-Formulierungen" in references/ETHICS.md; hier steht, wo dieselbe
# Liste noch einmal auftaucht und deshalb vollstaendig sein muss. Jeder Eintrag
# nennt die Datei und einen Marker, der genau eine Zeile trifft. In dieser Zeile
# muessen alle Formulierungen der Tabelle stehen.
#
# Das war der Befund: dieselbe Liste lief unter vier verschiedenen Laengen.
# SKILL.md Phase 6.1 kannte zwei Formulierungen, die Algorithmus-Regeln in
# TEMPLATES.md und das Sub-Kriterium in SCORING.md je drei, die Liste der
# verbotenen Woerter in TEMPLATES.md eine vierte Zusammenstellung. Wer sich an
# eine der kurzen Listen hielt, lieferte einen CTA aus, den eine andere Stelle
# im selben Skill verbietet.
CTA_FUNDSTELLEN = [
    ("references/PHASE-6-content.md", "- Kein Engagement-Bait:"),
    ("references/TEMPLATES.md", "7. Kein Engagement-Bait →"),
    ("references/TEMPLATES.md", "gesperrte CTA-Formulierungen, vollständige Liste"),
    ("references/SCORING.md", "| Engagement-Bait-Freiheit |"),
]

# Verweise, ohne die references/ETHICS.md eine Seite waere, die niemand liest.
# Der Ethik-Abgleich ist der einzige Schritt, der die Regeln vor der Uebergabe
# anwendet; faellt der Abschnitt aus SKILL.md, laeuft die Datei leer mit.
ETHIK_VERANKERUNG = [
    ("SKILL.md", "| `references/ETHICS.md` |",
     "Die Ressourcen-Uebersicht im Router muss references/ETHICS.md fuehren."),
    ("references/PHASE-8-report.md", "### 8.0 Ethik-Abgleich",
     "Phase 8 muss mit dem Ethik-Abgleich beginnen."),
    ("SKILL.md", "**Ethik**:",
     "Der Verifikations-Abschnitt im Router muss eine Ethik-Zeile fuehren."),
    ("SKILL.md", "| 8. Übergabe | Ethik-Abgleich für alle fünf Artefakte |",
     "Die Quality Gates im Router muessen den Ethik-Abgleich als Gate fuehren."),
]


def cta_formulierungen(ethik: str):
    """Die gesperrten CTA-Formulierungen aus references/ETHICS.md."""
    zeilen = tabelle(ethik, "## Gesperrte CTA-Formulierungen", 2)
    formulierungen = [zeile[0] for zeile in zeilen]
    if len(formulierungen) < 2:
        raise Fehler(
            "references/ETHICS.md: die Tabelle 'Gesperrte CTA-Formulierungen' hat weniger als "
            "zwei Zeilen. Eine Liste, die auf eine Zeile schrumpft, bindet nichts mehr."
        )
    return formulierungen


def pruefe_ethik(fehler, ethik):
    """Bindet die gesperrten CTA-Formulierungen und die Verweise auf ETHICS.md.

    Geprueft werden Schreibweisen und Verweise, nicht Verhalten. Was diese
    Pruefung nicht sieht, steht in references/ETHICS.md im Abschnitt "Was diese
    Seite nicht leistet": eine neu erfundene Bait-Formulierung, eine unbelegte
    Angabe im Profil, ein uebergangener Abgleich im Gespraech.
    """
    formulierungen = cta_formulierungen(ethik)

    for rel_pfad, marker in CTA_FUNDSTELLEN:
        text = lies_pfad(rel_pfad)
        treffer = [z for z in text.splitlines() if marker in z]
        if len(treffer) != 1:
            fehler.append(
                f"{rel_pfad}: der Marker {marker!r} trifft {len(treffer)} Zeilen, erwartet wird "
                "genau eine. Ohne ihn laesst sich nicht pruefen, ob die Liste vollstaendig ist."
            )
            continue
        for formulierung in formulierungen:
            if formulierung not in treffer[0]:
                fehler.append(
                    f"{rel_pfad}: die Zeile zu {marker!r} nennt die gesperrte Formulierung "
                    f"{formulierung!r} nicht. references/ETHICS.md fuehrt sie."
                )

    for rel_pfad, satz, grund in ETHIK_VERANKERUNG:
        if satz not in lies_pfad(rel_pfad):
            fehler.append(f"{rel_pfad}: {grund} Erwartet wird der Wortlaut {satz!r}.")


# Die Mindestzahl der Wettbewerber. Sie stand im Repo an zwei Stellen mit zwei
# verschiedenen Werten: das Quality Gate verlangte 3, die Fehlerbehandlung nannte
# daneben "Minimum 2 Wettbewerber fuer sinnvolle Matrix". Ein Gate, das der
# eigene Fehlerpfad unterlaeuft, ist kein Gate. Es gilt eine Zahl, und die muss
# an allen drei Stellen gleich lauten.
WETTBEWERBER_MINIMUM = "3"

# Wortlaute, die die Mindestzahl tragen. Jeder Eintrag nennt eine Datei, einen
# Marker, der genau eine Zeile trifft, eine Beschreibung und die Zeichenkette,
# die in dieser Zeile stehen muss. Die Zeichenkette traegt die Zahl im Kontext:
# ein blosses "3" waere in der Gate-Zeile schon durch die Phasennummer erfuellt.
MINIMUM_FUNDSTELLEN = [
    ("SKILL.md", "| 3. Wettbewerb |",
     "Quality Gate fuer Phase 3",
     "Min. {} Wettbewerber"),
    ("SKILL.md", "**Wettbewerber nicht abrufbar**:",
     "Fehlerbehandlung fuer Phase 3",
     "verlangt {} Wettbewerber"),
    ("references/COMPETITIVE.md", "Es gilt eine Zahl:",
     "Der Abschnitt zur nicht erreichten Mindestzahl",
     "Es gilt eine Zahl: {}."),
    ("references/COMPETITIVE.md", "Nimm 3 bis 5.",
     "Die Auswahlregel",
     "Nimm {} bis 5."),
]

# Die zweite Zahl darf nicht zurueckkommen, auch nicht in einer der
# Schreibweisen, in denen sie im Repo stand.
MINIMUM_VERBOTEN = [
    "Minimum 2 Wettbewerber",
    "Min. 2 Wettbewerber",
    "mindestens 2 Wettbewerber",
    # Die Fassung, die bis v2.4.0 im Repo stand. Sie nannte keine zweite Zahl
    # als Regel, hob das Gate aber genauso auf.
    "Sind nur 2 erreichbar",
    "erstelle die Matrix mit 2",
    "Bei <2:",
    "Ausnahme siehe Fehlerbehandlung",
]


def achsen_aus_competitive(competitive: str):
    """Die zehn Achsen der Wettbewerbsmatrix, in der Reihenfolge der Tabelle."""
    zeilen = tabelle(competitive, "## Die zehn Achsen", 4)
    achsen = [zeile[0] for zeile in zeilen]
    if len(achsen) != 10:
        raise Fehler(
            f"references/COMPETITIVE.md: die Achsen-Tabelle hat {len(achsen)} Zeilen, "
            "die Ueberschrift verspricht zehn."
        )
    return achsen


def achsen_aus_skill(skill: str):
    """Die Achsenliste aus SKILL.md Phase 3.1."""
    marker = "Erhebe auf diesen zehn Achsen, in dieser Reihenfolge:"
    treffer = [z for z in skill.splitlines() if marker in z]
    if len(treffer) != 1:
        raise Fehler(
            f"SKILL.md: der Marker {marker!r} trifft {len(treffer)} Zeilen, erwartet wird genau "
            "eine. Ohne ihn laesst sich die Achsenliste nicht gegen COMPETITIVE.md halten."
        )
    rest = treffer[0].split(marker, 1)[1].strip().rstrip(".")
    return [teil.strip() for teil in rest.split(",")]


def pruefe_wettbewerb(fehler, skill, competitive):
    """Bindet Achsen und Mindestzahl der Wettbewerbsanalyse.

    Geprueft werden eine Liste und eine Zahl im Text. Nicht geprueft wird, ob
    eine Erhebung stattgefunden hat, ob ihre Werte stimmen und ob die erhobenen
    Profile die Auswahlregel erfuellen; das steht in COMPETITIVE.md unter "Was
    diese Vorlage nicht leistet".
    """
    # Die Achsen und die Mindestzahl haengen nicht voneinander ab. Ein Fehler in
    # der einen Haelfte darf die andere nicht verdecken, sonst meldet ein Lauf
    # nur den ersten von mehreren Befunden.
    try:
        aus_datei = achsen_aus_competitive(competitive)
        aus_skill = achsen_aus_skill(skill)
        if aus_datei != aus_skill:
            fehler.append(
                "Die zehn Achsen stehen in references/COMPETITIVE.md und SKILL.md Phase 3.1 "
                "nicht in derselben Reihenfolge."
                f"\n      COMPETITIVE.md: {aus_datei}\n      SKILL.md:       {aus_skill}"
            )
    except Fehler as ausnahme:
        fehler.append(str(ausnahme))

    for rel_pfad, marker, was, vorlage in MINIMUM_FUNDSTELLEN:
        text = lies_pfad(rel_pfad)
        treffer = [z for z in text.splitlines() if marker in z]
        if len(treffer) != 1:
            fehler.append(
                f"{rel_pfad}: der Marker {marker!r} ({was}) trifft {len(treffer)} Zeilen, "
                "erwartet wird genau eine."
            )
            continue
        wortlaut = vorlage.format(WETTBEWERBER_MINIMUM)
        if wortlaut not in treffer[0]:
            fehler.append(
                f"{rel_pfad}: {was} nennt die Mindestzahl nicht im erwarteten Wortlaut "
                f"{wortlaut!r}."
            )

    for rel_pfad in (SKILL_TEXT, "README.md", "references/COMPETITIVE.md"):
        text = lies_pfad(rel_pfad)
        for verboten in MINIMUM_VERBOTEN:
            for nummer, zeile in enumerate(text.splitlines(), 1):
                if verboten not in zeile:
                    continue
                # In COMPETITIVE.md steht der abgeloeste Wortlaut einmal als
                # Blockzitat, damit nachvollziehbar bleibt, was sich geaendert
                # hat. Zitatzeilen sind ausgenommen, Regeln nicht. Die Ausnahme
                # gilt nur fuer diese Datei und nur fuer Zeilen, die mit '>'
                # beginnen; steht der Wortlaut daneben als Anweisung, faellt er
                # auf.
                if rel_pfad == "references/COMPETITIVE.md" and zeile.lstrip().startswith(">"):
                    continue
                fehler.append(
                    f"{rel_pfad}:{nummer}: {verboten!r} steht wieder im Skill. Es gilt eine "
                    f"Mindestzahl, und die ist {WETTBEWERBER_MINIMUM}."
                )


# Die drei Zeitfenster des Massnahmenplans. Das Repo fuehrte bis v2.4.0 drei
# unvereinbare Horizonte nebeneinander: SKILL.md Phase 7 endete nach 90 Tagen,
# Kapitel 8 des Reports lief bis Monat 6, und README wie Landingpage
# beschrieben das Deliverable als "Roadmap bis Monat 6". Wer den einen Plan
# umsetzte, arbeitete gegen den anderen. Es gibt jetzt ein Raster.
#
# Die positive Haelfte: jede Stelle muss die drei Fenster nennen. Die negative
# Haelfte weiter unten ist die, die die Vereinheitlichung misst; ohne sie liesse
# sich ein alter Horizont danebenstellen, ohne dass etwas anschlaegt.
ZEITFENSTER = [
    (SKILL_TEXT, ["Tag 1–30", "Tag 31–60", "Tag 61–90"]),
    ("scripts/generate_report.js", ["Tag 1-30", "Tag 31-60", "Tag 61-90"]),
    ("README.md", ["30/60/90-Tage-Roadmap", "Tag 1–30, 31–60 und 61–90"]),
    ("index.html", ["30/60/90-Tage-Roadmap", "Tag 1–30, 31–60, 61–90"]),
]

# Die abgeloesten Horizonte, in den Schreibweisen, in denen sie im Repo standen.
# Der Bindestrich steht in generate_report.js, der Halbgeviertstrich in den
# Markdown-Dateien und auf der Landingpage.
ALTE_HORIZONTE = [
    "Roadmap bis Monat 6",
    "12-Monats",
    "Woche 1-2", "Woche 1–2",
    "Woche 3-4", "Woche 3–4",
    "Monat 2-3", "Monat 2–3",
    "Monat 4-6", "Monat 4–6",
    "nach 3 Monaten",
]

# Dateien, in denen kein abgeloester Horizont mehr stehen darf. SKILL.md traegt
# den Changelog und darf die alten Wortlaute dort nennen; die Ausnahme ist auf
# den Changelog begrenzt und nicht auf die Datei.
HORIZONT_DATEIEN = [SKILL_TEXT, "README.md", "index.html", "scripts/generate_report.js"]


def pruefe_zeitfenster(fehler):
    """Bindet die drei Zeitfenster und weist die abgeloesten Horizonte zurueck.

    Geprueft werden Beschriftungen. Nicht geprueft wird, ob die Massnahmen in
    einem Fenster in dieses Fenster gehoeren, ob die Hypothesen aus Phase 7.2
    jemals gemessen wurden und ob ein Kunde den Plan durchhaelt.
    """
    for rel_pfad, erwartet in ZEITFENSTER:
        text = lies_pfad(rel_pfad)
        for wortlaut in erwartet:
            if wortlaut not in text:
                fehler.append(
                    f"{rel_pfad}: das Zeitfenster {wortlaut!r} fehlt. Der Massnahmenplan laeuft "
                    "an allen vier Stellen ueber Tag 1-30, 31-60 und 61-90."
                )

    for rel_pfad in HORIZONT_DATEIEN:
        # CHANGELOG.md steht bewusst nicht in HORIZONT_DATEIEN: dort werden die
        # abgeloesten Horizonte als Historie genannt, das ist ihr Platz.
        text = lies_pfad(rel_pfad)
        for nummer, zeile in enumerate(text.splitlines(), 1):
            for alt in ALTE_HORIZONTE:
                if alt in zeile:
                    fehler.append(
                        f"{rel_pfad}:{nummer}: der abgeloeste Horizont {alt!r} steht wieder im "
                        "Skill. Es gibt ein Raster: Tag 1-30, 31-60, 61-90."
                    )


def pruefe_deliverables(fehler, readme):
    vorhanden = deliverables_aus_readme(readme)
    for name in sorted(EXPECTED.glob("*.json")):
        erwartet = json.loads(lies(name))
        for eintrag in erwartet["pflicht_deliverables"]:
            if eintrag not in vorhanden:
                fehler.append(
                    f"{name.stem}: das Pflicht-Deliverable {eintrag!r} steht nicht in der "
                    "Deliverables-Tabelle der README."
                )


def pruefe_untrusted(fehler, _skill=None):
    """Bindet die Regel "erhobener Seitentext ist Daten" an ihre Fundstellen.

    Geprueft wird dreierlei: die Datei references/UNTRUSTED.md existiert, sie
    fuehrt die fuenf nummerierten Regeln, und der Skill verweist an beiden
    Stellen darauf, an denen fremder Text hereinkommt, also in Phase 1.1 und in
    Phase 3.1. Faellt einer der beiden Verweise bei einer Ueberarbeitung weg,
    steht die Regel zwar noch in der Referenz, aber nicht mehr im Weg.

    Der Abschnitt wird je Datei geschnitten und nicht im zusammengesetzten
    Skill-Text. Im zusammengesetzten Text endet der letzte Abschnitt einer Datei
    nicht an der Dateigrenze, sondern erst an der naechsten Ueberschrift der
    naechsten Datei: ein geloeschter Verweis in Phase 1 waere dann durch einen
    Treffer in Phase 2 gedeckt gewesen. Genau dieser Fall ist in der Review
    aufgefallen und hier behoben.

    Nicht geprueft wird, ob die Regel im Gespraech eingehalten wird. Das steht
    so in UNTRUSTED.md unter "Was diese Seite nicht leistet".
    """
    pfad = ROOT / "references" / "UNTRUSTED.md"
    if not pfad.exists():
        fehler.append("references/UNTRUSTED.md fehlt")
        return
    regel = lies(pfad)

    for nummer in range(1, 6):
        if f"{nummer}. **" not in regel:
            fehler.append(f"references/UNTRUSTED.md fuehrt Regel {nummer} nicht")

    for phase, ueberschrift in (
        ("1.1", "### 1.1 Profildaten via Chrome extrahieren"),
        ("3.1", "### 3.1 Nischen-Konkurrenten analysieren"),
    ):
        gefunden = False
        for datei in skill_dateien():
            text = lies(datei)
            if ueberschrift not in text:
                continue
            gefunden = True
            start = text.index(ueberschrift)
            ende = text.find("\n### ", start + len(ueberschrift))
            abschnitt = text[start:ende if ende != -1 else len(text)]
            if "references/UNTRUSTED.md" not in abschnitt:
                fehler.append(
                    f"{datei.relative_to(ROOT)}: Phase {phase} verweist nicht auf "
                    "references/UNTRUSTED.md"
                )
        if not gefunden:
            fehler.append(f"{SKILL_TEXT}: keine Ueberschrift fuer Phase {phase} mehr")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prueft die Scoring-Matrix gegen die Fixtures.")
    parser.add_argument("--fixture", help="Nur dieses Fixture pruefen.")
    parser.add_argument("--result", help="Ergebnis-JSON eines echten Laufs statt des Referenzlaufs.")
    args = parser.parse_args()

    if args.result and not args.fixture:
        parser.error("--result braucht --fixture, damit klar ist, gegen welche Baender geprueft wird.")

    fehler = []
    scoring = lies(ROOT / "references" / "SCORING.md")
    skill = lies_skill()
    seite = lies(ROOT / "index.html")
    js = lies(ROOT / "scripts" / "generate_report.js")
    readme = lies(ROOT / "README.md")
    ethik = lies(ROOT / "references" / "ETHICS.md")
    competitive = lies(ROOT / "references" / "COMPETITIVE.md")

    try:
        modell = gewichte_aus_scoring(scoring)
    except Fehler as ausnahme:
        print(f"FEHLER: {ausnahme}", file=sys.stderr)
        return 1

    print("  Gewichtsmodell aus references/SCORING.md:")
    for name, prozent in modell.items():
        print(f"    {prozent:>3}%  {name}")

    try:
        pruefe_quellen(fehler, scoring, skill, seite, js, modell)
        pruefe_profil_elemente(fehler, scoring, skill, js)

        namen = [args.fixture] if args.fixture else sorted(p.stem for p in FIXTURES.glob("*.json"))
        ergebnis = json.loads(lies(Path(args.result))) if args.result else None

        print("\n  Fixtures:")
        for name in namen:
            gesamt = pruefe_fixture(fehler, scoring, modell, name, ergebnis)
            if gesamt is not None:
                print(f"    {name:<14} Gesamtscore {gesamt}")

        if not args.result:
            pruefe_landing(fehler, seite)
            pruefe_landing_ehrlichkeit(fehler, seite)
            pruefe_deliverables(fehler, readme)
            pruefe_ethik(fehler, ethik)
            pruefe_wettbewerb(fehler, skill, competitive)
            pruefe_zeitfenster(fehler)
            pruefe_untrusted(fehler, skill)
    except Fehler as ausnahme:
        fehler.append(str(ausnahme))

    if fehler:
        print("\nFEHLER:", file=sys.stderr)
        for eintrag in fehler:
            print(f"  - {eintrag}", file=sys.stderr)
        return 1

    print("\nOK: Kategorienamen an vier Stellen gleich, Profil-Elemente an drei Stellen\n    gleich, gesperrte CTA-Formulierungen an vier Stellen vollstaendig,\n    Achsen und Mindestzahl der Wettbewerbsanalyse gebunden,\n    ein Zeitraster statt drei,\n    Untrusted-Regel an beiden Erhebungsstellen verankert,\n    alle Fixtures im Band.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
