# Shelly 3EM Prometheus Metrics - Useful Queries

## Power Metrics

### Individual Phase Power
```promql
# Active power per phase
shelly_phase_active_power_watts

# Specific phase
shelly_phase_active_power_watts{phase="a"}
shelly_phase_active_power_watts{phase="b"}
shelly_phase_active_power_watts{phase="c"}

# Apparent power per phase
shelly_phase_apparent_power_va
```

### Total Power
```promql
# Total active power across all phases
shelly_total_active_power_watts

# Sum of individual phases
sum(shelly_phase_active_power_watts)

# Total apparent power
shelly_total_apparent_power_va
```

### Power Analysis
```promql
# Maximum loaded phase
max(shelly_phase_active_power_watts)

# Minimum loaded phase
min(shelly_phase_active_power_watts)

# Average power per phase
avg(shelly_phase_active_power_watts)

# Phase imbalance (difference between max and min)
max(shelly_phase_active_power_watts) - min(shelly_phase_active_power_watts)

# Phase imbalance percentage
(max(shelly_phase_active_power_watts) - min(shelly_phase_active_power_watts)) / avg(shelly_phase_active_power_watts) * 100
```

## Current Metrics

### Individual Phase Current
```promql
# Current per phase
shelly_phase_current_amperes

# Specific phase current
shelly_phase_current_amperes{phase="a"}
shelly_phase_current_amperes{phase="b"}
shelly_phase_current_amperes{phase="c"}

# Total current
shelly_total_current_amperes
```

### Current Analysis
```promql
# Maximum current across phases
max(shelly_phase_current_amperes)

# Current imbalance
max(shelly_phase_current_amperes) - min(shelly_phase_current_amperes)

# Current exceeding threshold (e.g., 10A)
shelly_phase_current_amperes > 10
```

## Voltage Metrics

### Phase Voltage
```promql
# Voltage per phase
shelly_phase_voltage_volts

# Specific phase voltage
shelly_phase_voltage_volts{phase="a"}

# Voltage drop detection (below 210V)
shelly_phase_voltage_volts < 210

# Voltage spike detection (above 240V)
shelly_phase_voltage_volts > 240
```

### Voltage Analysis
```promql
# Average voltage across phases
avg(shelly_phase_voltage_volts)

# Voltage imbalance
max(shelly_phase_voltage_volts) - min(shelly_phase_voltage_volts)

# Voltage stability over time (5min average)
avg_over_time(shelly_phase_voltage_volts[5m])
```

## Power Factor Metrics

### Power Factor Monitoring
```promql
# Power factor per phase
shelly_phase_power_factor

# Low power factor detection (below 0.85)
shelly_phase_power_factor < 0.85

# Average power factor
avg(shelly_phase_power_factor)

# Poorest power factor
min(shelly_phase_power_factor)
```

## Frequency Metrics

### Frequency Monitoring
```promql
# Frequency per phase
shelly_phase_frequency_hertz

# Frequency deviation from 50Hz
abs(shelly_phase_frequency_hertz - 50)

# Frequency out of range (±1Hz)
shelly_phase_frequency_hertz < 49 or shelly_phase_frequency_hertz > 51
```

## Energy Metrics

### Total Energy Consumption
```promql
# Total accumulated energy
shelly_total_active_energy_wh

# Total energy in kWh
shelly_total_active_energy_wh / 1000

# Energy per phase
shelly_phase_total_active_energy_wh
```

### Energy Rate Calculations
```promql
# Energy consumption rate (Wh per minute)
rate(shelly_total_active_energy_wh[5m]) * 60

# Daily energy consumption estimate (kWh/day)
rate(shelly_total_active_energy_wh[1h]) * 24 / 1000

# Hourly energy consumption (last hour)
increase(shelly_total_active_energy_wh[1h]) / 1000

# Daily energy consumption (last 24h)
increase(shelly_total_active_energy_wh[24h]) / 1000

# Monthly energy consumption (last 30d)
increase(shelly_total_active_energy_wh[30d]) / 1000
```

### Energy Cost Calculations
```promql
# Daily cost (assuming $0.15 per kWh)
increase(shelly_total_active_energy_wh[24h]) / 1000 * 0.15

# Monthly cost estimate
increase(shelly_total_active_energy_wh[30d]) / 1000 * 0.15
```

## System Metrics

### Device Health
```promql
# Device uptime in hours
shelly_uptime_seconds / 3600

# Device uptime in days
shelly_uptime_seconds / 86400

# Free RAM in MB
shelly_ram_free_bytes / 1024 / 1024

# RAM usage percentage (if ram_size is available)
(1 - (shelly_ram_free_bytes / shelly_ram_size_bytes)) * 100

# Device temperature
shelly_temperature_celsius

# Temperature warning (above 60°C)
shelly_temperature_celsius > 60
```

### Connectivity
```promql
# WiFi signal strength
shelly_wifi_rssi_dbm

# Weak WiFi signal (below -70 dBm)
shelly_wifi_rssi_dbm < -70

# Cloud connection status (1 = connected, 0 = disconnected)
shelly_cloud_connected

# MQTT connection status
shelly_mqtt_connected
```

## Load Monitoring

### Peak Load Detection
```promql
# Peak power in last hour
max_over_time(shelly_total_active_power_watts[1h])

# Peak power in last 24 hours
max_over_time(shelly_total_active_power_watts[24h])

# Average load in last hour
avg_over_time(shelly_total_active_power_watts[1h])
```

### Load Threshold Alerts
```promql
# Total load exceeding 5kW
shelly_total_active_power_watts > 5000

# Any phase exceeding 2kW
shelly_phase_active_power_watts > 2000

# Total current exceeding 20A
shelly_total_current_amperes > 20
```

## Efficiency Metrics

### Power Efficiency
```promql
# Overall power factor (active/apparent power)
shelly_total_active_power_watts / shelly_total_apparent_power_va

# Reactive power calculation
sqrt(shelly_total_apparent_power_va^2 - shelly_total_active_power_watts^2)

# Efficiency loss per phase
shelly_phase_apparent_power_va - shelly_phase_active_power_watts
```

## Time-based Analysis

### Comparison Queries
```promql
# Current power vs 1 hour ago
shelly_total_active_power_watts - shelly_total_active_power_watts offset 1h

# Current power vs yesterday same time
shelly_total_active_power_watts - shelly_total_active_power_watts offset 24h

# Power change rate (W per minute)
deriv(shelly_total_active_power_watts[5m]) * 60
```

### Statistical Analysis
```promql
# Standard deviation of power (last hour)
stddev_over_time(shelly_total_active_power_watts[1h])

# 95th percentile power (last 24h)
quantile_over_time(0.95, shelly_total_active_power_watts[24h])

# Median power (last hour)
quantile_over_time(0.5, shelly_total_active_power_watts[1h])
```

## Combined Metrics

### Multi-device Monitoring
```promql
# Total power across all Shelly devices
sum(shelly_total_active_power_watts)

# Average power per device
avg(shelly_total_active_power_watts) by (mac)

# Top 5 power consumers
topk(5, shelly_total_active_power_watts)
```

### Correlation Analysis
```promql
# Power vs Temperature correlation
shelly_total_active_power_watts and shelly_temperature_celsius

# Devices with high power and high temperature
shelly_total_active_power_watts > 3000 and shelly_temperature_celsius > 50
```

## Alert Expressions

### Critical Alerts
```promql
# Overload alert (>80% of rated capacity, assuming 25A per phase)
shelly_phase_current_amperes > 20

# Voltage too low
shelly_phase_voltage_volts < 200

# Voltage too high
shelly_phase_voltage_volts > 250

# Device offline (no data for 5 minutes)
absent_over_time(shelly_total_active_power_watts[5m])

# High temperature
shelly_temperature_celsius > 70
```

### Warning Alerts
```promql
# Poor power factor
shelly_phase_power_factor < 0.7

# Phase imbalance >30%
(max(shelly_phase_active_power_watts) - min(shelly_phase_active_power_watts)) / avg(shelly_phase_active_power_watts) * 100 > 30

# Frequency deviation
abs(shelly_phase_frequency_hertz - 50) > 0.5

# Weak WiFi signal
shelly_wifi_rssi_dbm < -75
```

## Dashboard Recommendations

### Single Panel Queries
```promql
# Current power consumption (gauge)
shelly_total_active_power_watts

# Energy today (stat)
increase(shelly_total_active_energy_wh[24h]) / 1000

# Power per phase (graph)
shelly_phase_active_power_watts

# Voltage per phase (graph)
shelly_phase_voltage_volts

# Current per phase (graph)
shelly_phase_current_amperes
```

### Multi-Panel Dashboard Layout
1. **Overview Panel**: Total power, current, voltage
2. **Phase Details**: Individual phase metrics (A, B, C)
3. **Energy Panel**: Daily/monthly consumption and cost
4. **Health Panel**: Temperature, uptime, connectivity
5. **Quality Panel**: Power factor, frequency, imbalance
6. **Alerts Panel**: Active warnings and critical conditions
