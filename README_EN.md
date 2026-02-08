# Shelly 3EM JSON Exporter for Prometheus

## Description

A project for monitoring the three-phase energy monitor **Shelly 3EM** using **Prometheus** and **JSON Exporter**. The system converts the Shelly 3EM device's JSON API into Prometheus format metrics for subsequent analysis and visualization.

## Architecture

```
Shelly 3EM Device (192.168.10.69)
          ↓ (HTTP JSON API)
    JSON Exporter (127.0.0.1:7979)
          ↓ (Prometheus metrics)
    Prometheus (localhost:9090)
          ↓
    Grafana / Dashboards
```

## Project Structure

```
.
├── json_exporter/
│   └── config.yml          # JSON Exporter configuration
└── prometheus/
    └── prometheus.yml      # Prometheus configuration
```

## Components

### 1. JSON Exporter
JSON Exporter polls the Shelly 3EM device's JSON API and converts the data into Prometheus metrics.

**Device endpoint:** `http://192.168.10.69/rpc/Shelly.GetStatus`

**Port:** `7979`

### 2. Prometheus
Collects metrics from JSON Exporter every 15 seconds.

**Port:** `9090`

## Collected Metrics

### Phase Metrics (A, B, C)
The following metrics are collected for each phase:

- **Current** (`shelly_phase_{a|b|c}_current_amperes`) - Phase current in amperes
- **Voltage** (`shelly_phase_{a|b|c}_voltage_volts`) - Phase voltage in volts
- **Active Power** (`shelly_phase_{a|b|c}_active_power_watts`) - Active power in watts
- **Apparent Power** (`shelly_phase_{a|b|c}_apparent_power_va`) - Apparent power in volt-amperes
- **Power Factor** (`shelly_phase_{a|b|c}_power_factor`) - Power factor
- **Frequency** (`shelly_phase_{a|b|c}_frequency_hertz`) - Frequency in hertz
- **Total Energy** (`shelly_phase_{a|b|c}_total_active_energy_wh`) - Accumulated energy in watt-hours

### Total Metrics
- **Total Current** (`shelly_total_current_amperes`) - Sum of all phase currents
- **Total Active Power** (`shelly_total_active_power_watts`) - Total active power
- **Total Apparent Power** (`shelly_total_apparent_power_va`) - Total apparent power
- **Total Energy** (`shelly_total_active_energy_wh`) - Total consumed energy

### System Metrics
- **Uptime** (`shelly_uptime_seconds`) - Device uptime in seconds
- **Free RAM** (`shelly_ram_free_bytes`) - Free RAM in bytes
- **Temperature** (`shelly_temperature_celsius`) - Device temperature in degrees Celsius

### Network Metrics
- **WiFi RSSI** (`shelly_wifi_rssi_dbm`) - WiFi signal level in dBm
- **WiFi Status** (`shelly_wifi_status`) - WiFi connection status (1 = connected)
- **Cloud Status** (`shelly_cloud_connected`) - Cloud connection status
- **MQTT Status** (`shelly_mqtt_connected`) - MQTT connection status

## Configuration

### Shelly 3EM Device
- **IP Address:** 192.168.10.69
- **MAC Address:** 34987A468050
- **API Endpoint:** `/rpc/Shelly.GetStatus`

### Prometheus
- **Scrape Interval:** 15 seconds
- **Job Name:** `shelly_json`
- **Module:** `shelly_3em`

### Labels
Each metric contains standard labels:
- `mac` - Device MAC address
- `device` - Device identifier (shelly_192_168_10_69)
- `shelly_mac` - Shelly MAC address (34987A468050)
- `phase` - Phase (a/b/c) for phase metrics
- `ssid` - WiFi SSID for WiFi metrics

## Installation and Deployment

### Prerequisites
- Prometheus
- [JSON Exporter](https://github.com/prometheus-community/json_exporter)
- Shelly 3EM device on local network

### Running JSON Exporter
```bash
json_exporter --config.file=json_exporter/config.yml
```

### Running Prometheus
```bash
prometheus --config.file=prometheus/prometheus.yml
```

### Health Check
1. JSON Exporter: `http://127.0.0.1:7979/metrics`
2. Prometheus: `http://localhost:9090`
3. Targets: `http://localhost:9090/targets`

## PromQL Query Examples

### Current Power Consumption by Phase
```promql
shelly_phase_a_active_power_watts{device="shelly_192_168_10_69"}
shelly_phase_b_active_power_watts{device="shelly_192_168_10_69"}
shelly_phase_c_active_power_watts{device="shelly_192_168_10_69"}
```

### Total Power Consumption
```promql
shelly_total_active_power_watts{device="shelly_192_168_10_69"}
```

### Energy Consumption Over Last Hour
```promql
rate(shelly_total_active_energy_wh{device="shelly_192_168_10_69"}[1h]) * 3600
```

### Voltage Across All Phases
```promql
shelly_phase_a_voltage_volts{device="shelly_192_168_10_69"}
shelly_phase_b_voltage_volts{device="shelly_192_168_10_69"}
shelly_phase_c_voltage_volts{device="shelly_192_168_10_69"}
```

### Load Balance by Phase
```promql
avg(shelly_phase_a_current_amperes{device="shelly_192_168_10_69"})
avg(shelly_phase_b_current_amperes{device="shelly_192_168_10_69"})
avg(shelly_phase_c_current_amperes{device="shelly_192_168_10_69"})
```

## Using with Grafana

For metrics visualization, it's recommended to use Grafana with Prometheus as a data source. You can create dashboards to display:
- Power consumption graphs by phase
- Total power consumption
- Voltage and current
- Energy counters
- System metrics (temperature, uptime, WiFi signal)

## Notes

- All phase data is extracted from the `em:0` object in Shelly's JSON response
- Energy counter data is extracted from the `emdata:0` object
- Scrape frequency is set to 15 seconds to balance data freshness and device load
- Device MAC address is used as the primary label for identification

## Useful Links

- [Shelly 3EM Documentation](https://shelly-api-docs.shelly.cloud/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [JSON Exporter](https://github.com/prometheus-community/json_exporter)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## License

This project is created for personal use and energy consumption monitoring.
