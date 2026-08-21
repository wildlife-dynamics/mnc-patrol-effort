"""
Generate the MNC Patrol Effort User Guide as a PDF using ReportLab.
Run with: python3 generate_user_guide.py
Output: assets/MNC_Patrol_Effort_User_Guide.pdf
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, ListFlowable, ListItem,
)
from datetime import date

OUTPUT_FILE = Path(__file__).parent / "assets" / "MNC_Patrol_Effort_User_Guide.pdf"

# ── Colour palette (matches docs/index.html and the Technical Guide) ───────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
STEP     = _style("StepItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, leftIndent=14, firstLineIndent=-14, bulletIndent=0)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code_block(text):    return Paragraph(text, CODE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t

def numbered_steps(items):
    return ListFlowable(
        [ListItem(Paragraph(text, STEP), leftIndent=14) for text in items],
        bulletType="1", start=1, leftIndent=14, bulletFontSize=9,
        bulletColor=GREEN_MID,
    )


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Patrol Effort — User Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Patrol Effort", TITLE),
    p("User Guide", SUBTITLE),
    sp(4),
    p("Configuring and running the workflow that turns EarthRanger patrol data "
      "into trajectory maps, effort summaries, and a coverage dashboard for "
      "Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_patrol_effort</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Overview"),
    p("This guide walks you through configuring and running the MNC Patrol Effort "
      "workflow, which processes patrol events and observations from EarthRanger "
      "to produce trajectory maps, patrol effort summaries, a patrol coverage "
      "analysis, and a results dashboard for Mara North Conservancy."),
    sp(4),
    p("The workflow delivers, for each run:"),
    bullet("<b>Events summary</b> — total events recorded by date and by type, with a line chart (HTML + PNG)"),
    bullet("<b>Patrol purpose summary</b> — patrol count grouped by patrol purpose (CSV + table)"),
    bullet("<b>Patrol relocations</b> — full observation dataset as a GeoParquet file"),
    bullet("<b>Foot patrol report</b> — effort summary table (CSV) and coverage map (HTML + PNG)"),
    bullet("<b>Vehicle patrol report</b> — effort summary table (CSV) and coverage map (HTML + PNG)"),
    bullet("<b>Motorbike patrol report</b> — effort summary table (CSV) and coverage map (HTML + PNG)"),
    bullet("<b>Combined trajectories</b> — merged trajectory dataset (GeoParquet)"),
    bullet("<b>Overall patrol efforts</b> — per-ranger summary of patrols, distance, and duration (CSV + table)"),
    bullet("<b>Patrol coverage map</b> — 1 000 m grid-cell visit density map (HTML + PNG) with conservancy occupancy percentage (CSV + table)"),
    bullet("<b>Results dashboard</b> — the four coverage maps, the events chart, and the three summary tables assembled into a single dashboard view"),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PREREQUISITES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Prerequisites"),
    p("Before running the workflow, ensure you have:"),
    bullet("Access to an <b>EarthRanger</b> instance with <font face='Courier'>patrol_info</font> events and associated patrol observations recorded for the analysis period"),
    bullet("Network access to <b>Dropbox</b>, so the workflow can download the MNC conservancy boundary and parcels files at runtime"),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# STEP-BY-STEP CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Step-by-Step Configuration"),

    h2("Step 1 — Add the Workflow Template"),
    p("In the workflow runner, go to <b>Workflow Templates</b> and click "
      "<b>Add Workflow Template</b>. Paste the GitHub repository URL into the "
      "<b>Github Link</b> field, then click <b>Add Template</b>."),
    code_block("https://github.com/wildlife-dynamics/mnc-patrol-effort.git"),
    sp(6),

    h2("Step 2 — Configure the EarthRanger Connection"),
    p("Navigate to <b>Data Sources</b> and click <b>Connect</b>, then select "
      "<b>EarthRanger</b>. Fill in the connection form:"),
    make_table(
        [["Field", "Description"],
         ["Data Source Name", "A label to identify this connection (e.g. Mara North Conservancy)"],
         ["EarthRanger URL", "Your instance URL (e.g. your-site.pamdas.org)"],
         ["EarthRanger Username", "Your EarthRanger username"],
         ["EarthRanger Password", "Your EarthRanger password"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    note("Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs."),
    p("Click <b>Connect</b> to save."),
    sp(6),

    h2("Step 3 — Select the Workflow"),
    p("After the template is added, it appears in the <b>Workflow Templates</b> "
      "list as <b>mnc-patrol-effort</b>. Click the card to open the workflow "
      "configuration form."),
    sp(6),

    h2("Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection"),
    p("The configuration form has three sections on a single page."),
    h3("Set workflow details"),
    make_table(
        [["Field", "Description"],
         ["Workflow Name", "A short name to identify this run"],
         ["Workflow Description", "Optional notes (e.g. reporting month or site)"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    h3("Time range"),
    make_table(
        [["Field", "Description"],
         ["Timezone", "Select the local timezone (e.g. Africa/Nairobi UTC+03:00)"],
         ["Since", "Start date and time — all events and patrol data from this point are fetched"],
         ["Until", "End date and time of the analysis window"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    h3("Connect to ER"),
    p("Select the EarthRanger data source configured in Step 2 from the "
      "<b>Data Source</b> dropdown (e.g. Mara North Conservancy)."),
    p("Once all three sections are filled, click <b>Submit</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# RUNNING THE WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Running the Workflow"),
    p("Once submitted, the runner will:"),
    numbered_steps([
        "Download the MNC community conservancy boundary and parcels GeoPackage files from Dropbox; "
        "repair invalid geometries on the conservancy boundary; filter it down to the "
        "<font face='Courier'>Conservancy</font> grazing zone (used later as the coverage AOI) and to "
        "<font face='Courier'>Mara North Conservancy</font> (used for the map extent); build styled map "
        "layers for the conservancy boundary and parcels.",

        "Fetch all events from EarthRanger; extract the date from each timestamp; add a temporal index; "
        "exclude <font face='Courier'>distancecountwildlife_rep</font>, "
        "<font face='Courier'>distancecountpatrol_rep</font>, and <font face='Courier'>airstrip_operations</font> "
        "events; summarise the remainder by date and by type; draw a daily events line chart; save as "
        "<font face='Courier'>total_events_recorded_by_date.csv</font>, "
        "<font face='Courier'>total_events_recorded_by_type.csv</font>, and "
        "<font face='Courier'>total_events_recorded.html</font>/<font face='Courier'>.png</font>.",

        "Filter <font face='Courier'>patrol_info</font> events; flatten event details; save as "
        "<font face='Courier'>patrol_events.csv</font>; rename fields (patrol_id, participants, "
        "patrol_purpose, transport_type); summarise patrol count by patrol purpose; save as "
        "<font face='Courier'>patrol_purpose_summary.csv</font>.",

        "Drop records with no patrol ID; fill missing transport type with Undefined; explode the "
        "patrol_id column; fetch patrol records and patrol observations from EarthRanger; merge them with "
        "the patrol info; explode the participants column; process the result into relocations (filtering "
        "out sentinel coordinates); save as <font face='Courier'>patrol_relocations.geoparquet</font>.",

        "Split relocations into three transport-type branches — Foot, Vehicle, and Motorbike — and "
        "convert each to trajectories using type-appropriate segment filters (foot patrols use a tighter "
        "speed/distance envelope than vehicle and motorbike).",

        "For each patrol type: rename trajectory columns; summarise effort metrics (patrol count, "
        "distance km, duration hrs, average speed) by patrol_type_value; save effort CSV.",

        "For each patrol type, and again for the combined dataset: build a 1 000 m patrol coverage grid "
        "over the conservancy boundary; classify visit counts into 5 equal-interval bins; apply the "
        "RdYlGn colormap; draw the coverage map; save as HTML, convert to PNG, and wrap it in a map widget.",

        "Concatenate the foot, vehicle, and motorbike trajectories; summarise per-ranger effort (patrol "
        "count, distance, duration) from the combined dataset; fill missing participant names with "
        "Undefined; save as <font face='Courier'>overall_patrol_efforts.csv</font>.",

        "Reproject the conservancy boundary and compute what percentage of it is covered by the overall "
        "patrol coverage grid; save as <font face='Courier'>patrol_coverage.csv</font>.",

        "Render the events chart, the patrol purpose summary, the overall patrol efforts, and the "
        "conservancy occupancy as table/chart widgets, and assemble all four maps, the chart, and the "
        "three tables into a single results dashboard.",

        "Save all outputs to the directory specified by "
        "<font face='Courier'>ECOSCOPE_WORKFLOWS_RESULTS</font>.",
    ]),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Output Files"),
    p("All outputs are written to <font face='Courier'>$ECOSCOPE_WORKFLOWS_RESULTS/</font>."),

    h2("Events Summary"),
    make_table(
        [["File", "Description"],
         ["total_events_recorded_by_date.csv", "Daily event counts (all types combined)"],
         ["total_events_recorded_by_type.csv", "Daily event counts broken down by event type"],
         ["total_events_recorded.html / .png", "Line chart of daily event counts"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Patrol Purpose"),
    make_table(
        [["File", "Description"],
         ["patrol_events.csv", "Flattened patrol_info event details"],
         ["patrol_purpose_summary.csv", "Patrol count by patrol purpose"],
         ["patrol_purpose_summary_table.html", "Rendered HTML table backing the dashboard widget"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Relocations"),
    make_table(
        [["File", "Description"],
         ["patrol_relocations.geoparquet", "Full patrol observation dataset with patrol metadata"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Foot Patrols"),
    make_table(
        [["File", "Description"],
         ["foot_patrol_efforts.csv", "Patrol count, distance, duration, and average speed by patrol type"],
         ["foot_patrol_map.html / .png", "Foot patrol coverage grid map"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Vehicle Patrols"),
    make_table(
        [["File", "Description"],
         ["vehicle_patrol_efforts.csv", "Patrol count, distance, duration, and average speed by patrol type"],
         ["vehicle_patrol_map.html / .png", "Vehicle patrol coverage grid map"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Motorbike Patrols"),
    make_table(
        [["File", "Description"],
         ["motorbike_patrol_efforts.csv", "Patrol count, distance, duration, and average speed by patrol type"],
         ["motor_patrol_map.html / .png", "Motorbike patrol coverage grid map"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Combined Trajectories and Overall Effort"),
    make_table(
        [["File", "Description"],
         ["patrol_trajectories.geoparquet", "Reprojected overall patrol coverage grid (foot + vehicle + motorbike combined)"],
         ["overall_patrol_efforts.csv", "Per-ranger summary of total patrols, distance km, and duration hrs"],
         ["overall_patrol_efforts_table.html", "Rendered HTML table backing the dashboard widget"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),

    h2("Patrol Coverage"),
    make_table(
        [["File", "Description"],
         ["overall_patrol_map.html / .png", "1 000 m grid-cell visit density map, all patrol types combined"],
         ["patrol_coverage.csv", "Patrol occupancy percentage per conservancy region"],
         ["patrol_coverage_table.html", "Rendered HTML table backing the dashboard widget"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Dashboard"),
    p("The final dashboard step assembles eight widgets, in order: the foot, "
      "vehicle, motorbike, and overall patrol coverage maps; the total events "
      "chart; and the patrol purpose, overall patrol efforts, and conservancy "
      "occupancy tables."),
    make_table(
        [["Widget", "Source"],
         ["Foot Patrol Coverage Map", "foot_patrol_map.html"],
         ["Vehicle Patrol Coverage Map", "vehicle_patrol_map.html"],
         ["Motorbike Patrol Coverage Map", "motor_patrol_map.html"],
         ["Overall Patrol Coverage Map", "overall_patrol_map.html"],
         ["Total Events Recorded", "total_events_recorded.html"],
         ["Patrol Purpose Summary", "patrol_purpose_summary_table.html"],
         ["Overall Patrol Efforts", "overall_patrol_efforts_table.html"],
         ["Conservancy Patrol Occupancy", "patrol_coverage_table.html"]],
        col_widths=[7*cm, W-7*cm],
    ),
    sp(4),
    note("Each table widget is sortable and filterable in place; downloading directly from the widget is disabled — use the corresponding CSV output file for that."),
]

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Wrote {OUTPUT_FILE}")
