# MNC Patrol Effort — User Guide

This guide walks you through configuring and running the MNC Patrol Effort workflow, which processes patrol events and observations from EarthRanger to produce trajectory maps, patrol effort summaries, a patrol coverage analysis, and a results dashboard for Mara North Conservancy.

---

## Overview

The workflow delivers, for each run:

- **Events summary** — total events recorded by date and by type, with a line chart (HTML + PNG)
- **Patrol purpose summary** — patrol count grouped by patrol purpose (CSV + table)
- **Patrol relocations** — full observation dataset as a GeoParquet file
- **Foot patrol report** — effort summary table (CSV) and coverage map (HTML + PNG)
- **Vehicle patrol report** — effort summary table (CSV) and coverage map (HTML + PNG)
- **Motorbike patrol report** — effort summary table (CSV) and coverage map (HTML + PNG)
- **Combined trajectories** — merged trajectory dataset (GeoParquet)
- **Overall patrol efforts** — per-ranger summary of patrols, distance, and duration (CSV + table)
- **Patrol coverage map** — 1 000 m grid-cell visit density map (HTML + PNG) with conservancy occupancy percentage (CSV + table)
- **Results dashboard** — the four coverage maps, the events chart, and the three summary tables assembled into a single dashboard view

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `patrol_info` events and associated patrol observations recorded for the analysis period

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/mnc-patrol-effort.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Configure the EarthRanger Connection

Navigate to **Data Sources** and click **Connect**, then select **EarthRanger**. Fill in the connection form:

| Field | Description |
|-------|-------------|
| Data Source Name | A label to identify this connection (e.g. `Mara North Conservancy`) |
| EarthRanger URL | Your instance URL (e.g. `your-site.pamdas.org`) |
| EarthRanger Username | Your EarthRanger username |
| EarthRanger Password | Your EarthRanger password |

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **mnc-patrol-effort**. Click the card to open the workflow configuration form.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection

The configuration form has three sections on a single page.

**Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. reporting month or site) |

**Time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time — all events and patrol data from this point are fetched |
| Until | End date and time of the analysis window |

**Connect to ER**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Mara North Conservancy`).

Once all three sections are filled, click **Submit**.

![Configure Workflow Details, Time Range, and Connect to ER](data/screenshots/configure_workflow.png)

---

## Running the Workflow

Once submitted, the runner will:

1. Download the MNC community conservancy boundary and parcels GeoPackage files from Dropbox; repair invalid geometries on the conservancy boundary; filter it down to the `Conservancy` grazing zone (used later as the coverage AOI) and to `Mara North Conservancy` (used for the map extent); build styled map layers for the conservancy boundary and parcels.
2. Fetch all events from EarthRanger; extract the date from each timestamp; add a temporal index; exclude `distancecountwildlife_rep`, `distancecountpatrol_rep`, and `airstrip_operations` events; summarise the remainder by date and by type; draw a daily events line chart; save as `total_events_recorded_by_date.csv`, `total_events_recorded_by_type.csv`, and `total_events_recorded.html`/`.png`.
3. Filter `patrol_info` events; flatten event details; save as `patrol_events.csv`; rename fields (`patrol_id`, `participants`, `patrol_purpose`, `transport_type`); summarise patrol count by patrol purpose; save as `patrol_purpose_summary.csv`.
4. Drop records with no patrol ID; fill missing transport type with `Undefined`; explode the `patrol_id` column; fetch patrol records and patrol observations from EarthRanger; merge them with the patrol info; explode the `participants` column; process the result into relocations (filtering out sentinel coordinates); save as `patrol_relocations.geoparquet`.
5. Split relocations into three transport-type branches — **Foot**, **Vehicle**, and **Motorbike** — and convert each to trajectories using type-appropriate segment filters (foot patrols use a tighter speed/distance envelope than vehicle and motorbike).
6. For each patrol type: rename trajectory columns; summarise effort metrics (patrol count, distance km, duration hrs, average speed) by `patrol_type_value`; save effort CSV.
7. For each patrol type, and again for the combined dataset: build a 1 000 m patrol coverage grid over the conservancy boundary; classify visit counts into 5 equal-interval bins; apply the `RdYlGn` colormap; draw the coverage map; save as HTML, convert to PNG, and wrap it in a map widget.
8. Concatenate the foot, vehicle, and motorbike trajectories; summarise per-ranger effort (patrol count, distance, duration) from the combined dataset; fill missing participant names with `Undefined`; save as `overall_patrol_efforts.csv`.
9. Reproject the conservancy boundary and compute what percentage of it is covered by the overall patrol coverage grid; save as `patrol_coverage.csv`.
10. Render the events chart, the patrol purpose summary, the overall patrol efforts, and the conservancy occupancy as table/chart widgets, and assemble all four maps, the chart, and the three tables into a single results dashboard.
11. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

### Events Summary

| File | Description |
|------|-------------|
| `total_events_recorded_by_date.csv` | Daily event counts (all types combined) |
| `total_events_recorded_by_type.csv` | Daily event counts broken down by event type |
| `total_events_recorded.html` / `.png` | Line chart of daily event counts |

### Patrol Purpose

| File | Description |
|------|-------------|
| `patrol_events.csv` | Flattened `patrol_info` event details |
| `patrol_purpose_summary.csv` | Patrol count by patrol purpose |
| `patrol_purpose_summary_table.html` | Rendered HTML table backing the dashboard widget |

### Relocations

| File | Description |
|------|-------------|
| `patrol_relocations.geoparquet` | Full patrol observation dataset with patrol metadata |

### Foot Patrols

| File | Description |
|------|-------------|
| `foot_patrol_efforts.csv` | Patrol count, distance, duration, and average speed by patrol type |
| `foot_patrol_map.html` / `.png` | Foot patrol coverage grid map |

### Vehicle Patrols

| File | Description |
|------|-------------|
| `vehicle_patrol_efforts.csv` | Patrol count, distance, duration, and average speed by patrol type |
| `vehicle_patrol_map.html` / `.png` | Vehicle patrol coverage grid map |

### Motorbike Patrols

| File | Description |
|------|-------------|
| `motorbike_patrol_efforts.csv` | Patrol count, distance, duration, and average speed by patrol type |
| `motor_patrol_map.html` / `.png` | Motorbike patrol coverage grid map |

### Combined Trajectories and Overall Effort

| File | Description |
|------|-------------|
| `patrol_trajectories.geoparquet` | Reprojected overall patrol coverage grid (foot + vehicle + motorbike combined) |
| `overall_patrol_efforts.csv` | Per-ranger summary of total patrols, distance km, and duration hrs |
| `overall_patrol_efforts_table.html` | Rendered HTML table backing the dashboard widget |

### Patrol Coverage

| File | Description |
|------|-------------|
| `overall_patrol_map.html` / `.png` | 1 000 m grid-cell visit density map, all patrol types combined |
| `patrol_coverage.csv` | Patrol occupancy percentage per conservancy region |
| `patrol_coverage_table.html` | Rendered HTML table backing the dashboard widget |

### Dashboard

The final dashboard step assembles eight widgets, in order: the foot, vehicle, motorbike, and overall patrol coverage maps; the total events chart; and the patrol purpose, overall patrol efforts, and conservancy occupancy tables.
