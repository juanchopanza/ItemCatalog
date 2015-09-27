# ItemCatalog
A simple web application item catalog

### Installation

You can choose to run the application natively or in a virtual machine. Fist of all,
clone the repo and change directory to it:

    git clone https://github.com/juanchopanza/ItemCatalog
    cd ItemCatalog

#### Run locally

It is advised that you start a `virtualenv` and install the python external dependencies.
This is trivial using `pip`:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

Requires: `pip`, `virtualenv`.

#### Run in a virtual machine

First, initialize the virtual machine:

    vagrant u

This might take a few minutes. Go make yourself a coffee.

Next, log into the virtual machine and change to the shared directory:

    vagrant ssh # logs you in as user "vagrant"
    cd /vagrant

#### Initialize the database and launch the application

    ./init_db.py
    ./run.py

This created an sqlite3 database with the required (empty) tables and launches the
application server in debug mode on port 5000.

#### Profit

Point a browser at `localhost:5000` and enjoy.
