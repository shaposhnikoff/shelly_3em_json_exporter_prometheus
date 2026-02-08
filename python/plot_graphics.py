#!/usr/bin/env python3
"""
Prometheus Metrics to PNG Exporter
Queries Prometheus metrics and saves them as PNG images using matplotlib
"""

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Configuration
PROMETHEUS_URL = "http://localhost:9090"  # Change to your Prometheus URL
OUTPUT_DIR = "prometheus_graphs"
TIME_RANGE = "1h"  # Options: 1h, 6h, 12h, 24h, 7d, 30d
STEP = "15s"  # Query resolution

# Metrics to query
METRICS = [
    # Power metrics
    {
        "query": "shelly_phase_a_active_power_watts_power",
        "title": "Phase A Active Power",
        "ylabel": "Power (W)",
        "filename": "phase_a_power.png"
    },
    {
        "query": "shelly_phase_b_active_power_watts_power",
        "title": "Phase B Active Power",
        "ylabel": "Power (W)",
        "filename": "phase_b_power.png"
    },
    {
        "query": "shelly_phase_c_active_power_watts_power",
        "title": "Phase C Active Power",
        "ylabel": "Power (W)",
        "filename": "phase_c_power.png"
    },
    {
        "query": "shelly_total_active_power_watts_power",
        "title": "Total Active Power",
        "ylabel": "Power (W)",
        "filename": "total_power.png"
    },
    # Current metrics
    {
        "query": '{__name__=~"shelly_phase_[abc]_current_amperes_current"}',
        "title": "Phase Currents",
        "ylabel": "Current (A)",
        "filename": "phase_currents.png",
        "legend": True
    },
    # Voltage metrics
    {
        "query": '{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"}',
        "title": "Phase Voltages",
        "ylabel": "Voltage (V)",
        "filename": "phase_voltages.png",
        "legend": True
    },
    # Power factor
    {
        "query": '{__name__=~"shelly_phase_[abc]_power_factor_pf"}',
        "title": "Power Factor by Phase",
        "ylabel": "Power Factor",
        "filename": "power_factor.png",
        "legend": True
    },
    # Frequency
    {
        "query": '{__name__=~"shelly_phase_[abc]_frequency_hertz_frequency"}',
        "title": "Frequency by Phase",
        "ylabel": "Frequency (Hz)",
        "filename": "frequency.png",
        "legend": True
    },
    # Energy consumption rate
    {
        "query": "rate(shelly_total_active_energy_wh_energy[5m]) * 60",
        "title": "Energy Consumption Rate",
        "ylabel": "Wh/min",
        "filename": "energy_rate.png"
    },
    # Temperature
    {
        "query": "shelly_temperature_celsius_temperature",
        "title": "Device Temperature",
        "ylabel": "Temperature (°C)",
        "filename": "temperature.png"
    },
    # WiFi signal
    {
        "query": "shelly_wifi_rssi_dbm_rssi",
        "title": "WiFi Signal Strength",
        "ylabel": "RSSI (dBm)",
        "filename": "wifi_rssi.png"
    },
    # Phase imbalance
    {
        "query": '(max({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) - min({__name__=~"shelly_phase_[abc]_active_power_watts_power"})) / avg({__name__=~"shelly_phase_[abc]_active_power_watts_power"}) * 100',
        "title": "Phase Imbalance",
        "ylabel": "Imbalance (%)",
        "filename": "phase_imbalance.png"
    },
]


def parse_time_range(time_range):
    """Convert time range string to seconds"""
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }
    
    if time_range[-1] in units:
        value = int(time_range[:-1])
        unit = time_range[-1]
        return value * units[unit]
    else:
        raise ValueError(f"Invalid time range format: {time_range}")


def query_prometheus(query, time_range, step):
    """Query Prometheus and return data"""
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    
    end_time = datetime.now()
    start_time = end_time - timedelta(seconds=parse_time_range(time_range))
    
    params = {
        'query': query,
        'start': start_time.timestamp(),
        'end': end_time.timestamp(),
        'step': step
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'success':
            print(f"Error querying Prometheus: {data}")
            return None
            
        return data['data']['result']
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Prometheus: {e}")
        return None


def plot_metric(metric_data, title, ylabel, filename, show_legend=False):
    """Create and save plot for metric data"""
    
    if not metric_data:
        print(f"No data for {title}, skipping...")
        return
    
    plt.figure(figsize=(12, 6))
    
    for series in metric_data:
        timestamps = [datetime.fromtimestamp(float(point[0])) for point in series['values']]
        values = [float(point[1]) for point in series['values']]
        
        # Create label from metric labels
        labels = series.get('metric', {})
        if 'phase' in labels:
            label = f"Phase {labels['phase'].upper()}"
        elif '__name__' in labels:
            label = labels['__name__'].replace('shelly_phase_', '').replace('_', ' ').title()
        else:
            label = None
        
        plt.plot(timestamps, values, marker='o', markersize=2, linewidth=1.5, label=label)
    
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    if show_legend and len(metric_data) > 1:
        plt.legend()
    
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {output_path}")


def main():
    """Main function"""
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    print(f"Querying Prometheus at {PROMETHEUS_URL}")
    print(f"Time range: {TIME_RANGE}, Step: {STEP}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for metric in METRICS:
        query = metric['query']
        title = metric['title']
        ylabel = metric['ylabel']
        filename = metric['filename']
        show_legend = metric.get('legend', False)
        
        print(f"Processing: {title}...", end=' ')
        
        data = query_prometheus(query, TIME_RANGE, STEP)
        
        if data:
            plot_metric(data, title, ylabel, filename, show_legend)
            success_count += 1
        else:
            print(f"FAILED")
            fail_count += 1
    
    print("-" * 60)
    print(f"Completed: {success_count} successful, {fail_count} failed")
    print(f"Graphs saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
