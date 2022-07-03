import argparse
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.example.settings"

parser = argparse.ArgumentParser()
# Arguments from django-admin test
parser.add_argument(
    "-v",
    "--verbosity",
    default=1,
    type=int,
    choices=[0, 1, 2, 3],
    help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output",
)
parser.add_argument(
    "args",
    metavar="test_label",
    nargs="*",
    help="Module paths to test; can be modulename, modulename.TestCase or modulename.TestCase.test_method",
)
options = parser.parse_args()


django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=options.verbosity)
failures = test_runner.run_tests(options.args)
sys.exit(bool(failures))
