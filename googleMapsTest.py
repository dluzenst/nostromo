import geocode as gc

from pygeocoder import Geocoder


lat, lon = Geocoder.geocode("5, av du general leclerc, paris","france").coordinates
print lat, lon