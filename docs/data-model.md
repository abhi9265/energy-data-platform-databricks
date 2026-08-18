# Data Model

The first version will model energy operations around a star-schema approach.

## Planned Dimensions

- `dim_customer`
- `dim_meter`
- `dim_location`
- `dim_date`
- `dim_energy_product`

## Planned Facts

- `fact_meter_reading`
- `fact_energy_revenue`
- `fact_billing_statement`

## Initial Business Metrics

- total energy consumption
- daily / monthly revenue
- average consumption per meter
- meter reading completeness
- billing variance
- data-quality rejection rate
