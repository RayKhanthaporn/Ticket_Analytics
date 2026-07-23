# TechSolve Support Operations Power BI Dashboard

## Project overview

This project prepares and presents TechSolve support-ticket data for operational reporting in Microsoft Power BI. The dashboard is designed to give an Operations Manager clear visibility into:

- ticket demand and monthly trends;
- issue categories and sub-categories;
- ticket status and flow;
- first-response and resolution performance;
- reported SLA performance and SLA data-quality mismatches;
- escalation and customer satisfaction;
- public-holiday, weekend and business-day effects;
- team and assigned-staff workload;
- data-quality risks that affect management conclusions.

The reporting period is **1 January 2024 to 31 December 2025**. The current source contains **67,157 tickets dated in 2024 and only 10 tickets dated in 2025**. Therefore, 2025 results must be labelled as incomplete and must not be compared with complete 2024 months without a clear coverage warning.

---

## Decision supported

The dashboard supports the following management decision:

> Where should TechSolve focus operational, process, product, staffing and data-governance improvements to reduce support demand and improve response, resolution, SLA and customer-experience outcomes?

---

## Project files

| File | Purpose |
|---|---|
| `FactTickets_2024_2025.csv` | Detailed ticket-level fact table enriched with holiday, classification and quality fields |
| `DimHolidayCalendar_2024_2025.csv` | One row per date and region, with public-holiday, weekend and business-day attributes |
| `DimIssueTaxonomy.csv` | Controlled issue category, sub-category, operational owner and improvement-theme reference |
| `Measures.dax` | Power BI measures for volume, response, resolution, SLA, escalation, CSAT and holiday reporting |
| `PowerQuery_FactTickets.m` | Optional repeatable Power Query connection to the detailed fact CSV |
| `TechSolve_Operations_Theme.json` | Power BI report colour theme |
| `VisualData_MonthlyTrend.csv` | Pre-aggregated monthly validation and prototyping data |
| `VisualData_IssuePerformance.csv` | Pre-aggregated issue-category and sub-category performance data |
| `VisualData_Status.csv` | Pre-aggregated status data |
| `VisualData_CalendarImpact.csv` | Pre-aggregated holiday, weekend and business-day comparison data |
| `VisualData_TeamPerformance.csv` | Pre-aggregated team and assigned-staff performance data |
| `Model_and_Report_Spec.json` | Model relationships and planned report pages |
| `ExecutiveSnapshot.json` | Headline operational metrics from the prepared extract |
| `README_Dashboard_Build_Guide.md` | Original dashboard construction plan |

---

## Data lineage

```text
TechSolve - Ticket Data.xlsx
          |
          v
      tickets_df
          +
      holidays_df
          |
          v
 tickets_holidays_df
          +
 controlled category mapping
          |
          v
 tickets_holidays_categorised_df
          |
          v
 FactTickets_2024_2025.csv
          |
          v
 Power BI Operations Dashboard
```

The original `category` field is retained unchanged for auditability. The `RK_` fields contain standardised classifications, analytical flags or reporting attributes.

---

## Controlled issue taxonomy

The dashboard uses six broad categories and fourteen sub-categories.

### 1. Account & Access

- Login Issue
- Account Suspension

### 2. Billing, Payments & Subscription

- Payment Problem
- Refund Request
- Subscription Cancellation

### 3. Product Reliability & Defects

- Bug Report
- Performance Issue
- Data Sync Issue

### 4. Product Improvement

- Feature Request

### 5. Security & Privacy

- Security Concern

### 6. Unclassified & Data Quality

- Missing Category
- Unmapped Category
- Ambiguous Classification
- Manual Review Required

Supporting fields include:

| Field | Purpose |
|---|---|
| `RK_Category` | Broad operational issue group |
| `RK_SubCategory` | Specific support reason |
| `RK_CategoryMappingStatus` | Mapped, Missing, Unmapped or Ambiguous |
| `RK_CategoryMappingMethod` | Exact, Normalised Alias, Description Rule or Manual |
| `RK_CategoryReviewRequired` | `1` when classification requires review |
| `RK_OperationalOwner` | Suggested operational team |
| `RK_IssueNature` | Incident, Request, Security, Commercial or Data Quality |
| `RK_ImprovementTheme` | Automation, Product Fix, Process Fix, Training, Product Roadmap or Review |

---

## Power BI model

### Import these core tables

1. `FactTickets_2024_2025.csv`
2. `DimHolidayCalendar_2024_2025.csv`
3. `DimIssueTaxonomy.csv`

### Required relationship

```text
DimHolidayCalendar_2024_2025[DateRegionKey]
                         1
                         |
                         *
FactTickets_2024_2025[DateRegionKey]
```

Recommended relationship settings:

```text
Cardinality: One to many
Cross-filter direction: Single
Relationship: Active
```

`DateRegionKey` is formatted as:

```text
YYYYMMDD|Region
```

Example:

```text
20240129|Auckland
```

---

## Build sequence

### 1. Load data

Use **Home → Get data → Text/CSV** to import the three core tables.

Alternatively, create a Power Query parameter named:

```text
Parameter_FactTicketsPath
```

and paste the code from `PowerQuery_FactTickets.m` into the Advanced Editor of a blank query.

### 2. Add measures

Open `Measures.dax`. In Power BI Desktop, use:

```text
Modelling → New measure
```

Paste one complete measure at a time. Measures should be stored in a dedicated `_Measures` table where practical.

### 3. Import the theme

Use:

```text
View → Themes → Browse for themes
```

Select:

```text
TechSolve_Operations_Theme.json
```

### 4. Build the pages

Create the report pages described below.

### 5. Validate filters and interactions

Use **Format → Edit interactions** to confirm that slicers filter all intended cards, charts, matrices and tables.

### 6. Save the report

Save the native Power BI file as:

```text
TechSolve_Operations_Dashboard_2024_2025.pbix
```

---

## Report pages

## Page 1 — Operations Overview

### Purpose

Provide an immediate view of demand, issue mix, status, service performance and management alerts.

### Recommended cards

- Ticket Count
- Active Status Tickets
- Waiting Tickets
- Median Resolution Hours
- Reported SLA Breach Rate
- Escalation Rate
- Average CSAT

### Recommended visuals

#### Monthly ticket trend

Use a **Line and clustered column chart**:

```text
X-axis: Month Start
Column Y-axis: Ticket Count
Line Y-axis: Median Resolution Hours
```

Tooltips:

- Ticket Count
- Median First Response Hours
- Median Resolution Hours
- P90 Resolution Hours
- Reported SLA Breach Rate
- Escalation Rate
- Average CSAT

#### Category share

Use a donut chart or horizontal bar chart:

```text
Legend / Y-axis: RK_Category
Values / X-axis: Ticket Count
```

#### Status distribution

Use a stacked bar chart:

```text
Y-axis: RK_StatusGroup
X-axis: Ticket Count
Legend: status
```

Label Active values as **status based**, not confirmed backlog.

#### Operations alerts table

Recommended alerts:

- active or waiting status with a resolved date;
- reported/calculated SLA mismatch;
- resolution date before creation date;
- missing CSAT;
- category mapping review required;
- public-holiday tickets.

---

## Page 2 — Issue Demand & Root Cause

### Matrix hierarchy

```text
RK_Category
  → RK_SubCategory
      → service_area
```

Recommended values:

- Ticket Count
- Ticket Share
- Median Resolution Hours
- Reported SLA Breach Rate
- Escalation Rate
- Average CSAT

Keep **Stepped layout** and **+/- icons** on. Turn **Auto-size width** off, widen the hierarchy column and keep numeric columns compact.

### Additional visuals

- Monthly ticket demand by category
- Service-area × sub-category heatmap
- Ticket volume versus median resolution-time scatter plot
- Operational owner and improvement-theme analysis

---

## Page 3 — Status & Flow

### Cards

- Active — Status Based
- Waiting for Customer
- Completed
- Status / Resolution Conflict

### Stacked bar

```text
Y-axis: RK_Category
X-axis: Ticket Count
Legend: RK_StatusGroup
```

### Team table

Include:

- team
- assigned_to
- Ticket Count
- Median Resolution Hours
- Escalation Rate
- Average CSAT
- CSAT Response Rate

Use conditional formatting for ticket volume, resolution, escalation and CSAT.

### Governance warning

Open, In Progress and Pending Customer records may also have populated resolution dates. Do not label Active or Waiting counts as confirmed backlog until lifecycle definitions are approved.

---

## Page 4 — Resolution & SLA

### Cards

- Calculated SLA Mismatch Rate
- Reported SLA Breach Rate
- P90 First Response Hours
- P90 Resolution Hours

### Resolution distribution

Use a clustered column chart:

```text
X-axis: RK_ResolutionBand
Y-axis: Ticket Count
```

Sort the bands using:

```text
≤4h
4–8h
8–24h
24–48h
48–72h
3–7d
>7d
```

### Monthly trend

Use a line chart:

```text
X-axis: Month Start
Y-axis: Median Resolution Hours, P90 Resolution Hours
```

### Sub-category performance

Use a clustered bar chart:

```text
Y-axis: RK_SubCategory
X-axis: Median Resolution Hours
```

Sort descending and apply a minimum ticket-count filter to avoid ranking very small groups.

---

## Page 5 — Holiday & Capacity Impact

### Cards

- Holiday Ticket Count
- Holiday Ticket Share
- Holiday Median Resolution Hours
- Holiday versus Business Day Resolution Difference

### Demand by calendar type

```text
X-axis: RK_CalendarType
Y-axis: Ticket Count
```

### Performance by calendar type

Use a Line and clustered column chart:

```text
X-axis: RK_CalendarType
Column Y-axis: Ticket Count
Line Y-axis: Median Resolution Hours
```

### Category mix by calendar type

Use a 100% stacked bar chart:

```text
Y-axis: RK_CalendarType
X-axis: Ticket Count
Legend: RK_Category
```

### Holiday detail table

Include:

- HolidayName
- RegionAnalytics
- Ticket Count
- Median First Response Hours
- Median Resolution Hours
- P90 Resolution Hours
- Reported SLA Breach Rate
- Escalation Rate
- Average CSAT

Filter the table to records where `HolidayName` is not blank.

---

## Core DAX measures

```DAX
Ticket Count =
COUNTROWS(
    FactTickets_2024_2025
)
```

```DAX
Active Status Tickets =
CALCULATE(
    [Ticket Count],
    FactTickets_2024_2025[RK_StatusGroup] = "Active"
)
```

```DAX
Waiting Tickets =
CALCULATE(
    [Ticket Count],
    FactTickets_2024_2025[RK_StatusGroup] = "Waiting"
)
```

```DAX
Completed Tickets =
CALCULATE(
    [Ticket Count],
    FactTickets_2024_2025[RK_StatusGroup] = "Completed"
)
```

```DAX
Median Resolution Hours =
MEDIAN(
    FactTickets_2024_2025[resolution_time_hours]
)
```

```DAX
P90 Resolution Hours =
PERCENTILEX.INC(
    FILTER(
        FactTickets_2024_2025,
        NOT ISBLANK(
            FactTickets_2024_2025[resolution_time_hours]
        )
    ),
    FactTickets_2024_2025[resolution_time_hours],
    0.9
)
```

```DAX
Median First Response Hours =
MEDIAN(
    FactTickets_2024_2025[first_response_time_hours]
)
```

```DAX
P90 First Response Hours =
PERCENTILEX.INC(
    FILTER(
        FactTickets_2024_2025,
        NOT ISBLANK(
            FactTickets_2024_2025[first_response_time_hours]
        )
    ),
    FactTickets_2024_2025[first_response_time_hours],
    0.9
)
```

```DAX
Reported SLA Breach Rate =
DIVIDE(
    CALCULATE(
        [Ticket Count],
        FactTickets_2024_2025[sla_breached] = "Yes"
    ),
    [Ticket Count]
)
```

```DAX
Calculated SLA Mismatch Rate =
DIVIDE(
    SUM(
        FactTickets_2024_2025[RK_SLAMismatch]
    ),
    [Ticket Count]
)
```

```DAX
Escalation Rate =
DIVIDE(
    CALCULATE(
        [Ticket Count],
        FactTickets_2024_2025[escalated] = "Yes"
    ),
    [Ticket Count]
)
```

```DAX
Average CSAT =
AVERAGE(
    FactTickets_2024_2025[csat_score]
)
```

```DAX
CSAT Response Rate =
DIVIDE(
    COUNT(
        FactTickets_2024_2025[csat_score]
    ),
    [Ticket Count]
)
```

---

## Recommended slicers

Use consistent slicers across pages:

- `RK_ReportingYear`
- `RegionAnalytics`
- `RK_Category`
- `RK_SubCategory`
- `service_area`
- `priority`
- `team`
- `channel`
- `RK_CalendarType`
- `HolidayName` on the holiday page

Recommended styles:

| Slicer | Style |
|---|---|
| Year | Horizontal buttons |
| Priority | Horizontal buttons |
| Calendar type | Horizontal buttons |
| Region | Drop-down |
| Category | Drop-down |
| Sub-category | Drop-down |
| Service area | Drop-down |
| Team | Drop-down |
| Holiday name | Searchable drop-down |

Add a page-level reset bookmark and a **Reset filters** button.

---

## Theme and colour standards

Use stable colours consistently across pages.

| Meaning | Colour |
|---|---|
| General volume | `#123B5D` |
| Normal or completed performance | `#2F7E8D` |
| Secondary comparison | `#66A5AD` |
| Waiting / watch | `#D4A72C` |
| Elevated risk / slow performance | `#E08E45` |
| Critical / security / serious exception | `#B42318` |
| Unknown / missing / unclassified | `#6B7280` |
| Report background | `#F7F9FB` |
| Main text | `#1F2937` |

Category colours:

| Category | Colour |
|---|---|
| Account & Access | `#123B5D` |
| Billing, Payments & Subscription | `#2F7E8D` |
| Product Reliability & Defects | `#E08E45` |
| Product Improvement | `#66A5AD` |
| Security & Privacy | `#B42318` |
| Unclassified & Data Quality | `#6B7280` |

Avoid colours that change randomly after refresh. Stable colour meaning improves interpretation.

---

## Matrix formatting guidance

For the issue hierarchy matrix:

```text
Rows:
RK_Category
RK_SubCategory
service_area
```

Recommended formatting:

```text
Stepped layout: On
+/- icons: On
Auto-size width: Off
Hierarchy column: 380–450 px
Ticket column: 90–110 px
Share column: 80–100 px
Word wrap: Off after widening the hierarchy column
Row padding: 5–7
```

The Matrix visual does not automatically stretch columns to use all available width. Resize individual column boundaries manually.

---

## Tooltips

Recommended operational tooltip measures:

- Ticket Count
- Median First Response Hours
- P90 First Response Hours
- Median Resolution Hours
- P90 Resolution Hours
- Reported SLA Breach Rate
- Calculated SLA Mismatch Rate
- Escalation Rate
- Average CSAT
- CSAT Response Rate

Measures should be formatted in the model before being added to tooltips.

---

## Data-quality findings affecting interpretation

The validation identified material issues that must appear on the governance page and in report notes:

1. A large number of `customer_id` values map to multiple customer names.
2. Open, In Progress and Pending Customer records may contain populated resolution dates.
3. The reported SLA flag materially disagrees with the provisional comparison of resolution time against SLA target.
4. Some resolution dates occur before ticket creation dates.
5. Some CSAT responses are missing.
6. The 2025 extract is materially incomplete.

These issues do not prevent aggregate issue-demand and broad operational reporting, but the issues constrain customer-level, backlog and official SLA conclusions.

---

## Quality assurance checklist

Before publishing the dashboard:

- [ ] Confirm the fact table row count reconciles to the prepared extract.
- [ ] Confirm the holiday relationship is one-to-many and active.
- [ ] Confirm `DateRegionKey` has no duplicates in the holiday dimension.
- [ ] Confirm monthly charts sort chronologically.
- [ ] Confirm resolution bands use the intended custom sort order.
- [ ] Confirm percentages display as percentages, not decimal fractions.
- [ ] Confirm all slicers use the intended interactions.
- [ ] Confirm category and sub-category slicers cascade correctly.
- [ ] Confirm national and regional holidays display only in appropriate regions.
- [ ] Confirm the 2025 coverage warning is visible.
- [ ] Confirm Active is labelled as status based.
- [ ] Confirm reported and calculated SLA measures remain separate.
- [ ] Confirm customer-count measures are not used as trusted unique-customer KPIs.
- [ ] Confirm missing CSAT is not converted to zero.
- [ ] Confirm colours are consistent across pages.
- [ ] Confirm each page has a clear decision purpose and reset button.

---

## Suggested management interpretation

Prioritise issue combinations with:

- high ticket volume;
- long median and P90 resolution time;
- high escalation rate;
- high reported SLA breach rate;
- low CSAT;
- concentrated holiday or weekend deterioration.

Interpret combinations as follows:

| Pattern | Likely decision focus |
|---|---|
| High volume, normal resolution | Demand reduction, self-service or automation |
| High volume, slow resolution | Process redesign, staffing or product remediation |
| Low volume, very slow resolution | Specialist capability or escalation guidance |
| Stable median, rising P90 | Long-tail complex-ticket deterioration |
| High SLA mismatch | SLA governance and calculation definition |
| Holiday demand or performance deterioration | Roster, coverage and specialist availability |
| Missing or unmapped categories | Data capture, taxonomy maintenance and training |

---

## Limitations

- A native `.pbix` must be created and saved in Microsoft Power BI Desktop.
- The supplied dashboard pack is import-ready but is not itself a native `.pbix`.
- 2025 data coverage is insufficient for full-year comparison.
- The customer identifier is not a trusted person-level key.
- Status-based workload is not confirmed backlog.
- SLA flags require business-rule validation.
- Statistical comparisons identify associations, not causation.

---

## Final deliverable

Save the completed Power BI report as:

```text
TechSolve_Operations_Dashboard_2024_2025.pbix
```

Recommended audience:

- Operations Manager
- Support Team Leads
- Service Owners
- Product and Engineering Owners
- Billing and Subscription Operations
- Security and Risk
- Data Governance
