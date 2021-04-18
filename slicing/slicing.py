#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8

import os
import sys
import csv
import subprocess
from sys import platform

# sys.argv[1]: proceedings pdf
# sys.argv[2]: proceedings csv

if len(sys.argv) < 3:
    print("Please start the script as follows:")
    print("python slicing.py <proceedings pdf> <proceedings csv>")
    sys.exit(-1)

INPUT = sys.argv[1]
INPUT_csv = sys.argv[2]

csv_reader = csv.reader(open(INPUT_csv, "r"), delimiter=';')

for row in csv_reader:
    buildID = row[-1]
    page_start, page_end = row[-2].split("--")

    filename = os.path.join("parts", buildID + ".pdf")

    print("slicing PDF at page " + page_start + " until " + page_end + " and save it in '" + filename + "'")

    # "pdftk " + INPUT + " cat " + page_start + "-" + page_end + " output parts\\" + buildID + ".pdf"
    # "pdftk " + PATH + "\\" + INPUT + " cat " + page_start + "-" + page_end + " output " + PATH + "\\parts\\" + buildID + ".pdf"
    # subprocess.call(["pdftk", PATH + "\\" + INPUT, "cat", page_start + "-" + page_end, "output",
    #                  PATH + "\\parts\\" + buildID + ".pdf"], shell=True)
    subprocess.call(["pdftk", INPUT, "cat", page_start + "-" + page_end, "output", filename],
                    shell= (platform == "win32"))
