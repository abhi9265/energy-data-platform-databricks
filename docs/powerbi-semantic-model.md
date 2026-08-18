# Power BI Semantic Layer

The Gold layer is the contract for the BI semantic model.

## Core model

- `fact_energy` — atomic energy consumption
- `dim_meter` — meter and region attributes
- `dim_date` — calendar slicing
- `energy_daily_kpis` — pre-aggregated daily regional KPIs

## Recommended relationships

```text
DimDate[date_key] 1 ─── * FactEnergy[date_key]
DimMeter[meter_key] 1 ─── * FactEnergy[meter_key]
```

## Measures

### Total Energy (kWh)

`SUM(fact_energy[energy_kwh])`

### Active Meters

`DISTINCTCOUNT(fact_energy[meter_id])`

### Average Reading (kWh)

`AVERAGE(fact_energy[energy_kwh])`

### kWh per Active Meter

`DIVIDE([Total Energy (kWh)], [Active Meters])`

### Reading Completeness

Compare expected readings against actual reading count at the selected meter/date grain.

## Dashboard pages

1. Executive Energy Overview
2. Regional Consumption
3. Meter Performance
4. Data Quality & Pipeline Health
5. Trend Analysis

The semantic model should consume Gold tables only and should not contain transformation logic that belongs in Spark/SQL pipelines.
