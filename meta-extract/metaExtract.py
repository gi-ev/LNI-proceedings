#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# coding: utf-8

# call like this:
# python metaExtract.py papers.csv ws.csv proceedings.csv

# import textract
import sys
import re
import csv
from collections import OrderedDict

# sys.argv[1]: GI Guidelines csv
# sys.argv[2]: Workshop csv
# sys.argv[3]: proceedings csv

if len(sys.argv) < 4:
    print "Please start the script as follows:"
    print "python metaExtract.py <Paper Data csv> <Workshop Table csv> <proceedings csv>"
    sys.exit(-1)

INPUT = sys.argv[1]
INPUT_WS = sys.argv[2]
INPUT_PROCEEDINGS = sys.argv[3]
OUTPUT = "meta_extract.csv"

BAND_TITEL = "INFORMATIK 2017"
HRSG = "Eibl, Maximilian; Gaedke, Martin"
LNI = "Lecture Notes in Informatics (LNI) - Proceedings, Volume P-275"  # TODO Correct Volume Number
DOI = "doi:10.18420/in2017_"  # TODO fix DOI prefix
ISSN = "1617-5468"  # TODO include issn
ISBN = "978-3-88579-669-5"  # TODO include isbn
PUBLISHER = "Gesellschaft für Informatik, Bonn"
YEAR = "2017" # TODO fix year
DATE = "25.-29. September 2017" # TODO fix date
LOCATION = "Chemnitz" # TODO fix location


def empty_OrderedDict():
    return OrderedDict([('dc.contributor.author', None), ('dc.title', None), ('dc.title.subtitle', None),
                        ('dc.language.iso', None), ('dc.relation.ispartof', None), ('dc.contributor.editor', None),
                        ('dc.relation.ispartofseries', None),
                        ('dc.publisher', None), ('dc.date.issued', None), ('dc.description.abstract', None),
                        ('dc.subject', None), ('dc.identifier.doi', None),
                        ('dc.identifier.issn', None), ('dc.identifier.isbn', None), ('mci.refernce.pages', None),
                        ('mci.conference.date', None),
                        ('mci.conference.location', None), ('mci.conference.sessiontitle', None), ('filename', None)])


def getSpecificRow(input, key, value):
    for row in input:
        if row[key] == value:
            return row
    return None


def compPaperFolders(a,b):
    match_a=re.match('([A-Z])(\d+)-(\d+)',a)
    match_b=re.match('([A-Z])(\d+)-(\d+)',b)
    part_a=match_a.group(1)
    part_b=match_b.group(1)
    workshop_a=int(match_a.group(2))
    paper_a=int(match_a.group(3))
    paper_b=int(match_b.group(3))
    workshop_b=int(match_b.group(2))
    if part_a != part_b:
        return ord(part_a) - ord(part_b)
    if workshop_a != workshop_b:
        return workshop_a - workshop_b
    else:
        return paper_a - paper_b


input_file = csv.DictReader(open(INPUT, "r"))
build_ids = []
for row in input_file:
    if row['Build ID'] in build_ids and row['Build ID'] != '':
        print "Found double Build ID '" + row['Build ID'] + "'!"
    else:
        build_ids.append(row['Build ID'])


input_file = csv.DictReader(open(INPUT, "r"))
ordered_fieldnames = empty_OrderedDict()
output_file = csv.DictWriter(open(OUTPUT, "wb"), fieldnames=ordered_fieldnames)
output_file.writeheader()

input_file_filtered = filter(lambda x: x['Build ID']!='', input_file)
input_file = csv.DictReader(open(INPUT, "r"))
for row in input_file:
    if row not in input_file_filtered:
        print "Row has no Build ID:" + row.__str__()

workshopID = ""
ws_row = None
doi_counter = 1
for row in sorted(input_file_filtered, cmp=compPaperFolders, key=lambda x: x['Build ID'], reverse=False):
    row['Build ID'] = row['Build ID'].strip()
    temp_data = empty_OrderedDict()
    temp_data['dc.relation.ispartof'] = BAND_TITEL
    temp_data['dc.contributor.editor'] = HRSG
    temp_data['dc.relation.ispartofseries'] = LNI
    temp_data['dc.publisher'] = PUBLISHER
    temp_data['dc.date.issued'] = YEAR
    temp_data['dc.identifier.issn'] = ISSN
    temp_data['dc.identifier.isbn'] = ISBN
    temp_data['mci.conference.date'] = DATE
    temp_data['mci.conference.location'] = LOCATION

    if workshopID != row['Workshop ID']:
        workshopID = row['Workshop ID']
        with open(INPUT_WS, "r") as ws_file:
            ws_reader = csv.DictReader(ws_file)
            ws_row = getSpecificRow(ws_reader, 'Nummer', workshopID)

    temp_data['dc.identifier.doi'] = DOI + "%02d" % doi_counter
    doi_counter += 1

    temp_data['dc.description.abstract'] = " ".join(row['Abstract'].splitlines()).replace("- ", "-") if row['Abstract'] != "none" else ""
    subject = ""
    if row['Keywords'] != "none" and row['Keywords'] != '':
        keywords = row['Keywords'].strip()
        keywords = keywords[:-1] if keywords[-1] == '.' else keywords
        subject = " ".join(keywords.splitlines()).replace(";", ",")
        subject = subject.replace(" ,", ",").replace(". ", ", ")

    temp_data['dc.subject'] = subject
    temp_data['dc.language.iso'] = row['Sprache']

    temp_data['mci.conference.sessiontitle'] = ws_row['Kurztitel'].strip()

    with open(INPUT_PROCEEDINGS, "r") as pro_file:
        pro_reader = csv.reader(pro_file, delimiter=';')
        pro_row = getSpecificRow(pro_reader, -1, row['Build ID'])
        if pro_row != None:
            temp_data['mci.refernce.pages'] = pro_row[-2].replace("--","-")
            pages = temp_data['mci.refernce.pages'].split('-')
            if pages[0] == pages[1]:
                temp_data['mci.refernce.pages'] = pages[0]
        else:
            print "Build ID '"+ row['Build ID'] +"' has no reference to pages in the proceedings! Please check why!"

    # TODO richtige Filenames setzen
    temp_data['filename'] = row['Build ID'] + ".pdf"

    title = " ".join(row['Titel'].splitlines())
    if ' – ' in title:
        if title.count(' – ') > 1 or ': ' in title:
            print "Separation of title and subtitle at Build ID '" + row[
                'Build ID'] + "' is probably wrong. Please check if done right!"
        title_split = title.split(" – ")
        temp_data['dc.title'] = title_split[0]
        temp_data['dc.title.subtitle'] = " – ".join(title_split[1:])
    elif ': ' in title:
        if title.count(': ') > 1:
            print "Separation of title and subtitle at Build ID '" + row[
                'Build ID'] + "' is probably wrong. Please check if done right!"
        title_split = title.split(": ")
        temp_data['dc.title'] = title_split[0]
        temp_data['dc.title.subtitle'] = ": ".join(title_split[1:])
    else:
        temp_data['dc.title'] = title

    authors = row['Autoren'].split(',')
    author_string = ""
    corrected_authors = []
    for author in authors:
        author = author.strip().replace("\n", " ").replace("  ", " ")
        author_split = author.split(" ")
        if len(author_split) > 2:
            print "Author reordering of '" + author + "' at Build ID '" + row[
                'Build ID'] + "' is probably wrong. Please check if done right!"
        isLowerCase_index = len(author_split) - 1
        for i in range(len(author_split) - 2, -1, -1):
            if author_split[i][0].isupper():
                break
            isLowerCase_index = i
        author = ""
        for j in range(isLowerCase_index, len(author_split) - 1):
            author += author_split[j] + " "
        author += author_split[-1] + ", "
        for k in range(0, isLowerCase_index):
            author += author_split[k] + " "
        corrected_authors.append(author.strip())
    temp_data['dc.contributor.author'] = "; ".join(corrected_authors)

    output_file.writerow(temp_data)




##
# For Textract Abstract and Keywords from pdf. Not needed anymore due to information in main csv.
##

# text = textract.process("paper.pdf")
# array = text.split("Abstract:")
# array2 = array[1].split("Keywords:")
# array3 = array2[1].splitlines()

# abstract = array2[0].strip()
# abstract = re.sub('\\r\\n\\r\\n', ' ', abstract)
# abstract = re.sub('\\r\\n', ' ', abstract)


# f = open("test.log", 'w')
# f.write('"' + abstract + '"')

# index = 0
# for p in array3:
#	if p[-1] == ",":
#		index += 1
#	else:
#		break
#
# index2 = 0
# result = ""
# while index2 <= index:
#	result += array3[index2] + " "
#	index2 += 1
# f.write(result.strip())
