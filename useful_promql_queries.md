# Shelly 3EM Prometheus Metrics - Useful Queries

## Power Metrics

### Individual Phase Power
```promql
# Active power per phase
shelly_phase_a_active_power_watts_power
shelly_phase_b_active_power_watts_power
shelly_phase_c_active_power_watts_power

# All phases using regex
{__name__=~"shelly_phase_[abc]_active_power_watts_power"}

# Apparent power per phase
shelly_phase_a_apparent_power_va_power
shelly_phase_b_apparent_power_va_power
shelly_phase_c_apparent_power_va_power
```

### Total Power
```promql
# Total active power across all phases
shelly_total_active_power_watts_power

# Sum of individual phases
sum({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Total apparent power
shelly_total_apparent_power_va_power
```

### Power Analysis
```promql
# Maximum loaded phase
max({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Minimum loaded phase
min({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Average power per phase
avg({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Phase imbalance (difference between max and min)
max({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) - min({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Phase imbalance percentage
(max({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) - min({__name__=~"shelly_phase_[abc]_active_power_watts_power"})) / avg({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) * 100
```

## Current Metrics

### Individual Phase Current
```promql
# Current per phase
shelly_phase_a_current_amperes_current
shelly_phase_b_current_amperes_current
shelly_phase_c_current_amperes_current

# All phases using regex
{__name__=~"shelly_phase_[abc]_current_amperes_current"}

# Total current
shelly_total_current_amperes_current
```

### Current Analysis
```promql
# Maximum current across phases
max({__name__=~"shelly_phase_[abc]_current_amperes_current"})

# Current imbalance
max({__name__=~"shelly_phase_[abc]_current_amperes_current"}) - min({__name__=~"shelly_phase_[abc]_current_amperes_current"})

# Current exceeding threshold (e.g., 10A)
{__name__=~"shelly_phase_[abc]_current_amperes_current"} > 10

# Phase C high current (based on your data)
shelly_phase_c_current_amperes_current > 10
```

## Voltage Metrics

### Phase Voltage
```promql
# Voltage per phase
shelly_phase_a_voltage_volts_voltage
shelly_phase_b_voltage_volts_voltage
shelly_phase_c_voltage_volts_voltage

# All phases using regex
{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"}

# Voltage drop detection (below 210V)
{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"} < 210

# Voltage spike detection (above 240V)
{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"} > 240
```

### Voltage Analysis
```promql
# Average voltage across phases
avg({__name__=~"shelly_phase_[abc]_voltage_volts_voltage"})

# Voltage imbalance
max({__name__=~"shelly_phase_[abc]_voltage_volts_voltage"}) - min({__name__=~"shelly_phase_[abc]_voltage_volts_voltage"})

# Voltage stability over time (5min average)
avg_over_time(shelly_phase_a_voltage_volts_voltage[5m])
```

## Power Factor Metrics

### Power Factor Monitoring
```promql
# Power factor per phase
shelly_phase_a_power_factor_pf
shelly_phase_b_power_factor_pf
shelly_phase_c_power_factor_pf

# All phases
{__name__=~"shelly_phase_[abc]_power_factor_pf"}

# Low power factor detection (below 0.85)
{__name__=~"shelly_phase_[abc]_power_factor_pf"} < 0.85

# Average power factor
avg({__name__=~"shelly_phase_[abc]_power_factor_pf"})

# Poorest power factor
min({__name__=~"shelly_phase_[abc]_power_factor_pf"})
```

## Frequency Metrics

### Frequency Monitoring
```promql
# Frequency per phase
shelly_phase_a_frequency_hertz_frequency
shelly_phase_b_frequency_hertz_frequency
shelly_phase_c_frequency_hertz_frequency

# All phases
{__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"}

# Frequency deviation from 50Hz
abs({__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"} - 50)

# Frequency out of range (±1Hz)
{__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"} < 49 or {__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"} > 51
```

## Energy Metrics

### Total Energy Consumption
```promql
# Total accumulated energy
shelly_total_active_energy_wh_energy

# Total energy in kWh
shelly_total_active_energy_wh_energy / 1000

# Energy per phase
shelly_phase_a_total_active_energy_wh_energy
shelly_phase_b_total_active_energy_wh_energy
shelly_phase_c_total_active_energy_wh_energy

# All phases energy
{__name__=~"shelly_phase_[abc]_total_active_energy_wh_energy"}
```

### Energy Rate Calculations
```promql
# Energy consumption rate (Wh per minute)
rate(shelly_total_active_energy_wh_energy[5m]) * 60

# Daily energy consumption estimate (kWh/day)
rate(shelly_total_active_energy_wh_energy[1h]) * 24 / 1000

# Hourly energy consumption (last hour)
increase(shelly_total_active_energy_wh_energy[1h]) / 1000

# Daily energy consumption (last 24h)
increase(shelly_total_active_energy_wh_energy[24h]) / 1000

# Monthly energy consumption (last 30d)
increase(shelly_total_active_energy_wh_energy[30d]) / 1000
```

### Energy Cost Calculations
```promql
# Daily cost (assuming $0.15 per kWh)
increase(shelly_total_active_energy_wh_energy[24h]) / 1000 * 0.15

# Monthly cost estimate
increase(shelly_total_active_energy_wh_energy[30d]) / 1000 * 0.15

# Energy cost per phase (daily)
increase(shelly_phase_a_total_active_energy_wh_energy[24h]) / 1000 * 0.15
increase(shelly_phase_b_total_active_energy_wh_energy[24h]) / 1000 * 0.15
increase(shelly_phase_c_total_active_energy_wh_energy[24h]) / 1000 * 0.15
```

## System Metrics

### Device Health
```promql
# Device uptime in hours
shelly_uptime_seconds_uptime / 3600

# Device uptime in days
shelly_uptime_seconds_uptime / 86400

# Free RAM in MB
shelly_ram_free_bytes_ram_free / 1024 / 1024

# Device temperature
shelly_temperature_celsius_temperature

# Temperature warning (above 60°C)
shelly_temperature_celsius_temperature > 60
```

### Connectivity
```promql
# WiFi signal strength
shelly_wifi_rssi_dbm_rssi

# Weak WiFi signal (below -70 dBm)
shelly_wifi_rssi_dbm_rssi < -70

# Cloud connection status (1 = connected, 0 = disconnected)
shelly_cloud_connected_connected

# MQTT connection status
shelly_mqtt_connected_connected
```

## Load Monitoring

### Peak Load Detection
```promql
# Peak power in last hour
max_over_time(shelly_total_active_power_watts_power[1h])

# Peak power in last 24 hours
max_over_time(shelly_total_active_power_watts_power[24h])

# Average load in last hour
avg_over_time(shelly_total_active_power_watts_power[1h])

# Peak per phase in last hour
max_over_time(shelly_phase_a_active_power_watts_power[1h])
max_over_time(shelly_phase_b_active_power_watts_power[1h])
max_over_time(shelly_phase_c_active_power_watts_power[1h])
```

### Load Threshold Alerts
```promql
# Total load exceeding 5kW
shelly_total_active_power_watts_power > 5000

# Any phase exceeding 2kW
{__name__=~"shelly_phase_[abc]_active_power_watts_power"} > 2000

# Total current exceeding 20A
shelly_total_current_amperes_current > 20

# Phase C overload (based on your high current)
shelly_phase_c_active_power_watts_power > 2000
```

## Efficiency Metrics

### Power Efficiency
```promql
# Overall power factor (active/apparent power)
shelly_total_active_power_watts_power / shelly_total_apparent_power_va_power

# Reactive power calculation
sqrt(shelly_total_apparent_power_va_power^2 - shelly_total_active_power_watts_power^2)

# Efficiency loss per phase A
shelly_phase_a_apparent_power_va_power - shelly_phase_a_active_power_watts_power

# Efficiency loss per phase B
shelly_phase_b_apparent_power_va_power - shelly_phase_b_active_power_watts_power

# Efficiency loss per phase C
shelly_phase_c_apparent_power_va_power - shelly_phase_c_active_power_watts_power
```

## Time-based Analysis

### Comparison Queries
```promql
# Current power vs 1 hour ago
shelly_total_active_power_watts_power - shelly_total_active_power_watts_power offset 1h

# Current power vs yesterday same time
shelly_total_active_power_watts_power - shelly_total_active_power_watts_power offset 24h

# Power change rate (W per minute)
deriv(shelly_total_active_power_watts_power[5m]) * 60
```

### Statistical Analysis
```promql
# Standard deviation of power (last hour)
stddev_over_time(shelly_total_active_power_watts_power[1h])

# 95th percentile power (last 24h)
quantile_over_time(0.95, shelly_total_active_power_watts_power[24h])

# Median power (last hour)
quantile_over_time(0.5, shelly_total_active_power_watts_power[1h])
```

## Combined Metrics

### Multi-device Monitoring
```promql
# Total power across all Shelly devices
sum(shelly_total_active_power_watts_power)

# Average power per device
avg(shelly_total_active_power_watts_power) by (mac)

# Power grouped by MAC address
sum(shelly_total_active_power_watts_power) by (mac)
```

### Phase Distribution Analysis
```promql
# Phase A percentage of total
shelly_phase_a_active_power_watts_power / shelly_total_active_power_watts_power * 100

# Phase B percentage of total
shelly_phase_b_active_power_watts_power / shelly_total_active_power_watts_power * 100

# Phase C percentage of total
shelly_phase_c_active_power_watts_power / shelly_total_active_power_watts_power * 100
```

## Alert Expressions

### Critical Alerts
```promql
# Overload alert (>80% of rated capacity, assuming 16A per phase)
{__name__=~"shelly_phase_[abc]_current_amperes_current"} > 13

# Voltage too low
{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"} < 200

# Voltage too high
{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"} > 250

# Device offline (no data for 5 minutes)
absent_over_time(shelly_total_active_power_watts_power[5m])

# High temperature
shelly_temperature_celsius_temperature > 70

# Cloud disconnected
shelly_cloud_connected_connected == 0
```

### Warning Alerts
```promql
# Poor power factor
{__name__=~"shelly_phase_[abc]_power_factor_pf"} < 0.7

# Phase imbalance >50%
(max({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) - min({__name__=~"shelly_phase_[abc]_active_power_watts_power"})) / avg({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) * 100 > 50

# Frequency deviation
abs({__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"} - 50) > 0.5

# Weak WiFi signal
shelly_wifi_rssi_dbm_rssi < -75

# Temperature warning
shelly_temperature_celsius_temperature > 50
```

## Dashboard Recommendations

### Single Panel Queries
```promql
# Current power consumption (gauge)
shelly_total_active_power_watts_power

# Energy today (stat)
increase(shelly_total_active_energy_wh_energy[24h]) / 1000

# Power per phase (graph)
shelly_phase_a_active_power_watts_power
shelly_phase_b_active_power_watts_power
shelly_phase_c_active_power_watts_power

# Current per phase (graph)
shelly_phase_a_current_amperes_current
shelly_phase_b_current_amperes_current
shelly_phase_c_current_amperes_current

# WiFi signal (gauge)
shelly_wifi_rssi_dbm_rssi

# Device temperature (gauge)
shelly_temperature_celsius_temperature
```

### Grafana Variables
```promql
# For device selection
label_values(shelly_total_active_power_watts_power, mac)

# For SSID selection
label_values(shelly_wifi_rssi_dbm_rssi, ssid)
```

### Example Grafana Panel Queries
```promql
# Total power with phases stacked
sum({__name__=~"shelly_phase_[abc]_active_power_watts_power"})

# Individual phases for comparison
{__name__=~"shelly_phase_[abc]_active_power_watts_power"}

# Power factor by phase
{__name__=~"shelly_phase_[abc]_power_factor_pf"}

# Energy consumption rate (kW)
rate(shelly_total_active_energy_wh_energy[5m]) / 1000 * 60
```
