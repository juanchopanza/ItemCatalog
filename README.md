# ItemCatalog
A simple item catalog web application

## Features:

* 3rd party authentication with Google+ and Facebook (FB limited to google chrome
and Safari browsers.)
* CSRF protection for POST, PUT and DELETE operations
* CRUD read for all users.
* CRUD create, update and delete for authorized users
* JSON and ATOM API end-points

### JSON API

The JSON API provides read-only access via the following URLs:

* `/catalog/JSON/` Hierarchical representation of catalog categories including items.
* `/categories/JSON/` List of catagories.
* `/catagory/<id>/JSON/` Single category including items.
* `/items/JSON/` List of all items.
* `/item/<id>/JSON` Single catalog item.

### ATOM API

The ATOM API provides read-only access via the following URLs:

* `/categories/ATOM/` List of catagories.
* `/catagory/<id>/ATOM/` Single category including items.
* `/items/ATOM/` List of all items.
* `/item/<id>/ATOM` Single catalog item.


## Installation

You can choose to run the application natively or in a virtual machine. Fist of all,
clone the repo and change directory to it:

    git clone https://github.com/juanchopanza/ItemCatalog
    cd ItemCatalog

#### Run locally

Requires: `pip`, `virtualenv`.

It is advised that you start a `virtualenv` and install the python external dependencies.
This is trivial using `pip`:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

#### Run in a virtual machine

Requires: `vagrant`

First, initialize the virtual machine:

    vagrant up

This might take a few minutes. Go make yourself a coffee.

Next, log into the virtual machine and change to the shared directory:

    vagrant ssh # logs you in as user "vagrant"
    cd /vagrant

#### Initialize the database and launch the application

    ./init_db.py
    ./run.py

This creates an sqlite3 database with the required (empty) tables and launches the
application server in production mode on port 5000. To run on a different port, pass an
argument with the `-p` or `--port` option. For example, to run on port 8000:

    ./run.py --port 8000

To run in debug mode, invoke 

    ./run.py --config config_dev.py
    
To run an example with an existing `sqlite3` database, run  

    ./run.py --config config_example.py

For other command line options, invoke `run.py` with the `-h` or `--help` options.

Note that the `init_db.py` script also has a command line option for the configuration
file. This allows you to define the type and name of the database to be created.

#### Profit

Point a browser at `localhost:5000` and enjoy.
