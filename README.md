# IoT Sensor Monitoring Demo (Azure SQL Edge + Docker + Grafana)🤖

This is a **fully local, free-tier project** that demonstrates real-time IoT sensor data visualization using:

- **Azure SQL Edge** (Docker container) as the database
- **Python Flask API** (`sensor-api`) to generate and serve fake sensor data
- **Grafana OSS** (Docker container) to visualize data
- **Docker Compose** for orchestration
- **Environment variables** (.env) for secure configuration

![img](/img/grafana-screenshot.png)

---

## Features 🚢

- Generates fake sensor data for 3 devices every 5 seconds
- Stores data in Azure SQL Edge
- Provides `/data` API endpoint to expose the latest 100 records in JSON
- Grafana dashboard with:
  - Device Temperature (Time Series)
  - Device Humidity (Time Series)
- Fully local and free-tier (no cloud costs)
- Safe handling of credentials via `.env` (no hard-coded secrets)

---

## Good to have 💼

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- Optional: [VS Code + SQL Server extension](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) to inspect SQL Edge database

---

## Project Structure 🦴

```
azure-grafana/
├─ docker-compose.yml
├─ .env # Environment variables (not committed)
├─ sensor-api/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py # Flask API + fake data generator
├─ grafana/
│ └─ dashboards/
│   └─ sensor-dashboard.json
```

![system-design](/img/system-design.png)

## How to build and start containers 🖥️

```
docker-compose build
docker-compose up -d

```

## Access Grafana

- Open browser: http://localhost:3000
- Login: admin / admin

## Import Dashboard:

- Dashboards → Import → sensor-dashboard.json
- The dashboard will show live-updating temperature & humidity graphs

## How it works 🏃‍♀️

1. sensor-api/app.py:

- Uses environment variables to connect to Azure SQL Edge
- Creates SensorData table if it doesn't exist
- Starts a background thread that inserts fake data every 5 seconds
- Exposes /data endpoint returning latest 100 rows in JSON

2. Azure SQL Edge:

- Stores sensor data persistently in Docker volume
- Accessible from Grafana or local SQL clients

3. Grafana:

- Connects to sensor-api via JSON API plugin
- Dashboard visualizes temperature & humidity per device
- Refresh interval can be set (default 5s matches API data insertion)

## Note 📕

- Data insertion only occurs while Docker containers are running
- Stopping docker-compose down halts insertion, but existing data persists in Docker volume
- This is a fully local free-tier setup; no Azure cloud costs are incurred
- For security, credentials are kept in .env and never in code

## Further potential 🌕

- Connect real IoT sensors instead of fake data
- Add Grafana alerts for threshold values
- Integrate CI/CD pipelines for automatic deployment
- Use Docker Secrets or Azure Functions for more secure production deployments
