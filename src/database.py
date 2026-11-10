import mysql.connector


def connect_mysql(user, password, host="127.0.0.1", port=3306):
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )

    return connection

def create_database(connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS solar_energy_analytics"
        )
    finally:
        cursor.close()

def create_weather_table(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("USE solar_energy_analytics")

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


def insert_weather_data(connection, weather_df):
    query = """
        INSERT INTO solar_energy_analytics.weather_daily
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
