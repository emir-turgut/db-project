import mysql.connector
from mysql.connector import Error

#initial variable creation
selected_country = None


#sets selected country at the ui
def set_selected_country(country_name):
    global selected_country
    selected_country = country_name
    print(f"Selected country: {selected_country}")


#gets selected country at the ui
def get_selected_country():
    return selected_country


#initial variable creation
selected_location = None


#sets selected location at the ui
def set_selected_location(location_name):
    global selected_location
    selected_location = [location_name]
    print(f"Selected location: {selected_location}")


#gets selected location at the ui
def get_selected_location():
    location = selected_location
    if isinstance(location, str):
        return [location]
    elif isinstance(location, list):
        return location
    else:
        return []


#returns distinct country_name in country table
def distinct_country_name():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emirturgut",
            database="weather_db"
        )
        cursor = connection.cursor()

        query = """
        SELECT DISTINCT country_name
        FROM country;
                """
        cursor.execute(query)
        distinct_countries = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(e)
        distinct_countries = []
    #print(distinct_countries)
    return distinct_countries


# returns country.id
def get_country_id(country_names=None):
    if country_names is None:
        country_names = [get_selected_country()]
    if not country_names:
        return []

    country_ids = []

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emirturgut",
            database="weather_db"
        )
        cursor = connection.cursor()

        query = """
        SELECT id
        FROM country
        WHERE country_name = %s;
        """
        for country_name in country_names:
            cursor.execute(query, (country_name,))
            results = cursor.fetchall()
            for result in results:
                country_ids.append(result[0])

        cursor.close()
        connection.close()
    except Error as e:
        print(e)
        return []
    #print(country_ids)
    return country_ids


# return distinct location_name in location table
def distinct_location_name(country_ids=None):
    if country_ids is None:
        country_ids = get_country_id()
    if not country_ids:
        return []

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emirturgut",
            database="weather_db"
        )
        cursor = connection.cursor()

        query = f"""
        SELECT DISTINCT location_name
        FROM location
        WHERE id IN ({','.join(['%s'] * len(country_ids))});
        """
        cursor.execute(query, country_ids)
        location_names = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(e)
        location_names = []

    print(location_names)
    return location_names


#gets the location.id
def get_location_id(location_name=None):
    if location_name is None:
        location_name = get_selected_location()
    if location_name is None:
        return []

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emirturgut",
            database="weather_db"
        )
        cursor = connection.cursor()

        query = f"""
        SELECT id
        FROM location
        WHERE location_name = %s;
        """
        cursor.execute(query, (location_name,))
        location_id = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(e)
        location_id = []

    print(location_id)
    return location_id


# joins all tables together using their id, takes location_name as a filter
def query_location_data(location_name):
    try:
        if isinstance(location_name, list):
            location_name = location_name[0]  # Take the first element if it's a list

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emirturgut",
            database="weather_db"
        )
        cursor = connection.cursor()

        query = """
        SELECT country.*, location.*, weather_condition.*, wind.*, gust.*, air_pressure.*, air_quality.*, air_quality_index.*, moon.*, sun.*
        FROM country
        JOIN location ON country.id = location.id
        JOIN weather_condition ON country.id = weather_condition.id
        JOIN wind ON country.id = wind.id
        JOIN gust ON country.id = gust.id
        JOIN air_pressure ON country.id = air_pressure.id
        JOIN air_quality ON country.id = air_quality.id
        JOIN air_quality_index ON country.id = air_quality_index.id
        JOIN moon ON country.id = moon.id
        JOIN sun ON country.id = sun.id
        WHERE location_name = %s;
        """

        print("Query:", query)
        print("Location Name:", location_name)

        cursor.execute(query, (location_name,))
        result = cursor.fetchall()

        cursor.close()
        connection.close()
    except Error as e:
        print(e)
        result = []

    return result
