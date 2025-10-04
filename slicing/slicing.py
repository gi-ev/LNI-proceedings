#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8

import os
import sys
import csv
import subprocess
from sys import platform

# sys.argv[0]: page number of first not-empty page after table of contents
# sys.argv[1]: proceedings pdf
# sys.argv[2]: proceedings csv

if len(sys.argv) < 4:
    print("Please start the script as follows:")
    print("python slicing.py <page number of first not-empty page after table of contents> <proceedings pdf> <proceedings csv>")
    sys.exit(-1)

OFFSET = int(sys.argv[1]) - 1
INPUT = sys.argv[2]
INPUT_csv = sys.argv[3]

csv_reader = csv.reader(open(INPUT_csv, "r"), delimiter=';')

for row in csv_reader:
    buildID = row[-1]
    page_start, page_end = row[-2].split("--")

    filename = os.path.join("parts", buildID + ".pdf")
    page_start = int(page_start) + OFFSET
    page_end = int(page_end) + OFFSET

    print("slicing PDF at page " + str(page_start) + " until " + str(page_end) + " and save it in '" + filename + "'")

    # "pdftk " + INPUT + " cat " + page_start + "-" + page_end + " output parts\\" + buildID + ".pdf"
    # "pdftk " + PATH + "\\" + INPUT + " cat " + page_start + "-" + page_end + " output " + PATH + "\\parts\\" + buildID + ".pdf"
    # subprocess.call(["pdftk", PATH + "\\" + INPUT, "cat", page_start + "-" + page_end, "output",
    #                  PATH + "\\parts\\" + buildID + ".pdf"], shell=True)
    subprocess.call(["pdftk", INPUT, "cat", str(page_start) + "-" + str(page_end), "output", filename],
                    shell= (platform == "win32"))
