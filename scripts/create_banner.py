# -*- coding: utf-8 -*-
"""LinkedIn Banner Generator v2.0 mit Safe-Zone-Validierung.

Verwendung:
    python scripts/create_banner.py \
        --output banner.png \
        --title1 "Zeile 1" \
        --title2 "Zeile 2" \
        --subtitle "Untertitel" \
        --role "Position @ Unternehmen" \
        --tags "#GenAI  #EnterpriseAI" \
        [--background background.png] \
        [--book cover.png] \
        [--accent 0,200,255] \
        [--strict]

Ohne --background wird ein Gradient-Hintergrund erzeugt.
Mit --strict endet der Aufruf bei Safe-Zone-Verletzungen mit Exitcode 1.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import argparse
import sys


def find_font(name, size):
    """Suche Font mit Fallback auf DejaVuSans."""
    font_dirs = [
        "/usr/share/fonts/truetype/noto/",
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/truetype/",
    ]
    fallback_map = {
        "NotoSans-Bold.ttf": "DejaVuSans-Bold.ttf",
        "NotoSans-Regular.ttf": "DejaVuSans.ttf",
        "NotoSans-Light.ttf": "DejaVuSans.ttf",
    }
    for d in font_dirs:
        path = os.path.join(d, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    # Fallback
    fallback = fallback_map.get(name, "DejaVuSans.ttf")
    for d in font_dirs:
        path = os.path.join(d, fallback)
        if os.path.exists(path):
            print(f"⚠️  Font {name} nicht gefunden, Fallback: {fallback}")
            return ImageFont.truetype(path, size)
    # Letzter Fallback: PIL Default in der angeforderten Groesse
    print("⚠️  Kein passender Font gefunden, verwende PIL-Default")
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        # Pillow < 10.1 kennt den size-Parameter nicht; dann bleibt nur der
        # Bitmap-Font in fester Groesse, die Safe-Zone-Pruefung misst dann zu klein.
        print("⚠️  Pillow ohne size-Parameter, Safe-Zone-Pruefung ist ungenau")
        return ImageFont.load_default()


def create_linkedin_banner(
    background_path,
    output_path,
    title_line1,
    title_line2="",
    subtitle="",
    role="",
    tags="",
    book_cover_path=None,
    accent_color=(0, 200, 255),
    title_size=52,
    subtitle_size=24,
    role_size=20,
    tags_size=18,
):
    """
    Erstellt ein professionelles LinkedIn-Banner mit Safe-Zone-Validierung.

    Args:
        background_path: Pfad zum Hintergrund-Bild (None oder nicht vorhanden: Gradient-Fallback)
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
        Tuple (Pfad zum gespeicherten Banner, Liste der Safe-Zone-Verletzungen).
        Die Liste ist leer, wenn alle Elemente innerhalb der Safe Zone liegen.
    """

    # Validierung Schriftgrößen
    assert title_size >= 48, f"Titel zu klein: {title_size}px (min. 48)"
    assert subtitle_size >= 22, f"Untertitel zu klein: {subtitle_size}px (min. 22)"
    assert role_size >= 18, f"Rolle zu klein: {role_size}px (min. 18)"
    assert tags_size >= 16, f"Tags zu klein: {tags_size}px (min. 16)"

    violations = []

    # === SETUP ===
    SAFE_X_MIN = 520
    SAFE_X_MAX = 1200  # Universell sicher (auch mit Sidebar)
    SAFE_Y_MIN = 30
    SAFE_Y_MAX = 350
    TEXT_X = SAFE_X_MIN + 10  # 10px Padding

    # Basis laden oder Gradient-Fallback erzeugen
    if background_path and os.path.exists(background_path):
        base = Image.open(background_path).convert('RGBA')
        base = base.resize((1584, 396), Image.LANCZOS)
    else:
        print("⚠️  Kein Hintergrund-Bild, erzeuge Gradient-Fallback")
        base = Image.new('RGBA', (1584, 396), (10, 22, 40, 255))
        draw_bg = ImageDraw.Draw(base)
        for x in range(1584):
            progress = x / 1584
            r = int(10 + progress * 5)
            g = int(22 + progress * 10)
            b = int(40 + progress * 20)
            draw_bg.line([(x, 0), (x, 396)], fill=(r, g, b, 255))

    # Gradient-Overlay
    overlay = Image.new('RGBA', (1584, 396), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(400, 1584):
        progress = (x - 400) / (1584 - 400)
        alpha = min(200, int(progress * 210))
        od.line([(x, 0), (x, 396)], fill=(5, 10, 25, alpha))
    base = Image.alpha_composite(base, overlay)

    draw = ImageDraw.Draw(base)

    # Fonts mit Fallback
    f_title = find_font("NotoSans-Bold.ttf", title_size)
    f_sub = find_font("NotoSans-Regular.ttf", subtitle_size)
    f_role = find_font("NotoSans-Light.ttf", role_size)
    f_tags = find_font("NotoSans-Regular.ttf", tags_size)

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
                msg = f"Titel '{line}' ragt über Safe Zone (x={bbox[2]}, max={SAFE_X_MAX})"
                violations.append(msg)
                print(f"⚠️  WARNUNG: {msg}")
            y += title_size + 6

    # Akzentlinie
    y += 8
    draw.line([(TEXT_X, y), (TEXT_X + 200, y)], fill=accent_color, width=3)
    y += 14

    # Untertitel
    if subtitle:
        draw.text((TEXT_X, y), subtitle, fill=(180, 215, 245), font=f_sub)
        bbox = draw.textbbox((TEXT_X, y), subtitle, font=f_sub)
        if bbox[2] > SAFE_X_MAX:
            msg = f"Untertitel ragt über Safe Zone (x={bbox[2]}, max={SAFE_X_MAX})"
            violations.append(msg)
            print(f"⚠️  WARNUNG: {msg}")
        y += subtitle_size + 10

    # Rolle
    if role:
        draw.text((TEXT_X, y), role, fill=(150, 190, 220), font=f_role)
        bbox = draw.textbbox((TEXT_X, y), role, font=f_role)
        if bbox[2] > SAFE_X_MAX:
            msg = f"Rolle ragt über Safe Zone (x={bbox[2]}, max={SAFE_X_MAX})"
            violations.append(msg)
            print(f"⚠️  WARNUNG: {msg}")
        y += role_size + 12

    # Tags (KEIN farbiger Hintergrund – nur Textfarbe)
    if tags:
        draw.text((TEXT_X, y), tags, fill=accent_color, font=f_tags)
        bbox = draw.textbbox((TEXT_X, y), tags, font=f_tags)
        if bbox[2] > SAFE_X_MAX:
            msg = f"Tags ragen über Safe Zone (x={bbox[2]}, max={SAFE_X_MAX})"
            violations.append(msg)
            print(f"⚠️  WARNUNG: {msg}")
        y += tags_size + 8

    # Layout-Überlauf prüfen
    if y > SAFE_Y_MAX:
        msg = f"Content überläuft y-Safe-Zone (y={y}, max={SAFE_Y_MAX})"
        violations.append(msg)
        print(f"⚠️  WARNUNG: {msg}")

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
            msg = (f"Buchcover passt nicht in Safe Zone "
                   f"(x_end={bk_x + book_img.width}, max={SAFE_X_MAX}), wird weggelassen")
            violations.append(msg)
            print(f"⚠️  {msg}")

    # === SPEICHERN ===
    final = base.convert('RGB')
    final.save(output_path, quality=95)

    # Validierung
    assert final.size == (1584, 396), f"Falsche Größe: {final.size}"
    file_size = os.path.getsize(output_path)
    assert file_size < 8 * 1024 * 1024, f"Datei zu groß: {file_size / 1024 / 1024:.1f} MB (max. 8 MB)"

    print(f"✓ Banner gespeichert: {output_path}")
    print(f"  Größe: {final.size}, Datei: {file_size / 1024:.0f} KB")
    return output_path, violations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Banner Generator v2.0")
    parser.add_argument("--background", default=None,
                        help="Pfad zum Hintergrund-Bild (optional, sonst Gradient-Fallback)")
    parser.add_argument("--output", required=True, help="Ausgabepfad")
    parser.add_argument("--title1", required=True, help="Erste Titelzeile")
    parser.add_argument("--title2", default="", help="Zweite Titelzeile")
    parser.add_argument("--subtitle", default="", help="Untertitel")
    parser.add_argument("--role", default="", help="Position/Rolle")
    parser.add_argument("--tags", default="", help="Hashtags")
    parser.add_argument("--book", default=None, help="Pfad zum Buchcover")
    parser.add_argument("--accent", default="0,200,255", help="Akzent-Farbe als R,G,B")
    parser.add_argument("--strict", action="store_true",
                        help="Bei Safe-Zone-Verletzungen mit Exitcode 1 enden")
    args = parser.parse_args()

    accent = tuple(int(x) for x in args.accent.split(","))
    _, violations = create_linkedin_banner(
        background_path=args.background,
        output_path=args.output,
        title_line1=args.title1,
        title_line2=args.title2,
        subtitle=args.subtitle,
        role=args.role,
        tags=args.tags,
        book_cover_path=args.book,
        accent_color=accent,
    )

    if violations and args.strict:
        print(f"\n✗ {len(violations)} Safe-Zone-Verletzung(en):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        sys.exit(1)
