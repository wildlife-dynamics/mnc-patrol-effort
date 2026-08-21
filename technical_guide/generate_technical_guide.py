"""
Generate the MNC Patrol Effort Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_patrol_effort_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_patrol_effort_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
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


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Patrol Effort — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
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
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Patrol trajectory analysis, effort summaries, coverage mapping, and "
      "dashboard reporting for Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_patrol_effort</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_patrol_effort</b> workflow fetches all events and linked "
      "patrol observations from EarthRanger for a specified time window. It "
      "converts patrol observations into relocations and trajectories, "
      "splits them by transport type (foot, vehicle, motorbike), and "
      "produces per-type effort summaries, coverage-grid maps, an overall "
      "conservancy occupancy calculation, and a results dashboard."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>total_events_recorded_by_date.csv</b> / "
           "<b>total_events_recorded_by_type.csv</b> — event counts for "
           "the period"),
    bullet("<b>total_events_recorded.html/.png</b> — daily events line chart"),
    bullet("<b>patrol_events.csv</b> — flattened patrol_info event details"),
    bullet("<b>patrol_purpose_summary.csv</b> — patrol count by patrol purpose"),
    bullet("<b>patrol_relocations.geoparquet</b> — full observation dataset "
           "with patrol metadata"),
    bullet("<b>foot_patrol_efforts.csv</b> / <b>vehicle_patrol_efforts.csv</b> "
           "/ <b>motorbike_patrol_efforts.csv</b> — per-type effort summaries"),
    bullet("<b>foot_patrol_map.html/.png</b> / <b>vehicle_patrol_map.html/.png</b> "
           "/ <b>motor_patrol_map.html/.png</b> — per-type coverage-grid maps"),
    bullet("<b>patrol_trajectories.geoparquet</b> — reprojected overall "
           "coverage grid (foot + vehicle + motorbike combined)"),
    bullet("<b>overall_patrol_efforts.csv</b> — per-ranger summary"),
    bullet("<b>overall_patrol_map.html/.png</b> — combined 1 000 m grid-cell "
           "visit density map"),
    bullet("<b>patrol_coverage.csv</b> — patrol occupancy percentage per "
           "conservancy region"),
    bullet("A <b>results dashboard</b> assembling the four maps, the events "
           "chart, and the three summary tables"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output file", "Description"],
            ["total_events_recorded_by_date.csv",
             "Daily event counts (all non-excluded types)"],
            ["total_events_recorded_by_type.csv",
             "Daily event counts broken down by event type"],
            ["total_events_recorded.html / .png",
             "Line chart of daily event totals"],
            ["patrol_events.csv",
             "Flattened patrol_info event details"],
            ["patrol_purpose_summary.csv",
             "Patrol count grouped by patrol purpose"],
            ["patrol_relocations.geoparquet",
             "All patrol observations with full patrol metadata"],
            ["foot_patrol_efforts.csv",
             "Foot patrol metrics: count, distance, duration, average speed"],
            ["foot_patrol_map.html / .png",
             "Foot patrol coverage-grid map"],
            ["vehicle_patrol_efforts.csv",
             "Vehicle patrol metrics: count, distance, duration, average speed"],
            ["vehicle_patrol_map.html / .png",
             "Vehicle patrol coverage-grid map"],
            ["motorbike_patrol_efforts.csv",
             "Motorbike patrol metrics: count, distance, duration, average speed"],
            ["motor_patrol_map.html / .png",
             "Motorbike patrol coverage-grid map"],
            ["patrol_trajectories.geoparquet",
             "Reprojected overall coverage grid (foot + vehicle + motorbike)"],
            ["overall_patrol_efforts.csv",
             "Per-ranger patrol count, distance km, duration hrs"],
            ["overall_patrol_map.html / .png",
             "Combined grid-cell visit density map (RdYlGn, equal-interval 5 bins)"],
            ["patrol_coverage.csv",
             "Patrol occupancy percentage per conservancy region"],
        ],
        [6*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Requirements (spec.yaml)"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",               ">=2.15.0, <2.16.0",
             "repo.prefix.dev/ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",    "0.1.0rc14.*",
             "repo.prefix.dev/ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",       "0.0.0rc1.*",
             "repo.prefix.dev/ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*",
             "repo.prefix.dev/ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",  "1.0.1.*",
             "repo.prefix.dev/ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",       "1.0.2.*",
             "repo.prefix.dev/ecoscope-workflows-custom"],
            ["pydeck",                            "0.9.2",         "conda-forge"],
            ["opentelemetry-sdk",                 ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [6*cm, 3.2*cm, W - 9.2*cm],
    ),
    note("ecoscope-workflows-ext-wwf-virunga is declared as a requirement but "
         "none of its tasks are referenced in spec.yaml."),
    sp(6),
    h2("2.2  Connections"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch event records and patrol observations; passed to "
             "get_events, get_patrol_values, and "
             "get_patrol_observations_from_patrols_df."],
            ["Dropbox (HTTP)", "fetch_and_persist_file",
             "Download the MNC community conservancy boundary gpkg and MNC "
             "parcels gpkg. Downloads are skipped if the file already "
             "exists (overwrite_existing: false)."],
        ],
        [3.5*cm, 4.5*cm, W - 8*cm],
    ),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All data are processed as a single undivided dataset. The grouper "
      "is threaded through the temporal-index steps and the dashboard only — "
      "it produces no fan-out branching."),
    sp(6),
    h2("2.4  Skip conditions"),
    p("<b>task-instance-defaults.skipif</b> applies two conditions to every "
      "task instance in the workflow by default: <b>any_is_empty_df</b> "
      "(skip if any upstream DataFrame input is empty) and "
      "<b>any_dependency_skipped</b> (skip if any upstream task was itself "
      "skipped, propagating the skip state through dependent branches)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before any event data is fetched, the workflow downloads and prepares "
      "the two GeoPackage boundary files used as background layers on every "
      "map, and precomputes the map view state shared by all of them."),
    sp(6),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "fetch_and_persist_file\npersist_mnc_gpkg",
             "Download mnc_conservancy.gpkg from Dropbox. "
             "overwrite_existing: false — skipped on subsequent runs if "
             "the file is already present."],
            ["2", "fetch_and_persist_file\ndownload_mnc_parcels",
             "Download mnc_across_the_river_parcels.gpkg from Dropbox."],
            ["3", "load_df\nload_comm_shp",
             "Load the conservancy GeoPackage into a GeoDataFrame."],
            ["4", "ecoscope_workflows_ext_mnc.tasks.transformation.\n"
             "fix_invalid_geometries\nfix_comm_geom",
             "Repair invalid geometries (e.g. self-intersecting polygons) "
             "using shapely's make_valid()."],
            ["5", "filter_df\nfilter_conservancy_boundary",
             "Filter to rows where grazing_zone = 'Conservancy'. Used as "
             "the area-of-interest (AOI) for every coverage grid and for "
             "the occupancy calculation."],
            ["6", "filter_df\nfilter_mara_north",
             "Filter to rows where name = 'Mara North Conservancy'. Used "
             "only to compute the shared map view state."],
            ["7", "load_df\nload_mnc_parcels",
             "Load the parcels GeoPackage."],
            ["8", "ecoscope_workflows_ext_custom.tasks.results.\n"
             "create_geojson_layer\ncreate_conservancy_layer / "
             "create_parcels_layer",
             "Build the two static map layers reused as background on "
             "every patrol/coverage map: a grey conservancy boundary "
             "outline and a dark-khaki parcels fill."],
            ["9", "ecoscope_workflows_ext_ste.tasks.spatial_operations.\n"
             "envelope_gdf\nzoom_to_envelope",
             "Compute the bounding envelope of filter_mara_north."],
            ["10", "ecoscope_workflows_ext_ste.tasks.spatial_operations.\n"
             "compute_view_state_from_gdf\ngdf_image_extent",
             "Compute a zoom level and centre point from that envelope "
             "(pitch: 0, bearing: 0, max_zoom: 15). Reused unchanged for "
             "every draw_map call in the workflow."],
        ],
        [0.7*cm, 4.3*cm, W - 5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. EVENTS SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Events Summary"),
    hr(),
    p("A single <b>get_events</b> call (id: <b>get_events_data</b>) fetches "
      "all event types for the analysis period, with columns id, time, "
      "event_type, event_category, reported_by, serial_number, geometry, "
      "created_at, event_details, and patrols. include_details: true, "
      "raise_on_empty: true, force_point_geometry: true. The result feeds "
      "two branches: this events summary, and the patrol_info / "
      "observations pipeline in Sections 5–6."),
    sp(6),
    h2("4.1  Date extraction, temporal indexing, and exclusion"),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "extract_column_as_type\nextract_event_date",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new <b>date</b> column."],
            ["2", "add_temporal_index\nevents_temporal",
             "Add a temporal index keyed on <b>date</b>, using the empty "
             "grouper list. cast_to_datetime: true, format: mixed."],
            ["3", "exclude_row_values\nfilter_events",
             "Remove rows where event_type is any of: "
             "distancecountwildlife_rep, distancecountpatrol_rep, "
             "airstrip_operations."],
        ],
        [0.7*cm, 4*cm, W - 4.7*cm],
    ),
    sp(6),
    h2("4.2  Summaries, chart, and widget"),
    make_table(
        [
            ["Output", "Task / id", "Logic"],
            ["total_events_recorded_by_date.csv",
             "summarize_df\ntotal_events_recorded\n→ persist_df\npersist_tevents_df",
             "Group by <b>date</b>, count unique <b>id</b> → "
             "<b>no_of_events</b>. Persist as CSV."],
            ["total_events_recorded_by_type.csv",
             "summarize_df\ntotal_events_type_recorded\n→ persist_df\n"
             "persist_summary_event_type",
             "Group by <b>date</b> and <b>event_type</b>, count unique "
             "<b>id</b>. Persist as CSV."],
            ["total_events_recorded.html / .png",
             "draw_line_chart\ndraw_events_chart\n→ persist_text\n"
             "persist_total_events\n→ html_to_png\nconvert_events_chart_png",
             "Line chart: x = date, y = no_of_events, colour "
             "lightsteelblue, no legend. width 1280 / height 720, "
             "device_scale_factor 2.0, wait_for_timeout 10 ms."],
            ["Dashboard widget",
             "create_plot_widget_single_view\nevents_chart_widget",
             "Title: 'Total Events Recorded'. Wraps the persisted chart "
             "HTML for the results dashboard."],
        ],
        [3.3*cm, 3.7*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. PATROL PURPOSE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Patrol Purpose Summary"),
    hr(),
    p("This branch isolates <b>patrol_info</b> events from "
      "<b>events_temporal</b>, flattens their event details, and produces a "
      "per-purpose summary table and dashboard widget."),
    sp(6),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "filter_df\nfilter_patrol_info_events",
             "Keep rows where event_type = 'patrol_info'."],
            ["2", "process_events_details\nprocess_patrol_events",
             "Flatten event details. map_to_titles: true, ordered: true."],
            ["3", "normalize_json_column\nnormalize_patrols",
             "Normalize the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["4", "drop_column_prefix\ndrop_patrol_prefix",
             "Drop the <b>event_details__</b> prefix from column names "
             "(duplicate_strategy: keep_original)."],
            ["5", "persist_df\npersist_events",
             "Write the flattened patrol events to <b>patrol_events.csv</b>."],
            ["6", "map_columns\nrename_patrol_info",
             "Rename columns: patrols → patrol_id, Participants → "
             "participants, Patrol Purpose → patrol_purpose, "
             "Transport Type → transport_type."],
            ["7", "summarize_df\npatrol_info_summary",
             "Group by <b>patrol_purpose</b>. number_of_patrols = "
             "nunique(id), 0 decimal places."],
            ["8", "persist_df\npersist_patrol_df",
             "Write to <b>patrol_purpose_summary.csv</b>."],
            ["9", "draw_table\npatrol_summary_table_html\n→ persist_text\n"
             "patrol_summary_table_url\n→ create_table_widget_single_view\n"
             "patrol_summary_table_widget",
             "Render patrol_info_summary as an HTML table (sorting and "
             "filtering enabled, download disabled), persist it, and wrap "
             "it in a dashboard widget titled 'Patrol Purpose Summary'."],
        ],
        [0.7*cm, 3.5*cm, W - 4.2*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. PATROL OBSERVATIONS PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Patrol Observations Pipeline"),
    hr(),
    p("Starting from <b>rename_patrol_info</b>, this pipeline expands, "
      "fetches, and merges patrol observation points from EarthRanger with "
      "patrol metadata, and converts the result into relocations for "
      "trajectory building."),
    sp(6),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "filter_notna\nfilter_null_patrols",
             "Remove rows where <b>patrol_id</b> is null."],
            ["2", "fill_missing_values\nfill_transport_type",
             "Fill null values in <b>transport_type</b> with "
             "<b>'Undefined'</b>."],
            ["3", "explode\nexplode_patrol_id",
             "Explode the <b>patrol_id</b> column (reset_index: true; "
             "a row may reference multiple patrol IDs)."],
            ["4", "get_patrol_values\nget_patrol_event_values",
             "Fetch patrol records from EarthRanger for each patrol ID "
             "(max_workers: 10)."],
            ["5", "get_patrol_observations_from_patrols_df\nget_patrol_obs",
             "Fetch patrol observation points. include_patrol_details: "
             "true, raise_on_empty: true, sub_page_size: 100."],
            ["6", "map_columns\njoin_patrol_df",
             "From explode_patrol_id, retain id, patrol_id, participants, "
             "patrol_purpose, transport_type."],
            ["7", "merge_two_dataframes\nmerge_patrol_df_obs",
             "Merge get_patrol_obs (left) with join_patrol_df (right) on "
             "<b>patrol_id</b>."],
            ["8", "explode\nexplode_participants",
             "Explode the <b>participants</b> column (reset_index: true)."],
            ["9", "process_relocations\nobs_relocs",
             "Convert the merged observations to relocations, retaining "
             "extra__id, extra__created_at, extra__subject_id, geometry, "
             "groupby_col, fixtime, junk_status, patrol_id, patrol_title, "
             "patrol_serial_number, patrol_start_time, patrol_end_time, "
             "patrol_type, patrol_status, patrol_subject, "
             "patrol_type__value, participants, patrol_purpose, and "
             "transport_type. Filters sentinel coordinates: (180, 90), "
             "(0, 0), (1, 1)."],
            ["10", "persist_df\npersist_relocs",
             "Write to <b>patrol_relocations.geoparquet</b>."],
        ],
        [0.7*cm, 3.5*cm, W - 4.2*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. TRAJECTORY CONVERSION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Trajectory Conversion"),
    hr(),
    p("The relocations are split into three transport-type branches on the "
      "<b>transport_type</b> column. Each branch converts its relocations "
      "to trajectory segments using type-appropriate speed and distance "
      "filters, then adds a temporal index and renames columns."),
    sp(6),
    h2("7.1  Transport-type filtering"),
    make_table(
        [
            ["Branch", "Task / id", "Filter"],
            ["Foot",      "filter_df\nfilter_foot_patrols",
             "transport_type = 'Foot'"],
            ["Vehicle",   "filter_df\nfilter_vehicle_patrols",
             "transport_type = 'Vehicle'"],
            ["Motorbike", "filter_df\nfilter_motor_patrols",
             "transport_type = 'Motorbike'"],
        ],
        [2*cm, 3.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("7.2  Trajectory segment filters (relocations_to_trajectory)"),
    make_table(
        [
            ["Parameter", "Foot", "Vehicle", "Motorbike"],
            ["min_length_meters",  "0.001",   "0.35",    "0.35"],
            ["max_length_meters",  "5 000",   "5 000",   "5 000"],
            ["min_time_secs",      "1",       "1",       "1"],
            ["max_time_secs",      "14 400",  "18 000",  "18 000"],
            ["min_speed_kmhr",     "0.5",     "10.0",    "10.0"],
            ["max_speed_kmhr",     "9.0",     "100.0",   "100.0"],
        ],
        [4*cm, (W - 4*cm)/3, (W - 4*cm)/3, (W - 4*cm)/3],
    ),
    note("Foot patrols use a tighter speed envelope (0.5–9 km/h) and shorter "
         "maximum duration (4 h vs 5 h) than vehicle and motorbike patrols, "
         "which use identical filter values to each other."),
    sp(6),
    h2("7.3  Temporal indexing and column renaming"),
    p("Each branch (foot_trajs / vehicle_trajs / motor_trajs) then goes "
      "through two identical steps:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "add_temporal_index\ntemporal_foot_traj / "
             "temporal_vehicle_traj / temporal_motor_traj",
             "Add a temporal index on <b>segment_start</b>. "
             "cast_to_datetime: true, format: mixed."],
            ["2", "map_columns\nrename_foot_trajs / rename_vehicle_trajs / "
             "rename_motor_trajs",
             "Rename extra__* columns to clean names: created_at, id, "
             "participants, patrol_end_time, patrol_id, patrol_purpose, "
             "patrol_serial_number, patrol_start_time, patrol_status, "
             "patrol_subject, patrol_title, patrol_type, "
             "patrol_type_value, subject_id, transport_type. "
             "raise_if_not_found: true."],
        ],
        [0.7*cm, 5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. PER-TYPE EFFORT SUMMARIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Per-Type Effort Summaries"),
    hr(),
    p("Each of the three transport-type branches is summarised identically "
      "by <b>patrol_type_value</b> and persisted as CSV — no colormap or "
      "geometry filtering happens at this stage; that is deferred to the "
      "coverage-grid pipeline in Section 9."),
    sp(6),
    make_table(
        [
            ["Branch", "Task / id", "Detail"],
            ["Foot", "summarize_df\nfoot_patrol_metrics\n→ persist_df\n"
             "persist_foot_df",
             "no_of_patrols = nunique(patrol_id); distance_km = "
             "sum(dist_meters) m→km; duration_hrs = sum(timespan_seconds) "
             "s→h; average_speed = mean(speed_kmhr). "
             "Write to foot_patrol_efforts.csv."],
            ["Vehicle", "summarize_df\nvehicle_patrol_metrics\n→ persist_df\n"
             "persist_vehicle_df",
             "Same aggregations. Write to vehicle_patrol_efforts.csv."],
            ["Motorbike", "summarize_df\nmotor_patrol_metrics\n→ persist_df\n"
             "persist_motor_df",
             "Same aggregations. Write to motorbike_patrol_efforts.csv."],
        ],
        [2*cm, 3.7*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. COVERAGE-GRID MAP PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Coverage-Grid Map Pipeline"),
    hr(),
    p("Each of the three renamed trajectory branches — and, after "
      "concatenation, the combined dataset — goes through an identical "
      "grid, classification, colormap, and map-rendering pipeline. The "
      "foot branch is described here; vehicle, motorbike, and the "
      "combined ('overall') branch are identical except for task ids "
      "and output titles."),
    sp(6),
    make_table(
        [
            ["Step", "Task / id (foot example)", "Detail"],
            ["1", "create_patrol_coverage_grid\nfoot_patrol_coverage",
             "Overlay trajectories onto a 1 000 m grid clipped to "
             "filter_conservancy_boundary. Each cell records "
             "unique_patrol_count, time_spent_seconds/hours, and "
             "distance_patrolled_meters/km. keep_empty_cells: false."],
            ["2", "reproject_gdf\nreproject_foot",
             "Reproject the grid to EPSG:4326."],
            ["3", "apply_classification\napply_foot_class_grid",
             "Equal-interval classification of unique_patrol_count, "
             "k = 5 bins, output column density_bins."],
            ["4", "apply_color_map\napply_foot_grid_colormap",
             "Apply the RdYlGn colormap to density_bins, writing "
             "density_colors."],
            ["5", "create_geojson_layer\ngenerate_foot_grid_layer",
             "Build the DeckGL grid layer (opacity 0.55, fill from "
             "density_colors). Legend: title 'Grid Cell Visits', "
             "label_column density_bins, color_column density_colors."],
            ["6", "combine_deckgl_map_layers\ncombine_foot_patrol",
             "Combine the grid layer with the shared parcels and "
             "conservancy boundary static layers."],
            ["7", "draw_map\ndraw_foot_map",
             "Render using the ArcGIS hillshade/boundary tile layers, "
             "view state from gdf_image_extent, max_zoom: 10, legend "
             "placement bottom-right."],
            ["8", "persist_text\npersist_foot_urls",
             "Write to foot_patrol_map.html."],
            ["9", "html_to_png\nconvert_foot_png",
             "Render to PNG. full_page: false, device_scale_factor: 2.0, "
             "wait_for_timeout: 40 000 ms, max_concurrent_pages: 1."],
            ["10", "create_map_widget_single_view\nfoot_map_widget",
             "Title 'Foot Patrol Coverage Map'. Wraps the persisted map "
             "HTML for the results dashboard."],
        ],
        [0.7*cm, 4.3*cm, W - 5*cm],
    ),
    note("The 40 000 ms wait_for_timeout on every map's html_to_png step "
         "gives deck.gl time to finish loading basemap tiles before the "
         "screenshot is taken; the events chart, which has no tiles to "
         "load, uses 10 ms instead."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. COMBINED TRAJECTORIES AND OVERALL PATROL EFFORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Combined Trajectories and Overall Patrol Effort"),
    hr(),
    p("After the three renamed trajectory branches complete, they are "
      "concatenated and run through the same coverage-grid pipeline as "
      "Section 9 to produce the combined ('overall') map, and separately "
      "summarised per ranger."),
    sp(6),
    h2("10.1  Concatenation and overall coverage grid"),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "concatenate_dataframes\nconcat_dataframes",
             "Concatenate rename_foot_trajs, rename_vehicle_trajs, and "
             "rename_motor_trajs. axis: 0, join: outer, ignore_index: "
             "true, sort: false."],
            ["2", "create_patrol_coverage_grid\noverall_patrol_coverage\n"
             "→ reproject_gdf\nreproject_overall",
             "Same grid/reprojection as each per-type branch, applied to "
             "the concatenated dataset. Feeds the classification/colormap/"
             "map pipeline that produces overall_patrol_map.html / .png "
             "and the 'Overall Patrol Coverage Map' widget (ov_map_widget)."],
            ["3", "persist_df\npersist_trajectories_data",
             "Write reproject_overall — the reprojected overall coverage "
             "grid, not the raw concatenated trajectories — to "
             "<b>patrol_trajectories.geoparquet</b>."],
        ],
        [0.7*cm, 4*cm, W - 4.7*cm],
    ),
    note("persist_trajectories_data persists reproject_overall (the grid), "
         "not concat_dataframes (the raw trajectories) — despite the "
         "filename, patrol_trajectories.geoparquet contains grid-cell "
         "coverage statistics, not per-segment trajectory geometries."),
    sp(6),
    h2("10.2  Overall patrol effort (per-ranger summary)"),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "summarize_df\nranger_patrol_metrics",
             "Group concat_dataframes by <b>participants</b>. "
             "number_of_patrols = nunique(patrol_id) [0 d.p.]; "
             "distance_km = sum(dist_meters) m→km [2 d.p.]; "
             "duration_hours = sum(timespan_seconds) s→h [2 d.p.]."],
            ["2", "fill_missing_values\nfill_participants",
             "Fill null <b>participants</b> with 'Undefined'."],
            ["3", "convert_columns_to_int\nno_of_patrols_int",
             "Convert number_of_patrols to int (errors: coerce, "
             "fill_value: 0)."],
            ["4", "persist_df\npersist_total_df",
             "Write to <b>overall_patrol_efforts.csv</b>."],
            ["5", "draw_table\npatrol_efforts_table_html\n→ persist_text\n"
             "patrol_efforts_table_url\n→ create_table_widget_single_view\n"
             "patrol_efforts_table_widget",
             "Render, persist, and wrap as a dashboard widget titled "
             "'Overall Patrol Efforts'."],
        ],
        [0.7*cm, 3.5*cm, W - 4.2*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. CONSERVANCY OCCUPANCY
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Conservancy Occupancy"),
    hr(),
    p("This section computes what fraction of the conservancy boundary was "
      "actually patrolled, using the overall (combined) coverage grid."),
    sp(6),
    make_table(
        [
            ["Step", "Task / id", "Detail"],
            ["1", "reproject_gdf\nreproject_conservancy",
             "Reproject filter_conservancy_boundary to EPSG:3857 (metres)."],
            ["2", "ecoscope_workflows_ext_mnc.tasks.io.\n"
             "compute_patrol_occupancy\ncompute_cons_occupancy",
             "For each conservancy region, intersect its area with the "
             "unioned overall_patrol_coverage geometry. Both inputs must "
             "share a projected, metre-based CRS. Returns "
             "conservancy_name, conservancy_area_sqkm, "
             "patrolled_area_sqkm, and occupancy_percentage (rounded to "
             "2 d.p.) per region."],
            ["3", "persist_df\npersist_occupancy_df",
             "Write to <b>patrol_coverage.csv</b>."],
            ["4", "draw_table\noccupancy_table_html\n→ persist_text\n"
             "occupancy_table_url\n→ create_table_widget_single_view\n"
             "occupancy_table_widget",
             "Render, persist, and wrap as a dashboard widget titled "
             "'Conservancy Patrol Occupancy'."],
        ],
        [0.7*cm, 4*cm, W - 4.7*cm],
    ),
    note("compute_patrol_occupancy raises a ValueError if either input "
         "GeoDataFrame lacks a CRS or is in a geographic (degree-based) "
         "CRS — both conservancies and patrol_coverage must already be "
         "reprojected to a projected, metre-based CRS before this task "
         "runs."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. RESULTS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Results Dashboard"),
    hr(),
    p("The final step, <b>gather_dashboard</b> (id: "
      "<b>mnc_events_dashboard</b>), assembles the workflow details, time "
      "range, groupers, and every widget built in the sections above into "
      "a single dashboard. Widgets are included in this order:"),
    sp(4),
    make_table(
        [
            ["#", "Widget id", "Type", "Title"],
            ["1", "foot_map_widget",            "Map",   "Foot Patrol Coverage Map"],
            ["2", "vh_map_widget",              "Map",   "Vehicle Patrol Coverage Map"],
            ["3", "mr_map_widget",              "Map",   "Motorbike Patrol Coverage Map"],
            ["4", "ov_map_widget",              "Map",   "Overall Patrol Coverage Map"],
            ["5", "events_chart_widget",        "Chart", "Total Events Recorded"],
            ["6", "patrol_summary_table_widget","Table", "Patrol Purpose Summary"],
            ["7", "patrol_efforts_table_widget","Table", "Overall Patrol Efforts"],
            ["8", "occupancy_table_widget",     "Table", "Conservancy Patrol Occupancy"],
        ],
        [1*cm, 5.5*cm, 2.2*cm, W - 8.7*cm],
    ),
    sp(4),
    p("Every map and chart widget takes a path to precomputed HTML "
      "(created via persist_text on the corresponding draw_map / "
      "draw_line_chart output); every table widget takes a path to HTML "
      "rendered by draw_table from the relevant summary dataframe."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Output Files"),
    hr(),
    p("All files are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS/</b>."),
    sp(6),
    h2("13.1  Events summary"),
    make_table(
        [
            ["File", "Format", "Description"],
            ["total_events_recorded_by_date.csv",  "CSV",
             "Daily event counts (all non-excluded types)"],
            ["total_events_recorded_by_type.csv",  "CSV",
             "Daily event counts by event_type"],
            ["total_events_recorded.html",          "HTML",
             "Interactive line chart of daily event totals"],
            ["total_events_recorded.png",           "PNG",
             "Static version of the events chart (2× DPI)"],
        ],
        [5.5*cm, 1.5*cm, W - 7*cm],
    ),
    sp(4),
    h2("13.2  Patrol purpose"),
    make_table(
        [
            ["File", "Format", "Description"],
            ["patrol_events.csv", "CSV",
             "Flattened patrol_info event details"],
            ["patrol_purpose_summary.csv", "CSV",
             "Patrol count by patrol purpose"],
            ["patrol_purpose_summary_table.html", "HTML",
             "Rendered table backing the dashboard widget"],
        ],
        [5.5*cm, 1.5*cm, W - 7*cm],
    ),
    sp(4),
    h2("13.3  Relocations"),
    make_table(
        [
            ["File", "Format", "Description"],
            ["patrol_relocations.geoparquet", "GeoParquet",
             "Full observation dataset: all patrol types, with patrol "
             "metadata columns (patrol_id, patrol_title, patrol_type, "
             "patrol_purpose, transport_type, participants, etc.)"],
        ],
        [5.5*cm, 1.5*cm, W - 7*cm],
    ),
    sp(4),
    h2("13.4  Per-type patrol effort and coverage"),
    make_table(
        [
            ["File", "Format", "Description"],
            ["foot_patrol_efforts.csv",     "CSV",
             "Foot: patrol count, distance km, duration hrs, average speed"],
            ["foot_patrol_map.html / .png", "HTML / PNG",
             "Foot patrol coverage-grid map (RdYlGn)"],
            ["vehicle_patrol_efforts.csv",  "CSV",
             "Vehicle: patrol count, distance km, duration hrs, average speed"],
            ["vehicle_patrol_map.html / .png", "HTML / PNG",
             "Vehicle patrol coverage-grid map (RdYlGn)"],
            ["motorbike_patrol_efforts.csv", "CSV",
             "Motorbike: patrol count, distance km, duration hrs, average speed"],
            ["motor_patrol_map.html / .png", "HTML / PNG",
             "Motorbike patrol coverage-grid map (RdYlGn)"],
        ],
        [5.5*cm, 2.2*cm, W - 7.7*cm],
    ),
    sp(4),
    h2("13.5  Combined trajectories, overall effort, and coverage"),
    make_table(
        [
            ["File", "Format", "Description"],
            ["patrol_trajectories.geoparquet", "GeoParquet",
             "Reprojected overall coverage grid (foot + vehicle + "
             "motorbike combined)"],
            ["overall_patrol_efforts.csv", "CSV",
             "Per-ranger patrol count, distance km, duration hrs; nulls "
             "replaced with 'Undefined'"],
            ["overall_patrol_efforts_table.html", "HTML",
             "Rendered table backing the dashboard widget"],
            ["overall_patrol_map.html / .png", "HTML / PNG",
             "Combined 1 000 m grid-cell visit density map (RdYlGn)"],
            ["patrol_coverage.csv", "CSV",
             "Patrol occupancy percentage per conservancy region "
             "(2 decimal places)"],
            ["patrol_coverage_table.html", "HTML",
             "Rendered table backing the dashboard widget"],
        ],
        [5.5*cm, 1.5*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 14. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("14. Software Versions"),
    hr(),
    p("Duplicated from Section 2.1 for reference — see spec.yaml for the "
      "authoritative, current requirement pins."),
    sp(4),
    make_table(
        [
            ["Package", "Version constraint", "Channel"],
            ["ecoscope-platform", ">=2.15.0, <2.16.0",
             "https://repo.prefix.dev/ecoscope-workflows/"],
            ["ecoscope-workflows-ext-custom", "0.1.0rc14.*",
             "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ["ecoscope-workflows-ext-ste", "0.0.0rc1.*",
             "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ["ecoscope-workflows-ext-wwf-virunga", "0.0.0rc9.*",
             "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ["ecoscope-workflows-ext-big-life", "1.0.1.*",
             "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ["ecoscope-workflows-ext-mnc", "1.0.2.*",
             "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ["pydeck", "0.9.2", "conda-forge"],
            ["opentelemetry-sdk", ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [5.5*cm, 3.2*cm, W - 8.7*cm],
    ),
]


# ── Build PDF ──────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written: {OUTPUT_FILE}")
