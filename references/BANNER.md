# LinkedIn Banner – Technische Anleitung v2.0

## Spezifikationen

```
Größe:          1584 × 396 Pixel (LinkedIn Standard)
Seitenverhältnis: 4:1
Format:         PNG (bevorzugt, verlustfrei) oder JPG (max. 8 MB)
Farbraum:       sRGB
Qualität:       PNG oder JPG bei 95%
DPI:            72 (Bildschirm-Standard)
```

---

## LinkedIn Safe Zones (KRITISCH)

LinkedIn legt UI-Elemente über das Banner. Diese Zonen MÜSSEN freigehalten werden.

### Viewport-Matrix

LinkedIn rendert das Banner je nach Kontext unterschiedlich breit:

| Viewport | Effektive Breite | Rechter Rand sicher bis | Hinweis |
|----------|-----------------|------------------------|---------|
| Desktop ohne Sidebar | ~1584px | x=1480 | Volle Breite, aber Edit-Button oben rechts |
| Desktop mit Sidebar | ~1250px | x=1350 | Sidebar komprimiert Banner horizontal |
| Tablet (Landscape) | ~1100px | x=1250 | Starke Kompression |
| Mobile (Portrait) | ~600px | x=900 | Nur Mitte sichtbar, Ränder abgeschnitten |

**Konsequenz**: Alle wichtigen Elemente müssen im **universell sicheren Bereich** liegen:

```
UNIVERSELL SICHER: x = 520 bis x = 1200
```

### Zone Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [NAVIGATION BAR – obere ~20px]                                          │
│                                                               [EDIT ●]  │
│                                                                          │
│  ┌───────────┐                                                           │
│  │           │                                                           │
│  │  PROFIL-  │      ┌──────────────────────────────────┐                │
│  │   BILD    │      │                                  │                │
│  │  (Kreis)  │      │    UNIVERSELL SICHERE ZONE       │                │
│  │           │      │    x: 520 – 1200                 │                │
│  │           │      │    y: 30 – 350                   │                │
│  └───────────┘      │                                  │                │
│                      └──────────────────────────────────┘                │
│                                                                          │
│ [UNTERER BEREICH – Mobile-Beschneidung + Info-Overlap]                  │
└──────────────────────────────────────────────────────────────────────────┘

GESPERRTE ZONEN:
├── x < 520:    Profilbild-Overlap (Kreis, ragt ins Banner)
├── x > 1350:   Edit-Button + Sidebar-Schnitt (Desktop mit Sidebar)
├── x > 1480:   Immer abgeschnitten auf schmaleren Viewports
├── y < 30:     LinkedIn Navigation Bar
└── y > 350:    Mobile-Beschneidung + Profilinfo-Overlap
```

### Goldene Regel

> **Platziere alle Text- und Bildelemente als EINEN zusammenhängenden Block zwischen x=520 und x=1200. Verteile NICHTS über die volle Breite.**

Begründung: Wenn LinkedIn den Viewport verkleinert (Sidebar, Tablet), werden weit auseinanderliegende Elemente zusammengeschoben oder abgeschnitten. Ein kompakter Block bleibt immer lesbar.

---

## Design-System

### Farbpalette

```
HINTERGRUND (dunkel = maximaler Kontrast für weiße Schrift):
┌────────────────────────────────────────────────────┐
│ Dark Navy:    #0a1628 bis #0d1f3c  (empfohlen)    │
│ Tech-Blue:    #071525 bis #0c2340                  │
│ Pure Dark:    #050a14 bis #0a0a1a                  │
│ Warm Dark:    #1a1a2e bis #16213e                  │
└────────────────────────────────────────────────────┘

TEXT:
┌────────────────────────────────────────────────────┐
│ Titel:         #FFFFFF (reines Weiß)               │
│ Untertitel:    #B4D7F5 (helles Blau-Weiß, 85%)    │
│ Rolle:         #96BEDC (gedämpftes Blau, 70%)      │
│ Tags:          #50BEFF (Akzent-Blau, 100% Sättigung)│
└────────────────────────────────────────────────────┘

AKZENTE:
┌────────────────────────────────────────────────────┐
│ Akzentlinie:   #00C8FF (Cyan)                      │
│ Badge-Blau:    #0A66C2 (LinkedIn-Blau)             │
│ Energie-Grün:  #00D68F (für Energie-Branche)       │
│ Warn-Orange:   #FF8C42 (für Hervorhebungen)        │
└────────────────────────────────────────────────────┘
```

### Typografie

```
FONT-HIERARCHIE (bei 1584×396px):
┌──────────────────────────────────────────────────────────────┐
│ Element      │ Font              │ Min-Größe │ Empfohlen     │
├──────────────┼───────────────────┼───────────┼───────────────┤
│ Titel        │ NotoSans-Bold     │ 48px      │ 52–56px       │
│ Untertitel   │ NotoSans-Regular  │ 22px      │ 24–28px       │
│ Rolle/Pos.   │ NotoSans-Light    │ 18px      │ 20–22px       │
│ Tags         │ NotoSans-Regular  │ 16px      │ 18–20px       │
│ Small Print  │ NotoSans-Light    │ 14px      │ Nicht empfohlen│
└──────────────┴───────────────────┴───────────┴───────────────┘

FAUSTREGEL: Wenn Text auf dem Banner kleiner als 16px ist,
wird er auf LinkedIn unleserlich. Im Zweifel: GRÖSSER.
```

### Zeichen pro Zeile (bei empfohlener Schriftgröße)

| Font-Größe | Max. Zeichen/Zeile (x=520 bis x=1200) |
|------------|---------------------------------------|
| 52px Bold | ~20–22 Zeichen |
| 48px Bold | ~22–25 Zeichen |
| 24px Regular | ~40–45 Zeichen |
| 20px Light | ~50–55 Zeichen |
| 18px Regular | ~55–60 Zeichen |

---

## Erstellungs-Workflow

### Schritt 1: KI-Hintergrund generieren

Generiere einen thematisch passenden Hintergrund per KI-Bildgenerator:

```
PROMPT-VORLAGEN JE BRANCHE:

Tech/KI:
"Dark navy digital background with subtle AI neural network nodes and
circuit patterns, futuristic but professional, no text, no people,
soft glowing cyan accents, 1584x396 banner format"

Energie/Energiewende:
"Dark blue gradient background with wind turbines and power grid silhouettes
connected by glowing neural network lines, tech meets energy transition,
no text, no people, professional, 1584x396 banner format"

Finance:
"Dark sophisticated background with subtle financial chart lines and
data visualization elements, professional navy-to-black gradient,
minimal geometric patterns, no text, 1584x396 banner format"

Consulting:
"Clean dark gradient background, navy to dark blue, minimal geometric
patterns, executive professional feel, subtle grid lines,
no text, no people, 1584x396 banner format"

Healthcare:
"Dark blue professional background with subtle DNA helix and medical
data visualization elements, clean and trustworthy feel,
no text, no people, 1584x396 banner format"
```

**Wichtig**: Hintergrund MUSS dunkel sein, damit weiße Schrift kontrastreich lesbar ist.

### Schritt 2: Gradient-Overlay für Text-Lesbarkeit

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Basis laden und skalieren
base = Image.open('background.png').convert('RGBA')
base = base.resize((1584, 396), Image.LANCZOS)

# Gradient-Overlay: Links transparent → rechts deckend (für Textbereich)
overlay = Image.new('RGBA', (1584, 396), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for x in range(400, 1584):
    progress = (x - 400) / (1584 - 400)
    alpha = min(200, int(progress * 210))
    od.line([(x, 0), (x, 396)], fill=(5, 10, 25, alpha))
base = Image.alpha_composite(base, overlay)
```

### Schritt 3: Text-Overlay

```python
draw = ImageDraw.Draw(base)

# Font-Pfade (System-Fonts)
FONT_DIR = "/usr/share/fonts/truetype/noto/"
f_title = ImageFont.truetype(f"{FONT_DIR}NotoSans-Bold.ttf", 52)
f_sub   = ImageFont.truetype(f"{FONT_DIR}NotoSans-Regular.ttf", 24)
f_role  = ImageFont.truetype(f"{FONT_DIR}NotoSans-Light.ttf", 20)
f_tags  = ImageFont.truetype(f"{FONT_DIR}NotoSans-Regular.ttf", 18)

# === TEXT-BLOCK (alles zwischen x=530 und x=1200) ===
text_x = 530  # 10px Abstand zur Safe-Zone-Grenze

# Titel (1–2 Zeilen, max. 22 Zeichen pro Zeile bei 52px)
y_title = 30
title_lines = ["Zeile 1 des Titels", "Zeile 2 des Titels"]
for i, line in enumerate(title_lines):
    y = y_title + i * 58  # Zeilenhöhe = Font-Größe + 6px
    # Schatten für bessere Lesbarkeit
    draw.text((text_x + 2, y + 2), line, fill=(0, 0, 0, 180), font=f_title)
    draw.text((text_x, y), line, fill=(255, 255, 255), font=f_title)

# Akzentlinie (Cyan, 200px breit, 3px hoch)
y_accent = y_title + len(title_lines) * 58 + 10
draw.line(
    [(text_x, y_accent), (text_x + 200, y_accent)],
    fill=(0, 200, 255), width=3
)

# Untertitel
y_sub = y_accent + 14
draw.text((text_x, y_sub), "Untertitel-Text hier", fill=(180, 215, 245), font=f_sub)

# Rolle / Position
y_role = y_sub + 34
draw.text((text_x, y_role), "Position @ Unternehmen", fill=(150, 190, 220), font=f_role)

# Tags (OHNE farbigen Hintergrund – nur Text in Akzent-Farbe)
y_tags = y_role + 32
tags_text = "#GenAI  #EnterpriseAI  #Energiewende  #Agents"
draw.text((text_x, y_tags), tags_text, fill=(80, 190, 255), font=f_tags)

# === SICHERHEITS-CHECK ===
# Prüfe, dass kein Element über x=1200 hinausragt
# WICHTIG: Jedes Element mit seiner eigenen Font prüfen!
check_elements = [
    (title_lines[0], f_title),
    ("Untertitel-Text hier", f_sub),
    (tags_text, f_tags),
]
for text, font in check_elements:
    bbox = draw.textbbox((text_x, 0), text, font=font)
    assert bbox[2] < 1200, f"WARNUNG: '{text}' ragt über Safe Zone hinaus (x={bbox[2]})"
```

### Schritt 4: Buch-Cover integrieren (optional)

```python
# === REGELN FÜR BUCH-INTEGRATION ===
# 1. Buch NICHT am rechten Rand → wird abgeschnitten
# 2. Buch NICHT neben dem Text horizontal → kollidiert bei Viewport-Änderung
# 3. BESTE POSITION: Innerhalb des Textblocks, vertikal integriert
# 4. Buch-Höhe: max. 60% der Bannerhöhe (237px)
# 5. IMMER im universell sicheren Bereich bleiben (x=520–1200)

if book_cover_path:
    cover = Image.open(book_cover_path).convert('RGBA')

    # Buch auf max. 60% Bannerhöhe skalieren
    book_h = int(396 * 0.60)  # = 237px
    book_scale = book_h / cover.height
    book_w = int(cover.width * book_scale)
    cover_small = cover.resize((book_w, book_h), Image.LANCZOS)

    # 3D-Spine-Effekt
    spine_w = max(6, int(book_w * 0.06))
    spine = Image.new('RGBA', (spine_w, book_h), (18, 18, 18, 255))

    # Shadow
    book_img = Image.new('RGBA', (spine_w + book_w + 12, book_h + 12), (0, 0, 0, 0))
    shadow = Image.new('RGBA', book_img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle(
        [6, 6, spine_w + book_w + 6, book_h + 6],
        fill=(0, 0, 0, 120)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=6))
    book_img = Image.alpha_composite(book_img, shadow)
    book_img.paste(spine, (0, 0), spine)
    book_img.paste(cover_small, (spine_w - 1, 0), cover_small)

    # Position: Neben Untertitel, aber INNERHALB Safe Zone
    sub_bbox = draw.textbbox((text_x, y_sub), "Untertitel-Text hier", font=f_sub)
    book_x = sub_bbox[2] + 25  # 25px Abstand nach Untertitel-Ende
    book_y = y_sub - 10

    # KRITISCHER CHECK: Bleibt alles innerhalb x=1200?
    if book_x + book_img.width < 1200:
        base.paste(book_img, (book_x, book_y), book_img)
    else:
        # Fallback: Buch unter den Text statt daneben
        book_x = text_x
        book_y = y_tags + 30
        if book_y + book_img.height < 370:  # y-Safe-Zone
            base.paste(book_img, (book_x, book_y), book_img)
        else:
            print("WARNUNG: Buch passt nicht in Safe Zone – weglassen")
```

### Schritt 5: Speichern und Validieren

```python
# Zu RGB konvertieren und speichern
final = base.convert('RGB')
final.save(output_path, quality=95)
print(f"Banner gespeichert: {output_path}")
print(f"Größe: {final.size}")  # Muss (1584, 396) sein

# Validierung
assert final.size == (1584, 396), "Falsche Größe!"
```

---

## Vollständiges Code-Template

```python
# -*- coding: utf-8 -*-
"""LinkedIn Banner Generator v2.0 mit Safe-Zone-Validierung."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_linkedin_banner(
    background_path: str,
    output_path: str,
    title_line1: str,
    title_line2: str = "",
    subtitle: str = "",
    role: str = "",
    tags: str = "",
    book_cover_path: str = None,
    accent_color: tuple = (0, 200, 255),
    title_size: int = 52,
    subtitle_size: int = 24,
    role_size: int = 20,
    tags_size: int = 18,
) -> str:
    """
    Erstellt ein professionelles LinkedIn-Banner mit Safe-Zone-Validierung.

    Args:
        background_path: Pfad zum Hintergrund-Bild
        output_path: Ausgabepfad für das Banner
        title_line1: Erste Titelzeile (max. ~22 Zeichen bei 52px)
        title_line2: Zweite Titelzeile (optional)
        subtitle: Untertitel (max. ~45 Zeichen bei 24px)
        role: Position/Rolle (max. ~55 Zeichen bei 20px)
        tags: Hashtags als String (max. ~55 Zeichen bei 18px)
        book_cover_path: Optional – Pfad zum Buchcover
        accent_color: RGB-Tuple für Akzentlinie
        title_size: Schriftgröße Titel (min. 48)
        subtitle_size: Schriftgröße Untertitel (min. 22)
        role_size: Schriftgröße Rolle (min. 18)
        tags_size: Schriftgröße Tags (min. 16)

    Returns:
        Pfad zum gespeicherten Banner
    """

    # Validierung Schriftgrößen
    assert title_size >= 48, f"Titel zu klein: {title_size}px (min. 48)"
    assert subtitle_size >= 22, f"Untertitel zu klein: {subtitle_size}px (min. 22)"
    assert role_size >= 18, f"Rolle zu klein: {role_size}px (min. 18)"
    assert tags_size >= 16, f"Tags zu klein: {tags_size}px (min. 16)"

    # === SETUP ===
    SAFE_X_MIN = 520
    SAFE_X_MAX = 1200  # Universell sicher (auch mit Sidebar)
    SAFE_Y_MIN = 30
    SAFE_Y_MAX = 350
    TEXT_X = SAFE_X_MIN + 10  # 10px Padding

    # Basis laden
    base = Image.open(background_path).convert('RGBA')
    base = base.resize((1584, 396), Image.LANCZOS)

    # Gradient-Overlay
    overlay = Image.new('RGBA', (1584, 396), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(400, 1584):
        progress = (x - 400) / (1584 - 400)
        alpha = min(200, int(progress * 210))
        od.line([(x, 0), (x, 396)], fill=(5, 10, 25, alpha))
    base = Image.alpha_composite(base, overlay)

    draw = ImageDraw.Draw(base)

    # Fonts
    FONT_DIR = "/usr/share/fonts/truetype/noto/"
    f_title = ImageFont.truetype(f"{FONT_DIR}NotoSans-Bold.ttf", title_size)
    f_sub = ImageFont.truetype(f"{FONT_DIR}NotoSans-Regular.ttf", subtitle_size)
    f_role = ImageFont.truetype(f"{FONT_DIR}NotoSans-Light.ttf", role_size)
    f_tags = ImageFont.truetype(f"{FONT_DIR}NotoSans-Regular.ttf", tags_size)

    # === LAYOUT ===
    y = SAFE_Y_MIN

    # Titel (mit Schatten)
    for line in [title_line1, title_line2]:
        if line:
            draw.text((TEXT_X + 2, y + 2), line, fill=(0, 0, 0), font=f_title)
            draw.text((TEXT_X, y), line, fill=(255, 255, 255), font=f_title)
            # Safe-Zone-Check
            bbox = draw.textbbox((TEXT_X, y), line, font=f_title)
            if bbox[2] > SAFE_X_MAX:
                print(f"⚠️  WARNUNG: Titel '{line}' ragt über Safe Zone (x={bbox[2]})")
            y += title_size + 6

    # Akzentlinie
    y += 8
    draw.line([(TEXT_X, y), (TEXT_X + 200, y)], fill=accent_color, width=3)
    y += 14

    # Untertitel
    if subtitle:
        draw.text((TEXT_X, y), subtitle, fill=(180, 215, 245), font=f_sub)
        y += subtitle_size + 10

    # Rolle
    if role:
        draw.text((TEXT_X, y), role, fill=(150, 190, 220), font=f_role)
        y += role_size + 12

    # Tags (KEIN farbiger Hintergrund – nur Textfarbe)
    if tags:
        draw.text((TEXT_X, y), tags, fill=accent_color, font=f_tags)
        y += tags_size + 8

    # Layout-Überlauf prüfen
    if y > SAFE_Y_MAX:
        print(f"⚠️  WARNUNG: Content überläuft y-Safe-Zone (y={y}, max={SAFE_Y_MAX})")

    # === BUCH-COVER (optional) ===
    if book_cover_path and os.path.exists(book_cover_path):
        cover = Image.open(book_cover_path).convert('RGBA')
        book_h = int(396 * 0.60)
        bk_s = book_h / cover.height
        book_w = int(cover.width * bk_s)
        cover_sm = cover.resize((book_w, book_h), Image.LANCZOS)

        # 3D Spine
        spine_w = max(6, int(book_w * 0.06))
        spine = Image.new('RGBA', (spine_w, book_h), (18, 18, 18, 255))

        # Shadow + Assembly
        book_img = Image.new('RGBA', (spine_w + book_w + 12, book_h + 12), (0, 0, 0, 0))
        shd = Image.new('RGBA', book_img.size, (0, 0, 0, 0))
        ImageDraw.Draw(shd).rectangle(
            [6, 6, spine_w + book_w + 6, book_h + 6],
            fill=(0, 0, 0, 120)
        )
        shd = shd.filter(ImageFilter.GaussianBlur(radius=6))
        book_img = Image.alpha_composite(book_img, shd)
        book_img.paste(spine, (0, 0), spine)
        book_img.paste(cover_sm, (spine_w - 1, 0), cover_sm)

        # Positionierung: Innerhalb Safe Zone
        if subtitle:
            sub_bbox = draw.textbbox((TEXT_X, 0), subtitle, font=f_sub)
            bk_x = sub_bbox[2] + 25
        else:
            bk_x = TEXT_X + 400
        bk_y = SAFE_Y_MIN + 20

        # Safety Check
        if bk_x + book_img.width < SAFE_X_MAX:
            base.paste(book_img, (bk_x, bk_y), book_img)
        else:
            print(f"⚠️  Buch passt nicht in Safe Zone (x_end={bk_x + book_img.width})")
            print("   → Buch wird weggelassen. Untertitel kürzen oder Buch-Integration überdenken.")

    # === SPEICHERN ===
    final = base.convert('RGB')
    final.save(output_path, quality=95)

    # Validierung
    assert final.size == (1584, 396), f"Falsche Größe: {final.size}"
    file_size = os.path.getsize(output_path)
    assert file_size < 8 * 1024 * 1024, f"Datei zu groß: {file_size / 1024 / 1024:.1f} MB (max. 8 MB)"

    print(f"✓ Banner gespeichert: {output_path}")
    print(f"  Größe: {final.size}, Datei: {file_size / 1024:.0f} KB")
    return output_path
```

---

## Häufige Fehler (aus Praxis gelernt)

| # | Fehler | Ursache | Lösung |
|---|--------|---------|--------|
| 1 | Profilbild verdeckt Text | Text zu weit links (x < 520) | Alle Elemente ab x=530 |
| 2 | Edit-Button verdeckt Element | Element zu weit rechts | Max. x=1200 für universelle Sicherheit |
| 3 | Text unleserlich auf LinkedIn | Schrift zu klein oder kein Kontrast | Min. 16px + dunkler Gradient-Overlay |
| 4 | Buch wird abgeschnitten | Am rechten Rand platziert | Buch im Textblock integrieren, nie am Rand |
| 5 | Layout bricht bei Sidebar | Elemente zu weit auseinander | Alles als EINEN Block halten (x=520–1200) |
| 6 | Titel-Zeile zu lang | Text passt nicht in Safe Zone | Max. ~22 Zeichen pro Titelzeile bei 52px |
| 7 | Buch + Text überlappen | Nebeneinander platziert | Buch NEBEN Untertitel nur wenn genug Platz, sonst weglassen |
| 8 | Tags mit farbigem Hintergrund | Rectangles als Tag-Badges | Tags als einfachen Text in Akzent-Farbe schreiben |
| 9 | Position ändert sich zwischen Versionen | Hardcoded Y-Werte | Dynamisches Layout: Y akkumulieren statt hardcoden |
| 10 | Mobile-Darstellung schlecht | Keine Viewport-Prüfung | Immer den universell sicheren Bereich (520–1200) nutzen |

---

## Accessibility-Checkliste

```
KONTRAST-CHECK:
□ Titel (Weiß #FFFFFF) auf Hintergrund: Kontrastratio ≥ 4.5:1 (WCAG AA)
□ Untertitel (#B4D7F5) auf Hintergrund: Kontrastratio ≥ 3:1
□ Tags (#50BEFF) auf Hintergrund: Kontrastratio ≥ 3:1
□ Text-Schatten vorhanden für zusätzlichen Kontrast

LESBARKEIT:
□ Keine Schrift kleiner als 16px
□ Zeilenabstand mindestens Fontgröße + 6px
□ Maximal 4 Textebenen (Titel, Untertitel, Rolle, Tags)
□ Text linksbündig (nicht zentriert – besser lesbar)
□ Keine Text-Rotation oder Kursiv-Schrift

FARB-KONTRAST BERECHNEN (Python):
```python
def contrast_ratio(color1, color2):
    """Berechnet WCAG-Kontrastratio zwischen zwei RGB-Farben."""
    def luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    l1 = luminance(color1)
    l2 = luminance(color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

# Beispiel: Weiß auf Dark Navy
print(contrast_ratio((255, 255, 255), (10, 22, 40)))  # ≈ 16.8:1 (exzellent)
```

---

## Branchen-spezifische Banner-Varianten

| Branche | Hintergrund-Stil | Akzent-Farbe | Elemente |
|---------|-----------------|-------------|----------|
| Tech/KI | Neural Networks, Circuit Patterns | Cyan #00C8FF | Code-Elemente, Nodes |
| Energie | Windräder, Power Grid Silhouetten | Grün #00D68F | Turbinen, Leitungen |
| Finance | Chart-Lines, Data-Viz-Elemente | Gold #FFD700 | Graphen, Zahlen |
| Consulting | Geometrische Muster, Clean Gradient | Blau #0A66C2 | Minimal, Executive |
| Healthcare | DNA-Helix, Medical Data | Türkis #00B4D8 | Moleküle, Clean |
| Automotive | Technische Blueprints | Orange #FF8C42 | Fahrzeug-Silhouetten |
| Legal | Klassische Linien, Columns | Dunkelblau #1B3A5C | Säulen, Waage |
