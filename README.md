# overdoses
This project maps accidental overdoses reported by the Maryland Department of
Health for each county between 2013 and 2018. Using folium, a Python library
built upon Leaflet.js to visualize the data on a map, the project displays each
county's number of recorded deaths for the specific year and drug substance.

## Getting Started
This project targets Python 3.7, but could theoretically run under Python 3.6.
Its dependencies include GeoPandas and folium.

### Prerequisites
1. Required Python version and its dependencies
2. Internet connection

### Installing
Run `setup.py` from the root folder. To do that, you will need to open a
command-line application and type the following two commands:

    python3 setup.py build
    python3 setup.py install

This assumes you have created a virtual environment.

## Data
Health data come from the [Maryland Department of Health](
https://health.maryland.gov/vsa/Pages/overdose.aspx). The data only include
confirmed or suspected substance overdose (whether by accident or undetermined).

Political state and county boundaries come from [Maryland's Open Data Portal](
https://opendata.maryland.gov/browse?category=Boundaries).

## Usage
This program is run from the command line. It takes two arguments: the first one
for the year and the second one for the substance. The following table shows the
valid options that can be passed.

    -year           2013, 2014, 2015, 2016, 2017, 2018

    -substance      'Alcohol', 'Benzodiazepine', 'Cocaine', 'Fentanyl',
                    'Heroin', 'Methadone', 'Methamphetamine', 'Opioid',
                    'Oxycodone', 'Prescription Opioid'

After installing the appropriate packages, run the program by issuing a call to
the Python interpreter, the program name and the arguments. The command takes
the following format.

    python3 overdoses.py YEAR SUBSTANCE

For example, the following command is correct.

    python3 overdoses.py 2013 Alcohol

## Changelog
### [0.1] - 2019-10-16
* Initial release

## Authors
* Alexander Wesley Culp Cano - *Initial work* - <awccdev@gmail.com>

## License
This project is licensed under the MIT License. See License.txt for more
information.
