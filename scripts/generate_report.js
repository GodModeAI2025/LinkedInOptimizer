const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, LevelFormat, PageBreak, PageNumber, TabStopType, TabStopPosition,
} = require("docx");

// ── Farben & Layout ─────────────────────────────────────────────
const BLUE = "0A66C2", DARK = "1E293B", GREEN = "059669", YELLOW = "D97706", RED = "DC2626";
const GRAY = "6B7280", LIGHTBLUE = "DBEAFE", WHITE = "FFFFFF";
const TABLE_W = 9360;
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cm = { top: 60, bottom: 60, left: 100, right: 100 };

// ── Hilfsfunktionen ─────────────────────────────────────────────
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, bold: true, size: 32, font: "Arial", color: DARK })], spacing: { before: 360, after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 8 } } });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, bold: true, size: 26, font: "Arial", color: BLUE })], spacing: { before: 280, after: 140 } });
const h3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t, bold: true, size: 22, font: "Arial", color: DARK })], spacing: { before: 200, after: 100 } });
const p = (t, o = {}) => new Paragraph({ children: [new TextRun({ text: t, size: 21, font: "Arial", color: o.color || "333333", bold: o.bold, italics: o.italic })], spacing: { after: o.after || 120 }, alignment: o.align });
const richBullet = (runs, ref = "bullets") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs.map(r => new TextRun({ size: 21, font: "Arial", ...r })), spacing: { after: 60 } });
const bullet = (t, ref = "bullets") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: [new TextRun({ text: t, size: 21, font: "Arial" })], spacing: { after: 60 } });
const numItem = (b, t) => new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 60 }, children: [new TextRun({ text: b + " ", size: 21, font: "Arial", bold: true }), new TextRun({ text: t, size: 21, font: "Arial" })] });
const emptyLine = () => p("", { after: 60 });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });
const hCell = (t, w) => new TableCell({ borders, width: { size: w, type: WidthType.DXA }, shading: { fill: DARK, type: ShadingType.CLEAR }, margins: cm, children: [new Paragraph({ children: [new TextRun({ text: t, size: 20, font: "Arial", bold: true, color: WHITE })] })] });
const dCell = (t, w, o = {}) => new TableCell({ borders, width: { size: w, type: WidthType.DXA }, shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR } : undefined, margins: cm, verticalAlign: "center", children: [new Paragraph({ alignment: o.align || AlignmentType.LEFT, children: [new TextRun({ text: String(t), size: 20, font: "Arial", bold: o.bold, color: o.color || "333333" })] })] });
const scoreLabel = (s) => s >= 91 ? "Exzellent" : s >= 76 ? "Sehr gut" : s >= 61 ? "Gut" : s >= 41 ? "Durchschnitt" : "Schwach";
const scoreColor = (s) => s >= 76 ? GREEN : s >= 41 ? YELLOW : RED;

// ══════════════════════════════════════════════════════════════════
// KUNDENDATEN — NUR DIESEN BLOCK ANPASSEN.
// Alle Profil-, Scoring- und Textdaten stehen hier.
// Der Report-Body darunter ist generisch und referenziert diese Variablen.
// ══════════════════════════════════════════════════════════════════

const PROFILE = {
  name: "Max Mustermann",          // Vollständiger Name
  position: "Beispiel-Position",   // Aktuelle Rolle
  company: "Beispiel GmbH",        // Aktuelles Unternehmen
  location: "Musterstadt",         // Standort
  followers: 1000,                 // Follower-Anzahl (Zahl, nicht String)
  connections: 500,                // Connections (Zahl)
  profileUrl: "linkedin.com/in/beispiel",
  analysisDate: "TT.MM.JJJJ",
};

// Scoring: cat, raw (0-10), w, weighted (raw*w), max (w*10), pct, color, reason
const scoring = [
  { cat: "Headline",         raw: 5, w: 1.2, weighted: 6.0,  max: 12, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "About-Sektion",    raw: 5, w: 1.2, weighted: 6.0,  max: 12, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Banner",           raw: 5, w: 0.6, weighted: 3.0,  max: 6,  pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Content-Qualität", raw: 5, w: 1.5, weighted: 7.5,  max: 15, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Posting-Frequenz", raw: 5, w: 1.0, weighted: 5.0,  max: 10, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Engagement",       raw: 5, w: 1.5, weighted: 7.5,  max: 15, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Social Proof",     raw: 5, w: 1.0, weighted: 5.0,  max: 10, pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Netzwerk",         raw: 5, w: 0.8, weighted: 4.0,  max: 8,  pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Vollständigkeit",  raw: 5, w: 0.7, weighted: 3.5,  max: 7,  pct: 50, color: YELLOW, reason: "[Begründung]" },
  { cat: "Top Voice Ready",  raw: 5, w: 0.5, weighted: 2.5,  max: 5,  pct: 50, color: YELLOW, reason: "[Begründung]" },
];
const totalScore = scoring.reduce((s, d) => s + d.weighted, 0);

const posts = [
  { time: "[Zeitpunkt]", reactions: 0, comments: 0 },
];

const EXEC = {
  summary: "[Zusammenfassung mit Score, Bewertungsstufe, Kernaussage und Zeithorizont]",
  strengths: [
    { label: "[Stärke 1]:", text: "[Erklärung mit konkretem Befund]" },
    { label: "[Stärke 2]:", text: "[Erklärung mit konkretem Befund]" },
    { label: "[Stärke 3]:", text: "[Erklärung mit konkretem Befund]" },
  ],
  levers: [
    { label: "[Hebel 1]:", text: "[Erklärung + geschätzter Score-Impact]" },
    { label: "[Hebel 2]:", text: "[Erklärung + geschätzter Score-Impact]" },
    { label: "[Hebel 3]:", text: "[Erklärung + geschätzter Score-Impact]" },
  ],
  quickWins: [
    { bold: "[Quick Win 1]", text: "[Maßnahme + Auswirkung]" },
    { bold: "[Quick Win 2]", text: "[Maßnahme + Auswirkung]" },
    { bold: "[Quick Win 3]", text: "[Maßnahme + Auswirkung]" },
  ],
};

const HEADLINE = {
  current: "[Aktuelle Headline hier einfügen]",
  length: 0,
  first60: "[Erste 60 Zeichen]",
  positives: "[Was funktioniert]",
  issues: ["[Problem 1]", "[Problem 2]", "[Problem 3]"],
  variants: [
    { name: "Variante A (empfohlen)", text: "[Text]", chars: 0, first60: "[...]", explanation: "[Begründung]" },
    { name: "Variante B", text: "[Text]", chars: 0, first60: "[...]", explanation: "[Begründung]" },
    { name: "Variante C", text: "[Text]", chars: 0, first60: "[...]", explanation: "[Begründung]" },
  ],
};

const ABOUT = {
  hookPreview: "[Erste 270 Zeichen des About]",
  hookAssessment: "[Bewertung des Hooks]",
  issues: [
    { label: "[Befund 1]:", text: "[Detail + Vorschlag]" },
    { label: "[Befund 2]:", text: "[Detail + Vorschlag]" },
  ],
  currentCTA: "[Aktueller CTA]",
  ctaAssessment: "[Bewertung]",
  ctaSuggestion: "[Optimierter CTA]",
  hashtagStatus: "[Anzahl + Empfehlung]",
  charStatus: "[X von 2.600 Zeichen]",
};

// [Nr, Element, Status, Maßnahme, Farbe]
const AUDIT = [
  ["1",  "Professionelles Profilbild",  "[Status]", "[Maßnahme]", GREEN],
  ["2",  "Custom Banner",               "[Status]", "[Maßnahme]", YELLOW],
  ["3",  "Headline optimiert",          "[Status]", "[Maßnahme]", YELLOW],
  ["4",  "About-Sektion",               "[Status]", "[Maßnahme]", YELLOW],
  ["5",  "Featured Section",            "[Status]", "[Maßnahme]", RED],
  ["6",  "Creator Mode",                "[Status]", "[Maßnahme]", YELLOW],
  ["7",  "Custom CTA-Button",           "[Status]", "[Maßnahme]", YELLOW],
  ["8",  "Custom URL",                  "[Status]", "[Maßnahme]", GREEN],
  ["9",  "Eigener Newsletter",          "[Status]", "[Maßnahme]", RED],
  ["10", "Empfehlungen >= 5",           "[Status]", "[Maßnahme]", RED],
  ["11", "Skills",                      "[Status]", "[Maßnahme]", GREEN],
  ["12", "Positionen beschrieben",      "[Status]", "[Maßnahme]", GREEN],
  ["13", "Zertifikate/Publikationen",   "[Status]", "[Maßnahme]", RED],
  ["14", "Collaborative Articles",      "[Status]", "[Maßnahme]", RED],
  ["15", "Video-Content",               "[Status]", "[Maßnahme]", RED],
  ["16", "Ausbildung",                  "[Status]", "[Maßnahme]", GREEN],
  ["17", "Sprachen",                    "[Status]", "[Maßnahme]", GREEN],
];
const AUDIT_SUMMARY = "[X von 17 Elementen — Zusammenfassung]";

const ROADMAP = {
  week12: ["[Maßnahme]"],
  week34: ["[Maßnahme]"],
  month23: ["[Maßnahme]"],
  month46: ["[Maßnahme]"],
  expectedScore: "[Score-Prognose + Begründung]",
};

const LIMITS = [
  { label: "About-Text:", text: "[Erfassungsstatus]" },
  { label: "Impressions:", text: "Nicht öffentlich sichtbar. Engagement-Rate auf Basis der Follower-Zahl geschätzt." },
  { label: "SSI-Score:", text: "Nicht verfügbar (erfordert linkedin.com/sales/ssi)." },
  { label: "Kommentar-Aktivität:", text: "Häufigkeit bei Dritten nicht messbar." },
  { label: "Wettbewerbsanalyse:", text: "Phase 3 nicht durchgeführt (kein Kontext-Interview)." },
];

// ══════════════════════════════════════════════════════════════════
// REPORT-BODY — Generisch. Liest ausschließlich aus den Variablen.
// Keine Namen, Firmen oder profilspezifischen Texte im Code unten.
// ══════════════════════════════════════════════════════════════════

const SL = scoreLabel(totalScore);
const SC = scoreColor(totalScore);

const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, font: "Arial" }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial" }, paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, font: "Arial" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ] },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]},
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE, space: 6 } }, children: [ new TextRun({ text: "LinkedIn Profil-Analyse", size: 16, font: "Arial", color: GRAY }), new TextRun({ text: "\t" }), new TextRun({ text: "linkedin-profil-optimierung v2.2", size: 16, font: "Arial", color: GRAY }) ], tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 2, color: "CCCCCC", space: 6 } }, alignment: AlignmentType.CENTER, children: [ new TextRun({ text: "Seite ", size: 16, font: "Arial", color: GRAY }), new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Arial", color: GRAY }) ] })] }) },
    children: [
      // ═══ TITELSEITE ═══
      emptyLine(), emptyLine(), emptyLine(),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "LINKEDIN PROFIL-ANALYSE", size: 42, bold: true, font: "Arial", color: BLUE })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE, space: 12 } }, children: [new TextRun({ text: PROFILE.name, size: 56, bold: true, font: "Arial", color: DARK })] }),
      emptyLine(),
      p(`${PROFILE.position} @ ${PROFILE.company}`, { align: AlignmentType.CENTER, color: GRAY }),
      p(PROFILE.location, { align: AlignmentType.CENTER, color: GRAY, after: 300 }),
      new Table({ width: { size: 5000, type: WidthType.DXA }, columnWidths: [5000], alignment: AlignmentType.CENTER, rows: [new TableRow({ children: [new TableCell({ borders: { top: { style: BorderStyle.SINGLE, size: 4, color: BLUE }, bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE }, left: { style: BorderStyle.SINGLE, size: 4, color: BLUE }, right: { style: BorderStyle.SINGLE, size: 4, color: BLUE } }, width: { size: 5000, type: WidthType.DXA }, margins: { top: 200, bottom: 200, left: 200, right: 200 }, children: [
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "GESAMTSCORE", size: 20, font: "Arial", color: GRAY, bold: true })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: `${totalScore.toFixed(1)} / 100`, size: 52, font: "Arial", color: BLUE, bold: true })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `Bewertung: ${SL}`, size: 22, font: "Arial", color: SC, bold: true })] }),
      ] })] })] }),
      emptyLine(), emptyLine(),
      p(`Profil-URL: ${PROFILE.profileUrl}`, { align: AlignmentType.CENTER, color: GRAY }),
      p(`Analyse-Datum: ${PROFILE.analysisDate}`, { align: AlignmentType.CENTER, color: GRAY }),
      p(`${PROFILE.followers.toLocaleString("de-DE")} Follower | ${PROFILE.connections}+ Kontakte`, { align: AlignmentType.CENTER, color: GRAY }),

      // ═══ 1. EXECUTIVE SUMMARY ═══
      pageBreak(), h1("1. Executive Summary"), p(EXEC.summary),
      h2("1.1 Top 3 Stärken"), ...EXEC.strengths.map(s => richBullet([{ text: s.label + " ", bold: true }, { text: s.text }])),
      h2("1.2 Top 3 Hebel"), ...EXEC.levers.map(l => richBullet([{ text: l.label + " ", bold: true }, { text: l.text }])),
      h2("1.3 Drei Quick Wins"), ...EXEC.quickWins.map(q => numItem(q.bold, q.text)),

      // ═══ 2. SCORING ═══
      pageBreak(), h1("2. Scoring-Details"),
      p("Das Scoring basiert auf einem gewichteten 10-Kategorien-System. Content-Qualität und Engagement erhalten mit je 15% die höchste Gewichtung, weil der LinkedIn-Algorithmus 2025/2026 Dwell Time und Comment Quality als zentrale Ranking-Signale nutzt."),
      emptyLine(),
      new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: [2600, 800, 900, 1100, 800, 800, 2360], rows: [
        new TableRow({ children: [hCell("Kategorie", 2600), hCell("Roh", 800), hCell("Gew.", 900), hCell("Punkte", 1100), hCell("Max", 800), hCell("%", 800), hCell("Bewertung", 2360)] }),
        ...scoring.map(s => new TableRow({ children: [
          dCell(s.cat, 2600, { bold: true }), dCell(`${s.raw}/10`, 800, { align: AlignmentType.CENTER }), dCell(`x${s.w}`, 900, { align: AlignmentType.CENTER, color: GRAY }),
          dCell(s.weighted.toFixed(1), 1100, { align: AlignmentType.CENTER, bold: true, color: s.color }), dCell(String(s.max), 800, { align: AlignmentType.CENTER, color: GRAY }),
          dCell(`${s.pct}%`, 800, { align: AlignmentType.CENTER, color: s.color, bold: true }), dCell(s.pct >= 70 ? "Gut" : s.pct >= 50 ? "Ausbaufähig" : "Kritisch", 2360, { color: s.color }),
        ] })),
        new TableRow({ children: [ dCell("GESAMT", 2600, { bold: true, fill: LIGHTBLUE }), dCell("", 800, { fill: LIGHTBLUE }), dCell("", 900, { fill: LIGHTBLUE }),
          dCell(totalScore.toFixed(1), 1100, { align: AlignmentType.CENTER, bold: true, color: BLUE, fill: LIGHTBLUE }), dCell("100", 800, { align: AlignmentType.CENTER, color: GRAY, fill: LIGHTBLUE }),
          dCell(`${Math.round(totalScore)}%`, 800, { align: AlignmentType.CENTER, bold: true, color: BLUE, fill: LIGHTBLUE }), dCell(SL, 2360, { bold: true, color: SC, fill: LIGHTBLUE }) ] }),
      ] }),
      emptyLine(), p("Spalte 'Roh' = ungewichteter Score (0-10). 'Gew.' = Multiplikator. 'Punkte' = Roh x Gew. Rot <40%, Gelb 40-69%, Grün ab 70%.", { color: GRAY }),

      // ═══ 3. DETAILANALYSE ═══
      pageBreak(), h1("3. Detailanalyse je Kategorie"),
      p("Jede Kategorie wird einzeln begründet. Die Bewertung stützt sich auf die Sub-Kriterien aus der Scoring-Matrix und die via Chrome erhobenen Profildaten."),
      ...scoring.flatMap((s, i) => [h2(`3.${i + 1} ${s.cat} — ${s.weighted.toFixed(1)}/${s.max} Punkte (${s.pct}%)`), p(s.reason)]),

      // ═══ 4. CONTENT ═══
      pageBreak(), h1("4. Content-Aktivität"),
      p(`Die letzten ${posts.length} Posts wurden über die LinkedIn Activity-Seite via Chrome erhoben. Impressions sind nicht öffentlich verfügbar.`),
      emptyLine(),
      new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: [1800, 1500, 2400, 1500, 2160], rows: [
        new TableRow({ children: [hCell("Nr.", 1800), hCell("Zeitpunkt", 1500), hCell("Reaktionen", 2400), hCell("Kommentare", 1500), hCell("Eng.-Rate", 2160)] }),
        ...posts.map((post, i) => { const er = ((post.reactions + post.comments) / PROFILE.followers * 100).toFixed(1); return new TableRow({ children: [
          dCell(`Post ${i + 1}`, 1800), dCell(post.time, 1500), dCell(String(post.reactions), 2400, { align: AlignmentType.CENTER, bold: true, color: post.reactions >= 50 ? GREEN : DARK }),
          dCell(String(post.comments), 1500, { align: AlignmentType.CENTER }), dCell(`~${er}%`, 2160, { align: AlignmentType.CENTER, color: parseFloat(er) > 5 ? GREEN : YELLOW }),
        ] }); }),
      ] }),
      emptyLine(), p(`Engagement-Rate geschätzt als (Reaktionen + Kommentare) / ${PROFILE.followers.toLocaleString("de-DE")} Follower. Plattform-Durchschnitt: 3,4%.`, { color: GRAY }),

      // ═══ 5. HEADLINE ═══
      pageBreak(), h1("5. Headline-Analyse & Vorschläge"),
      h2("5.1 Aktuelle Headline"), p(HEADLINE.current, { italic: true }),
      p(`Länge: ${HEADLINE.length} Zeichen (max. 220). Erste 60: '${HEADLINE.first60}'`, { color: GRAY }),
      emptyLine(), h3("Bewertung"),
      richBullet([{ text: "Positiv: ", bold: true, color: GREEN }, { text: HEADLINE.positives }]),
      ...HEADLINE.issues.map(issue => richBullet([{ text: "Kritisch: ", bold: true, color: RED }, { text: issue }])),
      h2("5.2 Optimierungsvorschläge"),
      ...HEADLINE.variants.flatMap(v => [h3(v.name), p(v.text, { italic: true }), p(`${v.chars} Zeichen. Erste 60: '${v.first60}' — ${v.explanation}`, { color: GRAY })]),

      // ═══ 6. ABOUT ═══
      pageBreak(), h1("6. About-Sektion-Analyse"),
      h2("6.1 Erste 270 Zeichen"), p(ABOUT.hookPreview, { italic: true }), p(ABOUT.hookAssessment, { color: GRAY }),
      h2("6.2 Befunde"), ...ABOUT.issues.map(i => richBullet([{ text: i.label + " ", bold: true, color: RED }, { text: i.text }])),
      h2("6.3 CTA-Bewertung"), p(ABOUT.currentCTA, { italic: true }), p(ABOUT.ctaAssessment), p(`Optimierungsvorschlag: ${ABOUT.ctaSuggestion}`),
      h2("6.4 Fehlende Elemente"), richBullet([{ text: "Hashtags: ", bold: true }, { text: ABOUT.hashtagStatus }]), richBullet([{ text: "Zeichenauslastung: ", bold: true }, { text: ABOUT.charStatus }]),

      // ═══ 7. AUDIT ═══
      pageBreak(), h1("7. Profil-Audit"),
      p("17 Elemente geprüft. Fehlende Elemente sind die schnellsten Hebel zur Score-Verbesserung."),
      emptyLine(),
      new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: [500, 3200, 1200, 4460], rows: [
        new TableRow({ children: [hCell("#", 500), hCell("Element", 3200), hCell("Status", 1200), hCell("Maßnahme", 4460)] }),
        ...AUDIT.map(([nr, el, st, ma, co]) => new TableRow({ children: [dCell(nr, 500, { align: AlignmentType.CENTER }), dCell(el, 3200), dCell(st, 1200, { color: co, bold: true }), dCell(ma, 4460)] })),
      ] }),
      emptyLine(), p(AUDIT_SUMMARY),

      // ═══ 8. ROADMAP ═══
      pageBreak(), h1("8. Empfohlene Roadmap"),
      p("Maßnahmen priorisiert: Quick Wins zuerst, dann Skalierung, dann Authority Building."),
      h2("Woche 1-2: Quick Wins"), ...ROADMAP.week12.map(m => bullet(m)),
      h2("Woche 3-4: Content-Start"), ...ROADMAP.week34.map(m => bullet(m)),
      h2("Monat 2-3: Skalierung"), ...ROADMAP.month23.map(m => bullet(m)),
      h2("Monat 4-6: Authority Building"), ...ROADMAP.month46.map(m => bullet(m)),
      h2("Erwarteter Score nach 3 Monaten"), p(ROADMAP.expectedScore),

      // ═══ 9. METHODIK ═══
      pageBreak(), h1("9. Methodik & Einschränkungen"),
      h2("9.1 Datenerhebung"), p(`Daten erhoben am ${PROFILE.analysisDate} via Chrome-Browser (Hauptprofil + Activity-Seite). Extraktion per JavaScript im Browser-Kontext.`),
      h2("9.2 Scoring"), p("Gewichtete 10-Kategorien-Matrix (SCORING.md v2.0). Gewichtung priorisiert algorithmische Reichweite vor statischen Profil-Elementen."),
      h2("9.3 Einschränkungen"), ...LIMITS.map(l => richBullet([{ text: l.label + " ", bold: true }, { text: l.text }])),
    ],
  }],
});

const out = `/mnt/user-data/outputs/${PROFILE.name.replace(/\s+/g, "-")}-LinkedIn-Analyse.docx`;
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(out, buf); console.log(`Done: ${out}`); });
