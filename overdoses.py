"""This module downloads the needed shapefiles for mapping and utilizes
the SQLite database in the data folder to map the number of deaths for
each substance in each year.
"""

from argparse import ArgumentParser, ArgumentTypeError,\
    RawDescriptionHelpFormatter
import os
from sqlite3 import connect
from io import BytesIO
import sys
from urllib.error import URLError
from urllib.request import urlopen
from zipfile import ZipFile

import mapping

import pandas as pd
import geopandas


class OverdoseDatabase:
    """A class designed to open, query and close the connection to the
    database."""
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__),
                                    'data', 'substances.db')
        self.db_connection = connect(self.db_path)

    def query(self, year, substance):
        """Retrieves information from the database based on the year and
        substance.

            Parameters
            ----------
            year : int
                The year the data is pulled for
            substance : str
                The substance the user wants to find information about

            Returns
            -------
            sqlite3.Connection
                A SQLite Connection object of the query results
            """

        sql = f"SELECT * FROM substances WHERE year={year} AND " \
              f"name='{substance}'"

        with self.db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def close(self):
        self.db_connection.close()


def download_data(url, path):
    """Downloads the needed shapefiles from the Maryland Open Data Portal.

    Parameters
    ----------
    url : str
        The URL needed to download the ZIP archive
    path : str
        The path to unzip the folder
    """

    # Check to see if there is a file with the '.shp' ending
    exists = []
    if os.path.exists(path):
        files = os.listdir(path)
        exists = [file.endswith('.shp') for file in files]

    # If no shapefile is in the folder, download it
    if exists.count(True) == 0:
        print(f"Downloading and extracting needed data to {path}.")
        with urlopen(url) as response:
            with ZipFile(BytesIO(response.read())) as zip_file:
                zip_file.extractall(path)


def to_geojson(shp_file, database_data):
    """Converts the shapefile to a GeoJSON file. Only kept in memory.

    Parameters
    ----------
    shp_file : str
        The path of the shapefile to be used
    database_data : pandas.core.frame.DataFrame
        The database data

    Returns
    -------
    A merged GeoJSON file between the shapefile
    """
    counties_gdf = geopandas.read_file(shp_file)
    counties_gdf = counties_gdf.merge(database_data, on='county')
    return counties_gdf.to_json()


def main():
    year, substance = sys.argv[1:]

    # Get database data and convert to a GeoPandas dataframe for processing
    database = OverdoseDatabase()
    database_data = database.query(year, substance)
    database_data = pd.DataFrame(database_data)
    # database.close()
    database_data = database_data.fillna(0)
    database_data.columns = ['substanceID', 'substance', 'county', 'year',
                             'deaths']

    script_path = os.path.dirname(__file__)
    data_path = os.path.join(script_path, 'data')

    # Retrieve the MD shapefile and MD counties shapefile from the Internet
    imap = 'http://data.imap.maryland.gov/datasets/'
    md_shp = imap + '79b8acd97e3d4cc0ab81244edc2f83e4_0.zip'
    cnty_shp = imap + '4c172f80b626490ea2cff7b699febedb_1.zip'

    md_path = os.path.join(data_path, 'MD_State_Boundary')
    cnty_path = os.path.join(data_path, 'MD_County_Boundary')
    try:
        download_data(md_shp, md_path)
        download_data(cnty_shp, cnty_path)

        # Set up paths for the shapefiles
        shp = 'Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp'
        counties = os.path.join(data_path, 'MD_County_Boundary', shp)
        shp = 'Maryland_Political_Boundaries__State_Boundary.shp'
        state = os.path.join(md_path, shp)

        # Convert the state and counties shapefiles to GeoJSON
        state_shp = geopandas.read_file(state)
        counties_json = to_geojson(counties, database_data)

        # Open a new Folium map instance and add the needed information
        print("Creating web map and saving to disk.")
        web_map = mapping.Map(state_shp)
        web_map.get_root().title = f'Maryland Counties\' {year} {substance} ' \
                                   'Accidental Overdoses'
        web_map.add_layer(counties_json)
        web_map.add_minimap()

        # Create directory for web maps if it doesn't exist and save map
        map_path = os.path.join(script_path, 'maps')
        if not os.path.exists(map_path):
            os.mkdir(map_path)

        saved_map_path = os.path.join(map_path,
                                      f'{year}_{substance.lower()}.html')
        print(f"Saving map to {saved_map_path}")
        web_map.save(saved_map_path)
    except URLError:
        print("\n\n\nThere is something wrong with the Internet connection.",
              "Please try again.")
        sys.exit(1)


if __name__ == '__main__':
    def check_year(year):
        year = int(year)

        if type(year) is not int:
            raise ArgumentTypeError(f"{year} is not an integer.")

        if year < 2013 or year > 2018:
            raise ArgumentTypeError(f"{year} is not in the valid range.")

    def check_substance_name(substance):
        substance = substance.capitalize()
        substance_list = ['Alcohol', 'Benzodiazepine', 'Cocaine', 'Fentanyl',
                          'Heroin', 'Methadone', 'Methamphetamine', 'Opioid',
                          'Oxycodone', 'Prescription Opioid']

        if substance not in substance_list:
            raise ArgumentTypeError(f"{substance} is not one of the accepted "
                                    f"substances.")

    description = ('The year and substance for querying the database.\n\n'
                   'The year should be between 2013 and 2018 (including '
                   'interval ends). The substance should be one of the '
                   'following (without quotation marks):\n'
                   '\'Alcohol\', \'Benzodiazepine\', \'Cocaine\', '
                   '\'Fentanyl\', \'Heroin\', \'Methadone\', '
                   '\'Methamphetamine\', \'Opioid\', \'Oxycodone\', '
                   '\'Prescription Opioid\'')

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=description)
    parser.add_argument('year', help="The year to investigate the overdoses",
                        type=check_year)
    parser.add_argument('substance', help="The substance to investigate",
                        type=check_substance_name)
    arguments = parser.parse_args()
    main()
