#!/usr/bin/env python

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from itemcatalog import db, app


def parse_args():
    """parse command line arguments"""

    parser = ArgumentParser(description='ItemCatalog database initialization',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-n', '--name', dest='dbname',
                        default='itemcatalog',
                        help='Datbase name')

    parser.add_argument('-t', '--type', dest='dbtype',
                        default='sqlite',
                        choices=('psql', 'sqlite'),
                        help='Datbase type')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    basedir = os.path.abspath(os.path.dirname(__file__))
    DB = {'psql': 'postgresql:///%s' % args.dbname,
          'sqlite': 'sqlite:///%s' % os.path.join(basedir,
                                                  '%s.db' % args.dbname)}
    app.config['SQLALCHEMY_DATABASE_URI'] = DB[args.dbtype]
    db.create_all()
