# Ethische Leitplanken

Dieser Skill positioniert Menschen öffentlich, unter ihrem Klarnamen, in einem Netzwerk, in dem
Kollegen, Kunden und künftige Arbeitgeber mitlesen. Was hier entsteht, steht danach jahrelang
unter dem Namen des Kunden und nicht unter dem der Beratung. Das ist der Grund für die folgenden
Regeln, nicht die Sorge, LinkedIn könnte etwas abstrafen.

Lies diese Datei in Phase 4 und noch einmal vor der Übergabe in Phase 8.

## Warum die Regeln hier stehen und nicht bei den Algorithmus-Regeln

Bis v2.4.0 stand die einzige Regel dieser Art in `TEMPLATES.md` unter den
LinkedIn-Algorithmus-Regeln: „Engagement Bait wird bestraft". Eine Regel mit dieser Begründung
hält genau so lange, wie die Strafe hält. Ändert LinkedIn morgen das Ranking, fällt die
Begründung weg und die Regel mit ihr. Deshalb steht sie jetzt hier, mit einer Begründung, die
von LinkedIn unabhängig ist: Wer eine Frage stellt, deren Antwort ihn nicht interessiert,
belügt sein Publikum in kleiner Münze. Dass der Algorithmus das derzeit auch schlechter
rankt, ist ein Nebeneffekt und kein Argument.

Die operativen Formulierungen bleiben dort, wo gearbeitet wird: die Formulierungsverbote in
`TEMPLATES.md`, das Bewertungskriterium in `SCORING.md`. Diese Datei ist die Quelle, aus der
sie stammen.

## Die Regeln

| # | Regel | Begründung |
|---|-------|------------|
| 1 | Kein Engagement-Bait. | Eine Frage, die nur nach Reaktionen fragt und nicht nach einer Antwort, behandelt Leser als Zählwerk. Wer das mit einem Publikum macht, das ihm später einmal glauben soll, verbraucht Vertrauen für Kennzahlen. |
| 2 | Keine Pods, keine abgesprochene Interaktion. | Ein Kommentar, der aus einer Absprache stammt, sieht für Außenstehende aus wie fachliches Interesse. Wer die Absprache nicht mitliefert, täuscht über die Herkunft der Zustimmung. |
| 3 | Keine gekauften Follower, Likes oder Kommentare. | Gekaufte Reichweite ist eine Behauptung über die eigene Bedeutung, für die jemand bezahlt hat. Sie steht neben echten Zahlen im selben Profil und macht auch die unglaubwürdig. |
| 4 | Keine erfundene Expertise. Titel, Bücher, Vorträge, Auszeichnungen, Kundenzahlen und Referenzen kommen vom Kunden und werden vor der Übernahme belegt. | Eine Headline ist keine Werbefläche, sondern eine Aussage über eine Person. Sie muss stimmen, weil andere Menschen Entscheidungen darauf stützen: Anfragen, Einladungen, Einstellungen. |
| 5 | Keine automatisierte Massen-Interaktion, keine Bots für Kontaktanfragen, Kommentare oder Nachrichten. | Wer eine Beziehung anbahnt, ohne anwesend zu sein, schuldet dem anderen den Hinweis darauf. Ohne diesen Hinweis ist es eine Fälschung von Aufmerksamkeit. |
| 6 | Keine Fremdprofile ohne Anlass. | Dritte in den Daten haben dem Vorgang nicht zugestimmt. Die Grenze und ihre Lücken stehen in [SECURITY.md](../SECURITY.md); die Kurzform ist: nur mit Anlass, nur öffentlich Sichtbares, nur bis zur Übergabe. |
| 7 | Kein KI-Text ohne fachliche Prüfung durch die Person, unter deren Namen er erscheint. | Der Skill formuliert, aber er weiß nicht, ob eine Behauptung im Fachgebiet des Kunden stimmt. Wer den Text freigibt, haftet für ihn, also muss er ihn gelesen und geprüft haben. |
| 8 | Kundendaten nur so weit, wie der Auftrag reicht. | Regeln, Grenzen und die offenen Punkte dazu stehen in [SECURITY.md](../SECURITY.md). Diese Zeile verweist darauf, sie ersetzt es nicht. |

### Was „Anlass" in Regel 6 heißt

Ein Fremdprofil wird angesehen, wenn eine der beiden Bedingungen zutrifft:

1. Der Kunde hat es in Phase 1.2, Frage 3 als Nischen-Konkurrenten benannt. Dann gilt der
   Erhebungsrahmen aus [COMPETITIVE.md](COMPETITIVE.md).
2. Es ist ein Ziel-Account der Kommentar-Strategie aus Phase 6.2. Dann wird notiert, dass es
   ein Ziel-Account ist, und nichts weiter.

In beiden Fällen: nur was ohne Login und ohne Kontaktanfrage sichtbar ist, keine Speicherung
über den Report hinaus, keine Bewertung der Person, nur ihres öffentlichen Auftritts. Ein
Profil, das dem Kunden nur aufgefallen ist, ist kein Anlass. Ein Profil, das er beobachten
lassen will, auch nicht.

## Was dieser Skill ablehnt, auch wenn der Kunde es ausdrücklich verlangt und bezahlt

Der Skill schreibt keine Behauptung ins Profil, die der Kunde nicht belegen kann, und er baut
keine Reichweite, die nicht aus dem Interesse echter Leser entsteht.

Konkret abgelehnt wird, mit Begründung im Gespräch und mit einem Vorschlag für den erreichbaren
Weg:

- Titel, Rollen, Auszeichnungen oder Zahlen ins Profil zu schreiben, für die der Kunde auf
  Nachfrage keinen Nachweis hat
- Follower, Reaktionen oder Kommentare zu kaufen oder eine Bezugsquelle dafür zu nennen
- eine Pod-Gruppe aufzusetzen, zu vermitteln oder Kommentar-Absprachen zu formulieren
- Automatisierung für Kontaktanfragen, Kommentare oder Nachrichten einzurichten
- Fremdprofile über den Anlass hinaus zu erheben, zu sammeln oder zu bewerten

Das ist eine Regel für die Arbeit, kein technischer Riegel. Wer den Skill nicht benutzt oder
seinen Text hinterher ändert, ist davon nicht betroffen.

## Gesperrte CTA-Formulierungen

Diese Liste ist die Quelle für die Formulierungsverbote in `TEMPLATES.md` und für das
Sub-Kriterium „Engagement-Bait-Freiheit" in `SCORING.md`. Bis v2.4.0 führten die drei Stellen
drei verschieden lange Listen: SKILL.md kannte zwei Formulierungen, SCORING.md und die
Algorithmus-Regeln in TEMPLATES.md je drei, die Liste der verbotenen Wörter in TEMPLATES.md
eine vierte Variante. `tests/run_eval.py` hält die Stellen seit v2.5.0 gegen diese Tabelle.

| Formulierung | Warum sie fällt |
|--------------|-----------------|
| What do you think? | Fragt nach einer Reaktion, nicht nach einer Antwort. Wer sie stellt, hat keinen Adressaten im Kopf. |
| Agree? | Verlangt Zustimmung als Reflex und macht Widerspruch zur Mühe. |
| Thoughts? | Dieselbe Frage in kürzer, ohne Gegenstand, auf den sie sich bezieht. |
| Tag someone | Rekrutiert Leser als Verteiler, statt ihnen etwas zu geben, das sie weitergeben wollen. |

Ein CTA ist in Ordnung, wenn er eine Frage stellt, deren Antwort im Report als Erkenntnis
auftauchen könnte. Beispiele dafür stehen in `TEMPLATES.md` unter CTA-Varianten.

## Ethik-Abgleich vor der Übergabe

Phase 8 gibt Headline, About-Text, Content-Skill, Kommentar-Skill und Report frei. Vor der
Freigabe geht jedes dieser fünf Artefakte einmal gegen diese Tabelle:

| Artefakt | Geprüft gegen | Konkret |
|----------|---------------|---------|
| Headline | Regel 4 | Jede genannte Rolle, jeder Titel, jede Zahl ist vom Kunden belegt |
| About-Text | Regeln 4, 7 | Belege wie oben, dazu: der Kunde hat den Text gelesen und fachlich bestätigt |
| Content-Skill | Regel 1 | Keine der gesperrten CTA-Formulierungen, kein Hook, der eine Zahl erfindet |
| Kommentar-Skill | Regeln 2, 5, 6 | Ziel-Accounts sind öffentlich sichtbar, keine Absprache, keine Automatisierung |
| Report | Regeln 3, 4, 6 | Keine gekaufte Kennzahl, keine unbelegte Behauptung, Fremdprofile nur im Rahmen von Anlass |

Findet der Abgleich etwas, wird das Artefakt geändert und nicht der Abgleich.

## Was diese Seite nicht leistet

`tests/run_eval.py` prüft von alldem genau einen Ausschnitt: dass die vier gesperrten
CTA-Formulierungen oben in SKILL.md, `TEMPLATES.md` und `SCORING.md` vollständig ankommen, und
dass die Abgleich-Tabelle in SKILL.md Phase 8 verankert ist. Das sind Schreibweisen und
Verweise.

Nicht geprüft wird, und das ist der größere Teil:

- eine neu erfundene Bait-Formulierung, die in keiner Liste steht
- ob eine Angabe im Profil stimmt; der Skill kann einen Titel nicht verifizieren
- ob der Kunde den KI-Text tatsächlich gelesen hat
- ob im Gespräch nach dem Report jemand eine dieser Regeln übergeht
- ob ein Fremdprofil einen Anlass hatte; die Bedingung steht im Text, es gibt keinen Code, der
  eine Erhebung verweigern könnte, und kein Protokoll darüber

Ein Verstoß gegen diese Seite fällt also nicht automatisch auf. Sie ist eine Haltung, keine
Schranke.
