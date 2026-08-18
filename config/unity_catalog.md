# Unity Catalog Conventions

## Three-level namespace

All production tables should use:

`<catalog>.<schema>.<table>`

## Catalogs

- `energy_dev`
- `energy_test`
- `energy_prod`

## Schemas

- `bronze`
- `silver`
- `gold`
- `ops`

## Naming

| Layer | Example |
|---|---|
| Bronze | `energy_prod.bronze.energy_meter_readings` |
| Silver | `energy_prod.silver.energy_meter_readings` |
| Gold fact | `energy_prod.gold.fact_energy` |
| Gold dimension | `energy_prod.gold.dim_meter` |
| KPI | `energy_prod.gold.energy_daily_kpis` |
| Audit | `energy_prod.ops.pipeline_audit` |
| Quarantine | `energy_prod.ops.energy_meter_quarantine` |

## Governance

- No credentials or connection strings in source control.
- Production jobs should reference Unity Catalog objects rather than raw workspace paths.
- Access should follow least privilege by environment and layer.
- Gold objects are the supported BI contract; Bronze/Silver are engineering datasets.
