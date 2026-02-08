# Grafana Dashboard for Shelly 3EM

This directory contains a pre-configured Grafana dashboard for monitoring Shelly 3EM three-phase energy monitor.

## Dashboard File

**`grafana.json`** - Ready-to-import Grafana dashboard configuration with all necessary panels and queries for Shelly 3EM monitoring.

## Dashboard Features

The dashboard provides comprehensive visualization of:
- **Real-time power consumption** by phase (A, B, C)
- **Voltage and current** monitoring across all phases
- **Total energy consumption** counters
- **Power factor** and frequency metrics
- **System metrics** (temperature, uptime, WiFi signal)
- **Load balancing** visualization across phases

## How to Import Dashboard

### Method 1: Via Grafana UI

1. Open Grafana in your browser (default: `http://localhost:3000`)
2. Log in with your credentials
3. Click on **"+"** icon in the left sidebar
4. Select **"Import"**
5. Click **"Upload JSON file"**
6. Select `grafana.json` from this directory
7. Select your Prometheus data source
8. Click **"Import"**

### Method 2: Via Command Line

Copy the dashboard to Grafana's provisioning directory:

```bash
sudo cp grafana.json /etc/grafana/provisioning/dashboards/
sudo systemctl restart grafana-server
```

## Dashboard Screenshots

### Overview Panel
![Dashboard Overview](./%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-02-08%20%D0%B2%2014.12.20.png)

Main dashboard view showing all three phases power consumption, voltage, and current metrics.

### Energy Monitoring
![Energy Consumption](./%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-02-08%20%D0%B2%2014.12.39.png)

Detailed energy consumption graphs with historical data and trends.

### System Metrics
![System Status](./%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-02-08%20%D0%B2%2014.12.51.png)

System health monitoring including temperature, WiFi signal strength, and device uptime.

## Dashboard Customization

### Available Variables

The dashboard includes template variables that can be customized:
- `device` - Select specific Shelly device (useful for multi-device setup)
- `time_range` - Quick time range selection
- `refresh_interval` - Auto-refresh settings

### Adding New Panels

To add custom panels:
1. Click **"Add panel"** button
2. Use PromQL queries from `useful_promql_queries.md`
3. Configure visualization type (Graph, Gauge, Stat, etc.)
4. Save the dashboard

### Customizing Thresholds

Adjust alert thresholds for your needs:
- Voltage: Min/Max acceptable values
- Current: Overcurrent warnings
- Temperature: Overheating alerts
- Power Factor: Efficiency warnings

## Useful PromQL Queries

Common queries used in the dashboard:

```promql
# Total power consumption
shelly_total_active_power_watts{device="shelly_192_168_10_69"}

# Power by phase
shelly_phase_a_active_power_watts{device="shelly_192_168_10_69"}

# Energy consumption rate (per hour)
rate(shelly_total_active_energy_wh{device="shelly_192_168_10_69"}[1h]) * 3600

# Voltage across all phases
{__name__=~"shelly_phase_[abc]_voltage_volts"}

# Load imbalance indicator
stddev({__name__=~"shelly_phase_[abc]_current_amperes"})
```

For more queries, see: [`useful_promql_queries.md`](../useful_promql_queries.md)

## Dashboard Settings

### Recommended Refresh Intervals
- **Real-time monitoring:** 5-10 seconds
- **General usage:** 30 seconds to 1 minute
- **Historical analysis:** 5 minutes or more

### Time Ranges
- **Last 15 minutes** - Quick status check
- **Last 1 hour** - Recent activity monitoring
- **Last 24 hours** - Daily consumption patterns
- **Last 7 days** - Weekly trends analysis
- **Last 30 days** - Monthly consumption overview

## Alert Configuration

### Setting Up Alerts

1. Open panel menu → **"Edit"**
2. Go to **"Alert"** tab
3. Configure alert rule:
   - **Condition:** Define threshold
   - **Evaluation:** Set check interval
   - **Notifications:** Configure alert channels

### Example Alert Rules

**High Power Consumption:**
```
shelly_total_active_power_watts > 5000 for 5m
```

**Voltage Out of Range:**
```
shelly_phase_a_voltage_volts < 200 OR shelly_phase_a_voltage_volts > 240
```

**Device Offline:**
```
up{job="shelly_json"} == 0
```

## Troubleshooting

### No Data Displayed

1. **Check Prometheus data source:**
   - Settings → Data Sources → Test
   
2. **Verify metrics are being scraped:**
   - Open Prometheus: `http://localhost:9090`
   - Go to Status → Targets
   - Ensure `shelly_json` target is UP

3. **Check time range:**
   - Ensure selected time range includes scraped data

### Dashboard Not Loading

1. Check Grafana logs:
```bash
sudo journalctl -u grafana-server -f
```

2. Verify JSON file is valid:
```bash
jq . grafana.json
```

### Missing Panels

Ensure your Prometheus data source is correctly configured with the appropriate label matchers matching your device configuration.

## Exporting Dashboard

### Export Current Configuration

1. Open dashboard
2. Click dashboard settings (gear icon)
3. Select **"JSON Model"**
4. Click **"Copy to Clipboard"** or **"Save to file"**

### Share Dashboard

- **Snapshot:** Create a point-in-time view to share
- **Link:** Share direct URL (requires access permissions)
- **Export JSON:** Share configuration file

## Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)

## Dashboard Updates

To update the dashboard after modifications:
1. Make your changes in Grafana UI
2. Export JSON (Settings → JSON Model)
3. Replace `grafana.json` with new version
4. Commit changes to repository

## Support

For issues or questions:
- Check [INSTALL.md](../INSTALL.md) for setup instructions
- Review [README.md](../README.md) for system overview
- Consult Grafana documentation for specific UI questions
