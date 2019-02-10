## Growatt API client

This Python script logs in to server.growatt.com and retrieves data on solar panels.

## Usage

Create a new GrowattApi instance, log in, retrieve a list of plants and request details of these plants. An example can be found in [growatt/__main__.py](growatt/__main__.py), and can be run using `python -m growatt`.

## Unstable API

I reverse engineered the API from the Growatt mobile app. There is no specification and no support from Growatt.
