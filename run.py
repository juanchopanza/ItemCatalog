#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from itemcatalog import app

def _parse_args():
    """parse command line arguments"""
    parser = ArgumentParser(description='Test Web Server',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, dest='port',
                        default=5000,
                        help='Set port')

    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    app.run(host='0.0.0.0', port=args.port)
