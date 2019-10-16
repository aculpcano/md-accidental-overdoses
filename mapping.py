"""This module maps the layers out using Folium and Leaflet.js."""

import folium
from folium import plugins


class Map(folium.Map):
    """Create a Map based off of the Folium package.

    There are two defaults that are passed to the map: the zoom_start set
    at level 8 and using the dark CartoDB tiles for the map. The location
    (i.e. the center of the map) is set to the "centroid" of the state of
    Maryland.

    Methods
    -------
    add_layer
        Add a GeoJSON layer to the Map object
    add_minimap
        Add a minimap to the Map object
    """
    def __init__(self, centroid):
        """Constructor for the Map object.

        Parameters
        ----------
        centroid
            The centroid of the Maryland shapefile
        """
        super().__init__(location=[centroid.centroid.y, centroid.centroid.x],
                         zoom_start=8,
                         tiles='CartoDB dark_matter')

    def add_layer(self, layer):
        """Adds a GeoJSON layer to the Map object.

        Parameters
        ----------
        layer
            The layer that needs to be added to the map
        """
        folium.GeoJson(layer,
                       name='Counties\' Overdoses',
                       tooltip=folium.GeoJsonTooltip(
                           fields=['substance', 'county', 'year', 'deaths'],
                           labels=True,
                           sticky=False)).add_to(self)

    def add_minimap(self):
        """Add a minimap to the Map object."""
        minimap = plugins.MiniMap()
        self.add_child(minimap)
