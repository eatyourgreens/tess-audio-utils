from strauss.sonification import Sonification
from strauss.sources import Objects
from strauss.score import Score
from strauss.generator import Synthesizer

import numpy as np
import requests
import json

# specify audio system (e.g. mono, stereo, 5.1, ...)
system = "stereo"

# length of the sonification in s
length = 25.

# base notes for the sonification
notes = [["A2"]]

# set up synth and turn on LP filter
generator = Synthesizer()
generator.load_preset('pitch_mapper')
score = Score(notes, length)


def sonify(data):
    # set up source
    sources = Objects(data.keys())
    sources.fromdict(data)
    sources.apply_mapping_functions()

    return Sonification(score, sources, generator, system)


def normalise_light_curve(days, fluxes):
    def normalise_day(d):
        return d / days.max()

    normalised_days = map(normalise_day, days)
    x = np.fromiter(normalised_days, float)

    flux_min = fluxes.min()
    flux_max = fluxes.max()
    flux_range = flux_max - flux_min

    def normalise_flux(f):
        return (f - flux_min) / flux_range

    normalised_fluxes = map(normalise_flux, fluxes)
    y = np.fromiter(normalised_fluxes, float)
    return x, y


def light_curve_url(subject):
    json_locations = [
        location.get('text/plain')
        for location in subject.locations
        if location.get('text/plain')
    ]
    return json_locations[0]


def fetch_light_curve(url):
    json_data = requests.get(url).text
    response = json.loads(json_data)
    days = np.array(response['x'])
    fluxes = np.array(response['y'])
    return days, fluxes
