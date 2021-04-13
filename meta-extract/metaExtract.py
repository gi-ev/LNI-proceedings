#! /usr/bin/python
# -*- coding: utf-8 -*-
# call like so:
# python metaExtract.py papers.csv ws.csv proceedings.csv
# sys.argv[1]: GI Guidelines csv
# sys.argv[2]: Workshop csv
# sys.argv[3]: proceedings csv

import itertools
import sys
import re
import csv
from collections import OrderedDict
from functools import cmp_to_key

if len(sys.argv) < 4:
    print("Please start the script as follows:")
    print("python metaExtract.py <Paper Data csv> <Workshop Table csv> <proceedings csv>")
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
YEAR = "2017"  # TODO fix year
DATE = "25.-29. September 2017"  # TODO fix date
LOCATION = "Chemnitz"  # TODO fix location


def empty_OrderedDict():
    return OrderedDict([('dc.contributor.author', None), ('dc.title', None), ('dc.title.subtitle', None),
                        ('dc.language.iso', None), ('dc.relation.ispartof', None), ('dc.contributor.editor', None),
                        ('dc.relation.ispartofseries', None),
                        ('dc.publisher', None), ('dc.date.issued', None), ('dc.description.abstract', None),
                        ('dc.subject', None), ('dc.identifier.doi', None),
                        ('dc.identifier.issn', None), ('dc.identifier.isbn', None), ('mci.refernce.pages', None),
                        ('mci.conference.date', None),
                        ('mci.conference.location', None), ('mci.conference.sessiontitle', None), ('filename', None)])


def get_specific_row(reader, key, value):
    for row in reader:
        if row[key] == value:
            return row
    return None


def comp_paper_folders(a, b):
    match_a = re.match('([A-Z])(\d+)-(\d+)', a['Build ID'])
    match_b = re.match('([A-Z])(\d+)-(\d+)', b['Build ID'])
    part_a = match_a.group(1)
    part_b = match_b.group(1)
    workshop_a = int(match_a.group(2))
    paper_a = int(match_a.group(3))
    paper_b = int(match_b.group(3))
    workshop_b = int(match_b.group(2))
    if part_a != part_b:
        return ord(part_a) - ord(part_b)
    if workshop_a != workshop_b:
        return workshop_a - workshop_b
    else:
        return paper_a - paper_b


def extract_build_ids():
    with open(INPUT, "r") as paper_data:
        papers = csv.DictReader(paper_data)
        build_ids = []
        for paper in papers:
            if paper['Build ID'] in build_ids and paper['Build ID'] != '':
                print("Found double Build ID '" + paper['Build ID'] + "'!")
            else:
                build_ids.append(paper['Build ID'])
    return build_ids


def filter_missing_build_ids():
    with open(INPUT, "r") as paper_data:
        papers1, papers2 = itertools.tee(csv.DictReader(paper_data), 2)
        papers_filtered = [p for p in papers1 if p['Build ID'] != '']
        papers_without_build_id = [p for p in papers2 if p not in papers_filtered]
    for paper in papers_without_build_id:
        print("Row has no Build ID:" + paper.__str__())

    return papers_filtered


def authors(paper):
    authrs = paper['Autoren'].split(',')
    corrected_authors = []
    for author in authrs:
        author = author.strip().replace("\n", " ").replace("  ", " ")
        author_split = author.split(" ")
        if len(author_split) > 2:
            print("Author reordering of '" + author + "' at Build ID '" + paper[
                'Build ID'] + "' is probably wrong. Please check if done right!")
        is_lower_case_index = len(author_split) - 1
        for i in range(len(author_split) - 2, -1, -1):
            if author_split[i][0].isupper():
                break
            is_lower_case_index = i
        author = ""
        for j in range(is_lower_case_index, len(author_split) - 1):
            author += author_split[j] + " "
        author += author_split[-1] + ", "
        for k in range(0, is_lower_case_index):
            author += author_split[k] + " "
        corrected_authors.append(author.strip())
    return "; ".join(corrected_authors)


def title_subtitle(paper, temp_data):
    title = " ".join(paper['Titel'].splitlines())
    if ' – ' in title:
        if title.count(' – ') > 1 or ': ' in title:
            print("Separation of title and subtitle at Build ID '" + paper[
                'Build ID'] + "' is probably wrong. Please check if done right!")
        title_split = title.split(" – ")
        temp_data['dc.title'] = title_split[0]
        temp_data['dc.title.subtitle'] = " – ".join(title_split[1:])
    elif ': ' in title:
        if title.count(': ') > 1:
            print("Separation of title and subtitle at Build ID '" + paper[
                'Build ID'] + "' is probably wrong. Please check if done right!")
        title_split = title.split(": ")
        temp_data['dc.title'] = title_split[0]
        temp_data['dc.title.subtitle'] = ": ".join(title_split[1:])
    else:
        temp_data['dc.title'] = title


def page_refs(paper, temp_data):
    with open(INPUT_PROCEEDINGS, "r") as pro_file:
        pro_reader = csv.reader(pro_file, delimiter=';')
        pro_row = get_specific_row(pro_reader, -1, paper['Build ID'])
        if pro_row is not None:
            temp_data['mci.refernce.pages'] = pro_row[-2].replace("--", "-")
            pages = temp_data['mci.refernce.pages'].split('-')
            if pages[0] == pages[1]:
                temp_data['mci.refernce.pages'] = pages[0]
        else:
            print("Build ID '" + paper[
                'Build ID'] + "' has no reference to pages in the proceedings! Please check why!")


def subject(paper):
    subj = ""
    if paper['Keywords'] != "none" and paper['Keywords'] != '':
        keywords = paper['Keywords'].strip()
        keywords = keywords[:-1] if keywords[-1] == '.' else keywords
        subj = " ".join(keywords.splitlines()).replace(";", ",")
        subj = subj.replace(" ,", ",").replace(". ", ", ")
    return subj


def workshop_row(workshop_id):
    with open(INPUT_WS, "r") as ws_file:
        ws_reader = csv.DictReader(ws_file)
        ws_row = get_specific_row(ws_reader, 'Nummer', workshop_id)
    return ws_row


def initialize_metadata_row():
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
    return temp_data


def extract_metadata():
    metadata_rows = []
    workshop_id = ""
    ws_row = None
    doi_counter = 1

    for paper in sorted(papers_filtered, key=cmp_to_key(comp_paper_folders), reverse=False):
        paper['Build ID'] = paper['Build ID'].strip()
        temp_data = initialize_metadata_row()

        if workshop_id != paper['Workshop ID']:
            workshop_id = paper['Workshop ID']
            ws_row = workshop_row(workshop_id)

        temp_data['dc.identifier.doi'] = DOI + "%02d" % doi_counter
        doi_counter += 1

        temp_data['dc.description.abstract'] = " ".join(paper['Abstract'].splitlines()).replace("- ", "-") if paper['Abstract'] != "none" else ""

        temp_data['dc.subject'] = subject(paper)
        temp_data['dc.language.iso'] = paper['Sprache']

        temp_data['mci.conference.sessiontitle'] = ws_row['Kurztitel'].strip()

        page_refs(paper, temp_data)

        # TODO richtige Filenames setzen
        temp_data['filename'] = paper['Build ID'] + ".pdf"

        title_subtitle(paper, temp_data)

        temp_data['dc.contributor.author'] = authors(paper)

        metadata_rows.append(temp_data)
    return metadata_rows


if __name__ == "__main__":
    with open(OUTPUT, "w", newline='') as metadata_file:
        ordered_fieldnames = empty_OrderedDict()
        metadata = csv.DictWriter(metadata_file, fieldnames=ordered_fieldnames)
        metadata.writeheader()

        build_ids = extract_build_ids()
        papers_filtered = filter_missing_build_ids()

        metadata_rows = extract_metadata()
        metadata.writerows(metadata_rows)
