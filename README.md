# Shelly 3EM JSON Exporter для Prometheus

## Описание

Проект для мониторинга трехфазного энергомонитора **Shelly 3EM** с использованием **Prometheus** и **JSON Exporter**. Система преобразует JSON API устройства Shelly 3EM в метрики формата Prometheus для последующего анализа и визуализации.

## Архитектура

```
Shelly 3EM Device (192.168.10.69)
          ↓ (HTTP JSON API)
    JSON Exporter (127.0.0.1:7979)
          ↓ (Prometheus metrics)
    Prometheus (localhost:9090)
          ↓
    Grafana / Dashboards
```

## Структура проекта

```
.
├── json_exporter/
│   └── config.yml          # Конфигурация JSON Exporter
└── prometheus/
    └── prometheus.yml      # Конфигурация Prometheus
```

## Компоненты

### 1. JSON Exporter
JSON Exporter опрашивает JSON API устройства Shelly 3EM и преобразует данные в метрики Prometheus.

**Endpoint устройства:** `http://192.168.10.69/rpc/Shelly.GetStatus`

**Порт:** `7979`

### 2. Prometheus
Собирает метрики с JSON Exporter каждые 15 секунд.

**Порт:** `9090`

## Собираемые метрики

### Фазовые метрики (A, B, C)
Для каждой фазы собираются следующие метрики:

- **Ток** (`shelly_phase_{a|b|c}_current_amperes`) - Ток фазы в амперах
- **Напряжение** (`shelly_phase_{a|b|c}_voltage_volts`) - Напряжение фазы в вольтах
- **Активная мощность** (`shelly_phase_{a|b|c}_active_power_watts`) - Активная мощность в ваттах
- **Полная мощность** (`shelly_phase_{a|b|c}_apparent_power_va`) - Полная мощность в вольт-амперах
- **Коэффициент мощности** (`shelly_phase_{a|b|c}_power_factor`) - Power Factor
- **Частота** (`shelly_phase_{a|b|c}_frequency_hertz`) - Частота в герцах
- **Суммарная энергия** (`shelly_phase_{a|b|c}_total_active_energy_wh`) - Накопленная энергия в ватт-часах

### Суммарные метрики
- **Общий ток** (`shelly_total_current_amperes`) - Суммарный ток всех фаз
- **Общая активная мощность** (`shelly_total_active_power_watts`) - Суммарная активная мощность
- **Общая полная мощность** (`shelly_total_apparent_power_va`) - Суммарная полная мощность
- **Общая энергия** (`shelly_total_active_energy_wh`) - Суммарная потребленная энергия

### Системные метрики
- **Uptime** (`shelly_uptime_seconds`) - Время работы устройства в секундах
- **Свободная RAM** (`shelly_ram_free_bytes`) - Свободная оперативная память в байтах
- **Температура** (`shelly_temperature_celsius`) - Температура устройства в градусах Цельсия

### Сетевые метрики
- **WiFi RSSI** (`shelly_wifi_rssi_dbm`) - Уровень сигнала WiFi в dBm
- **WiFi статус** (`shelly_wifi_status`) - Статус WiFi подключения (1 = подключено)
- **Cloud статус** (`shelly_cloud_connected`) - Статус облачного подключения
- **MQTT статус** (`shelly_mqtt_connected`) - Статус MQTT подключения

## Пример метрик

Пример реального вывода метрик из JSON Exporter:

```prometheus
# HELP shelly_cloud_connected_connected Cloud connection status
# TYPE shelly_cloud_connected_connected untyped
shelly_cloud_connected_connected{mac=""} 1

# HELP shelly_mqtt_connected_connected MQTT connection status
# TYPE shelly_mqtt_connected_connected untyped
shelly_mqtt_connected_connected{mac=""} 0

# HELP shelly_phase_a_active_power_watts_power Phase A active power in watts
# TYPE shelly_phase_a_active_power_watts_power untyped
shelly_phase_a_active_power_watts_power{mac="",phase="a"} 296.6

# HELP shelly_phase_a_current_amperes_current Phase A current in amperes
# TYPE shelly_phase_a_current_amperes_current untyped
shelly_phase_a_current_amperes_current{mac="",phase="a"} 2.163

# HELP shelly_phase_a_voltage_volts_voltage Phase A voltage in volts
# TYPE shelly_phase_a_voltage_volts_voltage untyped
shelly_phase_a_voltage_volts_voltage{mac="",phase="a"} 220

# HELP shelly_total_active_power_watts_power Total active power in watts
# TYPE shelly_total_active_power_watts_power untyped
shelly_total_active_power_watts_power{mac=""} 435.066

# HELP shelly_total_current_amperes_current Total current in amperes
# TYPE shelly_total_current_amperes_current untyped
shelly_total_current_amperes_current{mac=""} 3.271

# HELP shelly_temperature_celsius_temperature Device temperature in Celsius
# TYPE shelly_temperature_celsius_temperature untyped
shelly_temperature_celsius_temperature{mac=""} 41.7

# HELP shelly_wifi_rssi_dbm_rssi WiFi RSSI in dBm
# TYPE shelly_wifi_rssi_dbm_rssi untyped
shelly_wifi_rssi_dbm_rssi{mac="",ssid="Tplink"} -41
```

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
