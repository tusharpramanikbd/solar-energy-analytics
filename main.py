
import mysql.connector
from getpass import getpass

from src.collect_weather import collect_weather
from src.collect_solar import collect_solar

from src.database import (
    connect_mysql,
    create_database,
    create_weather_table,
    insert_weather_data,
    create_solar_table,
    insert_solar_data
)


def bootstrap():
    user = input("MySQL Username: ")
    password = getpass("MySQL Password: ")

    connection = None

    try:
        # Step 1: Connect to MySQL
        connection = connect_mysql(user, password)
        print("MySQL connected.")

        # Step 2: Initialize database and table
        create_database(connection)
        create_weather_table(connection)
        create_solar_table(connection)
        print("Database and tables initialized.")

        # Step 3: Collect and process weather data
        weather_df = collect_weather()
        print(f"Weather records collected: {len(weather_df)}")

        solar_df = collect_solar()
        print(f"Solar records collected: {len(solar_df)}")

        # Step 4: Store cleaned data
        insert_weather_data(connection, weather_df)
        print("Weather data stored successfully.")

        insert_solar_data(connection, solar_df)
        print("Solar data stored successfully.")

        print("Bootstrap completed successfully!")

    except (mysql.connector.Error, RuntimeError, ValueError, KeyError, FileNotFoundError) as error:
        print(f"Bootstrap failed: {error}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    bootstrap()
