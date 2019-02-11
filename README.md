## Growatt API client

This Python script logs in to server.growatt.com and retrieves data on solar panels.

## Usage

Create a new GrowattApi instance, log in, retrieve a list of plants and request details of these plants. An example can be found in [growatt/__main__.py](growatt/__main__.py), and can be run using `python -m growatt`.

## API

Currently this package uses an API that I reverse engineered the API from the Growatt mobile app. This is more of an internal API that can be changed by Growatt if they want.

There is also an [API specification](http://www.growatt.pl/dokumenty/Inne/Growatt%20Server%20Open%20API%20protocol%20standards.pdf) for a more standard API, but that is currently not used by this package.
