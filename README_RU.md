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

## Конфигурация

### Устройство Shelly 3EM
- **IP-адрес:** 192.168.10.69
- **MAC-адрес:** 34987A468050
- **API Endpoint:** `/rpc/Shelly.GetStatus`

### Prometheus
- **Интервал сбора:** 15 секунд
- **Job name:** `shelly_json`
- **Module:** `shelly_3em`

### Labels
Каждая метрика содержит стандартные метки:
- `mac` - MAC-адрес устройства
- `device` - Идентификатор устройства (shelly_192_168_10_69)
- `shelly_mac` - MAC-адрес Shelly (34987A468050)
- `phase` - Фаза (a/b/c) для фазовых метрик
- `ssid` - SSID WiFi сети для WiFi метрик

## Установка и запуск

### Предварительные требования
- Prometheus
- [JSON Exporter](https://github.com/prometheus-community/json_exporter)
- Устройство Shelly 3EM в локальной сети

### Запуск JSON Exporter
```bash
json_exporter --config.file=json_exporter/config.yml
```

### Запуск Prometheus
```bash
prometheus --config.file=prometheus/prometheus.yml
```

### Проверка работы
1. JSON Exporter: `http://127.0.0.1:7979/metrics`
2. Prometheus: `http://localhost:9090`
3. Targets: `http://localhost:9090/targets`

## Примеры запросов PromQL

### Текущая потребляемая мощность по фазам
```promql
shelly_phase_a_active_power_watts{device="shelly_192_168_10_69"}
shelly_phase_b_active_power_watts{device="shelly_192_168_10_69"}
shelly_phase_c_active_power_watts{device="shelly_192_168_10_69"}
```

### Общая потребляемая мощность
```promql
shelly_total_active_power_watts{device="shelly_192_168_10_69"}
```

### Потребление энергии за последний час
```promql
rate(shelly_total_active_energy_wh{device="shelly_192_168_10_69"}[1h]) * 3600
```

### Напряжение по всем фазам
```promql
shelly_phase_a_voltage_volts{device="shelly_192_168_10_69"}
shelly_phase_b_voltage_volts{device="shelly_192_168_10_69"}
shelly_phase_c_voltage_volts{device="shelly_192_168_10_69"}
```

### Баланс нагрузки по фазам
```promql
avg(shelly_phase_a_current_amperes{device="shelly_192_168_10_69"})
avg(shelly_phase_b_current_amperes{device="shelly_192_168_10_69"})
avg(shelly_phase_c_current_amperes{device="shelly_192_168_10_69"})
```

## Использование с Grafana

Для визуализации метрик рекомендуется использовать Grafana с источником данных Prometheus. Можно создать дашборды для отображения:
- Графиков потребления мощности по фазам
- Суммарной мощности
- Напряжения и тока
- Счетчиков энергии
- Системных метрик (температура, uptime, WiFi сигнал)

## Примечания

- Все фазовые данные извлекаются из объекта `em:0` JSON ответа Shelly
- Данные счетчиков энергии извлекаются из объекта `emdata:0`
- Частота опроса настроена на 15 секунд для баланса между актуальностью данных и нагрузкой на устройство
- MAC-адрес устройства используется как основная метка для идентификации

## Полезные ссылки

- [Shelly 3EM Documentation](https://shelly-api-docs.shelly.cloud/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [JSON Exporter](https://github.com/prometheus-community/json_exporter)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Лицензия

Проект создан для личного использования и мониторинга энергопотребления.
