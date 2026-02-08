#!/usr/bin/env python3
"""
Prometheus Metrics to PNG Exporter - Extended version with CLI arguments
"""

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import argparse
import json
import os
from pathlib import Path


class PrometheusExporter:
    def __init__(self, prometheus_url, output_dir, time_range, step):
        self.prometheus_url = prometheus_url
        self.output_dir = output_dir
        self.time_range = time_range
        self.step = step
        
    def parse_time_range(self):
        """Convert time range string to seconds"""
        units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        
        if self.time_range[-1] in units:
            value = int(self.time_range[:-1])
            unit = self.time_range[-1]
            return value * units[unit]
        else:
            raise ValueError(f"Invalid time range format: {self.time_range}")
    
    def query_prometheus(self, query):
        """Query Prometheus and return data"""
        url = f"{self.prometheus_url}/api/v1/query_range"
        
        end_time = datetime.now()
        start_time = end_time - timedelta(seconds=self.parse_time_range())
        
        params = {
            'query': query,
            'start': start_time.timestamp(),
            'end': end_time.timestamp(),
            'step': self.step
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
    
    def plot_metric(self, metric_data, title, ylabel, filename, show_legend=False):
        """Create and save plot for metric data"""
        
        if not metric_data:
            print(f"No data for {title}, skipping...")
            return False
        
        plt.figure(figsize=(14, 7))
        
        for series in metric_data:
            timestamps = [datetime.fromtimestamp(float(point[0])) for point in series['values']]
            values = [float(point[1]) for point in series['values']]
            
            # Create label from metric labels
            labels = series.get('metric', {})
            if 'phase' in labels:
                label = f"Phase {labels['phase'].upper()}"
            elif '__name__' in labels:
                label = labels['__name__'].replace('shelly_', '').replace('_', ' ').title()
            else:
                label = None
            
            plt.plot(timestamps, values, marker='o', markersize=2, linewidth=2, label=label)
        
        plt.xlabel('Time', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
        
        if show_legend and len(metric_data) > 1:
            plt.legend(loc='best', fontsize=10)
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path}")
        return True
    
    def export_metrics(self, metrics_config):
        """Export all metrics from configuration"""
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"Querying Prometheus at {self.prometheus_url}")
        print(f"Time range: {self.time_range}, Step: {self.step}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 60)
        
        success_count = 0
        fail_count = 0
        
        for metric in metrics_config:
            query = metric['query']
            title = metric['title']
            ylabel = metric['ylabel']
            filename = metric['filename']
            show_legend = metric.get('legend', False)
            
            print(f"Processing: {title}...", end=' ')
            
            data = self.query_prometheus(query)
            
            if data and self.plot_metric(data, title, ylabel, filename, show_legend):
                success_count += 1
            else:
                print(f"✗ FAILED")
                fail_count += 1
        
        print("-" * 60)
        print(f"Completed: {success_count} successful, {fail_count} failed")
        print(f"Graphs saved to: {self.output_dir}/")


def load_metrics_config(config_file):
    """Load metrics configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        return None


def get_default_metrics():
    """Return default metrics configuration"""
    return [
        {
            "query": "shelly_total_active_power_watts_power",
            "title": "Total Active Power",
            "ylabel": "Power (W)",
            "filename": "total_power.png"
        },
        {
            "query": '{__name__=~"shelly_phase_[abc]_active_power_watts_power"}',
            "title": "Phase Active Power",
            "ylabel": "Power (W)",
            "filename": "phase_powers.png",
            "legend": True
        },
        {
            "query": '{__name__=~"shelly_phase_[abc]_current_amperes_current"}',
            "title": "Phase Currents",
            "ylabel": "Current (A)",
            "filename": "phase_currents.png",
            "legend": True
        },
        {
            "query": '{__name__=~"shelly_phase_[abc]_voltage_volts_voltage"}',
            "title": "Phase Voltages",
            "ylabel": "Voltage (V)",
            "filename": "phase_voltages.png",
            "legend": True
        },
        {
            "query": '{__name__=~"shelly_phase_[abc]_power_factor_pf"}',
            "title": "Power Factor by Phase",
            "ylabel": "Power Factor",
            "filename": "power_factor.png",
            "legend": True
        },
        {
            "query": "rate(shelly_total_active_energy_wh_energy[5m]) * 60 / 1000",
            "title": "Energy Consumption Rate",
            "ylabel": "kWh/hour",
            "filename": "energy_rate.png"
        },
        {
            "query": "shelly_temperature_celsius_temperature",
            "title": "Device Temperature",
            "ylabel": "Temperature (°C)",
            "filename": "temperature.png"
        },
        {
            "query": "shelly_wifi_rssi_dbm_rssi",
            "title": "WiFi Signal Strength",
            "ylabel": "RSSI (dBm)",
            "filename": "wifi_rssi.png"
        },
    ]


def main():
    parser = argparse.ArgumentParser(
        description='Export Prometheus metrics as PNG graphs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --url http://prometheus:9090 --time 24h
  %(prog)s --config metrics.json --output /tmp/graphs
  %(prog)s --time 7d --step 5m
        """
    )
    
    parser.add_argument(
        '--url',
        default='http://localhost:9090',
        help='Prometheus URL (default: http://localhost:9090)'
    )
    
    parser.add_argument(
        '--output',
        default='prometheus_graphs',
        help='Output directory for graphs (default: prometheus_graphs)'
    )
    
    parser.add_argument(
        '--time',
        default='1h',
        help='Time range: 1h, 6h, 12h, 24h, 7d, 30d (default: 1h)'
    )
    
    parser.add_argument(
        '--step',
        default='15s',
        help='Query resolution step (default: 15s)'
    )
    
    parser.add_argument(
        '--config',
        help='JSON config file with metrics definitions'
    )
    
    args = parser.parse_args()
    
    # Load metrics configuration
    if args.config:
        metrics = load_metrics_config(args.config)
        if not metrics:
            return 1
    else:
        metrics = get_default_metrics()
    
    # Create exporter and run
    exporter = PrometheusExporter(
        prometheus_url=args.url,
        output_dir=args.output,
        time_range=args.time,
        step=args.step
    )
    
    exporter.export_metrics(metrics)
    return 0


if __name__ == "__main__":
    exit(main())
