
import mysql.connector
from getpass import getpass

from src.collect_weather import collect_weather
from src.database import (
    connect_mysql,
    create_database,
    create_weather_table,
    insert_weather_data
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
        print("Database and table initialized.")

        # Step 3: Collect and process weather data
        weather_df = collect_weather()
        print(f"Weather records collected: {len(weather_df)}")

        # Step 4: Store cleaned data
        insert_weather_data(connection, weather_df)
        print("Weather data stored successfully.")

        print("Bootstrap completed successfully!")

    except (mysql.connector.Error, RuntimeError, ValueError, KeyError) as error:
        print(f"Bootstrap failed: {error}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    bootstrap()
