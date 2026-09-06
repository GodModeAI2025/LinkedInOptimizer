## Phase 5: Banner-Erstellung

Lies `references/BANNER.md` für die vollständige technische Anleitung. Nutze `scripts/create_banner.py` zur Erstellung.

Kritische Regeln im Überblick:
- Format: 1584×396px, PNG, sRGB
- Universell sichere Zone: x=520 bis x=1200, y=30 bis y=350
- Texte als EINEN Block zusammenhalten, nicht über volle Breite verteilen
- Dunkler Hintergrund + weiße Schrift für maximalen Kontrast
- Mindestschriftgrößen: Titel ≥48px, Untertitel ≥22px, Rolle ≥18px, Tags ≥16px

`scripts/create_banner.py` braucht Pillow ab 10.1. Fehlt es, endet der Aufruf mit `ModuleNotFoundError: No module named 'PIL'`. Installiere die Abhängigkeit vorher mit `pip install -r requirements.txt` im Skill-Verzeichnis, also dort, wo diese SKILL.md und requirements.txt nebeneinander liegen.

Banner erstellen:
```bash
python scripts/create_banner.py \
  --output banner.png \
  --title1 "Zeile 1" --title2 "Zeile 2" \
  --subtitle "Untertitel" \
  --role "Position @ Unternehmen" \
  --tags "#GenAI  #EnterpriseAI" \
  --strict
```

`--strict` gehört in jeden Aufruf: Ohne die Option meldet das Skript Safe-Zone-Verletzungen nur als Warnung und endet trotzdem mit Exitcode 0, mit der Option endet es mit 1. Ein eigenes Hintergrund-Bild kommt optional über `--background <bild.png>` dazu; fehlt die Option oder der Pfad, entsteht ein Gradient-Hintergrund.

Fehlt NotoSans, greift das Skript auf DejaVuSans zurück. Findet es gar keinen Font mit anwendbarer Größenangabe, sind die gemessenen Textbreiten wertlos; dieser Fall zählt selbst als Verletzung und beendet `--strict` mit 1, statt ein ungeprüftes Banner durchzulassen.

---
