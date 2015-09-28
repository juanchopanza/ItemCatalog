#!/usr/bin/env python
'''Commandline script to run the ItemCatalog app'''

from itemcatalog import app
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    """parse command line arguments"""

    parser = ArgumentParser(description='Start ItemCatalog Server',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--port', type=int, dest='port',
                        default=5000,
                        help='Set port')

    parser.add_argument('-c', '--config', dest='config',
                        default='config.py',
                        help='Set configuration file')

    return parser.parse_args()


if __name__ == '__main__':

    basedir = os.path.abspath(os.path.dirname(__file__))
    args = parse_args()
    config_file = os.path.join(basedir, args.config)
    app.config.from_pyfile(config_file)
    app.run(host='0.0.0.0', port=args.port)
