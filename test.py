#!/usr/bin/python3

import tests.test_helper as test_helper
import unittest
import argparse


parser = argparse.ArgumentParser(description='Big Fiubrother Test Runner')
parser.add_argument('--setup_db', dest='setup_db', action='store_true', help='Creates database from scratch')
parser.set_defaults(setup_db=False)

args = parser.parse_args()

if args.setup_db:
    test_helper.tear_down()
    test_helper.set_up()

test_suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(test_suite)
