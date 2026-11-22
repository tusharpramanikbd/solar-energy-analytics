import mysql.connector
import pandas as pd

# Connect to the MySQL server using the configured credentials.
def connect_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="YOUR_MYSQL_PASSWORD" # Replace with your MySQL password
    )

    return connection

# Create and select the solar energy analytics database.
def create_database(connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS solar_energy_analytics"
        )

        cursor.execute("USE solar_energy_analytics")
    finally:
        cursor.close()

# Create the table for daily weather observations.
def create_weather_table(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_daily (
                date DATE NOT NULL,
                city VARCHAR(100) NOT NULL,
                temperature_mean_c FLOAT NOT NULL,
                cloud_cover_mean_pct TINYINT UNSIGNED NOT NULL,
                sunshine_hours FLOAT NOT NULL,
                PRIMARY KEY (city, date)
            )
        """)

    finally:
        cursor.close()

# Create the table for daily solar irradiation data.
def create_solar_table(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solar_daily (
                date DATE NOT NULL,
                city VARCHAR(100) NOT NULL,
                solar_irradiation_kwh_m2_day FLOAT NOT NULL,
                PRIMARY KEY (city, date)
            )
        """)

    finally:
        cursor.close()

# Create the table for annual national solar electricity generation.
def create_statistics_table(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS national_solar (
                year SMALLINT UNSIGNED NOT NULL,
                country VARCHAR(100) NOT NULL,
                solar_generation_gwh FLOAT NOT NULL,
                PRIMARY KEY (country, year)
            )
        """)

    finally:
        cursor.close()

# Create the table for solar PV benchmarking statistics.
def create_pv_table(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pv_benchmarks (
                country VARCHAR(100) NOT NULL,
                reference_period VARCHAR(20) NOT NULL,
                metric VARCHAR(100) NOT NULL,
                metric_value FLOAT NOT NULL,
                unit VARCHAR(20) NOT NULL,
                source_page SMALLINT UNSIGNED NOT NULL,
                PRIMARY KEY (country, reference_period, metric)
            )
        """)

    finally:
        cursor.close()

# Store or update cleaned daily weather records in MySQL.
def insert_weather_data(connection, weather_df):
    query = """
        INSERT INTO weather_daily
            (date, city, temperature_mean_c, cloud_cover_mean_pct, sunshine_hours)
        VALUES (%s, %s, %s, %s, %s) AS incoming
        ON DUPLICATE KEY UPDATE
            temperature_mean_c = incoming.temperature_mean_c,
            cloud_cover_mean_pct = incoming.cloud_cover_mean_pct,
            sunshine_hours = incoming.sunshine_hours
    """

    rows = [
        (
            row.date.date(),
            row.city,
            float(row.temperature_mean_c),
            int(row.cloud_cover_mean_pct),
            float(row.sunshine_hours)
        )
        for row in weather_df.itertuples(index=False)
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
        connection.commit()

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()

# Store or update cleaned daily solar irradiation records in MySQL.
def insert_solar_data(connection, solar_df):
    query = """
        INSERT INTO solar_daily
            (date, city, solar_irradiation_kwh_m2_day)
        VALUES (%s, %s, %s) AS incoming
        ON DUPLICATE KEY UPDATE
            solar_irradiation_kwh_m2_day =
                incoming.solar_irradiation_kwh_m2_day
    """

    rows = [
        (
            row.date.date(),
            row.city,
            float(row.solar_irradiation_kwh_m2_day)
        )
        for row in solar_df.itertuples(index=False)
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
        connection.commit()

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()

# Store or update annual national solar generation records in MySQL.
def insert_statistics_data(connection, statistics_df):
    query = """
        INSERT INTO national_solar
            (year, country, solar_generation_gwh)
        VALUES (%s, %s, %s) AS incoming
        ON DUPLICATE KEY UPDATE
            solar_generation_gwh = incoming.solar_generation_gwh
    """

    rows = [
        (
            int(row.year),
            row.country,
            float(row.solar_generation_gwh)
        )
        for row in statistics_df.itertuples(index=False)
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
        connection.commit()

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()

# Store or update solar PV benchmarking records in MySQL.
def insert_pv_data(connection, pv_df):
    query = """
        INSERT INTO pv_benchmarks
            (country, reference_period, metric, metric_value, unit, source_page)
        VALUES (%s, %s, %s, %s, %s, %s) AS incoming
        ON DUPLICATE KEY UPDATE
            metric_value = incoming.metric_value,
            unit = incoming.unit,
            source_page = incoming.source_page
    """

    rows = [
        (
            row.country,
            row.reference_period,
            row.metric,
            float(row.metric_value),
            row.unit,
            int(row.source_page)
        )
        for row in pv_df.itertuples(index=False)
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
        connection.commit()

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()

# Load combined weather and solar irradiation data for Vaasa.
def load_analytics_data(connection):
    query = """
        SELECT
            w.date,
            w.city,
            w.temperature_mean_c,
            w.cloud_cover_mean_pct,
            w.sunshine_hours,
            s.solar_irradiation_kwh_m2_day
        FROM solar_energy_analytics.weather_daily AS w
        INNER JOIN solar_energy_analytics.solar_daily AS s
            ON w.date = s.date AND w.city = s.city
        WHERE w.city = %s
        ORDER BY w.date
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, ("Vaasa",))
        rows = cursor.fetchall()
    finally:
        cursor.close()

    analytics_df = pd.DataFrame(rows)

    if analytics_df.empty:
        raise ValueError("No matching analytics data found.")

    analytics_df["date"] = pd.to_datetime(analytics_df["date"])

    return analytics_df

# Load Finland's annual solar electricity generation data for trend analysis.
def load_national_solar_data(connection):
    query = """
        SELECT
            year,
            country,
            solar_generation_gwh
        FROM solar_energy_analytics.national_solar
        WHERE country = %s
        ORDER BY year
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, ("Finland",))
        rows = cursor.fetchall()
    finally:
        cursor.close()

    national_df = pd.DataFrame(rows)

    if national_df.empty:
        raise ValueError("No national solar data found.")

    return national_df

# Load Finland and Belgium's 2024 solar PV shares for benchmarking.
def load_pv_benchmark_data(connection):
    query = """
        SELECT
            country,
            metric_value AS pv_share_pct
        FROM solar_energy_analytics.pv_benchmarks
        WHERE metric = 'pv_electricity_share'
            AND reference_period = '2024'
            AND country IN ('Finland', 'Belgium')
        ORDER BY country
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        cursor.close()

    benchmark_df = pd.DataFrame(rows)

    if len(benchmark_df) != 2:
        raise ValueError("Expected two PV benchmark records.")

    return benchmark_df