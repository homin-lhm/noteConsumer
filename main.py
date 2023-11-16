import os
import unittest
from BeautifulReport import BeautifulReport

Dir = os.path.abspath(os.path.dirname(__file__))
print(Dir)
ENVIRON = "Online"


def run(test_suite):
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description="Test Report", report_dir=Dir)


if __name__ == "__main__":
    pattern = "all"  # all: run all case,  smoking: run smoking case
    if pattern == "all":
        suite = unittest.TestLoader().discover(start_dir="./testCase", pattern="test_*.py")
    elif pattern == "smoking":
        suite = unittest.TestLoader().discover(start_dir="./testCase", pattern="test_major*")
    else:
        raise "pattern error"
    run(suite)

