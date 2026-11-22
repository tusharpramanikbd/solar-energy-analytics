# Solar Energy Analytics

## 1. Prerequisites

Make sure the following software is installed:

- **Conda** (Miniconda or Anaconda)
- **MySQL Server** (version 8.4 recommended)
- **MySQL Client** (Sequel Ace, MySQL Workbench, or similar)

## 2. Project Setup

### Step 1: Open the project directory

1. Extract the provided ZIP file.
2. Open a terminal in the extracted project root directory.

### Step 2: Create and activate the Conda environment

Create the environment using the provided configuration:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate solar-energy-analytics
```

All required Python dependencies are defined in `environment.yml`.

### Step 3: Configure the MySQL connection

Make sure your MySQL Server is running.

Open `src/database.py` and update the credentials inside the `connect_mysql()` function:

```python
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="YOUR_MYSQL_PASSWORD"
)
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password. Update the host, port, or username if necessary.

## 3. Database Setup

Choose **one** of the following options.

### Option A: Import the existing database (Recommended)

1. Open a MySQL client and connect to your MySQL Server.
2. Create a new database:

```sql
CREATE DATABASE IF NOT EXISTS solar_energy_analytics;
```

3. Select the `solar_energy_analytics` database.
4. Import the SQL file:

```text
database/solar_energy_analytics_2026-11-22.sql
```

The imported database should contain four tables:

- `weather_daily`
- `solar_daily`
- `national_solar`
- `pv_benchmarks`

**Note:** Import into a new or empty database because the SQL file contains `DROP TABLE` statements.

After importing, proceed to Section 4.

### Option B: Build the database from source data

Alternatively, run:

```bash
python main.py
```

This creates the database tables and loads data from the Open-Meteo API and the local files in `external_data/`.

An internet connection is required for the API request.

## 4. Run the Analytics

Once the database is ready, run:

```bash
python run_analytics.py
```

The script generates analytical results and saves the output files in:

- `charts/` — Generated charts and visualizations.
- `exports/` — Generated CSV and Excel files.

**Note:** Run all Python commands from the project root directory with the Conda environment activated.

## 5. Project Directory Structure

| File / Directory | Description |
|---|---|
| `main.py` | Entry point for collecting, processing, and storing data in MySQL. |
| `run_analytics.py` | Entry point for running analytics and generating outputs. |
| `environment.yml` | Conda environment and Python dependency configuration. |
| `src/` | Python modules for data collection, database operations, analytics, and plotting. |
| `external_data/` | Original external datasets downloaded from NASA POWER (CSV), Statistics Finland (XLSX), and IEA PVPS (PDF). |
| `database/` | MySQL database export (`.sql`) containing table structures and stored records. |
| `charts/` | Python-generated charts for descriptive, predictive, KPI, trend, correlation, and benchmarking analyses. |
| `exports/` | Generated CSV and Excel files, including KPI summaries and Power BI input data. |
| `reports/` | Final project report and exported Power BI report in PDF format. |