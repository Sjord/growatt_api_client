## Growatt API client

This Python script logs in to server.growatt.com and retrieves data on solar panels.

## Deprecated

Use [indykoning/PyPi\_GrowattServer](https://github.com/indykoning/PyPi_GrowattServer) instead.

## Usage

Create a new GrowattApi instance, log in, retrieve a list of plants and request details of these plants. An example can be found in [growatt/\_\_main\_\_.py](growatt/__main__.py), and can be run using `python -m growatt`.

## API

Currently this package uses an API that I reverse engineered the API from the Growatt mobile app. This is more of an internal API that can be changed by Growatt if they want.

There is also an [API specification](http://www.growatt.pl/dokumenty/Inne/Growatt%20Server%20Open%20API%20protocol%20standards.pdf) for a more standard API, but that is currently not used by this package.

## Getting started

Run the following commands to set up a new virtualenv and run the growatt API example:

    git clone https://github.com/Sjord/growatt_api_client
    cd growatt_api_client
    python3 -m venv venv                    # create a new virtual environment in the directory 'venv'
    . venv/bin/activate                     # activate this environment
    ./setup.py install                      # install all dependencies
    python -m growatt 'username' 'password' # retrieve data for today

After setting up like this, you can just run the python from the virtualenv each time you want to run it:

    venv/bin/python -m growatt 'username' 'password'

If you want to create your own client, start from growatt/\_\_main\_\_.py. Copy it and change it to your liking, and then run it like this:

    venv/bin/python myscript.py 'username' 'password'

