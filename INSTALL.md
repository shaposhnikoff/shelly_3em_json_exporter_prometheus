# Installation Guide

Complete installation guide for setting up Shelly 3EM monitoring system with Prometheus, JSON Exporter, and Grafana.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installing Prometheus](#installing-prometheus)
- [Installing JSON Exporter](#installing-json-exporter)
- [Installing Grafana](#installing-grafana)
- [Configuration](#configuration)
- [Starting Services](#starting-services)

## Prerequisites

**System Requirements:**
- Raspberry Pi (or any Linux-based system)
- Internet connection
- Root or sudo access

**Update your system:**
```bash
sudo apt update
sudo apt upgrade -y
```

## Installing Prometheus

### Option 1: Using Package Manager (Recommended for Raspberry Pi)

1. Download the latest Prometheus release for ARM architecture:
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-armv7.tar.gz
```

2. Extract the archive:
```bash
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

3. Move binaries to system path:
```bash
sudo mv prometheus /usr/local/bin/
sudo mv promtool /usr/local/bin/
```

4. Create Prometheus user and directories:
```bash
sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
```

5. Copy configuration files:
```bash
sudo cp -r consoles /etc/prometheus
sudo cp -r console_libraries /etc/prometheus
sudo cp prometheus.yml /etc/prometheus/
```

6. Set ownership:
```bash
sudo chown -R prometheus:prometheus /etc/prometheus
sudo chown -R prometheus:prometheus /var/lib/prometheus
```

7. Create systemd service file:
```bash
sudo nano /etc/systemd/system/prometheus.service
```

Add the following content:
```ini
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

8. Enable and start Prometheus:
```bash
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
```

9. Verify Prometheus is running:
```bash
sudo systemctl status prometheus
```

Access Prometheus at: `http://localhost:9090`

## Installing JSON Exporter

1. Download JSON Exporter:
```bash
wget https://github.com/prometheus-community/json_exporter/releases/download/v0.6.0/json_exporter-0.6.0.linux-armv7.tar.gz
```

2. Extract the archive:
```bash
tar xvfz json_exporter-*.tar.gz
cd json_exporter-*
```

3. Move binary to system path:
```bash
sudo mv json_exporter /usr/local/bin/
```

4. Create JSON Exporter user and directories:
```bash
sudo useradd --no-create-home --shell /bin/false json_exporter
sudo mkdir /etc/json_exporter
```

5. Copy configuration file:
```bash
sudo cp config.yml /etc/json_exporter/
```
Or use the configuration from this repository:
```bash
sudo cp json_exporter/config.yml /etc/json_exporter/
```

6. Set ownership:
```bash
sudo chown -R json_exporter:json_exporter /etc/json_exporter
```

7. Create systemd service file:
```bash
sudo nano /etc/systemd/system/json_exporter.service
```

Add the following content:
```ini
[Unit]
Description=JSON Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=json_exporter
Group=json_exporter
Type=simple
ExecStart=/usr/local/bin/json_exporter \
    --config.file=/etc/json_exporter/config.yml

[Install]
WantedBy=multi-user.target
```

8. Enable and start JSON Exporter:
```bash
sudo systemctl daemon-reload
sudo systemctl enable json_exporter
sudo systemctl start json_exporter
```

9. Verify JSON Exporter is running:
```bash
sudo systemctl status json_exporter
```

Access JSON Exporter at: `http://localhost:7979`

## Installing Grafana

### Installation on Raspberry Pi

1. Add the Grafana APT key to your Raspberry Pi's keychain:
```bash
curl https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana-archive-keyrings.gpg >/dev/null
```

2. Add the Grafana repository to your Pi's list of package sources:
```bash
echo "deb [signed-by=/usr/share/keyrings/grafana-archive-keyrings.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

3. Update the package list:
```bash
sudo apt update
```

4. Install Grafana:
```bash
sudo apt install grafana
```

5. Enable Grafana to start at boot:
```bash
sudo systemctl enable grafana-server
```

6. Start the Grafana server:
```bash
sudo systemctl start grafana-server
```

7. Verify Grafana is running:
```bash
sudo systemctl status grafana-server
```

Access Grafana at: `http://localhost:3000`

**Default credentials:**
- Username: `admin`
- Password: `admin`

You will be prompted to change the password on first login.

## Configuration

### Configure Prometheus

1. Edit Prometheus configuration:
```bash
sudo nano /etc/prometheus/prometheus.yml
```

2. Use the configuration from this repository or add the Shelly 3EM job manually:

```yaml
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "shelly_json"
    metrics_path: /probe
    params:
      module: ["shelly_3em"]
    static_configs:
      - targets:
          - "http://192.168.10.69/rpc/Shelly.GetStatus"
        labels:
          device: "shelly_192_168_10_69"
          shelly_mac: "34987A468050"
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: "127.0.0.1:7979"
```

3. Restart Prometheus:
```bash
sudo systemctl restart prometheus
```

### Configure Grafana

1. Open Grafana in your browser: `http://localhost:3000`

2. Log in with default credentials (admin/admin)

3. Add Prometheus as a data source:
   - Click **Configuration** → **Data Sources**
   - Click **Add data source**
   - Select **Prometheus**
   - Set URL to `http://localhost:9090`
   - Click **Save & Test**

4. Create a new dashboard or import an existing one for Shelly 3EM metrics

## Starting Services

### Start all services:
```bash
sudo systemctl start prometheus
sudo systemctl start json_exporter
sudo systemctl start grafana-server
```

### Check status of all services:
```bash
sudo systemctl status prometheus
sudo systemctl status json_exporter
sudo systemctl status grafana-server
```

### View logs:
```bash
# Prometheus logs
sudo journalctl -u prometheus -f

# JSON Exporter logs
sudo journalctl -u json_exporter -f

# Grafana logs
sudo journalctl -u grafana-server -f
```

## Troubleshooting

### Service won't start
Check the logs for errors:
```bash
sudo journalctl -u <service-name> -n 50
```

### Cannot access web interface
Verify the service is listening on the correct port:
```bash
sudo netstat -tulpn | grep <port-number>
```

### Prometheus can't scrape metrics
1. Verify JSON Exporter is running
2. Test the endpoint manually:
```bash
curl http://localhost:7979/probe?module=shelly_3em&target=http://192.168.10.69/rpc/Shelly.GetStatus
```

### Shelly device unreachable
1. Verify network connectivity:
```bash
ping 192.168.10.69
```
2. Check if the Shelly API endpoint is accessible:
```bash
curl http://192.168.10.69/rpc/Shelly.GetStatus
```

## Firewall Configuration

If you have a firewall enabled, allow the following ports:

```bash
# Prometheus
sudo ufw allow 9090/tcp

# JSON Exporter
sudo ufw allow 7979/tcp

# Grafana
sudo ufw allow 3000/tcp
```

## Updating

### Update Prometheus:
1. Download the latest version
2. Stop the service: `sudo systemctl stop prometheus`
3. Replace the binary in `/usr/local/bin/`
4. Start the service: `sudo systemctl start prometheus`

### Update JSON Exporter:
Follow the same process as Prometheus

### Update Grafana:
```bash
sudo apt update
sudo apt upgrade grafana
sudo systemctl restart grafana-server
```

## Security Recommendations

1. **Change default Grafana password** immediately after first login
2. **Use HTTPS** for production deployments
3. **Configure authentication** for Prometheus if exposed to network
4. **Limit network access** using firewall rules
5. **Regular backups** of Grafana dashboards and Prometheus data
6. **Keep software updated** to latest stable versions

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [JSON Exporter GitHub](https://github.com/prometheus-community/json_exporter)
- [Grafana Documentation](https://grafana.com/docs/)
- [Shelly API Documentation](https://shelly-api-docs.shelly.cloud/)
