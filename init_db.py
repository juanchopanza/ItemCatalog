#!/usr/bin/env python

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from itemcatalog import db, app


def parse_args():
    """parse command line arguments"""

    parser = ArgumentParser(description='ItemCatalog database initialization',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c', '--config', dest='config',
                        default='config.py',
                        help='Set configuration file')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    config_file = os.path.join(os.getcwd(), args.config)
    app.config.from_pyfile(config_file)
    db.create_all()
